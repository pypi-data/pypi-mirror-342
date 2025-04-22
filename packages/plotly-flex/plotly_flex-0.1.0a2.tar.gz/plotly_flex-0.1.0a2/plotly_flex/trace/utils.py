import math
# import polars as pl


def range_to_idx(start: float, end: float) -> tuple[int, int]:
    """Round the start & end values similar to how bisect_left and bisect_right work.

    If the start value is negative, it is set to 0.
    """
    assert start <= end, f"start={start} should be less than or equal to end={end}"
    start, end = math.ceil(start), math.floor(end) + 1
    start = start if start > 0 else 0
    assert start < end, f"start={start} should be less than end={end}"
    return start, end


# def is_sorted(data: pl.Series | pl.DataFrame | pl.LazyFrame) -> bool:
#     if isinstance(data, pl.Series):
#         return data.is_sorted()
#     elif isinstance(data, pl.DataFrame):
#         return data.to_series().is_sorted()
#     elif isinstance(data, pl.LazyFrame):
#         return data.select(pl.is_sorted()).collect().item()
#     raise ValueError(f"Unsupported type {type(data)}")


# def _is_sorted(s: Any):
#     if isinstance(s, nw.Series):
#         assert s.is_sorted()
#     elif isinstance(s, nw.DataFrame):
#         assert s.to_series().is_sorted()
#         s.set_sorted()
#     elif hasattr(s, "is_monotonic_increasing"):
#         return s.is_monotonic_increasing
#     elif np is not None and isinstance(s, np.ndarray):
#         return np.all(s[:-1] <= s[1:])
#     # elif hasattr(s, "__len__"):
#     # return all(s[i] <= s[i + 1] for i in range(len(s) - 1))
#     raise ValueError(f"Unsupported type {type(s)}")
