import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich, grade
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_minkowski(g0_boosted, g1_boosted, phi):
        # vector_part: [g0_coeff, g1_coeff, g2_coeff, g3_coeff]
        # Diagram: x-axis = space (g1), y-axis = time (g0)
        g0b_x, g0b_y = g0_boosted.vector_part[1], g0_boosted.vector_part[0]
        g1b_x, g1b_y = g1_boosted.vector_part[1], g1_boosted.vector_part[0]
        arrow_scale = 2
        max_extent = max(
            3,
            abs(arrow_scale * g0b_x),
            abs(arrow_scale * g0b_y),
            abs(arrow_scale * g1b_x),
            abs(arrow_scale * g1b_y),
        )
        fig, ax = plt.subplots(figsize=(5, 5))
        lc = np.linspace(-max_extent, max_extent, 100)
        ax.plot(lc, lc, 'k--', alpha=0.3, label='light cone')
        ax.plot(lc, -lc, 'k--', alpha=0.3)
        # Rest frame
        ax.annotate('', xy=(0, 2), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='steelblue', lw=2))
        ax.annotate('', xy=(2, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='steelblue', lw=2))
        ax.plot([], [], color='steelblue', label='γ₀, γ₁ (rest)')
        # Boosted frame
        ax.annotate('', xy=(arrow_scale * g0b_x, arrow_scale * g0b_y), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='crimson', lw=2))
        ax.annotate('', xy=(arrow_scale * g1b_x, arrow_scale * g1b_y), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='crimson', lw=2))
        ax.plot([], [], color='crimson', label="γ₀', γ₁' (boosted)")
        ax.set_xlim(-max_extent, max_extent); ax.set_ylim(-max_extent, max_extent)
        ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
        ax.set_xlabel('x (space)'); ax.set_ylabel('t (time)')
        ax.set_title(f'Minkowski Diagram — φ = {phi:.2f}')
        ax.legend(loc='upper left'); plt.close(fig)
        return fig

    return (draw_minkowski,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    That gives one timelike basis vector, $\gamma_0^2 = +1$, and three spacelike basis vectors, $\gamma_1^2 = \gamma_2^2 = \gamma_3^2 = -1$. Mixed products like $\gamma_0\gamma_1$ form bivectors, and in STA those timelike planes generate Lorentz boosts rather than ordinary Euclidean rotations.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, sta


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lorentz Boosts in Spacetime Algebra

    In **Spacetime Algebra** (STA), the Clifford algebra $\mathrm{Cl}(1,3)$, we have one timelike basis vector ($\gamma_0^2 = +1$) and three spacelike ($\gamma_i^2 = -1$).

    **Timelike bivectors** like $\gamma_0\gamma_1$ square to $+1$ and generate **Lorentz boosts** — hyperbolic rotations that mix space and time.

    The boost rotor for rapidity $\varphi$ in the $\gamma_0\gamma_1$ plane is:

    $$R = \cosh(\varphi/2) + \sinh(\varphi/2)\,\gamma_0\gamma_1$$

    We transform vectors with the sandwich product $v' = Rv\tilde{R}$, just like spatial rotations.

    Key relations:
    - $\beta = v/c = \tanh \varphi$ (velocity as fraction of $c$)
    - $\gamma = \cosh \varphi$ (Lorentz factor)
    - Rapidities add linearly: $\varphi_{\text{total}} = \varphi_1 + \varphi_2$

    Use the slider below to boost the basis vectors and watch the Minkowski diagram respond.
    """)
    return


@app.cell
def _(mo):
    phi_slider = mo.ui.slider(0.0, 3.0, step=0.05, value=0.5, label="Rapidity φ", show_value=True)
    return (phi_slider,)


@app.cell
def _(draw_minkowski, exp, g0, g1, gm, mo, np, phi_slider, sta):
    phi = sta.scalar(phi_slider.value).name(latex=r"\varphi")
    B = (g0 * g1).name("B")
    R = exp(B * phi / 2).name("R")
    g0p = (R * g0 * ~R).name(latex=r"\gamma_0'")
    g1p = (R * g1 * ~R).name(latex=r"\gamma_1'")

    beta = np.tanh(phi_slider.value)
    gamma = np.cosh(phi_slider.value)

    _md = t"""
    {phi.display()} $\\quad$ (rapidity) <br/>
    {B.display()} $\\quad$ (boost plane) <br/>
    {R.display()} <br/>
    {g0p.display()} <br/>
    {g1p.display()} <br/>
    $\\beta = v/c = \\tanh\\varphi = {beta:.4f} \\quad$ ({beta*100:.1f}% the speed of light) <br/>
    $\\gamma = \\cosh\\varphi = {gamma:.4f}$
    """

    mo.vstack([phi_slider, gm.md(_md), draw_minkowski(g0p, g1p, phi_slider.value)])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
