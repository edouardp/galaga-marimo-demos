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
    # Radical Axis of Two Circles

    For two circles, the radical axis is the Euclidean locus of points with equal
    power to both circles. In CGA terms, it is the linear difference between two
    circle objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For circles

    $$
    (x-c_1)^2 = r_1^2,
    \qquad
    (x-c_2)^2 = r_2^2,
    $$

    subtracting the two equations removes the quadratic term and leaves a line:

    $$
    2(c_2-c_1)\cdot x
    =
    r_1^2-r_2^2 + c_2^2-c_1^2.
    $$
    """)
    return


@app.cell
def _(mo):
    c1x = mo.ui.slider(-1.5, 1.5, step=0.05, value=-0.5, label="circle 1 centre e1", show_value=True)
    c1y = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.0, label="circle 1 centre e2", show_value=True)
    r1 = mo.ui.slider(0.2, 1.8, step=0.05, value=0.9, label="circle 1 radius", show_value=True)
    c2x = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.8, label="circle 2 centre e1", show_value=True)
    c2y = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.3, label="circle 2 centre e2", show_value=True)
    r2 = mo.ui.slider(0.2, 1.8, step=0.05, value=1.1, label="circle 2 radius", show_value=True)
    return c1x, c1y, c2x, c2y, r1, r2


@app.cell
def _(c1x, c1y, c2x, c2y, gm, mo, np, radical_axis_plot, r1, r2):
    c1 = np.array([c1x.value, c1y.value], dtype=float)
    c2 = np.array([c2x.value, c2y.value], dtype=float)
    n = 2 * (c2 - c1)
    rhs = r1.value**2 - r2.value**2 + float(np.dot(c2, c2) - np.dot(c1, c1))

    _md = rf"""
    Circle 1:
    $$
    (x-{c1[0]:.2f})^2 + (y-{c1[1]:.2f})^2 = {r1.value:.2f}^2
    $$

    Circle 2:
    $$
    (x-{c2[0]:.2f})^2 + (y-{c2[1]:.2f})^2 = {r2.value:.2f}^2
    $$

    Radical axis:
    $$
    {n[0]:.2f}x + {n[1]:.2f}y = {rhs:.3f}
    $$
    """

    mo.vstack([c1x, c1y, r1, c2x, c2y, r2, gm.md(_md), radical_axis_plot(c1, r1.value, c2, r2.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def radical_axis_plot(c1, r1, c2, r2):
        t = np.linspace(0, 2 * np.pi, 240)
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.4, 5.2))

        for ax in (ax0, ax1):
            ax.plot(c1[0] + r1 * np.cos(t), c1[1] + r1 * np.sin(t), color="#2563eb", lw=2.2)
            ax.plot(c2[0] + r2 * np.cos(t), c2[1] + r2 * np.sin(t), color="#d62828", lw=2.2)
            ax.scatter([c1[0], c2[0]], [c1[1], c2[1]], color=["#2563eb", "#d62828"], s=35)
            ax.set_xlim(-2.2, 2.2)
            ax.set_ylim(-2.2, 2.2)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        n = 2 * (c2 - c1)
        rhs = r1**2 - r2**2 + float(np.dot(c2, c2) - np.dot(c1, c1))
        if np.linalg.norm(n) > 1e-9:
            if abs(n[1]) > 1e-9:
                xs = np.linspace(-2.3, 2.3, 200)
                ys = (rhs - n[0] * xs) / n[1]
                ax0.plot(xs, ys, color="#111111", lw=2.0)
            else:
                x0 = rhs / n[0]
                ax0.axvline(x0, color="#111111", lw=2.0)

        xs = np.linspace(-2.2, 2.2, 120)
        ys = np.linspace(-2.2, 2.2, 120)
        gx, gy = np.meshgrid(xs, ys)
        p1 = (gx - c1[0]) ** 2 + (gy - c1[1]) ** 2 - r1**2
        p2 = (gx - c2[0]) ** 2 + (gy - c2[1]) ** 2 - r2**2
        ax1.contour(gx, gy, p1 - p2, levels=[0], colors="#111111", linewidths=2.0)

        ax0.set_title("Two circles and the radical axis")
        ax1.set_title("Equal-power locus: $P_1 - P_2 = 0$")

        plt.close(fig)
        return fig

    return (radical_axis_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
