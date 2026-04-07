import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Inversion Maps Lines and Circles

    In Euclidean geometry, inversion swaps lines and circles in a way that can
    feel mysterious. CGA packages them as one family of objects, so this becomes
    a natural conformal action rather than a trick.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Under inversion in the unit circle:

    - a line not through the origin maps to a circle through the origin
    - a circle through the origin maps to a line

    The Euclidean view changes shape. The conformal view treats both as the same
    kind of geometric object.
    """)
    return


@app.cell
def _(mo):
    mode = mo.ui.dropdown(
        options={
            "Line to circle": "line",
            "Circle through origin to line": "circle",
        },
        value="Line to circle",
        label="Example",
    )
    height = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.55, label="line height / circle centre e2", show_value=True)
    radius = mo.ui.slider(0.2, 1.8, step=0.05, value=0.75, label="circle radius", show_value=True)
    return height, mode, radius


@app.cell
def _(gm, height, inversion_swap_plot, mode, mo, radius):
    _md = rf"""
    Inversion radius is fixed at $1$.

    Current mode: **{mode.value}**
    """
    mo.vstack([mode, height, radius, gm.md(_md), inversion_swap_plot(mode.value, height.value, radius.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _invert_points(x, y):
        d = x**2 + y**2
        return x / d, y / d

    def inversion_swap_plot(mode, height, radius):
        t = np.linspace(0, 2 * np.pi, 400)
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.2))

        for ax in (ax0, ax1):
            ax.plot(np.cos(t), np.sin(t), color="#999999", lw=1.0, alpha=0.45)
            ax.set_xlim(-2.2, 2.2)
            ax.set_ylim(-2.2, 2.2)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        if mode == "line":
            xs = np.linspace(-2.0, 2.0, 400)
            ys = np.full_like(xs, height)
            mask = xs**2 + ys**2 > 1e-8
            xi, yi = _invert_points(xs[mask], ys[mask])
            ax0.plot(xs, ys, color="#2563eb", lw=2.2)
            ax1.plot(xi, yi, color="#7c3aed", lw=2.2)
            ax0.set_title("Line not through the origin")
            ax1.set_title("Inverted image: circle through the origin")
        else:
            cy = height
            r = max(abs(cy), radius)
            xs = r * np.cos(t)
            ys = cy + r * np.sin(t)
            mask = xs**2 + ys**2 > 1e-8
            xi, yi = _invert_points(xs[mask], ys[mask])
            ax0.plot(xs, ys, color="#2563eb", lw=2.2)
            ax1.plot(xi, yi, color="#7c3aed", lw=2.2)
            ax0.set_title("Circle through the origin")
            ax1.set_title("Inverted image: line")

        plt.close(fig)
        return fig

    return (inversion_swap_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
