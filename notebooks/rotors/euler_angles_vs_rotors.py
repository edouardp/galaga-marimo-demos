import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, log
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, log, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Euler Angles vs Rotors

    Euler angles are a coordinate system for orientation. Rotors are the
    orientation itself. That difference matters most near gimbal lock, where the
    Euler coordinates become degenerate but the rotor stays perfectly well-behaved.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We work in $\mathrm{Cl}(3,0)$.

    Yaw, pitch, and roll are built as three ordinary rotors:

    $$
    R_{\mathrm{yaw}},\quad R_{\mathrm{pitch}},\quad R_{\mathrm{roll}},
    $$

    and then composed into one total rotor

    $$
    R = R_{\mathrm{yaw}} R_{\mathrm{pitch}} R_{\mathrm{roll}}.
    $$

    The orientation itself is just that one rotor. Gimbal lock appears only when
    we try to describe the same orientation with the Euler coordinates.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    yaw = mo.ui.slider(-180, 180, step=1, value=35, label="Yaw ψ", show_value=True)
    pitch = mo.ui.slider(-90, 90, step=1, value=70, label="Pitch θ", show_value=True)
    roll = mo.ui.slider(-180, 180, step=1, value=20, label="Roll ϕ", show_value=True)
    return pitch, roll, yaw


@app.cell
def _(
    alg,
    draw_euler_vs_rotor,
    e1,
    e2,
    e3,
    exp,
    gm,
    log,
    mo,
    np,
    pitch,
    roll,
    yaw,
):
    half = alg.frac(1, 2)
    psi = alg.scalar(np.radians(yaw.value)).name(latex=r"\psi")
    theta = alg.scalar(np.radians(pitch.value)).name(latex=r"\theta")
    phi = alg.scalar(np.radians(roll.value)).name(latex=r"\phi")

    B_yaw = (e1 * e2).name(latex=r"B_{\mathrm{yaw}}")
    B_pitch = (e3 * e1).name(latex=r"B_{\mathrm{pitch}}")
    B_roll = (e2 * e3).name(latex=r"B_{\mathrm{roll}}")

    R_yaw = exp(-B_yaw * psi * half).name(latex=r"R_{\mathrm{yaw}}")
    R_pitch = exp(-B_pitch * theta * half).name(latex=r"R_{\mathrm{pitch}}")
    R_roll = exp(-B_roll * phi * half).name(latex=r"R_{\mathrm{roll}}")
    R = (R_yaw * R_pitch * R_roll).name(latex="R")
    G = log(R).name(latex=r"\log(R)")

    x_body = (R * e1 * ~R).name(latex=r"x_{\mathrm{body}}")
    y_body = (R * e2 * ~R).name(latex=r"y_{\mathrm{body}}")
    z_body = (R * e3 * ~R).name(latex=r"z_{\mathrm{body}}")

    _delta = np.radians(5.0)
    _R_yaw_plus = exp(-B_yaw * alg.scalar(psi.scalar_part + _delta) * half) * R_pitch * R_roll
    _R_roll_plus = R_yaw * R_pitch * exp(-B_roll * alg.scalar(phi.scalar_part + _delta) * half)
    _axes_yaw_plus = [_R_yaw_plus * _basis * ~_R_yaw_plus for _basis in (e1, e2, e3)]
    _axes_roll_plus = [_R_roll_plus * _basis * ~_R_roll_plus for _basis in (e1, e2, e3)]
    _lock_metric = sum(
        np.linalg.norm(_a.eval().vector_part[:3] - _b.eval().vector_part[:3])
        for _a, _b in zip(_axes_yaw_plus, _axes_roll_plus)
    ) / 3.0

    _md = t"""
    {psi.display()} <br/>
    {theta.display()} <br/>
    {phi.display()} <br/>
    {R_yaw.display()} <br/>
    {R_pitch.display()} <br/>
    {R_roll.display()} <br/>
    {R.display()} <br/>
    {G.display()} <br/>
    {x_body.display()} <br/>
    {y_body.display()} <br/>
    {z_body.display()} <br/>
    Near gimbal lock, a small yaw change and a small roll change produce almost the same change in orientation. Current yaw/roll perturbation separation: ${_lock_metric:.4f}$.
    """

    mo.vstack([yaw, pitch, roll, gm.md(_md), draw_euler_vs_rotor(R, yaw.value, pitch.value, roll.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Euler angles are not the orientation. They are one chart on orientation
    space. Near pitch $= \pm 90^\circ$, the yaw and roll coordinates start
    describing almost the same motion. The rotor does not suffer any singularity;
    it stays one smooth object representing the orientation itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(e1, e2, e3, exp, np, plt):
    def _rotor_from_euler(yaw_deg, pitch_deg, roll_deg):
        _half = 0.5
        _psi = np.radians(yaw_deg)
        _theta = np.radians(pitch_deg)
        _phi = np.radians(roll_deg)
        _Ry = exp(-_half * _psi * (e1 * e2))
        _Rp = exp(-_half * _theta * (e3 * e1))
        _Rr = exp(-_half * _phi * (e2 * e3))
        return _Ry * _Rp * _Rr

    def _axis_vec(_R, _basis):
        return np.array((_R * _basis * ~_R).eval().vector_part[:3], dtype=float)

    def _frame_metric(_R_a, _R_b):
        return sum(np.linalg.norm(_axis_vec(_R_a, _basis) - _axis_vec(_R_b, _basis)) for _basis in (e1, e2, e3)) / 3.0

    def draw_euler_vs_rotor(R, yaw_deg, pitch_deg, roll_deg):
        _fig = plt.figure(figsize=(12.4, 5.4))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        _R = R.eval()
        _x = _axis_vec(_R, e1)
        _y = _axis_vec(_R, e2)
        _z = _axis_vec(_R, e3)
        for _vec, _color, _label in [(_x, "#d62828", "body x"), (_y, "#2563eb", "body y"), (_z, "#10b981", "body z")]:
            _ax0.quiver(0, 0, 0, _vec[0], _vec[1], _vec[2], color=_color, linewidth=2.8, arrow_length_ratio=0.1)
            _ax0.text(1.08 * _vec[0], 1.08 * _vec[1], 1.08 * _vec[2], _label, color=_color)
        _ax0.quiver(0, 0, 0, 1, 0, 0, color="#888888", linewidth=1.2, alpha=0.35)
        _ax0.quiver(0, 0, 0, 0, 1, 0, color="#888888", linewidth=1.2, alpha=0.35)
        _ax0.quiver(0, 0, 0, 0, 0, 1, color="#888888", linewidth=1.2, alpha=0.35)
        _ax0.set_xlim(-1.2, 1.2)
        _ax0.set_ylim(-1.2, 1.2)
        _ax0.set_zlim(-1.2, 1.2)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_title("One orientation, represented by one rotor")
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_zlabel("e3")

        _delta = 5.0
        _pitches = np.linspace(-90, 90, 361)
        _metrics = []
        for _p in _pitches:
            _R_yaw_plus = _rotor_from_euler(yaw_deg + _delta, _p, roll_deg)
            _R_roll_plus = _rotor_from_euler(yaw_deg, _p, roll_deg + _delta)
            _metrics.append(_frame_metric(_R_yaw_plus, _R_roll_plus))
        _metrics = np.array(_metrics)
        _current_yaw_plus = _rotor_from_euler(yaw_deg + _delta, pitch_deg, roll_deg)
        _current_roll_plus = _rotor_from_euler(yaw_deg, pitch_deg, roll_deg + _delta)
        _current_metric = _frame_metric(_current_yaw_plus, _current_roll_plus)

        _ax1.plot(_pitches, _metrics, color="#7c3aed", linewidth=2.5)
        _ax1.plot([pitch_deg], [_current_metric], "o", color="#222222", ms=7)
        _ax1.axvline(90, color="#999999", alpha=0.25, linestyle="--")
        _ax1.axvline(-90, color="#999999", alpha=0.25, linestyle="--")
        _ax1.set_xlabel("pitch θ (degrees)")
        _ax1.set_ylabel("difference between +δ yaw and +δ roll changes")
        _ax1.grid(True, alpha=0.18)
        _ax1.set_title("Euler gimbal-lock diagnostic")

        plt.close(_fig)
        return _fig

    return (draw_euler_vs_rotor,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
