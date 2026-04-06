import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Maxwell Equations in STA

    In spacetime algebra, the four Maxwell equations compress into one equation:

    $$
    \nabla F = J.
    $$

    This notebook uses a reduced plane-wave ansatz to show how that one equation
    naturally splits into two grade channels. In vacuum, both must vanish.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$ and an observer
    $\gamma_0$ with relative spatial basis

    $$
    \sigma_i = \gamma_i \gamma_0.
    $$

    We restrict to a wave traveling along $\sigma_3$, with electric field along
    $\sigma_1$ and magnetic field along $\sigma_2$.
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
    ## Plane-Wave Ansatz

    Use the phase

    $$
    \xi = kz - \omega t + \phi
    $$

    with

    $$
    E_x = E_0 \cos \xi,
    \qquad
    B_y = B_0 \cos \xi.
    $$

    For this restricted ansatz, $\nabla F = 0$ reduces to two scalar residuals:

    $$
    \text{grade-1 coefficient} \propto \omega E_0 - k B_0
    $$

    $$
    \text{grade-3 coefficient} \propto \omega B_0 - k E_0.
    $$
    """
    )
    return


@app.cell
def _(mo):
    e_amplitude = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="E amplitude", show_value=True)
    b_amplitude = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="B amplitude", show_value=True)
    omega = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="ω", show_value=True)
    wave_number = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="k", show_value=True)
    phase = mo.ui.slider(0.0, 2 * 3.14159, step=0.05, value=0.0, label="Phase offset", show_value=True)
    return b_amplitude, e_amplitude, omega, phase, wave_number


@app.cell
def _(
    I,
    b_amplitude,
    draw_maxwell_plane_wave,
    e_amplitude,
    gm,
    mo,
    np,
    omega,
    phase,
    s1,
    s2,
    s3,
    wave_number,
):
    _xi = phase.value
    _E_coeff = e_amplitude.value * np.cos(_xi)
    _B_coeff = b_amplitude.value * np.cos(_xi)

    _E = (_E_coeff * s1).name("E")
    _B = (_B_coeff * s2).name("B")
    _k_dir = s3.name("k")
    _F = (_E + I * _B).name("F")

    _grade1_coeff = (omega.value * e_amplitude.value - wave_number.value * b_amplitude.value) * np.sin(_xi)
    _grade3_coeff = (omega.value * b_amplitude.value - wave_number.value * e_amplitude.value) * np.sin(_xi)

    _vacuum_like = abs(_grade1_coeff) < 1e-9 and abs(_grade3_coeff) < 1e-9
    _status = "Both channels vanish, so this ansatz satisfies the vacuum equation." if _vacuum_like else "At least one channel is nonzero, so this ansatz does not satisfy the vacuum equation."

    _md = t"""
    {_E.display()} <br/>
    {_B.display()} <br/>
    {_F.display()} <br/>
    For this plane-wave ansatz:

    $$\\langle \\nabla F \\rangle_1 \\text{{ coefficient}} = {_grade1_coeff:.4f}$$

    $$\\langle \\nabla F \\rangle_3 \\text{{ coefficient}} = {_grade3_coeff:.4f}$$

    {_status}
    """

    mo.vstack(
        [
            e_amplitude,
            b_amplitude,
            omega,
            wave_number,
            phase,
            gm.md(_md),
            draw_maxwell_plane_wave(
                _E.eval(),
                _B.eval(),
                _k_dir.eval(),
                e_amplitude.value,
                b_amplitude.value,
                omega.value,
                wave_number.value,
                phase.value,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    In this reduced setting, the single STA equation is already doing the real
    conceptual work. It does not merely bundle four equations together: its
    geometric product naturally separates into grade channels, and those channels
    encode the different Maxwell constraints.
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
    def draw_maxwell_plane_wave(E_rel, B_rel, k_rel, e_amp, b_amp, omega, wave_number, phase_value):
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
        _E_wave = e_amp * np.cos(_xs - phase_value)
        _B_wave = b_amp * np.cos(_xs - phase_value)
        _grade1 = (omega * e_amp - wave_number * b_amp) * np.sin(phase_value)
        _grade3 = (omega * b_amp - wave_number * e_amp) * np.sin(phase_value)

        _fig = plt.figure(figsize=(14.0, 5.0))
        _ax1 = _fig.add_subplot(131, projection="3d")
        _ax2 = _fig.add_subplot(132)
        _ax3 = _fig.add_subplot(133)

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
        _ax1.set_title("Field and propagation directions")
        _ax1.plot([], [], color="#d62828", label="E")
        _ax1.plot([], [], color="#2563eb", label="B")
        _ax1.plot([], [], color="#222222", label="propagation")
        _ax1.legend(loc="upper left")

        _ax2.plot(_xs, _E_wave, color="#d62828", linewidth=2.6, label=r"$E_x$")
        _ax2.plot(_xs, _B_wave, color="#2563eb", linewidth=2.0, linestyle="--", label=r"$B_y$")
        _ax2.set_xlabel("Phase coordinate")
        _ax2.set_ylabel("Field amplitude")
        _ax2.set_ylim(-2.2, 2.2)
        _ax2.grid(True, alpha=0.25)
        _ax2.set_title("Wave profiles")
        _ax2.legend(loc="upper right")

        _ax3.bar(
            [0, 1],
            [_grade1, _grade3],
            color=["#7c3aed", "#f59e0b"],
            alpha=0.82,
            width=0.6,
        )
        _ax3.set_xticks([0, 1], [r"$\langle \nabla F \rangle_1$", r"$\langle \nabla F \rangle_3$"])
        _ax3.set_ylim(-2.2, 2.2)
        _ax3.axhline(0, color="#555555", lw=1.0, alpha=0.45)
        _ax3.grid(True, axis="y", alpha=0.25)
        _ax3.set_title("Grade-channel residuals")

        plt.close(_fig)
        return _fig

    return (draw_maxwell_plane_wave,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
