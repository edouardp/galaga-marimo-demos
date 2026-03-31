import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, scalar_sqrt, symbolic
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, scalar_sqrt


@app.cell
def _(np, plt):
    def draw_energy_branches(mass, px):
        p_vals = np.linspace(-3.0, 3.0, 300)
        energies = np.sqrt(mass**2 + p_vals**2)
        current_energy = np.sqrt(mass**2 + px**2)

        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.plot(p_vals, energies, color="steelblue", lw=2, label="positive-energy branch")
        ax.plot(p_vals, -energies, color="crimson", lw=2, label="negative-energy branch")
        ax.scatter([px], [current_energy], color="steelblue", s=45, zorder=3)
        ax.scatter([px], [-current_energy], color="crimson", s=45, zorder=3)
        ax.axhline(0, color="black", lw=1, alpha=0.35)
        ax.axvline(0, color="black", lw=1, alpha=0.2)
        ax.set_xlim(-3, 3)
        ax.set_xlabel(r"$p_x$")
        ax.set_ylabel(r"$E$")
        ax.set_title("Mass shell: the two energy branches")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")
        plt.close(fig)
        return fig

    return (draw_energy_branches,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Dirac's Negative-Energy Surprise in Spacetime Algebra

    Dirac discovered that the relativistic electron equation admits two symmetric energy branches. In matrix language this appears through gamma matrices and four-component spinors; here we retrace the same idea using spacetime algebra, where the geometry of spacetime is the algebra from the start.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    That gives one timelike basis vector, $\gamma_0^2 = +1$, and three spacelike basis vectors, $\gamma_1^2 = \gamma_2^2 = \gamma_3^2 = -1$. The pseudoscalar $I = \gamma_0\gamma_1\gamma_2\gamma_3$ squares to $-1$, so it can play the role usually handled by the ordinary imaginary unit in relativistic wave mechanics.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), names="gamma")
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.pseudoscalar(lazy=True).name("I")
    return I, g0, g1, g2, g3, sta


@app.cell
def _(I, g0, g1, g2, g3, gm):
    gm.md(t"""
    Basis vectors:
    - {g0.display()} with {(g0**2).display(compact=True)}
    - {g1.display()} with {(g1**2).display(compact=True)}
    - {g2.display()} with {(g2**2).display(compact=True)}
    - {g3.display()} with {(g3**2).display(compact=True)}

    Pseudoscalar:
    - {I.display()}
    - {(I**2).display()}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dirac Equation in STA

    In the Hestenes form of the free Dirac equation, the wavefunction is an even multivector $\Psi$ and the matrix-valued Dirac operator becomes the spacetime vector derivative:

    $$
    \nabla \Psi I \sigma_3 = m \Psi \gamma_0,
    \qquad
    \nabla = \gamma^\mu \partial_\mu,
    \qquad
    \sigma_3 = \gamma_3 \gamma_0.
    $$

    For a plane wave, differentiation pulls down the momentum vector $p$, and the equation reduces to the on-shell condition

    $$
    p^2 = m^2.
    $$

    That single geometric statement already forces two energy branches:

    $$
    E = \pm \sqrt{m^2 + \mathbf{p}^2}.
    $$
    """)
    return


@app.cell
def _(mo):
    mass = mo.ui.slider(0.2, 2.5, step=0.1, value=1.0, label="Mass $m$", show_value=True)
    px = mo.ui.slider(-2.5, 2.5, step=0.1, value=0.8, label="Momentum $p_x$", show_value=True)
    time = mo.ui.slider(0.0, 6.0, step=0.1, value=1.0, label="Time $t$", show_value=True)
    x_pos = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.5, label="Position $x$", show_value=True)
    return mass, px, time, x_pos


@app.cell
def _(
    I,
    draw_energy_branches,
    exp,
    g0,
    g1,
    gm,
    mass,
    mo,
    px,
    scalar_sqrt,
    sta,
    time,
    x_pos,
):
    #m = mass.value
    #p_x = px.value
    #t = time.value
    #x = x_pos.value

    m = sta.scalar(mass.value).name("m")
    p_x = sta.scalar(px.value).name(latex=r"p_{x}")
    t = sta.scalar(time.value).name("t")
    x = sta.scalar(x_pos.value).name("x")

    E = scalar_sqrt(m**2 + p_x**2)
    one = sta.scalar(1).name("1")
    theta = (E * t - p_x * x).name(latex=r"\theta")

    p_plus = (E * g0 + p_x * g1).name("p_+")
    p_minus = (-E * g0 + p_x * g1).name("p_-")

    P_plus = ((one + g0) / 2).name("P_+")
    P_minus = ((one - g0) / 2).name("P_-")

    phase_plus = exp(-I * theta).name("e^{-I\\theta}")
    phase_minus = exp(I * theta).name("e^{+I\\theta}")

    _md = t"""
    **Current mass shell:**<br/>
    {p_plus.display()} $\\quad with \\quad$ {p_plus.sq.display(compact=True)} $\\quad(= m^2)$ <br/>
    {p_minus.display()} $\\quad with \\quad$ {p_minus.sq.display(compact=True)} $\\quad(= m^2)$ <br/>

    **Rest-frame energy projectors:**<br/>
    {P_plus.display()} $\\quad and \\quad$ {P_minus.display()} <br/>
    {P_plus.sq.display()} $\\quad and \\quad$ {P_minus.sq.display()} $\\quad$ (Projector * Projector = Projector)<br/>
    {(P_plus * P_minus).display()}  $\\quad$ (Projector * Orthognal Projector = 0)<br/>

    **Phase at the chosen event:**<br/>
    {theta.display()} <br/>
    {phase_plus.display()} <br/>
    {phase_minus.display()} <br/>

    **Energy values:**<br/>
    {E.copy_as(latex=r"E_+").display()} <br/>
    {(-E).copy_as(latex=r"E_-").display()} <br/>
    """

    mo.vstack([mass, px, time, x_pos, gm.md(_md), draw_energy_branches(m.scalar_part, p_x.scalar_part)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pseudoscalar and Phase

    The pseudoscalar $I$ satisfies $I^2 = -1$, so exponentials like $e^{\pm I\theta}$ generate oscillatory phase factors. In this notebook the two signs track the two branches of the relativistic energy shell: same mass, same momentum magnitude, opposite energy sign.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Antiparticles from Symmetry

    The negative branch is not a disposable artifact. Relativistic quantum theory interprets it as the antiparticle branch: for the electron, the corresponding physical state is the positron. In spacetime algebra this comes out cleanly because the Clifford structure already encodes the spacetime symmetry that makes the two branches unavoidable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    Repeating Dirac's logic in spacetime algebra leads to the same discovery: once the relativistic equation is written in spacetime form, the mass shell naturally splits into positive- and negative-energy solutions. The antiparticle is not added by hand; it is already present in the geometry.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
