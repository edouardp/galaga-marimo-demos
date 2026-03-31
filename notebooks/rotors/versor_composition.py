import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, reflect, reverse
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt, reflect, reverse


@app.cell
def _(plt):
    def draw_versor_action(normal1, normal2, v, v1, v2):
        _n1 = normal1.vector_part[:2]
        _n2 = normal2.vector_part[:2]
        _m1 = [-_n1[1], _n1[0]]
        _m2 = [-_n2[1], _n2[0]]
        _v = v.vector_part[:2]
        _v1 = v1.vector_part[:2]
        _v2 = v2.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.8, 5.8))
        _ax.plot([-2.5 * _m1[0], 2.5 * _m1[0]], [-2.5 * _m1[1], 2.5 * _m1[1]], color="gray", alpha=0.45)
        _ax.plot([-2.5 * _m2[0], 2.5 * _m2[0]], [-2.5 * _m2[1], 2.5 * _m2[1]], color="steelblue", alpha=0.45)
        _ax.annotate("", xy=_n1, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="gray", lw=1.2, alpha=0.35, linestyle="--"))
        _ax.annotate("", xy=_n2, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.2, alpha=0.35, linestyle="--"))
        _ax.annotate("", xy=_v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        _ax.annotate("", xy=_v1, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.annotate("", xy=_v2, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkorange", lw=2))
        _ax.plot([], [], color="gray", label="first mirror line")
        _ax.plot([], [], color="steelblue", label="second mirror line")
        _ax.plot([], [], color="black", label="input v")
        _ax.plot([], [], color="crimson", label="after first reflection")
        _ax.plot([], [], color="darkorange", label="after second reflection")
        _ax.set_xlim(-2, 2)
        _ax.set_ylim(-2, 2)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Versor composition from reflections")
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_versor_action,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Versor Composition

    Reflections are the primitive rigid motions in Euclidean GA. A versor is what you get when you compose them by geometric multiplication.

    This is the middle notebook in the reflection-to-rotor sequence. [reflections_ga.py](./reflections_ga.py) introduces one reflection; [rotors_from_reflections.py](./rotors_from_reflections.py) specializes this composition to the rotor case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    If $n_1$ and $n_2$ are unit normals for two mirror lines, then the composed versor is

    $$
    V = n_2 n_1.
    $$

    Acting with the two reflections in sequence gives the same result as the sandwich action

    $$
    v'' = V v \widetilde{V}.
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
    first_mirror = mo.ui.slider(0, 360, step=1, value=25, label="First mirror line", show_value=True)
    second_mirror = mo.ui.slider(0, 360, step=1, value=70, label="Second mirror line", show_value=True)
    vector_angle = mo.ui.slider(0, 180, step=1, value=40, label="Input vector angle", show_value=True)
    return first_mirror, second_mirror, vector_angle


@app.cell
def _(
    draw_versor_action,
    e1,
    e2,
    first_mirror,
    gm,
    mo,
    np,
    reflect,
    reverse,
    second_mirror,
    vector_angle,
):
    _a1 = np.radians(first_mirror.value)
    _a2 = np.radians(second_mirror.value)
    _av = np.radians(vector_angle.value)
    _line1 = np.cos(_a1) * e1 + np.sin(_a1) * e2
    _line2 = np.cos(_a2) * e1 + np.sin(_a2) * e2
    _n1 = ((-_line1 | e2) * e1 + (_line1 | e1) * e2).name("n_1")
    _n2 = ((-_line2 | e2) * e1 + (_line2 | e1) * e2).name("n_2")
    _v = (np.cos(_av) * e1 + np.sin(_av) * e2).name("v")
    _first_reflection = reflect(_v, _n1).name(latex=r"v_1")
    _versor = (_n2 * _n1).name("V")
    _versor_reverse = reverse(_versor).name(latex=r"\widetilde{V}")
    _second_reflection = reflect(_first_reflection, _n2).name(latex=r"v_2")
    _sandwich_result = (_versor * _v * _versor_reverse).name(latex=r"V v \widetilde{V}")

    _md = t"""
    {_n1.display()} <br/>
    {_n2.display()} <br/>
    {_versor.display()} <br/>
    {_versor_reverse.display()} <br/>
    {_first_reflection.display()} <br/>
    {_second_reflection.display()} <br/>
    {_sandwich_result.display()} <br/>
    The sliders set mirror line angles; $n_1$ and $n_2$ are the corresponding unit normals used in the formulas. <br/>
    Two reflections compose into one versor action, and the sandwich form matches the explicit sequential reflections.
    """

    mo.vstack(
        [
            first_mirror,
            second_mirror,
            vector_angle,
            gm.md(_md),
            draw_versor_action(_n1, _n2, _v, _first_reflection, _second_reflection),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Versors package a sequence of reflections into one object. Rotors are the even versors, but the broader idea is that geometric multiplication composes the transformations directly.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
