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
    # Entanglement as Geometric Correlation

    A product pair can be understood from two individual Bloch directions. An
    entangled singlet cannot. In the singlet, each subsystem by itself has no
    preferred Bloch direction, yet the pair still has a strong geometric
    correlation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ and keep the measurement axes in one visible plane.

    The point is not to build a full two-particle GA formalism here. The point is
    to compare two geometric correlation stories:

    - a separable product pair, where local Bloch directions already explain the
      joint statistics
    - the Bell singlet, where the local Bloch directions vanish but the joint
      correlation still depends on the relative measurement geometry
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    state_kind = mo.ui.dropdown(
        options={
            "Product pair |↑x↑x⟩": "product",
            "Bell singlet": "singlet",
        },
        value="Product pair |↑x↑x⟩",
        label="State type",
    )
    delta = mo.ui.slider(0, 180, step=1, value=45, label="Angle between measurement axes δ", show_value=True)
    return delta, state_kind


@app.cell
def _(alg, delta, draw_entanglement_geometry, e1, e2, exp, gm, mo, np, state_kind):
    angle = alg.scalar(np.radians(delta.value)).name(latex=r"\delta")

    a = e1.name(latex="a")
    rotor = exp(-(angle.scalar_part / 2.0) * (e1 * e2)).name(latex=r"R_\delta")
    b = (rotor * e1 * ~rotor).name(latex="b")

    one = alg.scalar(1).name(latex="1")
    half = alg.frac(1, 2)

    if state_kind.value == "product":
        s_A = e1.name(latex=r"s_A")
        s_B = e1.name(latex=r"s_B")
        correlation = (((a | s_A) * (b | s_B))).name(latex=r"E(a,b)")
        p_same = (half * (one + correlation)).name(latex=r"P_{\mathrm{same}}")
        p_opp = (half * (one - correlation)).name(latex=r"P_{\mathrm{opp}}")
        _story = "The correlation is explained by the two local Bloch directions."
    else:
        s_A = (alg.scalar(0) * e1).name(latex=r"s_A")
        s_B = (alg.scalar(0) * e1).name(latex=r"s_B")
        correlation = (-(a | b)).name(latex=r"E(a,b)")
        p_same = (half * (one + correlation)).name(latex=r"P_{\mathrm{same}}")
        p_opp = (half * (one - correlation)).name(latex=r"P_{\mathrm{opp}}")
        _story = "The local Bloch directions vanish, so the correlation is genuinely relational."

    _md = t"""
    {angle.display()} <br/>
    {a.display()} <br/>
    {rotor.display()} <br/>
    {b.display()} <br/>
    {s_A.display()} <br/>
    {s_B.display()} <br/>
    {correlation.display()} <br/>
    {p_same.display()} <br/>
    {p_opp.display()} <br/>
    {_story}
    """

    mo.vstack([state_kind, delta, gm.md(_md), draw_entanglement_geometry(state_kind.value, b, correlation.scalar_part, p_same.scalar_part, p_opp.scalar_part, delta.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In a product pair, the joint statistics are already encoded in two local Bloch
    directions. In the singlet, there are no local Bloch directions to assign at
    all, yet the pair still has a precise geometric correlation. That is the kind
    of structure entanglement adds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_entanglement_geometry(state_kind, b, correlation, p_same, p_opp, delta_deg):
        _b = np.array(b.vector_part[:2], dtype=float)
        _angles = np.linspace(0.0, np.pi, 400)
        _product_curve = np.cos(_angles)
        _singlet_curve = -np.cos(_angles)
        _state_label = "Product pair" if state_kind == "product" else "Bell singlet"

        _fig, (_ax0, _ax1, _ax2) = plt.subplots(1, 3, figsize=(14.2, 4.8))

        _ax0.quiver(0, 0, 1, 0, angles="xy", scale_units="xy", scale=1, color="#d62828", width=0.015)
        _ax0.quiver(0, 0, _b[0], _b[1], angles="xy", scale_units="xy", scale=1, color="#2563eb", width=0.015)
        _ax0.text(1.06, 0.05, "a", color="#d62828")
        _ax0.text(_b[0] + 0.06, _b[1] + 0.05, "b", color="#2563eb")
        if state_kind == "product":
            _ax0.quiver(0, 0, 1, 0, angles="xy", scale_units="xy", scale=1, color="#7c3aed", width=0.010, alpha=0.5)
            _ax0.quiver(0, 0, 1, 0, angles="xy", scale_units="xy", scale=1, color="#10b981", width=0.010, alpha=0.5)
            _ax0.text(0.86, -0.12, r"$s_A,s_B$", color="#444444")
        else:
            _ax0.scatter([0], [0], color="#7c3aed", s=42, alpha=0.7)
            _ax0.text(0.07, 0.08, r"$s_A=s_B=0$", color="#444444")
        _ax0.set_aspect("equal")
        _ax0.set_xlim(-1.3, 1.35)
        _ax0.set_ylim(-1.25, 1.25)
        _ax0.grid(True, alpha=0.18)
        _ax0.set_xticks([])
        _ax0.set_yticks([])
        _ax0.set_title("Measurement geometry and local-state picture")

        _ax1.plot(np.degrees(_angles), _product_curve, color="#999999", linewidth=1.8, alpha=0.45, label="product template")
        _ax1.plot(np.degrees(_angles), _singlet_curve, color="#999999", linewidth=1.8, alpha=0.45, linestyle="--", label="singlet template")
        _active_curve = _product_curve if state_kind == "product" else _singlet_curve
        _active_color = "#d62828" if state_kind == "product" else "#2563eb"
        _ax1.plot(np.degrees(_angles), _active_curve, color=_active_color, linewidth=2.8)
        _ax1.plot([delta_deg], [correlation], "o", color="#222222", ms=7)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.45)
        _ax1.set_xlabel("axis angle difference (degrees)")
        _ax1.set_ylabel(r"$E(a,b)$")
        _ax1.set_ylim(-1.05, 1.05)
        _ax1.grid(True, alpha=0.18)
        _ax1.set_title(f"{_state_label} correlation")

        _ax2.bar([0, 1], [p_same, p_opp], color=["#7c3aed", "#10b981"], alpha=0.86, width=0.55)
        _ax2.text(0, p_same + 0.03, f"{p_same:.3f}", ha="center", va="bottom")
        _ax2.text(1, p_opp + 0.03, f"{p_opp:.3f}", ha="center", va="bottom")
        _ax2.set_xticks([0, 1], ["same", "opp"])
        _ax2.set_ylim(0, 1.05)
        _ax2.grid(True, axis="y", alpha=0.18)
        _ax2.set_title("Joint probabilities")

        plt.close(_fig)
        return _fig

    return (draw_entanglement_geometry,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
