import polars as pl

from typing import List, Set, Optional, Callable
from dataclasses import dataclass


try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import pyarrow as pa
except ImportError:
    pa = None


def polars_lf_from(data) -> pl.LazyFrame:
    if isinstance(data, (pl.DataFrame, pl.LazyFrame)):
        return data.lazy()
    elif pd is not None and isinstance(data, pd.DataFrame):
        return pl.from_pandas(data).lazy()
    elif pa is not None and isinstance(data, pa.Table):
        return pl.from_arrow(data).lazy()
    # elif hasattr("__dataframe__", data): ??? # TODO?
    #     return pl.from_dataframe(data)
    raise ValueError(f"Unsupported data type: {type(data)}")


def polars_col_from(col: str | pl.Expr) -> pl.Expr:
    if isinstance(col, str):
        col = pl.col(col)
    return col


def get_col_name(col: str | pl.Expr) -> str:
    if isinstance(col, str):
        return col
    assert col.meta.is_column()
    return col.meta.output_name()


@dataclass
class AggregationSpec:
    """Specifications for data aggregation in Polars.

    This class provides a unified way to specify aggregations using either a LazyFrame
    or an Expression, with an optional transformation function. It ensures that exactly
    one aggregation method (LazyFrame or Expression) is specified.

    Parameters
    ----------
    lf : Optional[pl.LazyFrame]
        A Polars LazyFrame to be aggregated. Mutually exclusive with expr.
    expr : Optional[pl.Expr]
        A Polars expression for aggregation. Mutually exclusive with lf.
    transform : Optional[Callable[[pl.LazyFrame], pl.LazyFrame]]
        Optional transformation function to modify the LazyFrame before applying expr.
        Only valid when using expr, not with lf.

    Raises
    ------
    ValueError
        If neither lf nor expr is provided, or if both are provided.
        If transform is provided along with lf.
    """

    lf: Optional[pl.LazyFrame] = None
    expr: Optional[pl.Expr] = None
    transform: Optional[Callable[[pl.LazyFrame], pl.LazyFrame]] = None

    def __post_init__(self):
        if (self.lf is not None) == (self.expr is not None):  # XOR check
            raise ValueError("Must provide either lf or expr, but not both")
        if self.transform and self.lf:
            raise ValueError("transform can only be used with expr")

    def is_lf(self) -> bool:
        """Check if this spec contains a LazyFrame."""
        return self.lf is not None

    def is_only_expr(self) -> bool:
        """Check if this spec contains only an expression without transformation."""
        return self.expr is not None and self.transform is None


class LFQueryBuilder:
    """
    Query builder for LazyFrame.
    """

    def __init__(
        self,
        ldf: pl.LazyFrame,
        row_index_col: Optional[str | pl.Expr] = None,
        cache_schema: bool = True,
    ):
        ldf = polars_lf_from(ldf)
        assert isinstance(ldf, pl.LazyFrame)
        if row_index_col is not None:
            row_index_col = polars_col_from(row_index_col)
        else:
            ldf = ldf.with_row_index(name="row_index")
            row_index_col = pl.col("row_index")
        assert row_index_col.meta.is_column()
        # Store the lazy frame and the row index column
        self._ldf: pl.LazyFrame = ldf
        self._row_index_col: pl.Expr = row_index_col  # TODO: keep Expr or store as str?
        self._cache_schema: bool = cache_schema  # whether to cache the ldf its schema
        self._sorted_cols: Set[str] = set()  # columns that are sorted

        # Check if the row index column is sorted and set it as sorted
        self.check_sorted(row_index_col)

    @property
    def row_index_col(self) -> str:
        return self._row_index_col.meta.output_name()

    # Is ~ 40x faster than LazyFrame.collect_schema() when the LazyFrame is in memory
    @property
    def schema(self):
        if self._cache_schema and hasattr(self, "_cached_schema"):
            return self._cached_schema

        schema = self._ldf.collect_schema()

        if self._cache_schema:
            self._cached_schema = schema

        return schema

    # --------------- Handling flags ---------------

    def check_sorted(self, col: str | pl.Expr):
        """
        Check if a column is sorted and set it as sorted, if not already set.

        This uses under the hood ._sorted_cols to keep track of the columns that are
        sorted. This is useful as one cannot query the flags of a LazyFrame.

        Parameters
        ----------
        col : str | pl.Expr
            Column name or expression.

        Raises
        ------
        AssertionError
            If the column is not in the schema or if the column is not sorted.
        """
        col: str = get_col_name(col)
        assert col in self.schema, f"Column '{col}' not in schema"
        if col not in self._sorted_cols:
            # TODO: how expensive is this?
            s: pl.Series = self._ldf.select(col).collect().to_series()
            assert s.is_sorted(), f"Column '{col}' not sorted"
            self._ldf = self._ldf.set_sorted(col)
            self._sorted_cols.add(col)

    # --------------- Aggregation ---------------

    def aggregate(
        self, filter_exprs: List[pl.Expr], agg_specs: List[AggregationSpec]
    ) -> pl.DataFrame:
        """Aggregate the data using the provided expressions.

        Parameters
        ----------
        filter_exprs : List[pl.Expr]
            List of filter expressions to apply before aggregation.
            These filters come from the selection (cross-filtering).
        agg_specs : List[AggregationSpec]
            List of aggregation specifications to apply.

        Returns
        -------
        pl.DataFrame
            The aggregated data.
        """
        filtered_ldf = self._ldf.filter(*filter_exprs)
        select_exprs = []
        lfs = []
        for agg_spec in agg_specs:
            if agg_spec.is_only_expr():  # expr only => execute in .select(...)
                select_exprs.append(agg_spec.expr)
            elif agg_spec.is_lf():  # lf => execute separately in pl.collect_all(...)
                lfs.append(agg_spec.lf)
            else:  # expr + transform => pipe the transform -> execute as separate lf
                lfs.append(filtered_ldf.pipe(agg_spec.transform).select(agg_spec.expr))
        return pl.concat(
            pl.collect_all([filtered_ldf.select(*select_exprs)] + lfs),
            how="horizontal",
        )
