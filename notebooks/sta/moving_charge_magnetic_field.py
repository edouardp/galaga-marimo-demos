import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, sandwich, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Magnetic Field from a Moving Charge

    In the charge rest frame, the field is purely electric. In a boosted frame, the same Faraday bivector develops a magnetic part. This is one of the cleanest ways to see magnetism emerge from special relativity.

    This notebook follows [electromagnetism_one_bivector.py](./electromagnetism_one_bivector.py): there the goal is to see $F$ as one bivector, while here the goal is to see a moving charge turn part of a pure electric field into a magnetic field.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    The setup is deliberately local and inertial:

    - start with a Coulomb field sample in the charge rest frame
    - represent that sample as one bivector $F_{\mathrm{rest}}$
    - boost both the field and the sampled event into the lab frame

    This is a frame-transformation notebook, not a full retarded-field derivation.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), names="gamma")
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.I.name("I")
    s1 = (g1 * g0).name(latex=r"\sigma_1")
    s2 = (g2 * g0).name(latex=r"\sigma_2")
    s3 = (g3 * g0).name(latex=r"\sigma_3")
    return I, g0, g1, g2, g3, s1, s2, s3, sta


@app.cell
def _(np, plt, s1, s2, s3):
    def draw_moving_charge_scene(point_lab, beta_vec, E_lab, B_lab, coeffs):
        def _rel_coeffs(_mv):
            return np.array(
                [
                    (_mv | s1).scalar_part / ((s1 | s1).scalar_part),
                    (_mv | s2).scalar_part / ((s2 | s2).scalar_part),
                    (_mv | s3).scalar_part / ((s3 | s3).scalar_part),
                ],
                dtype=float,
            )

        _point = _rel_coeffs(point_lab)
        _beta = _rel_coeffs(beta_vec)
        _E = _rel_coeffs(E_lab)
        _B = _rel_coeffs(B_lab)

        _fig = plt.figure(figsize=(11.6, 5.4))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _ax1.scatter([0], [0], [0], color="black", s=45)
        _ax1.text(0.05, 0.05, 0.05, "charge")
        _ax1.scatter([_point[0]], [_point[1]], [_point[2]], color="darkgreen", s=55)
        _ax1.text(_point[0] + 0.05, _point[1] + 0.05, _point[2] + 0.05, "field point")
        _ax1.plot([0, _point[0]], [0, _point[1]], [0, _point[2]], color="gray", alpha=0.4)

        _ax1.quiver(0, 0, 0, _beta[0], _beta[1], _beta[2], color="purple", linewidth=2.5)
        _ax1.quiver(_point[0], _point[1], _point[2], _E[0], _E[1], _E[2], color="crimson", linewidth=2.5)
        _ax1.quiver(_point[0], _point[1], _point[2], _B[0], _B[1], _B[2], color="steelblue", linewidth=2.5)
        _ax1.plot([], [], color="purple", label=r"$\beta$")
        _ax1.plot([], [], color="crimson", label="E")
        _ax1.plot([], [], color="steelblue", label="B")
        _ax1.legend(loc="upper left")

        _ax1.set_xlim(-3.0, 3.0)
        _ax1.set_ylim(-3.0, 3.0)
        _ax1.set_zlim(-3.0, 3.0)
        _ax1.set_xlabel(r"$\sigma_1$")
        _ax1.set_ylabel(r"$\sigma_2$")
        _ax1.set_zlabel(r"$\sigma_3$")
        _ax1.set_title("Lab-frame geometry")

        _labels = [r"$\gamma_1\gamma_0$", r"$\gamma_2\gamma_0$", r"$\gamma_3\gamma_0$", r"$\gamma_2\gamma_3$", r"$\gamma_3\gamma_1$", r"$\gamma_1\gamma_2$"]
        _x = np.arange(len(_labels))
        _ax2.bar(_x, coeffs, color=["crimson", "crimson", "crimson", "steelblue", "steelblue", "steelblue"], alpha=0.82)
        _ax2.axhline(0, color="black", linewidth=0.8)
        _ax2.set_xticks(_x, _labels)
        _ax2.set_ylim(-2.5, 2.5)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title("Boosted Faraday bivector coefficients")

        plt.close(_fig)
        return _fig

    return (draw_moving_charge_scene,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Constrained Setup

    The field sample point is chosen in the charge rest frame. The controls are narrow enough that the point usually stays away from the velocity axis, so the induced magnetic field is easy to see instead of accidentally vanishing.
    """)
    return


@app.cell
def _(mo):
    rx = mo.ui.slider(-0.5, 0.7, step=0.05, value=0.1, label="rest x", show_value=True)
    ry = mo.ui.slider(0.6, 1.6, step=0.05, value=1.0, label="rest y", show_value=True)
    rz = mo.ui.slider(-0.5, 0.5, step=0.05, value=0.2, label="rest z", show_value=True)
    beta = mo.ui.slider(0.0, 0.9, step=0.02, value=0.55, label="speed β", show_value=True)
    azimuth = mo.ui.slider(0, 360, step=1, value=0, label="velocity azimuth", show_value=True)
    elevation = mo.ui.slider(-30, 30, step=1, value=0, label="velocity elevation", show_value=True)
    return azimuth, beta, elevation, rx, ry, rz


@app.cell
def _(
    I,
    azimuth,
    beta,
    draw_moving_charge_scene,
    elevation,
    exp,
    g0,
    g1,
    g2,
    g3,
    gm,
    mo,
    np,
    rx,
    ry,
    rz,
    s1,
    s2,
    s3,
    sandwich,
    sta,
    unit,
):
    _r_rel_rest = (rx.value * s1 + ry.value * s2 + rz.value * s3).name(latex=r"r_{\mathrm{rest}}")
    _rho = float(np.sqrt(rx.value**2 + ry.value**2 + rz.value**2))
    _E_rest = ((1.0 / (_rho**3)) * _r_rel_rest).name(latex=r"E_{\mathrm{rest}}")
    _F_rest = _E_rest.name(latex=r"F_{\mathrm{rest}}")

    _az = np.radians(azimuth.value)
    _el = np.radians(elevation.value)
    _n = unit((np.cos(_el) * np.cos(_az)) * g1 + (np.cos(_el) * np.sin(_az)) * g2 + (np.sin(_el)) * g3).name("n")
    _phi = float(np.arctanh(beta.value))
    _R = exp((-(sta.scalar(_phi)) / 2) * (g0 * _n)).name("R")
    _u = sandwich(_R, g0).name("u")

    _event_rest = (rx.value * g1 + ry.value * g2 + rz.value * g3).name(latex=r"x_{\mathrm{rest}}")
    _event_lab = sandwich(_R, _event_rest).name(latex=r"x_{\mathrm{lab}}")
    _F_lab = sandwich(_R, _F_rest).name(latex=r"F_{\mathrm{lab}}")

    _E_lab = (_F_lab | g0).name(latex=r"E_{\mathrm{lab}}")
    _B_lab = (
        ((_F_lab | (I * s1)).scalar_part / ((I * s1) | (I * s1)).scalar_part) * s1
        + ((_F_lab | (I * s2)).scalar_part / ((I * s2) | (I * s2)).scalar_part) * s2
        + ((_F_lab | (I * s3)).scalar_part / ((I * s3) | (I * s3)).scalar_part) * s3
    ).name(latex=r"B_{\mathrm{lab}}")
    _beta_vec = (beta.value * ((np.cos(_el) * np.cos(_az)) * s1 + (np.cos(_el) * np.sin(_az)) * s2 + (np.sin(_el)) * s3)).name(latex=r"\beta")
    _point_lab = (
        _event_lab.eval().vector_part[1] * s1
        + _event_lab.eval().vector_part[2] * s2
        + _event_lab.eval().vector_part[3] * s3
    ).name(latex=r"r_{\mathrm{lab}}")

    _basis_bivectors = [g1 * g0, g2 * g0, g3 * g0, g2 * g3, g3 * g1, g1 * g2]
    _coeffs = np.array(
        [(_F_lab | _basis).scalar_part / (_basis | _basis).scalar_part for _basis in _basis_bivectors],
        dtype=float,
    )

    _md = t"""
    {_r_rel_rest.display()} <br/>
    {_E_rest.display()} <br/>
    {_F_rest.display()} <br/>
    {_n.display()} <br/>
    {_u.display()} <br/>
    {_event_lab.display()} <br/>
    {_F_lab.display()} <br/>
    {_E_lab.display()} <br/>
    {_B_lab.display()} <br/>
    Rest-frame field: purely electric. Lab-frame field: electric plus magnetic, from the same boosted bivector.
    """

    mo.vstack([rx, ry, rz, beta, azimuth, elevation, gm.md(_md),
               draw_moving_charge_scene(_point_lab, _beta_vec, _E_lab, _B_lab, _coeffs)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In the rest frame of the charge, there is no magnetic field in this example at all. After a boost, the same field bivector decomposes differently relative to the lab observer, and a magnetic part appears automatically. That is the special-relativistic origin story this notebook is meant to isolate.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
