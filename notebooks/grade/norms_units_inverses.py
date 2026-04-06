import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, inverse, norm, squared, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, inverse, mo, norm, np, plt, squared, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Norms, Units, and Inverses

    These operations answer related but different questions. `squared(...)` keeps the algebraic product, `norm(...)` reports magnitude, `unit(...)` normalizes, and `inverse(...)` solves a multiplicative equation.

    This notebook fits next to [subspace_actions.py](../subspaces/subspace_actions.py): before projecting onto a subspace or using a blade as a generator, you often need to know whether it is normalized and invertible.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    For Euclidean vectors and unit bivectors, these operations line up cleanly. The point is not that they are the same operation, but that they answer different geometric questions about the same object.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    length = mo.ui.slider(0.2, 5.0, step=0.1, value=3.0, label="Vector length", show_value=True)
    angle = mo.ui.slider(0, 180, step=1, value=35, label="Vector angle", show_value=True)
    bivector_angle = mo.ui.slider(5, 175, step=1, value=50, label="Bivector opening angle", show_value=True)
    bivector_scale = mo.ui.slider(0.2, 3.0, step=0.1, value=1.4, label="Bivector scale", show_value=True)
    return angle, bivector_angle, bivector_scale, length


@app.cell
def _(
    angle,
    bivector_angle,
    bivector_scale,
    draw_normalization,
    e1,
    e2,
    gm,
    inverse,
    length,
    mo,
    norm,
    np,
    squared,
    unit,
):
    _theta = np.radians(angle.value)
    _vector = (length.value * np.cos(_theta) * e1 + length.value * np.sin(_theta) * e2).eval().name("v")

    _phi = np.radians(bivector_angle.value)
    _a_biv = e1.name(latex=r"a_B")
    _b_biv = (
        bivector_scale.value * np.cos(_phi) * e1
        + bivector_scale.value * np.sin(_phi) * e2
    ).eval().name(latex=r"b_B")
    _bivector = (_a_biv ^ _b_biv).name("B")

    _md_v = t"""
    {_vector.display()} <br/>
    {squared(_vector).display()} <br/>
    {norm(_vector).display()} <br/>
    {unit(_vector).display()} <br/>
    {inverse(_vector).display()} <br/>
    """
    _md_B = t"""
    {_bivector.display()} <br/>
    {squared(_bivector).display()} <br/>
    {norm(_bivector).display()} <br/>
    {unit(_bivector).display()} <br/>
    {inverse(_bivector).display()} <br/>
    """

    mo.vstack([mo.hstack([length, bivector_scale], justify="center", widths="equal"), 
               mo.hstack([angle, bivector_angle], justify="center", widths="equal"),
               mo.hstack([gm.md(_md_v), gm.md(_md_B)], justify="center", widths="equal"),
               "The same object can have a square, a magnitude, a normalized version, and an inverse, but those are not interchangeable notions.",
               draw_normalization(_vector, unit(_vector), _a_biv, _b_biv, unit(_a_biv), unit(_b_biv)),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    `norm(...)` tells you how big something is. `unit(...)` rescales it. `inverse(...)` tells you what multiplies it back to $1$. Those are closely related operations, but each answers a different question.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(plt):
    def draw_normalization(v, vhat, a_biv, b_biv, ahat_biv, bhat_biv):
        _v = v.vector_part[:2]
        _vhat = vhat.vector_part[:2]
        _a_biv = a_biv.vector_part[:2]
        _b_biv = b_biv.vector_part[:2]
        _ahat_biv = ahat_biv.vector_part[:2]
        _bhat_biv = bhat_biv.vector_part[:2]

        _fig, (_ax_vec, _ax_biv) = plt.subplots(1, 2, figsize=(11.2, 5.4))

        _circle = plt.Circle((0, 0), 1.0, color="gray", fill=False, alpha=0.35, linestyle="--")
        _ax_vec.add_patch(_circle)
        _ax_vec.annotate("", xy=_v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax_vec.annotate("", xy=_vhat, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax_vec.plot([], [], color="steelblue", label="v")
        _ax_vec.plot([], [], color="crimson", label="unit(v)")
        _ax_vec.set_xlim(-5.5, 5.5)
        _ax_vec.set_ylim(-5.5, 5.5)
        _ax_vec.set_aspect("equal")
        _ax_vec.grid(True, alpha=0.25)
        _ax_vec.set_xlabel("e1")
        _ax_vec.set_ylabel("e2")
        _ax_vec.set_title("Vector magnitude vs normalization")
        _ax_vec.legend(loc="upper left")

        _ax_biv.fill(
            [0, _a_biv[0], _a_biv[0] + _b_biv[0], _b_biv[0]],
            [0, _a_biv[1], _a_biv[1] + _b_biv[1], _b_biv[1]],
            color="goldenrod",
            alpha=0.25,
            label="B",
        )
        _ax_biv.annotate("", xy=_a_biv, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="goldenrod", lw=2))
        _ax_biv.annotate("", xy=_b_biv, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="goldenrod", lw=2))
        _ax_biv.fill(
            [0, _ahat_biv[0], _ahat_biv[0] + _bhat_biv[0], _bhat_biv[0]],
            [0, _ahat_biv[1], _ahat_biv[1] + _bhat_biv[1], _bhat_biv[1]],
            color="crimson",
            alpha=0.12,
            label="unit(B)",
        )
        _ax_biv.annotate("", xy=_ahat_biv, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2, linestyle="--"))
        _ax_biv.annotate("", xy=_bhat_biv, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2, linestyle="--"))
        _ax_biv.set_xlim(-3.2, 3.2)
        _ax_biv.set_ylim(-3.2, 3.2)
        _ax_biv.set_aspect("equal")
        _ax_biv.grid(True, alpha=0.25)
        _ax_biv.set_xlabel("e1")
        _ax_biv.set_ylabel("e2")
        _ax_biv.set_title("Bivector area element vs normalization")
        _ax_biv.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_normalization,)


if __name__ == "__main__":
    app.run()
