import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, grade, unit
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, grade, mo, np, plt, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Angular Velocity as a Bivector

    A rotor is often introduced as a static transformation. In dynamics, the more
    important object is its generator: angular velocity. In GA that generator is a
    bivector, because the motion lives in a plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ and write

    $$
    \Omega = \omega \widehat B,
    \qquad
    R(t) = e^{-\frac{1}{2}\Omega t}.
    $$

    Then the rotor equation of motion is

    $$
    \frac{dR}{dt} = -\frac{1}{2}\Omega R.
    $$

    The point of this notebook is that the generator is a plane element
    $\widehat B$, not a disguised axial vector.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    plane = mo.ui.dropdown(options=["e12 plane", "e23 plane", "e13 plane"], value="e12 plane", label="Rotation plane")
    omega = mo.ui.slider(-3.0, 3.0, step=0.05, value=1.20, label="Angular speed ω", show_value=True)
    time = mo.ui.slider(0.0, 6.0, step=0.05, value=1.0, label="Time t", show_value=True)
    return omega, plane, time


@app.cell
def _(alg, draw_angular_velocity_bivector, e1, e2, e3, exp, gm, grade, mo, np, omega, plane, time, unit):
    _plane_data = {
        "e12 plane": {"blade": (e1 * e2).name(latex=r"\hat B"), "basis": e3, "vector": e1 + 0.35 * e3, "span": (e1, e2), "labels": (r"e_1", r"e_2")},
        "e23 plane": {"blade": (e2 * e3).name(latex=r"\hat B"), "basis": e1, "vector": e2 + 0.35 * e1, "span": (e2, e3), "labels": (r"e_2", r"e_3")},
        "e13 plane": {"blade": (e1 * e3).name(latex=r"\hat B"), "basis": e2, "vector": e1 + 0.35 * e2, "span": (e1, e3), "labels": (r"e_1", r"e_3")},
    }[plane.value]

    B_hat = unit(_plane_data["blade"]).name(latex=r"\hat B")
    w = alg.scalar(omega.value).name(latex=r"\omega")
    t = alg.scalar(time.value).name(latex="t")
    Omega = (w * B_hat).name(latex=r"\Omega")
    R = exp(-(Omega * t) * alg.frac(1, 2)).name(latex=r"R(t)")

    v0 = unit(_plane_data["vector"]).name(latex=r"v_0")
    v = (R * v0 * ~R).name(latex=r"v(t)")

    _dt = 1e-4
    _R_plus = exp(-(_plane_data["blade"] * (omega.value) * (time.value + _dt)) / 2.0)
    _R_minus = exp(-(_plane_data["blade"] * (omega.value) * (time.value - _dt)) / 2.0)
    dR_fd = (((_R_plus - _R_minus) / (2.0 * _dt))).name(latex=r"\dot R_{\mathrm{fd}}")
    dR_model = ((-(Omega) * alg.frac(1, 2) * R)).name(latex=r"-\frac{1}{2}\Omega R")
    g0_fd = grade(dR_fd, 0).name(latex=r"\langle \dot R_{\mathrm{fd}} \rangle_0")
    g2_fd = grade(dR_fd, 2).name(latex=r"\langle \dot R_{\mathrm{fd}} \rangle_2")
    g0_model = grade(dR_model, 0).name(latex=r"\langle -\frac{1}{2}\Omega R \rangle_0")
    g2_model = grade(dR_model, 2).name(latex=r"\langle -\frac{1}{2}\Omega R \rangle_2")

    _md = t"""
    {B_hat.display()} <br/>
    {w.display()} <br/>
    {t.display()} <br/>
    {Omega.display()} <br/>
    {R.display()} <br/>
    {v0.display()} <br/>
    {v.display()} <br/>
    {dR_fd.display()} <br/>
    {dR_model.display()} <br/>
    {g0_fd.display()} <br/>
    {g0_model.display()} <br/>
    {g2_fd.display()} <br/>
    {g2_model.display()} <br/>
    The finite-difference derivative and the bivector evolution law agree: the rotor moves because the bivector plane generator drives it.
    """

    mo.vstack([plane, omega, time, gm.md(_md), draw_angular_velocity_bivector(B_hat, Omega, R, v0, v, dR_fd, dR_model, _plane_data["span"], _plane_data["labels"])])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Angular velocity is not fundamentally an axial vector. The rotating object
    does not "point along an axis" first and only later pick out a plane. The
    plane is primary. GA keeps that visible by using a bivector generator
    directly in the rotor evolution equation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _bivector_coeff(_mv, _blade):
        return (_mv.eval() | _blade.eval()).scalar_part / ((_blade.eval() | _blade.eval()).scalar_part)

    def draw_angular_velocity_bivector(B_hat, Omega, R, v0, v, dR_fd, dR_model, span, labels):
        _b1, _b2 = span
        _blade = (_b1 * _b2)

        def _vec(_mv):
            return np.array(_mv.eval().vector_part[:3], dtype=float)

        _v0 = _vec(v0)
        _v = _vec(v)
        _plane_u = _vec(_b1)
        _plane_v = _vec(_b2)
        _normal = np.cross(_plane_u, _plane_v)
        _normal = _normal / max(np.linalg.norm(_normal), 1e-12)
        _tangent = np.cross(_normal, _v)

        _scalar_fd = dR_fd.scalar_part
        _scalar_model = dR_model.scalar_part
        _biv_fd = _bivector_coeff(dR_fd, _blade)
        _biv_model = _bivector_coeff(dR_model, _blade)

        _fig = plt.figure(figsize=(12.0, 5.3))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        _patch = np.array(
            [
                0.7 * _plane_u + 0.7 * _plane_v,
                -0.7 * _plane_u + 0.7 * _plane_v,
                -0.7 * _plane_u - 0.7 * _plane_v,
                0.7 * _plane_u - 0.7 * _plane_v,
                0.7 * _plane_u + 0.7 * _plane_v,
            ]
        )
        _ax0.plot(_patch[:, 0], _patch[:, 1], _patch[:, 2], color="#7c3aed", alpha=0.75)
        _ax0.plot_trisurf(_patch[:4, 0], _patch[:4, 1], _patch[:4, 2], color="#7c3aed", alpha=0.10)
        _ax0.quiver(0, 0, 0, _v0[0], _v0[1], _v0[2], color="#999999", linewidth=1.8, alpha=0.45, arrow_length_ratio=0.1)
        _ax0.quiver(0, 0, 0, _v[0], _v[1], _v[2], color="#d62828", linewidth=2.8, arrow_length_ratio=0.1)
        _ax0.quiver(_v[0], _v[1], _v[2], 0.35 * _tangent[0], 0.35 * _tangent[1], 0.35 * _tangent[2], color="#2563eb", linewidth=2.0, arrow_length_ratio=0.18)
        _ax0.text(0.6 * _plane_u[0], 0.6 * _plane_u[1], 0.6 * _plane_u[2], labels[0], color="#333333")
        _ax0.text(0.6 * _plane_v[0], 0.6 * _plane_v[1], 0.6 * _plane_v[2], labels[1], color="#333333")
        _ax0.set_xlim(-1.2, 1.2)
        _ax0.set_ylim(-1.2, 1.2)
        _ax0.set_zlim(-1.2, 1.2)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_title("Rotation plane and moving vector")
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_zlabel("e3")

        _labels = [r"$\langle \dot R \rangle_0$", r"$\langle \dot R \rangle_2$"]
        _x = np.arange(2)
        _w = 0.34
        _ax1.bar(_x - _w / 2, [_scalar_fd, _biv_fd], width=_w, color="#2563eb", alpha=0.82, label="finite diff")
        _ax1.bar(_x + _w / 2, [_scalar_model, _biv_model], width=_w, color="#d62828", alpha=0.82, label=r"$-\frac{1}{2}\Omega R$")
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.5)
        _ax1.set_xticks(_x, _labels)
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("Rotor derivative channels")
        _ax1.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_angular_velocity_bivector,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
