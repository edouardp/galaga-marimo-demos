import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, grade
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Torque and Angular Momentum as Bivectors

    In elementary mechanics, angular momentum and torque are often introduced with
    cross products, which makes them look like mysterious axial vectors. In GA the
    geometry is plain: both are plane quantities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$.

    The basic objects are

    $$
    L = r \wedge p,
    \qquad
    \tau = r \wedge F.
    $$

    Both are bivectors. They encode the plane spanned by the corresponding vector
    pairs, together with the signed area scale of that plane element.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(mo):
    r_theta = mo.ui.slider(0, 360, step=1, value=35, label="Position angle θ_r", show_value=True)
    p_theta = mo.ui.slider(0, 360, step=1, value=125, label="Momentum angle θ_p", show_value=True)
    p_mag = mo.ui.slider(0.2, 2.5, step=0.05, value=1.2, label="Momentum magnitude |p|", show_value=True)
    f_theta = mo.ui.slider(0, 360, step=1, value=100, label="Force angle θ_F", show_value=True)
    f_mag = mo.ui.slider(0.0, 2.5, step=0.05, value=1.0, label="Force magnitude |F|", show_value=True)
    return f_mag, f_theta, p_mag, p_theta, r_theta


@app.cell
def _(
    draw_bivector_mechanics,
    e1,
    e2,
    e3,
    f_mag,
    f_theta,
    gm,
    mo,
    np,
    p_mag,
    p_theta,
    r_theta,
):
    _rt = np.radians(r_theta.value)
    _pt = np.radians(p_theta.value)
    _ft = np.radians(f_theta.value)

    r = (np.cos(_rt) * e1 + np.sin(_rt) * e2 + 0.45 * e3).name(latex="r")
    p = (p_mag.value * (np.cos(_pt) * e1 + np.sin(_pt) * e2)).name(latex="p")
    F = (f_mag.value * (np.cos(_ft) * e1 + np.sin(_ft) * e2)).name(latex="F")

    L = (r ^ p).name(latex="L")
    tau = (r ^ F).name(latex=r"\tau")

    e12 = (e1 * e2).name(latex=r"e_{12}")
    e23 = (e2 * e3).name(latex=r"e_{23}")
    e31 = (e3 * e1).name(latex=r"e_{31}")
    L12 = L | e12
    L23 = L | e23
    L31 = L | e31
    T12 = tau | e12
    T23 = tau | e23
    T31 = tau | e31

    _radial_force = abs((r | F).scalar_part) / (np.linalg.norm(r.vector_part[:3]) * max(np.linalg.norm(F.vector_part[:3]), 1e-9))
    _radial_note = ""
    if _radial_force > 0.995 and f_mag.value > 1e-8:
        _radial_note = "The force is almost radial, so the torque bivector is almost zero."

    _md = t"""
    {r.display()} <br/>
    {p.display()} <br/>
    {F.display()} <br/>
    {L.display()} <br/>
    {tau.display()} <br/>
    {L12.display()} <br/>
    {L23.display()} <br/>
    {L31.display()} <br/>
    {T12.display()} <br/>
    {T23.display()} <br/>
    {T31.display()} <br/>
    {_radial_note}
    """

    mo.vstack(
        [
            r_theta,
            p_theta,
            p_mag,
            f_theta,
            f_mag,
            gm.md(_md),
            draw_bivector_mechanics(r, p, F, L, tau, e1 * e2, e2 * e3, e3 * e1),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The mechanics is planar before it is axial. $L$ and $\tau$ are bivectors
    because they record the planes spanned by $(r,p)$ and $(r,F)$. The common
    vector-cross-product picture is a dual representation, not the underlying
    geometry itself.
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
    def _coeff(_mv, _blade):
        return (_mv.eval() | _blade.eval()).scalar_part / ((_blade.eval() | _blade.eval()).scalar_part)

    def draw_bivector_mechanics(r, p, F, L, tau, e12, e23, e31):
        _r = np.array(r.eval().vector_part[:3], dtype=float)
        _p = np.array(p.eval().vector_part[:3], dtype=float)
        _F = np.array(F.eval().vector_part[:3], dtype=float)
        _L = np.array([_coeff(L, e12), _coeff(L, e23), _coeff(L, e31)], dtype=float)
        _T = np.array([_coeff(tau, e12), _coeff(tau, e23), _coeff(tau, e31)], dtype=float)

        _fig = plt.figure(figsize=(12.2, 5.2))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        for _vec, _color, _label in [(_r, "#222222", "r"), (_p, "#2563eb", "p"), (_F, "#d62828", "F")]:
            _ax0.quiver(0, 0, 0, _vec[0], _vec[1], _vec[2], color=_color, linewidth=2.7, arrow_length_ratio=0.1)
            _ax0.text(1.08 * _vec[0], 1.08 * _vec[1], 1.08 * _vec[2], _label, color=_color)
        _ax0.set_xlim(-1.7, 1.7)
        _ax0.set_ylim(-1.7, 1.7)
        _ax0.set_zlim(-1.7, 1.7)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_zlabel("e3")
        _ax0.set_title("Vectors whose wedge products define the mechanics")

        _x = np.arange(3)
        _w = 0.34
        _ax1.bar(_x - _w / 2, _L, width=_w, color="#2563eb", alpha=0.84, label="L = r ∧ p")
        _ax1.bar(_x + _w / 2, _T, width=_w, color="#d62828", alpha=0.84, label=r"τ = r ∧ F")
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.5)
        _ax1.set_xticks(_x, [r"$e_{12}$", r"$e_{23}$", r"$e_{31}$"])
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("Bivector components")
        _ax1.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_bivector_mechanics,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
