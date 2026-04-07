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
    # Coaxal Circle Families

    A coaxal family is a one-parameter linear family of circles sharing the same
    radical axis. This is one of the cleanest places where “circles become linear
    objects” starts to feel real.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If two circle objects are $C_1$ and $C_2$, then a linear family

    $$
    C(\lambda) = (1-\lambda)C_1 + \lambda C_2
    $$

    stays inside the same coaxal family. In the Euclidean picture, the circles
    change, but one line of equal power stays fixed.
    """)
    return


@app.cell
def _(mo):
    c1x = mo.ui.slider(-1.5, 1.5, step=0.05, value=-0.8, label="circle 1 centre e1", show_value=True)
    c1y = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.0, label="circle 1 centre e2", show_value=True)
    r1 = mo.ui.slider(0.3, 1.8, step=0.05, value=0.9, label="circle 1 radius", show_value=True)
    c2x = mo.ui.slider(-1.5, 1.5, step=0.05, value=1.0, label="circle 2 centre e1", show_value=True)
    c2y = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.1, label="circle 2 centre e2", show_value=True)
    r2 = mo.ui.slider(0.3, 1.8, step=0.05, value=1.2, label="circle 2 radius", show_value=True)
    lam = mo.ui.slider(-1.0, 2.0, step=0.01, value=0.5, label="family parameter λ", show_value=True)
    return c1x, c1y, c2x, c2y, lam, r1, r2


@app.cell
def _(c1x, c1y, c2x, c2y, coaxal_family_plot, gm, lam, mo, np, r1, r2):
    c1 = np.array([c1x.value, c1y.value], dtype=float)
    c2 = np.array([c2x.value, c2y.value], dtype=float)
    _md = rf"""
    Base circles:
    $$
    (x-{c1[0]:.2f})^2 + (y-{c1[1]:.2f})^2 = {r1.value:.2f}^2
    $$
    $$
    (x-{c2[0]:.2f})^2 + (y-{c2[1]:.2f})^2 = {r2.value:.2f}^2
    $$

    Interpolating in circle-object space with $\lambda = {lam.value:.2f}$ keeps
    the family coaxal.
    """
    mo.vstack([c1x, c1y, r1, c2x, c2y, r2, lam, gm.md(_md), coaxal_family_plot(c1, r1.value, c2, r2.value, lam.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def coaxal_family_plot(c1, r1, c2, r2, lam):
        t = np.linspace(0, 2 * np.pi, 240)
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.2))

        n = 2 * (c2 - c1)
        rhs = r1**2 - r2**2 + float(np.dot(c2, c2) - np.dot(c1, c1))

        q = (1 - lam) * (np.dot(c1, c1) - r1**2) + lam * (np.dot(c2, c2) - r2**2)
        c = (1 - lam) * c1 + lam * c2
        rad_sq = float(np.dot(c, c) - q)

        for ax in (ax0, ax1):
            ax.plot(c1[0] + r1 * np.cos(t), c1[1] + r1 * np.sin(t), color="#2563eb", lw=1.6, alpha=0.45)
            ax.plot(c2[0] + r2 * np.cos(t), c2[1] + r2 * np.sin(t), color="#d62828", lw=1.6, alpha=0.45)
            if abs(n[1]) > 1e-9:
                xs = np.linspace(-2.4, 2.4, 200)
                ys = (rhs - n[0] * xs) / n[1]
                ax.plot(xs, ys, color="#111111", lw=1.6, alpha=0.85)
            else:
                ax.axvline(rhs / n[0], color="#111111", lw=1.6, alpha=0.85)
            ax.set_xlim(-2.3, 2.3)
            ax.set_ylim(-2.3, 2.3)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        if rad_sq > 1e-8:
            rad = np.sqrt(rad_sq)
            ax0.plot(c[0] + rad * np.cos(t), c[1] + rad * np.sin(t), color="#7c3aed", lw=2.3)
        ax0.scatter([c[0]], [c[1]], color="#7c3aed", s=35)

        xs = np.linspace(-2.3, 2.3, 160)
        ys = np.linspace(-2.3, 2.3, 160)
        gx, gy = np.meshgrid(xs, ys)
        p1 = (gx - c1[0]) ** 2 + (gy - c1[1]) ** 2 - r1**2
        p2 = (gx - c2[0]) ** 2 + (gy - c2[1]) ** 2 - r2**2
        ax1.contour(gx, gy, p1 - p2, levels=[0], colors="#111111", linewidths=1.6)
        if rad_sq > 1e-8:
            ax1.contour(gx, gy, (gx - c[0]) ** 2 + (gy - c[1]) ** 2 - rad_sq, levels=[0], colors="#7c3aed", linewidths=2.3)

        ax0.set_title("A circle moving inside one coaxal family")
        ax1.set_title("The radical axis stays fixed")

        plt.close(fig)
        return fig

    return (coaxal_family_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
