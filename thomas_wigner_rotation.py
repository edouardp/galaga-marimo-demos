import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, sandwich, unit


@app.cell
def _(plt):
    def draw_residual_rotation(g1_rot, g2_rot):
        _e1 = g1_rot.eval().vector_part[1:3]
        _e2 = g2_rot.eval().vector_part[1:3]

        _fig, _ax = plt.subplots(figsize=(6, 6))
        _ax.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.annotate("", xy=(_e1[0], _e1[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.annotate("", xy=(_e2[0], _e2[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkorange", lw=2))
        _ax.plot([], [], color="steelblue", label="original spatial axes")
        _ax.plot([], [], color="crimson", label=r"$W \gamma_1 \widetilde{W}$")
        _ax.plot([], [], color="darkorange", label=r"$W \gamma_2 \widetilde{W}$")
        _ax.set_aspect("equal")
        _ax.set_xlim(-1.2, 1.2)
        _ax.set_ylim(-1.2, 1.2)
        _ax.set_xlabel("x")
        _ax.set_ylabel("y")
        _ax.set_title("Residual spatial rotation")
        _ax.grid(True, alpha=0.25)
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_residual_rotation,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Thomas-Wigner Rotation

    Two boosts in different directions do not compose to a pure boost. After factoring out the net boost, there is a leftover spatial rotation. That finite leftover is the Thomas-Wigner rotation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    Timelike bivectors such as $\gamma_0\gamma_1$ and $\gamma_0\gamma_2$ generate boosts. The key effect in this notebook comes from the fact that boosts in different planes do not commute.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), names="gamma")
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, g2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Finite Non-Collinear Boosts

    First boost along $x$, then along $y$:

    $$
    R = R_y R_x.
    $$

    This gives a final boosted time axis

    $$
    u = R \gamma_0 \widetilde{R}.
    $$

    There is a pure boost $L$ that carries $\gamma_0$ to that same $u$. Once we factor that out, the remainder

    $$
    W = \widetilde{L} R
    $$

    fixes $\gamma_0$ and acts as a pure spatial rotation. That is the Thomas-Wigner rotor.
    """)
    return


@app.cell
def _(mo):
    phi_x = mo.ui.slider(0.0, 2.0, step=0.02, value=0.7, label="x-rapidity", show_value=True)
    phi_y = mo.ui.slider(0.0, 2.0, step=0.02, value=0.9, label="y-rapidity", show_value=True)
    return phi_x, phi_y


@app.cell
def _(
    draw_residual_rotation,
    exp,
    g0,
    g1,
    g2,
    gm,
    mo,
    np,
    phi_x,
    phi_y,
    sandwich,
    unit,
):
    _Bx = (g0 * g1).name(latex=r"B_x")
    _By = (g0 * g2).name(latex=r"B_y")
    _Rx = exp((phi_x.value / 2) * _Bx).name(latex=r"R_x")
    _Ry = exp((phi_y.value / 2) * _By).name(latex=r"R_y")
    _R = (_Ry * _Rx).name("R")

    _u = sandwich(_R, g0).name("u")
    _L = unit(1 + _u * g0).name("L")
    _W = (~_L * _R).name("W")

    _g1_rot = sandwich(_W, g1).name(latex=r"\gamma_1'")
    _g2_rot = sandwich(_W, g2).name(latex=r"\gamma_2'")

    _cos_angle = np.clip(_g1_rot.eval().vector_part[1], -1.0, 1.0)
    _angle = np.degrees(np.arccos(_cos_angle))

    _md = t"""
    {_Bx.display()} $\\quad$ and $\\quad$ {_By.display()} <br/>
    {_Rx.display()} <br/>
    {_Ry.display()} <br/>
    {_R.display()} <br/>
    {_u.display()} <br/>
    {_L.display()} <br/>
    {_W.display()} <br/>
    {sandwich(_W, g0).display()} $\\quad$ so $W$ is purely spatial. <br/>
    Residual rotation angle in the $x$-$y$ plane: ${_angle:.3f}^\\circ$
    """

    mo.vstack([
        phi_x,
        phi_y,
        gm.md(_md),
        draw_residual_rotation(_g1_rot, _g2_rot),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    The finite effect above is the discrete version of Thomas precession. If an object keeps changing its velocity direction, as in relativistic circular motion, its instantaneous rest frame is built from many tiny non-collinear boosts, and those tiny residual rotations accumulate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motivating Example

    A charged particle in a magnetic field, or any relativistic object in circular motion, is a natural special-relativistic example: the speed can stay nearly constant while the velocity direction keeps changing, so Thomas precession appears without needing gravity.

    An object orbiting a black hole is different. A true black-hole orbit is a general-relativistic problem, because spacetime itself is curved. For large-radius or weak-field circular motion you can still use special-relativistic intuition locally, but a faithful black-hole treatment would need GR rather than flat-spacetime STA alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    The Thomas-Wigner rotation is what remains after two non-collinear boosts are composed and the net boost is factored out. In spacetime algebra that structure is visible directly in the rotor factorization, rather than being hidden inside matrix algebra.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
