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


@app.cell
def _(e1, e2, e3, plt):
    _e12 = e1 * e2
    _e13 = e1 * e3
    _e23 = e2 * e3

    def draw_multivector_action(v, vr, B, Br):
        _v = v.vector_part[:3]
        _vr = vr.vector_part[:3]
        _fig = plt.figure(figsize=(11.0, 5.6))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _ax1.quiver(0, 0, 0, _v[0], _v[1], _v[2], color="black", linewidth=2)
        _ax1.quiver(0, 0, 0, _vr[0], _vr[1], _vr[2], color="crimson", linewidth=2)
        _ax1.set_xlim(-1.4, 1.4)
        _ax1.set_ylim(-1.4, 1.4)
        _ax1.set_zlim(-1.4, 1.4)
        _ax1.set_xlabel("e1")
        _ax1.set_ylabel("e2")
        _ax1.set_zlabel("e3")
        _ax1.set_title("Vector rotation")

        _b = np.array(
            [
                B.scalar_part,
                -(B | _e12).scalar_part,
                -(B | _e13).scalar_part,
                -(B | _e23).scalar_part,
            ]
        )
        _br = np.array(
            [
                Br.scalar_part,
                -(Br | _e12).scalar_part,
                -(Br | _e13).scalar_part,
                -(Br | _e23).scalar_part,
            ]
        )
        _labels = ["1", "e12", "e13", "e23"]
        _x = np.arange(len(_labels))
        _w = 0.35
        _ax2.bar(_x - _w / 2, _b, width=_w, color="steelblue", alpha=0.75, label="before")
        _ax2.bar(_x + _w / 2, _br, width=_w, color="darkorange", alpha=0.75, label="after")
        _ax2.set_xticks(_x, _labels)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title("Bivector coefficients under rotor action")
        _ax2.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_multivector_action,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotor Action on Multivectors

    Rotors do not only rotate vectors. The sandwich action rotates any multivector, preserving its grade while changing its orientation inside the algebra.

    This notebook is the action-side companion to [rotor_space.py](./rotor_space.py): that file focuses on how rotors themselves move, while this one focuses on what the same rotor does to different grades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    If

    $$
    R = e^{-\theta \widehat{B}/2},
    $$

    then the same sandwich rule rotates vectors, bivectors, and higher-grade objects:

    $$
    M' = R M \widetilde{R}.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 180, step=1, value=55, label="Rotation angle", show_value=True)
    plane = mo.ui.dropdown(
        options=["e12 plane", "e23 plane", "e13 plane"],
        value="e12 plane",
        label="Rotor plane",
    )
    vector_tilt = mo.ui.slider(-80, 80, step=1, value=30, label="Input vector tilt", show_value=True)
    return angle, plane, vector_tilt


@app.cell
def _(alg, angle, draw_multivector_action, e1, e2, e3, exp, gm, mo, np, plane, sandwich, unit, vector_tilt):
    _planes = {
        "e12 plane": (e1 * e2).name("B"),
        "e23 plane": (e2 * e3).name("B"),
        "e13 plane": (e1 * e3).name("B"),
    }
    _rotation_plane = unit(_planes[plane.value]).name(latex=r"\widehat{B}")
    _theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
    _rotor = exp(((-_theta / 2) * _rotation_plane)).name("R")
    _vector = (np.cos(np.radians(vector_tilt.value)) * e1 + 0.4 * e2 + np.sin(np.radians(vector_tilt.value)) * e3).name("v")
    _rotated_vector = sandwich(_rotor, _vector).name(latex=r"R v \widetilde{R}")
    _bivector = (e1 * e2 + 0.4 * e2 * e3).name("B")
    _rotated_bivector = sandwich(_rotor, _bivector).name(latex=r"R B \widetilde{R}")

    _md = t"""
    {_rotation_plane.display()} <br/>
    {_theta.display()} <br/>
    {_rotor.display()} <br/>
    {_vector.display()} <br/>
    {_rotated_vector.display()} <br/>
    {_bivector.display()} <br/>
    {_rotated_bivector.display()} <br/>
    The rotor changes orientation but keeps the bivector in grade 2.
    """

    mo.vstack([plane, angle, vector_tilt, gm.md(_md), draw_multivector_action(_vector, _rotated_vector, _bivector, _rotated_bivector)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The sandwich action is not “for vectors only.” It is the natural way to move geometric objects of any grade through the same rotation.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
