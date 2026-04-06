import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, b_cga, exp
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA: Rigid Motions

    Once rotations and translations both become versor actions, they can be
    composed into one conformal motion.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In 2D CGA we can combine

    $$
    R = \exp\!\left(-\frac{1}{2}\theta e_{12}\right),
    \qquad
    T = \exp\!\left(-\frac{1}{2} t e_\infty\right),
    $$

    into one motion versor

    $$
    M = T R.
    $$

    Then the transformed conformal point is

    $$
    X' = M X \widetilde M.
    $$
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    px = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.8, label="Point x", show_value=True)
    py = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.0, label="Point y", show_value=True)
    angle = mo.ui.slider(0, 360, step=1, value=70, label="Rotation angle", show_value=True)
    tx = mo.ui.slider(-1.0, 1.0, step=0.05, value=0.4, label="Translation x", show_value=True)
    ty = mo.ui.slider(-1.0, 1.0, step=0.05, value=0.3, label="Translation y", show_value=True)
    return angle, px, py, tx, ty


@app.cell
def _(alg, angle, e1, e2, em, ep, exp, gm, mo, np, px, py, rigid_motion_plot, tx, ty):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (px.value * e1 + py.value * e2).name(latex="x")
    X = (eo + x + half * (x | x) * einf).name(latex="X")

    theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
    B = (e1 * e2).name(latex="B")
    R = exp(-half * theta * B).name(latex="R")

    t = (tx.value * e1 + ty.value * e2).name(latex="t")
    T = exp(-half * t * einf).name(latex="T")
    M = (T * R).name(latex="M")

    Xp = (M * X * ~M).name(latex=r"X'")
    x_prime = (((Xp | e1) * e1) + ((Xp | e2) * e2)).name(latex=r"x'")
    Xp_sq = (Xp * Xp).name(latex=r"{X'}^2")

    _md = t"""
    {B.display()} <br/>
    {R.display()} <br/>
    {t.display()} <br/>
    {T.display()} <br/>
    {M.display()} <br/>
    {X.display()} <br/>
    {Xp.display()} <br/>
    {Xp_sq.display()} <br/>
    {x_prime.display()} <br/>
    One versor now carries the full Euclidean rigid motion.
    """

    mo.vstack([px, py, angle, tx, ty, gm.md(_md), rigid_motion_plot(x, x_prime)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In the conformal model, rotations and translations belong to the same versor
    framework. This is one of the clearest conceptual reasons to move from
    ordinary Euclidean GA into CGA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(plt):
    def rigid_motion_plot(x, x_prime):
        _x = x.vector_part[:2]
        _xp = x_prime.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.5, 5.5))
        _ax.scatter([_x[0], _xp[0]], [_x[1], _xp[1]], color=["#2563eb", "#d62828"], s=60)
        _ax.annotate("", xy=_xp, xytext=_x, arrowprops=dict(arrowstyle="->", color="#555555", lw=1.8))
        _ax.text(_x[0] + 0.05, _x[1] + 0.05, "x", color="#2563eb")
        _ax.text(_xp[0] + 0.05, _xp[1] + 0.05, "x'", color="#d62828")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Rigid motion in the Euclidean picture")
        plt.close(_fig)
        return _fig

    return (rigid_motion_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
