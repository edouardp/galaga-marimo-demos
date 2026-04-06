import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, unit
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, gm, mo, np, plt, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Fresnel Polarisation in GA

    At a dielectric interface, the two polarization channels do not reflect the
    same way. The parallel and perpendicular components see different Fresnel
    coefficients, so the reflected field is a new geometric combination of those
    two basis directions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(2,0)$ and treat the two axes as the two polarization
    channels:

    - $e_1$: parallel / p polarization
    - $e_2$: perpendicular / s polarization

    The input field is decomposed into those channels, each channel is scaled by
    its Fresnel reflection coefficient, and the reflected field is rebuilt from
    the result.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    incidence = mo.ui.slider(0, 89, step=1, value=45, label="Incidence angle θᵢ", show_value=True)
    n1 = mo.ui.slider(1.0, 2.0, step=0.01, value=1.0, label="Index n₁", show_value=True)
    n2 = mo.ui.slider(1.0, 2.5, step=0.01, value=1.5, label="Index n₂", show_value=True)
    pol = mo.ui.slider(0, 90, step=1, value=30, label="Input polarization angle α", show_value=True)
    return incidence, n1, n2, pol


@app.cell
def _(alg, draw_fresnel, e1, e2, gm, incidence, mo, n1, n2, np, pol, unit):
    theta_i = alg.scalar(np.radians(incidence.value)).name(latex=r"\theta_i")
    alpha = alg.scalar(np.radians(pol.value)).name(latex=r"\alpha")
    n_1 = alg.scalar(n1.value).name(latex=r"n_1")
    n_2 = alg.scalar(n2.value).name(latex=r"n_2")

    _sin_t = np.clip(n1.value * np.sin(theta_i.scalar_part) / n2.value, -1.0, 1.0)
    theta_t = alg.scalar(np.arcsin(_sin_t)).name(latex=r"\theta_t")

    r_s = alg.scalar(
        (n1.value * np.cos(theta_i.scalar_part) - n2.value * np.cos(theta_t.scalar_part))
        / (n1.value * np.cos(theta_i.scalar_part) + n2.value * np.cos(theta_t.scalar_part))
    ).name(latex=r"r_s")
    r_p = alg.scalar(
        (n2.value * np.cos(theta_i.scalar_part) - n1.value * np.cos(theta_t.scalar_part))
        / (n2.value * np.cos(theta_i.scalar_part) + n1.value * np.cos(theta_t.scalar_part))
    ).name(latex=r"r_p")

    input_field = unit(np.cos(alpha.scalar_part) * e1 + np.sin(alpha.scalar_part) * e2).name(latex=r"E_{\mathrm{in}}")
    p_component = ((input_field | e1) * e1).name(latex=r"E_p")
    s_component = ((input_field | e2) * e2).name(latex=r"E_s")
    reflected_field = (r_p * p_component + r_s * s_component).name(latex=r"E_r")

    _brewed = abs(r_p.scalar_part) < 1e-4
    _brewster = ""
    if _brewed:
        _brewster = "At this angle, the p-polarized reflection is approximately zero."

    _md = t"""
    {n_1.display()} <br/>
    {n_2.display()} <br/>
    {theta_i.display()} <br/>
    {theta_t.display()} <br/>
    {input_field.display()} <br/>
    {p_component.display()} <br/>
    {s_component.display()} <br/>
    {r_p.display()} <br/>
    {r_s.display()} <br/>
    {reflected_field.display()} <br/>
    {_brewster}
    """

    mo.vstack(
        [
            incidence,
            n1,
            n2,
            pol,
            gm.md(_md),
            draw_fresnel(theta_i.scalar_part, n1.value, n2.value, input_field, p_component, s_component, reflected_field, r_p.scalar_part, r_s.scalar_part),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The interface does not act on the whole field uniformly. It acts differently
    on the two polarization channels. GA makes that explicit: decompose, scale
    each channel, then recombine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_fresnel(theta_i, n1, n2, input_field, p_component, s_component, reflected_field, r_p, r_s):
        _Ein = np.array(input_field.vector_part[:2], dtype=float)
        _Ep = np.array(p_component.vector_part[:2], dtype=float)
        _Es = np.array(s_component.vector_part[:2], dtype=float)
        _Er = np.array(reflected_field.vector_part[:2], dtype=float)

        _angles = np.radians(np.linspace(0, 89, 300))
        _theta_t_curve = np.arcsin(np.clip(n1 * np.sin(_angles) / n2, -1.0, 1.0))
        _rs_curve = (n1 * np.cos(_angles) - n2 * np.cos(_theta_t_curve)) / (n1 * np.cos(_angles) + n2 * np.cos(_theta_t_curve))
        _rp_curve = (n2 * np.cos(_angles) - n1 * np.cos(_theta_t_curve)) / (n2 * np.cos(_angles) + n1 * np.cos(_theta_t_curve))

        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.4, 4.8))

        for _vec, _label, _color in [
            (_Ein, "input", "#222222"),
            (_Ep, "p part", "#d62828"),
            (_Es, "s part", "#2563eb"),
            (_Er, "reflected", "#7c3aed"),
        ]:
            if np.linalg.norm(_vec) < 1e-9:
                continue
            _ax0.annotate(
                "",
                xy=_vec,
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=_color, lw=2.6, mutation_scale=18, alpha=0.95),
            )
            _ax0.text(_vec[0] + 0.06, _vec[1] + 0.05, _label, color=_color)

        _ax0.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax0.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax0.set_xlim(-1.45, 1.45)
        _ax0.set_ylim(-1.45, 1.45)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.18)
        _ax0.set_xlabel("p channel (e1)")
        _ax0.set_ylabel("s channel (e2)")
        _ax0.set_title("Field decomposition and recombination")

        _ax1.plot(np.degrees(_angles), _rs_curve, color="#2563eb", linewidth=2.5, label=r"$r_s$")
        _ax1.plot(np.degrees(_angles), _rp_curve, color="#d62828", linewidth=2.5, label=r"$r_p$")
        _ax1.plot([np.degrees(theta_i)], [r_s], "o", color="#2563eb", ms=7)
        _ax1.plot([np.degrees(theta_i)], [r_p], "o", color="#d62828", ms=7)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.4)
        _ax1.set_xlabel("incidence angle (degrees)")
        _ax1.set_ylabel("reflection coefficient")
        _ax1.set_ylim(-1.05, 1.05)
        _ax1.grid(True, alpha=0.18)
        _ax1.set_title("Fresnel reflection coefficients")
        _ax1.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_fresnel,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
