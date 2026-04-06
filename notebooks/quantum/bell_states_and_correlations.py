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
    # Bell Singlet Correlations

    The Bell singlet does not prefer any spatial direction. What matters is only
    the geometric angle between the two measurement axes. In GA language, the
    correlation is just the negative dot product of those axes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$, but keep the measurement axes in one visible plane.

    For the singlet state,

    $$
    E(a,b) = -\,a \cdot b.
    $$

    So once the two measurement directions are chosen, the correlation and the
    same-result / opposite-result probabilities are fixed by geometry alone.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    delta = mo.ui.slider(0, 180, step=1, value=45, label="Angle between axes δ", show_value=True)
    return (delta,)


@app.cell
def _(alg, delta, draw_bell_singlet, e1, e2, exp, gm, mo, np):
    angle = alg.scalar(np.radians(delta.value)).name(latex=r"\delta")

    a = e1.name(latex="a")
    rotor = exp(-(angle.scalar_part / 2.0) * (e1 * e2)).name(latex=r"R_\delta")
    b = (rotor * e1 * ~rotor).name(latex="b")

    correlation = (-(a | b)).name(latex=r"E(a,b)")
    p_same = (alg.frac(1, 2) * (alg.scalar(1).name(latex="1") + correlation)).name(latex=r"P_{\mathrm{same}}")
    p_opp = (alg.frac(1, 2) * (alg.scalar(1).name(latex="1") - correlation)).name(latex=r"P_{\mathrm{opp}}")

    _md = t"""
    {angle.display()} <br/>
    {a.display()} <br/>
    {rotor.display()} <br/>
    {b.display()} <br/>
    {correlation.display()} <br/>
    {p_same.display()} <br/>
    {p_opp.display()} <br/>
    In the singlet, aligned axes give perfect anti-correlation and opposite axes give perfect correlation.
    """

    mo.vstack([delta, gm.md(_md), draw_bell_singlet(delta.value, b, correlation.scalar_part, p_same.scalar_part, p_opp.scalar_part)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The singlet correlation is not an extra rule pasted on top of the geometry.
    It is exactly the geometry: the whole dependence is the relative angle between
    the two axes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_bell_singlet(delta_deg, b, correlation, p_same, p_opp):
        _b = np.array(b.vector_part[:2], dtype=float)
        _angles = np.linspace(0.0, np.pi, 400)
        _curve = -np.cos(_angles)

        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.2, 4.8))

        _ax0.plot(np.degrees(_angles), _curve, color="#2563eb", linewidth=2.5)
        _ax0.plot([delta_deg], [correlation], "o", color="#222222", ms=7)
        _ax0.axhline(0, color="#333333", lw=1.0, alpha=0.45)
        _ax0.set_xlabel("axis angle difference (degrees)")
        _ax0.set_ylabel(r"$E(a,b)$")
        _ax0.set_ylim(-1.05, 1.05)
        _ax0.grid(True, alpha=0.18)
        _ax0.set_title("Bell singlet correlation")

        _ax1.quiver(0, 0, 1, 0, angles="xy", scale_units="xy", scale=1, color="#d62828", width=0.015)
        _ax1.quiver(0, 0, _b[0], _b[1], angles="xy", scale_units="xy", scale=1, color="#2563eb", width=0.015)
        _ax1.text(1.05, 0.05, "a", color="#d62828")
        _ax1.text(_b[0] + 0.06, _b[1] + 0.05, "b", color="#2563eb")
        _ax1.bar([0, 1], [p_same, p_opp], color=["#7c3aed", "#10b981"], alpha=0.86, width=0.35, bottom=[-1.15, -1.15])
        _ax1.text(0, -1.12 + p_same, f"same\n{p_same:.3f}", ha="center", va="bottom", color="#222222", fontsize=10)
        _ax1.text(1, -1.12 + p_opp, f"opp\n{p_opp:.3f}", ha="center", va="bottom", color="#222222", fontsize=10)
        _ax1.set_aspect("equal")
        _ax1.set_xlim(-1.3, 1.45)
        _ax1.set_ylim(-1.25, 1.25)
        _ax1.grid(True, alpha=0.18)
        _ax1.set_xticks([])
        _ax1.set_yticks([])
        _ax1.set_title("Measurement-axis geometry and probabilities")

        plt.close(_fig)
        return _fig

    return (draw_bell_singlet,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
