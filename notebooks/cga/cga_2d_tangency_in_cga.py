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
    # Tangency in 2D CGA

    Tangency is where two intersections collapse into one. In the Euclidean
    picture that means “touching.” Algebraically it means a discriminant goes to
    zero.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a horizontal line $y=h$ and a circle of radius $r$ centred at the
    origin:

    $$
    x^2 + h^2 = r^2.
    $$

    So:

    - $|h| < r$: two intersections
    - $|h| = r$: tangency
    - $|h| > r$: no real intersections
    """)
    return


@app.cell
def _(mo):
    height = mo.ui.slider(-1.5, 1.5, step=0.01, value=0.8, label="line height h", show_value=True)
    radius = mo.ui.slider(0.2, 1.5, step=0.01, value=0.8, label="circle radius r", show_value=True)
    return height, radius


@app.cell
def _(gm, height, mo, radius, tangency_plot):
    disc = radius.value**2 - height.value**2
    if disc > 1e-6:
        status = "two intersections"
    elif abs(disc) <= 1e-6:
        status = "tangent"
    else:
        status = "no real intersections"

    _md = rf"""
    $$
    x^2 + ({height.value:.2f})^2 = {radius.value:.2f}^2
    $$

    Discriminant:
    $$
    r^2 - h^2 = {disc:.4f}
    $$

    Status: **{status}**
    """
    mo.vstack([height, radius, gm.md(_md), tangency_plot(height.value, radius.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def tangency_plot(height, radius):
        t = np.linspace(0, 2 * np.pi, 240)
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.4, 5.2))

        for ax in (ax0, ax1):
            ax.plot(radius * np.cos(t), radius * np.sin(t), color="#2563eb", lw=2.2)
            ax.axhline(height, color="#d62828", lw=2.0)
            ax.set_xlim(-1.9, 1.9)
            ax.set_ylim(-1.9, 1.9)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        disc = radius**2 - height**2
        xs = np.linspace(-1.9, 1.9, 160)
        ys = np.linspace(-1.9, 1.9, 160)
        gx, gy = np.meshgrid(xs, ys)
        circle_eq = gx**2 + gy**2 - radius**2
        line_eq = gy - height

        ax1.contour(gx, gy, circle_eq, levels=[0], colors="#2563eb", linewidths=2.2)
        ax1.contour(gx, gy, line_eq, levels=[0], colors="#d62828", linewidths=2.0)

        if disc >= 0:
            root = np.sqrt(max(disc, 0))
            pts = [(-root, height), (root, height)] if root > 1e-8 else [(0, height)]
            ax0.scatter([p[0] for p in pts], [p[1] for p in pts], color="#111111", s=50, zorder=4)
            ax1.scatter([p[0] for p in pts], [p[1] for p in pts], color="#111111", s=50, zorder=4)

        ax0.set_title("Euclidean touching picture")
        ax1.set_title("Intersections collapsing at tangency")

        plt.close(fig)
        return fig

    return (tangency_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
