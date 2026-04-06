import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, log, sandwich
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, log, mo, np, plt, sandwich


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Multi-Rotor Blending

    Slerp blends two rotors along a shortest path on the rotor manifold. For more
    than two rotations, a useful geometric-algebra strategy is to move into
    bivector-generator space with $\log$, take a weighted average there, and then
    return with $\exp$.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use $\mathrm{Cl}(2,0)$ so rotor space is easy to see.

    In the plane, every rotor has the form

    $$
    R_i = e^{-B \theta_i / 2},
    $$

    with a single unit bivector generator $B = e_{12}$. That means each
    $\log(R_i)$ lives in the same one-dimensional bivector direction, so a
    weighted average of those logs is easy to interpret.
    """
    )
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Blend in Log Space

    For a set of rotors $R_i$ with normalized weights $w_i$, define

    $$
    G_{\mathrm{blend}} = \sum_i w_i \log(R_i),
    \qquad
    R_{\mathrm{blend}} = e^{G_{\mathrm{blend}}}.
    $$

    This keeps the blend inside rotor space and treats the bivector generators as
    the place where weighted averaging happens.
    """
    )
    return


@app.cell
def _(mo):
    theta_1 = mo.ui.slider(-170, 170, step=1, value=-50, label="Rotor 1 angle θ₁", show_value=True)
    theta_2 = mo.ui.slider(-170, 170, step=1, value=40, label="Rotor 2 angle θ₂", show_value=True)
    theta_3 = mo.ui.slider(-170, 170, step=1, value=130, label="Rotor 3 angle θ₃", show_value=True)

    weight_1 = mo.ui.slider(0.0, 1.0, step=0.01, value=0.45, label="Weight w₁", show_value=True)
    weight_2 = mo.ui.slider(0.0, 1.0, step=0.01, value=0.35, label="Weight w₂", show_value=True)
    weight_3 = mo.ui.slider(0.0, 1.0, step=0.01, value=0.20, label="Weight w₃", show_value=True)
    return theta_1, theta_2, theta_3, weight_1, weight_2, weight_3


@app.cell
def _(
    alg,
    draw_multi_rotor_blend,
    e1,
    e2,
    exp,
    gm,
    log,
    mo,
    np,
    sandwich,
    theta_1,
    theta_2,
    theta_3,
    weight_1,
    weight_2,
    weight_3,
):
    B = (e1 * e2).name(latex="B")
    half = alg.frac(1, 2)

    total_weight = weight_1.value + weight_2.value + weight_3.value
    if total_weight < 1e-9:
        w1_value = w2_value = w3_value = 1 / 3
    else:
        w1_value = weight_1.value / total_weight
        w2_value = weight_2.value / total_weight
        w3_value = weight_3.value / total_weight

    w1 = alg.scalar(w1_value).name(latex="w_1")
    w2 = alg.scalar(w2_value).name(latex="w_2")
    w3 = alg.scalar(w3_value).name(latex="w_3")

    t1 = alg.scalar(np.radians(theta_1.value)).name(latex=r"\theta_1")
    t2 = alg.scalar(np.radians(theta_2.value)).name(latex=r"\theta_2")
    t3 = alg.scalar(np.radians(theta_3.value)).name(latex=r"\theta_3")

    R1 = exp(-B * t1 * half).name(latex="R_1")
    R2 = exp(-B * t2 * half).name(latex="R_2")
    R3 = exp(-B * t3 * half).name(latex="R_3")

    G1 = log(R1).name(latex=r"\log(R_1)")
    G2 = log(R2).name(latex=r"\log(R_2)")
    G3 = log(R3).name(latex=r"\log(R_3)")
    G_blend = (w1 * G1 + w2 * G2 + w3 * G3).name(latex=r"G_{\mathrm{blend}}")
    R_blend = exp(G_blend).name(latex=r"R_{\mathrm{blend}}")

    v = e1.name(latex="v")
    v1 = sandwich(R1, v).name(latex=r"v_1")
    v2 = sandwich(R2, v).name(latex=r"v_2")
    v3 = sandwich(R3, v).name(latex=r"v_3")
    v_blend = sandwich(R_blend, v).name(latex=r"v_{\mathrm{blend}}")

    _md = t"""
    {B.display()} <br/>
    {w1.display()} <br/>
    {w2.display()} <br/>
    {w3.display()} <br/>
    {R1.display()} <br/>
    {R2.display()} <br/>
    {R3.display()} <br/>
    {G1.display()} <br/>
    {G2.display()} <br/>
    {G3.display()} <br/>
    {G_blend.display()} <br/>
    {R_blend.display()} <br/>
    {v_blend.display()} <br/>
    The weights are normalized before blending, so the average happens in bivector-generator space rather than by directly mixing rotor coefficients.
    """

    mo.vstack(
        [
            theta_1,
            theta_2,
            theta_3,
            weight_1,
            weight_2,
            weight_3,
            gm.md(_md),
            draw_multi_rotor_blend(R1, R2, R3, R_blend, v1, v2, v3, v_blend),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    Rotor blending works best when the average is taken in the bivector
    generators, not directly in coefficient space. The plot shows that the
    blended rotor stays on the rotor circle while still producing a weighted
    orientation in vector space.
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
def _(np, plt):
    def draw_multi_rotor_blend(R1, R2, R3, R_blend, v1, v2, v3, v_blend):
        _fig, (_ax_rot, _ax_vec) = plt.subplots(1, 2, figsize=(11.4, 4.8))

        _t = np.linspace(0, 2 * np.pi, 250)
        _ax_rot.plot(np.cos(_t), np.sin(_t), color="#666666", alpha=0.22)

        def _rot_xy(_R):
            _Re = _R.eval()
            return float(_Re.data[0]), float(_Re.data[3])

        def _vec_xy(_v):
            return np.array(_v.vector_part[:2], dtype=float)

        _rotors = [
            (_rot_xy(R1), "#2563eb", "R₁"),
            (_rot_xy(R2), "#d62828", "R₂"),
            (_rot_xy(R3), "#16a34a", "R₃"),
            (_rot_xy(R_blend), "#7c3aed", "blend"),
        ]
        for (_xy, _color, _label) in _rotors:
            _ax_rot.annotate("", xy=_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=_color, lw=2.4, mutation_scale=16, alpha=0.95))
            _ax_rot.text(_xy[0] + 0.05, _xy[1] + 0.05, _label, color=_color)

        _ax_rot.set_xlim(-1.15, 1.15)
        _ax_rot.set_ylim(-1.15, 1.15)
        _ax_rot.set_aspect("equal")
        _ax_rot.grid(True, alpha=0.18)
        _ax_rot.set_xlabel("scalar part")
        _ax_rot.set_ylabel("e12 part")
        _ax_rot.set_title("Rotor circle")

        _vectors = [
            (_vec_xy(v1), "#2563eb", "v₁", 0.38, 1.9),
            (_vec_xy(v2), "#d62828", "v₂", 0.38, 1.9),
            (_vec_xy(v3), "#16a34a", "v₃", 0.38, 1.9),
            (_vec_xy(v_blend), "#7c3aed", "blend", 0.95, 2.9),
        ]
        for (_xy, _color, _label, _alpha, _lw) in _vectors:
            _ax_vec.annotate("", xy=_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=_color, lw=_lw, mutation_scale=18, alpha=_alpha))
            _ax_vec.text(_xy[0] + 0.05, _xy[1] + 0.05, _label, color=_color, alpha=max(_alpha, 0.75))

        _ax_vec.axhline(0, color="#333333", lw=1.0, alpha=0.6)
        _ax_vec.axvline(0, color="#333333", lw=1.0, alpha=0.6)
        _ax_vec.set_xlim(-1.35, 1.35)
        _ax_vec.set_ylim(-1.35, 1.35)
        _ax_vec.set_aspect("equal")
        _ax_vec.grid(True, alpha=0.18)
        _ax_vec.set_xlabel("e1")
        _ax_vec.set_ylabel("e2")
        _ax_vec.set_title("Action on one vector")

        plt.close(_fig)
        return _fig

    return (draw_multi_rotor_blend,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
