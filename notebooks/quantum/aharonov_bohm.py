import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Aharonov-Bohm Holonomy

    A charged matter wave can travel only through regions where the magnetic field
    is zero, and still have its interference pattern shifted by magnetic flux
    trapped in an inaccessible interior region.

    The right geometric object is not the phase on one open path by itself. It is
    the closed-loop holonomy around the enclosed flux.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(2,0)$ only as a phase plane.

    Its pseudoscalar

    $$
    I = e_{12}, \qquad I^2 = -1
    $$

    plays the role of the usual imaginary unit. The path phase factor is then an
    even multivector

    $$
    U(\phi) = e^{-I\phi}.
    $$

    This is an ordinary $U(1)$ phase story, not a spinor half-angle story.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    I = (e1 * e2).name(latex="I")
    return I, alg


@app.cell
def _(mo):
    flux_quanta = mo.ui.slider(0.0, 2.0, step=0.01, value=0.50, label="Enclosed flux Φ / Φ₀", show_value=True)
    split = mo.ui.slider(0.0, 1.0, step=0.01, value=0.50, label="Gauge split to upper path", show_value=True)
    screen_phase = mo.ui.slider(-3.14, 3.14, step=0.01, value=0.0, label="Detector phase χ = κx", show_value=True)
    return flux_quanta, screen_phase, split


@app.cell
def _(I, aharonov_bohm_plot, alg, exp, flux_quanta, gm, mo, np, screen_phase, split):
    phi_flux = alg.scalar(2 * np.pi * flux_quanta.value).name(latex=r"\Delta\phi_{\mathrm{AB}}")
    chi = alg.scalar(screen_phase.value).name(latex=r"\chi")

    phi_upper = alg.scalar(split.value * phi_flux.scalar_part).name(latex=r"\phi_{\mathrm{upper}}")
    phi_lower = alg.scalar(-(1.0 - split.value) * phi_flux.scalar_part).name(latex=r"\phi_{\mathrm{lower}}")

    U_upper = exp(-I * phi_upper.scalar_part).name(latex=r"U_{\mathrm{upper}}")
    U_lower = exp(-I * phi_lower.scalar_part).name(latex=r"U_{\mathrm{lower}}")
    holonomy = (U_upper * ~U_lower).name(latex=r"\mathcal{H}")

    total_phase = alg.scalar(chi.scalar_part + phi_flux.scalar_part).name(latex=r"\chi + \Delta\phi_{\mathrm{AB}}")
    bright = alg.scalar(0.5 * (1.0 + np.cos(total_phase.scalar_part))).name(latex=r"P_{\mathrm{bright}}")
    dark = alg.scalar(0.5 * (1.0 - np.cos(total_phase.scalar_part))).name(latex=r"P_{\mathrm{dark}}")

    _shift_deg = np.degrees(phi_flux.scalar_part)
    _md = t"""
    {I.display()} <br/>
    {phi_flux.display()} <br/>
    {phi_upper.display()} <br/>
    {phi_lower.display()} <br/>
    {U_upper.display()} <br/>
    {U_lower.display()} <br/>
    {holonomy.display()} <br/>
    {chi.display()} <br/>
    {total_phase.display()} <br/>
    {bright.display()} <br/>
    {dark.display()} <br/>
    Fringe shift from the enclosed flux: ${_shift_deg:.1f}^\\circ$. The split between upper and lower path phases changes the open-path factors, but not the holonomy or the detector probabilities.
    """

    mo.vstack(
        [
            flux_quanta,
            split,
            screen_phase,
            gm.md(_md),
            aharonov_bohm_plot(U_upper, U_lower, holonomy, phi_flux.scalar_part, screen_phase.value, bright.scalar_part, dark.scalar_part, split.value),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The magnetic field can vanish on both paths and still matter through the
    enclosed flux. That is why the effect is best understood as holonomy:
    individual open-path phases can be redistributed, but the closed-loop phase
    difference and the shifted interference pattern are gauge-invariant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(I, np, plt):
    def _phase_coords(U):
        _scalar = U.scalar_part
        _biv = (U | I).scalar_part / ((I | I).scalar_part)
        return _scalar, _biv

    def aharonov_bohm_plot(U_upper, U_lower, holonomy, delta_phi, screen_phase, bright, dark, split):
        _uu = _phase_coords(U_upper)
        _ul = _phase_coords(U_lower)
        _hh = _phase_coords(holonomy)

        _fig = plt.figure(figsize=(14.2, 4.8))
        _ax0 = _fig.add_subplot(131)
        _ax1 = _fig.add_subplot(132)
        _ax2 = _fig.add_subplot(133)

        _theta = np.linspace(0, 2 * np.pi, 240)
        _ax0.fill(0.35 * np.cos(_theta), 0.35 * np.sin(_theta), color="#2563eb", alpha=0.18)
        _ax0.text(0, 0, r"$\Phi$", ha="center", va="center", color="#2563eb", fontsize=13)
        _upper = np.linspace(np.pi, 0, max(40, int(260 * split)))
        _lower = np.linspace(np.pi, 2 * np.pi, max(40, int(260 * (1 - split))))
        _ax0.plot(1.7 * np.cos(_upper), 1.1 * np.sin(_upper), color="#d62828", linewidth=2.5)
        _ax0.plot(1.7 * np.cos(_lower), 1.1 * np.sin(_lower), color="#10b981", linewidth=2.5)
        _ax0.plot([-1.7], [0], "ks", ms=8)
        _ax0.plot([1.7], [0], "k^", ms=9)
        _ax0.text(-1.7, -0.22, "source", ha="center")
        _ax0.text(1.7, -0.22, "screen", ha="center")
        _ax0.set_xlim(-2.1, 2.1)
        _ax0.set_ylim(-1.5, 1.5)
        _ax0.set_aspect("equal")
        _ax0.axis("off")
        _ax0.set_title("Two field-free paths around the flux tube")

        _circle = plt.Circle((0, 0), 1.0, fill=False, color="#999999", alpha=0.28, linewidth=1.2)
        _ax1.add_patch(_circle)
        _ax1.axhline(0, color="#999999", alpha=0.18, linewidth=0.8)
        _ax1.axvline(0, color="#999999", alpha=0.18, linewidth=0.8)
        for (_x, _y), _label, _color in [
            (_uu, r"$U_{\mathrm{upper}}$", "#d62828"),
            (_ul, r"$U_{\mathrm{lower}}$", "#10b981"),
            (_hh, r"$\mathcal{H}$", "#7c3aed"),
        ]:
            _ax1.annotate(
                "",
                xy=(_x, _y),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=_color, lw=2.5, mutation_scale=18),
            )
            _ax1.text(1.1 * _x, 1.1 * _y, _label, color=_color, ha="center", va="center")
        _ax1.set_xlim(-1.35, 1.35)
        _ax1.set_ylim(-1.35, 1.35)
        _ax1.set_aspect("equal")
        _ax1.set_xticks([])
        _ax1.set_yticks([])
        _ax1.set_title("Open-path phases and closed-loop holonomy")

        _chi = np.linspace(-np.pi, np.pi, 500)
        _bright_curve = 0.5 * (1.0 + np.cos(_chi + delta_phi))
        _dark_curve = 0.5 * (1.0 - np.cos(_chi + delta_phi))
        _ax2.plot(_chi, _bright_curve, color="#2563eb", linewidth=2.5, label="bright")
        _ax2.plot(_chi, _dark_curve, color="#d62828", linewidth=2.5, label="dark")
        _ax2.plot([screen_phase], [bright], "o", color="#2563eb", ms=7)
        _ax2.plot([screen_phase], [dark], "o", color="#d62828", ms=7)
        _ax2.set_xlim(-np.pi, np.pi)
        _ax2.set_ylim(-0.05, 1.05)
        _ax2.set_xlabel(r"detector phase $\chi = \kappa x$")
        _ax2.set_ylabel("detector probability")
        _ax2.set_title("Enclosed flux shifts the interference fringes")
        _ax2.grid(True, alpha=0.2)
        _ax2.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (aharonov_bohm_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
