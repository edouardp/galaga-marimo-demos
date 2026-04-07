import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA Pole-Polar Geometry of a Circle

    A point outside a circle determines a special line, its polar. Every point on
    that line has a reciprocal geometric relation to the original point. In CGA,
    this is one of the cleanest examples of incidence between a point-object and
    a circle-object.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the unit circle and an external point $P=(p_x,p_y)$, the polar line is

    $$
    p_x x + p_y y = 1.
    $$

    When $P$ lies outside the circle, this line is the chord joining the two
    tangency points of the tangents from $P$.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    px = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.55, label="P along e1", show_value=True)
    py = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.65, label="P along e2", show_value=True)
    return px, py


@app.cell
def _(alg, e1, e2, em, ep, gm, mo, polar_plot, px, py):
    norm_sq = px.value**2 + py.value**2
    half = alg.frac(1, 2)
    eo = half * (em - ep)
    einf = (ep + em).name(latex=r"e_\infty")
    p = (px.value * e1 + py.value * e2).name(latex="p")
    P = (eo + p + half * (p | p) * einf).name(latex=r"P = \operatorname{up}(p)")
    if norm_sq > 1.0 + 1e-8:
        status = "outside the circle"
    elif abs(norm_sq - 1.0) <= 1e-8:
        status = "on the circle"
    else:
        status = "inside the circle"

    _md = t"""
    {P.display()} <br/>
    For the unit circle, the polar of the Euclidean point $p=({px.value:.2f},{py.value:.2f})$ is
    $$
    {px.value:.2f}x + {py.value:.2f}y = 1.
    $$
    In CGA terms, this is the line reciprocally associated with the point-object $P$ relative to the circle-object.
    <br/><br/>
    Point status: **{status}**
    """

    mo.vstack([px, py, gm.md(_md), polar_plot(px.value, py.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def polar_plot(px, py):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.2))
        t = np.linspace(0, 2 * np.pi, 240)
        circle_x = np.cos(t)
        circle_y = np.sin(t)

        for ax in (ax0, ax1):
            ax.plot(circle_x, circle_y, color="#2563eb", lw=2.2)
            ax.scatter([px], [py], color="#7c3aed", s=44, zorder=5)
            ax.set_xlim(-2.1, 2.1)
            ax.set_ylim(-2.1, 2.1)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        norm_sq = px**2 + py**2
        if abs(py) > 1e-9:
            xs = np.linspace(-2.2, 2.2, 240)
            ys = (1 - px * xs) / py
            ax0.plot(xs, ys, color="#111111", lw=2.0)
            ax1.plot(xs, ys, color="#111111", lw=2.0)
        elif abs(px) > 1e-9:
            x0 = 1 / px
            ax0.axvline(x0, color="#111111", lw=2.0)
            ax1.axvline(x0, color="#111111", lw=2.0)

        if norm_sq > 1.0 + 1e-8:
            p = np.array([px, py], dtype=float)
            s = 1.0 / norm_sq
            foot = s * p
            tangent_offset = np.sqrt(max(0.0, 1.0 - s))
            perp = np.array([-p[1], p[0]], dtype=float) / np.sqrt(norm_sq)
            t1 = foot + tangent_offset * perp
            t2 = foot - tangent_offset * perp
            ax0.scatter([t1[0], t2[0]], [t1[1], t2[1]], color="#d62828", s=38, zorder=6)
            ax0.plot([px, t1[0]], [py, t1[1]], color="#7c3aed", alpha=0.4, lw=1.5)
            ax0.plot([px, t2[0]], [py, t2[1]], color="#7c3aed", alpha=0.4, lw=1.5)
            ax1.scatter([t1[0], t2[0]], [t1[1], t2[1]], color="#d62828", s=38, zorder=6)

        ax0.set_title("Tangents from the external point")
        ax1.set_title("The polar line through the tangency points")

        plt.close(fig)
        return fig

    return (polar_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
