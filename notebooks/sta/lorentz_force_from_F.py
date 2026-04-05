import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_force_geometry(v_vec, E_vec, B_vec, accel_vec, trajectory):
        _fig = plt.figure(figsize=(11.0, 5.2))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        for _vec, _color, _label in [
            (v_vec, "black", "v"),
            (E_vec, "crimson", "E"),
            (B_vec, "steelblue", "B"),
            (accel_vec, "darkorange", "q(E + v×B)"),
        ]:
            _ax1.quiver(0, 0, 0, _vec[0], _vec[1], _vec[2], color=_color, linewidth=2.5)
            _ax1.plot([], [], color=_color, label=_label)

        _ax1.set_xlim(-2.5, 2.5)
        _ax1.set_ylim(-2.5, 2.5)
        _ax1.set_zlim(-2.5, 2.5)
        _ax1.set_xlabel(r"$\sigma_1$")
        _ax1.set_ylabel(r"$\sigma_2$")
        _ax1.set_zlabel(r"$\sigma_3$")
        _ax1.set_title("Velocity, field, and instantaneous force")
        _ax1.legend(loc="upper left")

        _ax2.plot(trajectory[:, 0], trajectory[:, 1], color="darkorange", linewidth=2.4)
        _ax2.scatter([trajectory[0, 0]], [trajectory[0, 1]], color="black", s=35)
        _ax2.set_aspect("equal")
        _ax2.grid(True, alpha=0.25)
        _ax2.set_xlabel(r"$\sigma_1$")
        _ax2.set_ylabel(r"$\sigma_2$")
        _ax2.set_title("Qualitative projected path")

        plt.close(_fig)
        return _fig

    return (draw_force_geometry,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lorentz Force from One Bivector

    In spacetime algebra, the electromagnetic field is one bivector $F$. The Lorentz-force story is then about how that one field acts on the particle velocity, not about two unrelated vector fields pushing independently.

    This notebook follows [boosting_em_field.py](./boosting_em_field.py): there the focus is on transforming the field, while here the focus is on how a chosen observer-relative field acts on a moving charge.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    In an observer split, the familiar instantaneous force law is

    $$
    \mathbf{f} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B}).
    $$

    The pedagogical point here is that both pieces come from one field bivector $F = E + I B$.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.I.name("I")
    s1 = (g1 * g0).name(latex=r"\sigma_1")
    s2 = (g2 * g0).name(latex=r"\sigma_2")
    s3 = (g3 * g0).name(latex=r"\sigma_3")
    return I, g0, g1, g2, g3, s1, s2, s3, sta


@app.cell
def _(mo):
    ex = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.4, label="E along σ1", show_value=True)
    bz = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="B along σ3", show_value=True)
    speed = mo.ui.slider(0.0, 0.95, step=0.01, value=0.55, label="speed β", show_value=True)
    heading = mo.ui.slider(0, 360, step=1, value=0, label="velocity heading", show_value=True)
    charge_sign = mo.ui.dropdown(
        options=["positive charge", "negative charge"],
        value="positive charge",
        label="charge",
    )
    return bz, charge_sign, ex, heading, speed


@app.cell
def _(I, bz, charge_sign, draw_force_geometry, ex, gm, heading, mo, np, s1, s2, s3, speed):
    _q = 1.0 if charge_sign.value == "positive charge" else -1.0
    _E = (ex.value * s1).name("E")
    _B = (bz.value * s3).name("B")
    _F = (_E + I * _B).name("F")

    _theta = np.radians(heading.value)
    _v_vec = speed.value * np.array([np.cos(_theta), np.sin(_theta), 0.0], dtype=float)
    _E_vec = np.array([ex.value, 0.0, 0.0], dtype=float)
    _B_vec = np.array([0.0, 0.0, bz.value], dtype=float)
    _force_vec = _q * (_E_vec + np.cross(_v_vec, _B_vec))

    _v_rel = (_v_vec[0] * s1 + _v_vec[1] * s2 + _v_vec[2] * s3).name("v")
    _force_rel = (_force_vec[0] * s1 + _force_vec[1] * s2 + _force_vec[2] * s3).name("f")

    _t = np.linspace(0.0, 8.0, 250)
    if abs(bz.value) < 1e-9:
        _x = _v_vec[0] * _t + 0.5 * _q * ex.value * _t**2
        _y = _v_vec[1] * _t
    elif abs(ex.value) < 1e-9:
        _omega = _q * bz.value
        _x = (_v_vec[0] * np.sin(_omega * _t) - _v_vec[1] * (1 - np.cos(_omega * _t))) / _omega
        _y = (_v_vec[1] * np.sin(_omega * _t) + _v_vec[0] * (1 - np.cos(_omega * _t))) / _omega
    else:
        _dt = _t[1] - _t[0]
        _pos = np.zeros((len(_t), 2))
        _vel = _v_vec[:2].copy()
        for _i in range(1, len(_t)):
            _acc = _q * (_E_vec[:2] + np.array([_vel[1] * bz.value, -_vel[0] * bz.value]))
            _vel = _vel + _dt * _acc
            _pos[_i] = _pos[_i - 1] + _dt * _vel
        _x = _pos[:, 0]
        _y = _pos[:, 1]
    _trajectory = np.column_stack([_x, _y])

    _md = t"""
    {_E.display()} <br/>
    {_B.display()} <br/>
    {_F.display()} <br/>
    {_v_rel.display()} <br/>
    {_force_rel.display()} <br/>
    The electric term pushes along the field. The magnetic term bends the motion sideways. Both come from the same bivector field.
    """

    mo.vstack(
        [
            ex,
            bz,
            speed,
            heading,
            charge_sign,
            gm.md(_md),
            draw_force_geometry(_v_vec, _E_vec, _B_vec, _force_vec, _trajectory),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The electric and magnetic responses look different in the observer split, but they are still two faces of one field bivector $F$. The split is about how the observer reads the action, not about two unrelated physical objects.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
