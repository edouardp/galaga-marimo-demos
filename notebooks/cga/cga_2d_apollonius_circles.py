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
    # 2D CGA Apollonius Circles

    An Apollonius circle is the Euclidean locus of points whose distances to two
    fixed sites stay in a constant ratio. It is another example of a curved
    Euclidean object becoming a clean algebraic condition on lifted points.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For fixed sites $A$ and $B$, and ratio $k>0$,

    $$
    \|x-A\| = k\,\|x-B\|.
    $$

    Squaring gives

    $$
    (x-A)^2 - k^2 (x-B)^2 = 0,
    $$

    which is a circle unless $k=1$, in which case it collapses to the ordinary
    perpendicular bisector.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    ax = mo.ui.slider(-1.6, 1.6, step=0.05, value=-1.0, label="A along e1", show_value=True)
    ay = mo.ui.slider(-1.6, 1.6, step=0.05, value=-0.1, label="A along e2", show_value=True)
    bx = mo.ui.slider(-1.6, 1.6, step=0.05, value=1.0, label="B along e1", show_value=True)
    by = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.15, label="B along e2", show_value=True)
    ratio = mo.ui.slider(0.25, 2.5, step=0.01, value=1.4, label="distance ratio k", show_value=True)
    return ax, ay, bx, by, ratio


@app.cell
def _(alg, apollonius_plot, ax, ay, bx, by, e1, e2, em, ep, gm, mo, np, ratio):
    a = np.array([ax.value, ay.value], dtype=float)
    b = np.array([bx.value, by.value], dtype=float)
    k = ratio.value
    denom = 1.0 - k**2

    half = alg.frac(1, 2)
    eo = half * (em - ep)
    einf = ep + em
    a_mv = (ax.value * e1 + ay.value * e2).name(latex="a")
    b_mv = (bx.value * e1 + by.value * e2).name(latex="b")
    A = (eo + a_mv + half * (a_mv | a_mv) * einf).name(latex="A")
    B = (eo + b_mv + half * (b_mv | b_mv) * einf).name(latex="B")
    k_sq = alg.scalar(k**2).name(latex="k^2")

    if abs(denom) > 1e-6:
        center = (a - (k**2) * b) / denom
        radius_sq = float(np.dot(center, center) - (np.dot(a, a) - k**2 * np.dot(b, b)) / denom)
        radius_text = f"{max(radius_sq, 0.0) ** 0.5:.3f}"
        center_text = rf"({center[0]:.3f}, {center[1]:.3f})"
    else:
        center_text = r"\text{at infinity}"
        radius_text = r"\text{not a finite circle}"

    _md = t"""
    {A.display()} <br/>
    {B.display()} <br/>
    {k_sq.display()} <br/>
    For a probe point $X = \\operatorname{{up}}(x)$, the Apollonius condition is
    $$
    X \\cdot A = {k**2:.3f}\\,(X \\cdot B),
    $$
    because each conformal inner product encodes a squared Euclidean distance.
    In coordinates this becomes
    $$
    (x-A)^2 - {k**2:.3f}(x-B)^2 = 0.
    $$
    Center:
    $$
    c = {center_text}
    $$
    Radius:
    $$
    r = {radius_text}
    $$
    """

    mo.vstack([ax, ay, bx, by, ratio, gm.md(_md), apollonius_plot(a, b, k)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def apollonius_plot(a, b, k):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.2))

        xs = np.linspace(-2.2, 2.2, 220)
        ys = np.linspace(-2.2, 2.2, 220)
        gx, gy = np.meshgrid(xs, ys)
        da = np.sqrt((gx - a[0]) ** 2 + (gy - a[1]) ** 2)
        db = np.sqrt((gx - b[0]) ** 2 + (gy - b[1]) ** 2)
        eq = (gx - a[0]) ** 2 + (gy - a[1]) ** 2 - k**2 * ((gx - b[0]) ** 2 + (gy - b[1]) ** 2)

        ratio_field = np.divide(da, np.maximum(db, 1e-6))
        ax0.contour(gx, gy, ratio_field, levels=[k], colors=["#7c3aed"], linewidths=2.2)
        ax1.contour(gx, gy, eq, levels=[0], colors=["#111111"], linewidths=2.2)

        for ax in (ax0, ax1):
            ax.scatter([a[0], b[0]], [a[1], b[1]], color=["#2563eb", "#d62828"], s=42, zorder=5)
            ax.text(a[0] + 0.05, a[1] + 0.05, "A", color="#2563eb", fontsize=11, weight="bold")
            ax.text(b[0] + 0.05, b[1] + 0.05, "B", color="#d62828", fontsize=11, weight="bold")
            ax.set_xlim(-2.2, 2.2)
            ax.set_ylim(-2.2, 2.2)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        ax0.set_title(r"Distance-ratio contour $\|x-A\|/\|x-B\| = k$")
        ax1.set_title("Same locus from one quadratic condition")

        plt.close(fig)
        return fig

    return (apollonius_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
