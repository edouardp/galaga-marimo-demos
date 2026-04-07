import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, sqrt
    from galaga.blade_convention import b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt, sqrt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA Distance on the Paraboloid

    Two Euclidean points lift to two null points upstairs. Their conformal inner
    product does not depend on where they sit individually, only on their
    Euclidean separation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With

    $$
    X = \operatorname{up}(x), \qquad Y = \operatorname{up}(y),
    $$

    the conformal model gives

    $$
    X \cdot Y = -\frac{1}{2}(x-y)^2.
    $$

    So Euclidean squared distance becomes a simple inner product upstairs.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    ax = mo.ui.slider(-1.8, 1.8, step=0.05, value=-0.7, label="A along e1", show_value=True)
    ay = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.2, label="A along e2", show_value=True)
    bx = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.9, label="B along e1", show_value=True)
    by = mo.ui.slider(-1.8, 1.8, step=0.05, value=-0.5, label="B along e2", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return ax, ay, bx, by, view_yaw


@app.cell
def _(
    alg,
    ax,
    ay,
    bx,
    by,
    e1,
    e2,
    em,
    ep,
    gm,
    mo,
    paraboloid_distance_plot,
    sqrt,
    view_yaw,
):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    a = (ax.value * e1 + ay.value * e2).name(latex="a")
    b = (bx.value * e1 + by.value * e2).name(latex="b")
    A = (eo + a + half * (a | a) * einf).name(latex="A")
    B = (eo + b + half * (b | b) * einf).name(latex="B")
    delta = (b - a).name(latex=r"b-a")
    dist_sq = ((delta | delta)).name(latex=r"(b-a)^2")
    dist = sqrt(dist_sq).name(latex=r"\|b-a\|")
    overlap = (A | B).name(latex=r"A \cdot B")
    overlap_relation = ((-2) * overlap).name(latex=r"-2(A \cdot B)")
    overlap_distance = sqrt(overlap_relation).name(latex=r"\sqrt{-2(A \cdot B)}")

    _md = t"""
    {a.display()} <br/>
    {b.display()} <br/>
    {A.display()} <br/>
    {B.display()} <br/>
    {delta.display()} <br/>
    {dist_sq.display()} <br/>
    {dist.display()} <br/>
    {overlap.display()} <br/>
    {overlap_relation.display()} $\\quad$ (equals squared Euclidean distance)<br/>
    {overlap_distance.display()} $\\quad$ (equals Euclidean distance)<br/>
    The two lifted points lie on the same paraboloid, but their conformal inner product only tracks the Euclidean separation.
    """

    mo.vstack([ax, ay, bx, by, gm.md(_md), paraboloid_distance_plot(a, b, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def paraboloid_distance_plot(a, b, view_yaw_deg):
        _a = np.array(a.vector_part[:2], dtype=float)
        _b = np.array(b.vector_part[:2], dtype=float)
        _ha = 0.5 * float(np.dot(_a, _a))
        _hb = 0.5 * float(np.dot(_b, _b))

        _grid = np.linspace(-1.8, 1.8, 80)
        _gx, _gy = np.meshgrid(_grid, _grid)
        _gz = 0.5 * (_gx**2 + _gy**2)

        _fig = plt.figure(figsize=(11.4, 5.2))
        _ax0 = _fig.add_subplot(121)
        _ax1 = _fig.add_subplot(122, projection="3d")

        _ax0.scatter([_a[0], _b[0]], [_a[1], _b[1]], color=["#2563eb", "#d62828"], s=55)
        _ax0.plot([_a[0], _b[0]], [_a[1], _b[1]], color="#555555", alpha=0.7, linewidth=1.8)
        _ax0.set_xlim(-1.9, 1.9)
        _ax0.set_ylim(-1.9, 1.9)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.18)
        _ax0.set_xlabel(r"$\mathbf{e_1}$")
        _ax0.set_ylabel(r"$\mathbf{e_2}$")
        _ax0.set_title("Euclidean points")

        _ax1.plot_surface(_gx, _gy, _gz, color="#ddd6fe", alpha=0.28, linewidth=0, shade=False)
        for _xy, _h, _color in [(_a, _ha, "#2563eb"), (_b, _hb, "#d62828")]:
            _ax1.scatter([_xy[0]], [_xy[1]], [0], color=_color, s=28, alpha=0.55)
            _ax1.scatter([_xy[0]], [_xy[1]], [_h], color=_color, s=52)
            _ax1.plot([_xy[0], _xy[0]], [_xy[1], _xy[1]], [0, _h], color=_color, alpha=0.28, linewidth=1.6)
        _ax1.plot([_a[0], _b[0]], [_a[1], _b[1]], [_ha, _hb], color="#444444", alpha=0.5, linewidth=1.4)
        _ax1.set_xlim(-1.9, 1.9)
        _ax1.set_ylim(-1.9, 1.9)
        _ax1.set_zlim(0, 3.4)
        _ax1.set_box_aspect((1, 1, 0.85))
        _ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        _ax1.set_xlabel(r"$\mathbf{e_1}$")
        _ax1.set_ylabel(r"$\mathbf{e_2}$")
        _ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        _ax1.set_title("Lifted points upstairs")

        plt.close(_fig)
        return _fig

    return (paraboloid_distance_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
