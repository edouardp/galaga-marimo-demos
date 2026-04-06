import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, grade
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, grade, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Electromagnetic Waves in STA

    A vacuum plane wave is one of the cleanest spacetime-algebra field examples.
    The electric and magnetic fields still split relative to an observer, but
    together they form one null bivector field.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    Relative to the observer $\gamma_0$, the spatial relative vectors are

    $$
    \sigma_i = \gamma_i \gamma_0.
    $$

    In this notebook the wave propagates along $\sigma_3$, with electric field
    along $\sigma_1$ and magnetic field along $\sigma_2$.
    """
    )
    return


@app.cell
def _(Algebra):
    from galaga.blade_convention import b_sta

    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.I.name("I")
    s1 = (g1 * g0).name(latex=r"\sigma_1")
    s2 = (g2 * g0).name(latex=r"\sigma_2")
    s3 = (g3 * g0).name(latex=r"\sigma_3")
    return I, g0, g1, g2, g3, s1, s2, s3, sta


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## One Null Field

    A vacuum plane wave satisfies:

    - $E \perp B$
    - $|E| = |B|$
    - both field invariants vanish

    So the wave is a null electromagnetic field in STA.
    """
    )
    return


@app.cell
def _(mo):
    amplitude = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="Field amplitude", show_value=True)
    phase = mo.ui.slider(0.0, 2 * 3.14159, step=0.05, value=0.0, label="Phase", show_value=True)
    return amplitude, phase


@app.cell
def _(
    I,
    amplitude,
    draw_em_wave,
    gm,
    grade,
    mo,
    np,
    phase,
    s1,
    s2,
    s3,
):
    _amp = amplitude.value * np.cos(phase.value)
    _E = (_amp * s1).name("E")
    _B = (_amp * s2).name("B")
    _k = s3.name("k")
    _F = (_E + I * _B).name("F")

    _F2 = (_F * _F).name(latex=r"F^2")
    _scalar_invariant = grade(_F2, 0).name(latex=r"\langle F^2 \rangle_0")
    _pseudo_invariant = grade(_F2, 4).name(latex=r"\langle F^2 \rangle_4")

    _md = t"""
    {_E.display()} <br/>
    {_B.display()} <br/>
    {_F.display()} <br/>
    {_F2.display()} <br/>
    {_scalar_invariant.display()} <br/>
    {_pseudo_invariant.display()} <br/>
    This is a null field: the electric and magnetic pieces stay orthogonal, equal in magnitude, and the two invariants vanish.
    """

    mo.vstack([amplitude, phase, gm.md(_md), draw_em_wave(_E.eval(), _B.eval(), _k.eval(), amplitude.value, phase.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    For a vacuum plane wave, the Faraday bivector is not just “an electric field
    plus a magnetic field.” It is one null bivector whose observer-relative split
    happens to have orthogonal electric and magnetic parts of equal size.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Appendum: Plotting Code
    """
    )
    return


@app.cell(hide_code=True)
def _(np, plt, s1, s2, s3):
    def draw_em_wave(E_rel, B_rel, k_rel, amplitude, phase_value):
        def _sigma_components(_mv):
            return np.array(
                [
                    (_mv | s1).scalar_part / ((s1 | s1).scalar_part),
                    (_mv | s2).scalar_part / ((s2 | s2).scalar_part),
                    (_mv | s3).scalar_part / ((s3 | s3).scalar_part),
                ],
                dtype=float,
            )

        _E = _sigma_components(E_rel)
        _B = _sigma_components(B_rel)
        _k = _sigma_components(k_rel)

        _xs = np.linspace(0, 2 * np.pi, 300)
        _wave = amplitude * np.cos(_xs - phase_value)

        _fig = plt.figure(figsize=(11.4, 5.2))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _ax1.quiver(0, 0, 0, _E[0], _E[1], _E[2], color="#d62828", linewidth=2.8)
        _ax1.quiver(0, 0, 0, _B[0], _B[1], _B[2], color="#2563eb", linewidth=2.8)
        _ax1.quiver(0, 0, 0, _k[0], _k[1], _k[2], color="#222222", linewidth=2.2, alpha=0.8)
        _ax1.set_xlim(-2.2, 2.2)
        _ax1.set_ylim(-2.2, 2.2)
        _ax1.set_zlim(-2.2, 2.2)
        _ax1.set_box_aspect((1, 1, 1))
        _ax1.set_xlabel(r"$\sigma_1$")
        _ax1.set_ylabel(r"$\sigma_2$")
        _ax1.set_zlabel(r"$\sigma_3$")
        _ax1.set_title("Observer-relative field directions")
        _ax1.plot([], [], color="#d62828", label="E")
        _ax1.plot([], [], color="#2563eb", label="B")
        _ax1.plot([], [], color="#222222", label="propagation")
        _ax1.legend(loc="upper left")

        _ax2.plot(_xs, _wave, color="#d62828", linewidth=2.6, label=r"$E_{\sigma_1}$")
        _ax2.plot(_xs, _wave, color="#2563eb", linewidth=2.0, linestyle="--", label=r"$B_{\sigma_2}$")
        _ax2.set_xlabel("Phase coordinate")
        _ax2.set_ylabel("Field amplitude")
        _ax2.set_ylim(-2.2, 2.2)
        _ax2.grid(True, alpha=0.25)
        _ax2.set_title("Vacuum plane wave: E and B stay in phase")
        _ax2.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_em_wave,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
