import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Spinor Sign in an Interferometer

    A spinor and its negative give the same spin-direction measurement. That can
    make the double cover feel unphysical.

    But in a coherent two-path interferometer, the relative sign between the two
    path amplitudes matters. Then $\psi$ and $-\psi$ no longer lead to the same
    output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ and a very simple physical picture:

    - one path is left untouched
    - in the other path, the spinor is rotated about the $e_3$ axis
    - the two paths are recombined coherently

    This is the right kind of setup for neutron or electron interferometry. The
    observable spin direction in each arm can stay the same, while the spinor
    phase still changes the interference pattern.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    e12 = (e1 * e2).name(latex=r"e_{12}")
    return e12, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Arm Rotates

    The reference arm keeps the spinor $\psi_{\mathrm{ref}} = 1$.

    The rotated arm uses

    $$
    R_z(\alpha) = e^{-(\alpha/2)e_{12}}.
    $$

    Because this is a rotation about $e_3$, both arms still have the same Bloch
    direction $e_3$. So a model that only tracks spin direction predicts no
    change at recombination.
    """)
    return


@app.cell
def _(mo):
    rotation_angle = mo.ui.slider(0, 720, step=1, value=120, label="Spin rotation α in upper arm", show_value=True)
    return (rotation_angle,)


@app.cell
def _(draw_spinor_interferometer, e12, e3, exp, gm, mo, np, rotation_angle):
    _alpha = np.radians(rotation_angle.value)
    _psi_ref = (1 + 0 * e3).name(latex=r"\psi_{\mathrm{ref}}")
    _Rz = exp((-_alpha / 2) * e12).name(latex=r"R_z")
    _psi_upper = (_Rz * _psi_ref).name(latex=r"\psi_{\mathrm{upper}}")

    _spin_ref = (_psi_ref * e3 * ~_psi_ref).name(latex=r"s_{\mathrm{ref}}")
    _spin_upper = (_psi_upper * e3 * ~_psi_upper).name(latex=r"s_{\mathrm{upper}}")

    _psi_bright = (( _psi_ref + _psi_upper) / 2).name(latex=r"\psi_{\mathrm{bright}}")
    _psi_dark = (( _psi_ref - _psi_upper) / 2).name(latex=r"\psi_{\mathrm{dark}}")
    _bright = (~_psi_bright * _psi_bright).scalar_part
    _dark = (~_psi_dark * _psi_dark).scalar_part

    _naive_bright = 1.0
    _naive_dark = 0.0

    _md = t"""
    {_psi_ref.display()} <br/>
    {_Rz.display()} <br/>
    {_psi_upper.display()} <br/>
    {_spin_ref.display()} <br/>
    {_spin_upper.display()} <br/>
    {_psi_bright.display()} <br/>
    {_psi_dark.display()} <br/>
    Coherent bright-port probability: ${_bright:.4f}$ <br/>
    Coherent dark-port probability: ${_dark:.4f}$ <br/>
    Bloch-only prediction: bright ${_naive_bright:.1f}$, dark ${_naive_dark:.1f}$
    """

    mo.vstack(
        [
            rotation_angle,
            gm.md(_md),
            draw_spinor_interferometer(
                _Rz.eval(),
                _spin_ref.eval(),
                _spin_upper.eval(),
                _bright,
                _dark,
                rotation_angle.value,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The Bloch vector is enough for single-path spin measurements, but not for
    coherent path recombination. At $\alpha = 360^\circ$, the upper-arm spinor is
    the negative of the reference spinor, even though the measured spin direction
    is unchanged. That minus sign is invisible in observation space and decisive
    in interference space.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(e12, np, plt):
    def draw_spinor_interferometer(rotor_upper, spin_ref, spin_upper, bright, dark, angle_deg):
        _rotor_scalar = rotor_upper.scalar_part
        _rotor_bivector = -(rotor_upper | e12).scalar_part / ((e12 | e12).scalar_part)
        _spin_ref = np.array(spin_ref.vector_part[:3], dtype=float)
        _spin_upper = np.array(spin_upper.vector_part[:3], dtype=float)

        _fig = plt.figure(figsize=(14.0, 5.2))
        _ax1 = _fig.add_subplot(131, projection="3d")
        _ax2 = _fig.add_subplot(132)
        _ax3 = _fig.add_subplot(133)

        _u = np.linspace(0, 2 * np.pi, 32)
        _v = np.linspace(0, np.pi, 16)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax1.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08)
        _ax1.quiver(0, 0, 0, _spin_ref[0], _spin_ref[1], _spin_ref[2], color="#2563eb", linewidth=2.8, arrow_length_ratio=0.1)
        _ax1.quiver(0, 0, 0, _spin_upper[0], _spin_upper[1], _spin_upper[2], color="#d62828", linewidth=2.2, linestyle="--", arrow_length_ratio=0.1)
        _ax1.set_xlim(-1, 1)
        _ax1.set_ylim(-1, 1)
        _ax1.set_zlim(-1, 1)
        _ax1.set_box_aspect((1, 1, 1))
        _ax1.set_title("Both arms give the same spin direction")

        _circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", alpha=0.25, linewidth=1.2)
        _ax2.add_patch(_circle)
        _ax2.axhline(0, color="gray", alpha=0.15, linewidth=0.8)
        _ax2.axvline(0, color="gray", alpha=0.15, linewidth=0.8)
        _ax2.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.5))
        _ax2.annotate("", xy=(_rotor_scalar, -_rotor_bivector), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.5))
        _ax2.text(1.08, 0.0, r"$\psi_{\mathrm{ref}}$", color="#2563eb", ha="center", va="center")
        _ax2.text(1.08 * _rotor_scalar, -1.08 * _rotor_bivector, r"$\psi_{\mathrm{upper}}$", color="#d62828", ha="center", va="center")
        _ax2.set_xlim(-1.3, 1.3)
        _ax2.set_ylim(-1.3, 1.3)
        _ax2.set_aspect("equal")
        _ax2.set_xticks([])
        _ax2.set_yticks([])
        _ax2.set_title("Rotor-space sign does change")

        _alphas = np.linspace(0, 720, 721)
        _bright_curve = np.cos(np.radians(_alphas) / 4) ** 2
        _dark_curve = np.sin(np.radians(_alphas) / 4) ** 2
        _ax3.plot(_alphas, _bright_curve, color="#2563eb", linewidth=2.5, label="bright port")
        _ax3.plot(_alphas, _dark_curve, color="#d62828", linewidth=2.5, label="dark port")
        _ax3.plot([0, 720], [1, 1], color="#2563eb", alpha=0.18, linewidth=1.6, linestyle="--", label="Bloch-only bright")
        _ax3.plot([0, 720], [0, 0], color="#d62828", alpha=0.18, linewidth=1.6, linestyle="--", label="Bloch-only dark")
        _ax3.plot([angle_deg], [bright], "o", color="#2563eb", ms=7)
        _ax3.plot([angle_deg], [dark], "o", color="#d62828", ms=7)
        _ax3.set_xlim(0, 720)
        _ax3.set_ylim(-0.05, 1.05)
        _ax3.set_xlabel("spin rotation α (degrees)")
        _ax3.set_ylabel("output probability")
        _ax3.grid(True, alpha=0.25)
        _ax3.set_title("Only spinor-space tracking gets the interference right")
        _ax3.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_spinor_interferometer,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
