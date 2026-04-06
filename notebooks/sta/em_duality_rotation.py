import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, grade
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_sta, exp, gm, grade, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Electromagnetic Duality Rotation

    Boosts mix electric and magnetic fields because observers change. Duality
    rotation mixes them even for the same observer. In STA, that mixing is just
    one pseudoscalar phase rotation applied to the Faraday bivector.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(1,3)$ and the observer-relative spatial vectors

    $$
    \sigma_i = \gamma_i \gamma_0.
    $$

    Start with

    $$
    F = E + I B.
    $$

    A duality rotation uses

    $$
    D(\alpha) = e^{-I\alpha},
    \qquad
    F' = D(\alpha) F,
    $$

    which rotates electric and magnetic content into each other.
    """)
    return


@app.cell
def _(Algebra, b_sta):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.I.name("I")
    s1 = (g1 * g0).name(latex=r"\sigma_1")
    s2 = (g2 * g0).name(latex=r"\sigma_2")
    s3 = (g3 * g0).name(latex=r"\sigma_3")
    return I, s1, s2, s3, sta


@app.cell
def _(mo):
    e_amp = mo.ui.slider(0.0, 2.0, step=0.05, value=1.0, label="Initial |E|", show_value=True)
    b_amp = mo.ui.slider(0.0, 2.0, step=0.05, value=0.5, label="Initial |B|", show_value=True)
    alpha = mo.ui.slider(0, 360, step=1, value=40, label="Duality angle α", show_value=True)
    return alpha, b_amp, e_amp


@app.cell
def _(I, alpha, b_amp, draw_duality_rotation, e_amp, gm, grade, mo, np, s1, s2, s3, sta):
    E = (e_amp.value * s1).name("E", latex="E")
    B = (b_amp.value * s2).name("B", latex="B")
    F = (E + I * B).name("F", latex="F")

    dual_angle = sta.scalar(np.radians(alpha.value)).name(latex=r"\alpha")
    D = exp(-I * dual_angle.scalar_part).name(latex="D")
    F_rot = (D * F).name(latex=r"F'")

    _ca = np.cos(dual_angle.scalar_part)
    _sa = np.sin(dual_angle.scalar_part)
    E_rot = (_ca * E - _sa * B).name(latex=r"E'")
    B_rot = (_ca * B + _sa * E).name(latex=r"B'")

    energy_like = ((E | E) + (B | B)).name(latex=r"|E|^2 + |B|^2")
    energy_like_rot = ((E_rot | E_rot) + (B_rot | B_rot)).name(latex=r"|E'|^2 + |B'|^2")
    F2 = (F * F).name(latex=r"F^2")
    F2_rot = (F_rot * F_rot).name(latex=r"{F'}^2")
    scalar_part = grade(F2, 0).name(latex=r"\langle F^2 \rangle_0")
    scalar_part_rot = grade(F2_rot, 0).name(latex=r"\langle {F'}^2 \rangle_0")
    pseudo_part = grade(F2, 4).name(latex=r"\langle F^2 \rangle_4")
    pseudo_part_rot = grade(F2_rot, 4).name(latex=r"\langle {F'}^2 \rangle_4")

    _md = t"""
    {E.display()} <br/>
    {B.display()} <br/>
    {F.display()} <br/>
    {dual_angle.display()} <br/>
    {D.display()} <br/>
    {F_rot.display()} <br/>
    {E_rot.display()} <br/>
    {B_rot.display()} <br/>
    {energy_like.display()} <br/>
    {energy_like_rot.display()} <br/>
    {scalar_part.display()} <br/>
    {scalar_part_rot.display()} <br/>
    {pseudo_part.display()} <br/>
    {pseudo_part_rot.display()} <br/>
    Duality rotation preserves the total field strength $|E|^2 + |B|^2$, while rotating electric and magnetic content into each other.
    """

    mo.vstack([e_amp, b_amp, alpha, gm.md(_md), draw_duality_rotation(E, B, E_rot, B_rot, alpha.value, e_amp.value, b_amp.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    A boost mixes $E$ and $B$ because two observers split the same bivector field
    differently. A duality rotation mixes $E$ and $B$ even for one observer,
    because it rotates the Faraday bivector in its own electric-magnetic plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt, s1, s2, s3):
    def _sigma_components(_mv):
        return np.array(
            [
                (_mv.eval() | s1).scalar_part / ((s1 | s1).scalar_part),
                (_mv.eval() | s2).scalar_part / ((s2 | s2).scalar_part),
                (_mv.eval() | s3).scalar_part / ((s3 | s3).scalar_part),
            ],
            dtype=float,
        )

    def draw_duality_rotation(E, B, E_rot, B_rot, alpha_deg, e_amp, b_amp):
        _E = _sigma_components(E)
        _B = _sigma_components(B)
        _Er = _sigma_components(E_rot)
        _Br = _sigma_components(B_rot)

        _alphas = np.linspace(0, 2 * np.pi, 361)
        _E1 = e_amp * np.cos(_alphas)
        _E2 = -b_amp * np.sin(_alphas)
        _B1 = e_amp * np.sin(_alphas)
        _B2 = b_amp * np.cos(_alphas)

        _fig = plt.figure(figsize=(12.0, 5.2))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        for _vec, _color, _label, _alpha in [(_E, "#d62828", "E", 0.35), (_B, "#2563eb", "B", 0.35), (_Er, "#d62828", "E'", 1.0), (_Br, "#2563eb", "B'", 1.0)]:
            _ax0.quiver(0, 0, 0, _vec[0], _vec[1], _vec[2], color=_color, linewidth=2.8 if _alpha > 0.9 else 1.8, alpha=_alpha, arrow_length_ratio=0.1)
            if _alpha > 0.9:
                _ax0.text(1.08 * _vec[0], 1.08 * _vec[1], 1.08 * _vec[2], _label, color=_color)
        _ax0.set_xlim(-2.1, 2.1)
        _ax0.set_ylim(-2.1, 2.1)
        _ax0.set_zlim(-2.1, 2.1)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_xlabel(r"$\sigma_1$")
        _ax0.set_ylabel(r"$\sigma_2$")
        _ax0.set_zlabel(r"$\sigma_3$")
        _ax0.set_title("E and B after duality rotation")

        _ax1.plot(np.degrees(_alphas), _E1, color="#d62828", linewidth=2.2, label=r"$E'_{\sigma_1}$")
        _ax1.plot(np.degrees(_alphas), _E2, color="#d62828", linewidth=2.2, linestyle="--", label=r"$E'_{\sigma_2}$")
        _ax1.plot(np.degrees(_alphas), _B1, color="#2563eb", linewidth=2.2, label=r"$B'_{\sigma_1}$")
        _ax1.plot(np.degrees(_alphas), _B2, color="#2563eb", linewidth=2.2, linestyle="--", label=r"$B'_{\sigma_2}$")
        _ax1.plot([alpha_deg], [_Er[0]], "o", color="#d62828", ms=6)
        _ax1.plot([alpha_deg], [_Er[1]], "o", color="#d62828", ms=6)
        _ax1.plot([alpha_deg], [_Br[0]], "o", color="#2563eb", ms=6)
        _ax1.plot([alpha_deg], [_Br[1]], "o", color="#2563eb", ms=6)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.4)
        _ax1.set_xlim(0, 360)
        _ax1.set_xlabel("duality angle α (degrees)")
        _ax1.set_ylabel("channel amplitude")
        _ax1.grid(True, alpha=0.18)
        _ax1.set_title("Duality rotates electric and magnetic channels")
        _ax1.legend(loc="upper right", ncol=2)

        plt.close(_fig)
        return _fig

    return (draw_duality_rotation,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
