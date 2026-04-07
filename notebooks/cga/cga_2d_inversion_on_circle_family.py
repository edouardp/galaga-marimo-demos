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
    # 2D CGA Inversion on a Circle Family

    Inversion is one of the cleanest conformal actions: circles and lines are all
    sent to circles or lines. This notebook keeps the family small so the pattern
    is easy to see.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For inversion in the unit circle,

    $$
    x \mapsto \frac{x}{\|x\|^2}.
    $$

    A circle family that does not pass through the origin remains a family of
    circles, but its sizes and positions shift in a coordinated Möbius way.
    """)
    return


@app.cell
def _(mo):
    family_y = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.45, label="family centre offset along e2", show_value=True)
    radius = mo.ui.slider(0.15, 0.9, step=0.05, value=0.28, label="member radius", show_value=True)
    span = mo.ui.slider(0.4, 1.6, step=0.05, value=1.0, label="family spread along e1", show_value=True)
    return family_y, radius, span


@app.cell
def _(family_plot, family_y, gm, mo, radius, span):
    _md = rf"""
    Family before inversion:

    $$
    (x-c_i)^2 = {radius.value:.2f}^2
    $$

    with centers moving along

    $$
    c_i = (s_i, {family_y.value:.2f}), \qquad s_i \in [-{span.value:.2f}, {span.value:.2f}]
    $$

    The image family is no longer a simple translation family, but every member
    is still a circle.
    """

    mo.vstack([family_y, radius, span, gm.md(_md), family_plot(family_y.value, radius.value, span.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _invert_points(points):
        norms = np.sum(points**2, axis=1, keepdims=True)
        return points / np.maximum(norms, 1e-8)

    def family_plot(family_y, radius, span):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.8, 5.2))
        t = np.linspace(0, 2 * np.pi, 360)
        centers_x = np.linspace(-span, span, 5)
        colors = ["#2563eb", "#3b82f6", "#7c3aed", "#d62828", "#f97316"]

        unit_x = np.cos(t)
        unit_y = np.sin(t)

        for ax in (ax0, ax1):
            ax.plot(unit_x, unit_y, color="#111111", lw=1.6, alpha=0.8)
            ax.set_xlim(-2.2, 2.2)
            ax.set_ylim(-2.2, 2.2)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        for cx, color in zip(centers_x, colors):
            x = cx + radius * np.cos(t)
            y = family_y + radius * np.sin(t)
            pts = np.stack([x, y], axis=1)
            inv = _invert_points(pts)
            ax0.plot(x, y, color=color, lw=2.0)
            ax1.plot(inv[:, 0], inv[:, 1], color=color, lw=2.0)

        ax0.set_title("A small Euclidean circle family")
        ax1.set_title("Its image under unit-circle inversion")

        plt.close(fig)
        return fig

    return (family_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
