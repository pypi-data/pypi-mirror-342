# plotly-flex
Make plotly scalable - visualize large data with [plotly.py](https://github.com/plotly/plotly.py)!

This library aims to make plotly scalable by *aggregating data in the backend* before sending it to the frontend. This avoids loading all data into the frontend, which is how vanilla plotly works. This library is built on top of [polars](https://github.com/pola-rs/polars) to provide efficient data handling in the backend.


## Features

1. ⚡ **Making existing plotly traces scalable**
2. 🪄 **Aggregating data on events** (e.g. zooming, selection)  
    => support for cross-filtering
3. 🗃️ **Efficient handling of multiple lazyframes**

### Scalable Visualization Support

Overview of the supported trace types and their scalable support.
- Update on zoom = update the view when zooming in/out (e.g. by aggregating data)
- Update on selection (cross-filtering) = update the view when selecting related data (in another subplot)

| Plot Type  | Scalable Support | Update on Zoom | Update on Selection in other trace | Allow Selection |
|------------|------------------|----------------|---------------------|----------------|
| Scatter    | Supported        | Supported      | Supported           | Supported      |
| Scattergl  | Supported        | Supported      | Supported           | Supported      |
| Histogram  | Supported        | Supported      | Supported           | Supported      |
| Box        | Supported        | Not sensible   | Supported           | Supported      |
| Bar        | Supported        | Not sensible   | Supported           | Supported      |
| Pie        | Supported        | Not sensible   | Not possible        | Not supported  |


---

### Dependency management

This project uses [uv](https://github.com/astral-sh/uv) as dependency manager.

Dependencies are automatically installed when you run the `uv sync` command. The virtualenv is created in the `.venv` folder.

- Running scripts / commands in the virtualenv is as simple as running `uv run <command>`. This will automatically activate the virtualenv and run the command.
- Adding a dependency is as simple as running `uv add <package>`. Make sure to add `--dev` if the package is only needed for development.

> [!NOTE]  
> When developing, to [update the dependencies](https://github.com/astral-sh/uv/issues/1419#issuecomment-2457314237), run: `uv lock --upgrade; uv sync`
