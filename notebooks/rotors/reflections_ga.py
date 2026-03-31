import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, reflect
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt, reflect


@app.cell
def _(np, plt):
    def draw_reflection(normal, v, vr):
        _normal = normal.vector_part[:2]
        _mirror = np.array([-_normal[1], _normal[0]])
        _v = v.vector_part[:2]
        _vr = vr.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.8, 5.8))
        _ax.plot(
            [-2.5 * _mirror[0], 2.5 * _mirror[0]],
            [-2.5 * _mirror[1], 2.5 * _mirror[1]],
            color="gray",
            alpha=0.5,
        )
        _ax.annotate("", xy=_normal, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, alpha=0.45, linestyle="--"))
        _ax.annotate("", xy=_v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        _ax.annotate("", xy=_vr, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.plot([], [], color="gray", label="mirror line")
        _ax.plot([], [], color="gray", alpha=0.45, label="mirror normal n")
        _ax.plot([], [], color="black", label="v")
        _ax.plot([], [], color="crimson", label="reflected v")
        _ax.set_xlim(-2, 2)
        _ax.set_ylim(-2, 2)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Reflection in a line")
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_reflection,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Reflections in Geometric Algebra

    Reflections are the primitive rigid motions in Euclidean GA. Rotors are built from them, but the reflection itself is already a clean geometric operation.

    This is the first notebook in the reflection-to-rotor sequence. It is followed by [versor_composition.py](./versor_composition.py) and then [rotors_from_reflections.py](./rotors_from_reflections.py).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    A line is represented here by a unit normal vector $n$. Reflecting a vector $v$ in that line is

    $$
    v' = -n v n.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    mirror_angle = mo.ui.slider(0, 360, step=1, value=30, label="Mirror line angle", show_value=True)
    vector_angle = mo.ui.slider(0, 180, step=1, value=70, label="Input vector angle", show_value=True)
    return mirror_angle, vector_angle


@app.cell
def _(
    draw_reflection,
    e1,
    e2,
    gm,
    mirror_angle,
    mo,
    np,
    reflect,
    vector_angle,
):
    _line_angle = np.radians(mirror_angle.value)
    _v = np.radians(vector_angle.value)
    _line_direction = np.cos(_line_angle) * e1 + np.sin(_line_angle) * e2
    _n = ((-_line_direction | e2) * e1 + (_line_direction | e1) * e2).name("n")
    _x = (np.cos(_v) * e1 + np.sin(_v) * e2).name("v")
    _xr = reflect(_x, _n).name("v'")

    _md = t"""
    {_n.display()} <br/>
    {_x.display()} <br/>
    {_xr.display()} <br/>
    The slider sets the mirror line angle; $n$ is the unit normal used in the reflection formula. <br/>
    Reflection rule: $v' = -n v n$ <br/>
    One mirror gives one reflection. Two mirrors will give a composed motion.
    """

    mo.vstack([mirror_angle, vector_angle, gm.md(_md), draw_reflection(_n, _x, _xr)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    A single reflection already knows about subspaces and orientation. Two reflections compose to a rotor, which is why reflections are the right primitive object rather than a side trick.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
