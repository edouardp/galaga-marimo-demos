import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, inverse, norm, squared, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, inverse, mo, norm, np, plt, squared, unit


@app.cell
def _(np, plt):
    def draw_normalization(v, vhat):
        _v = v.vector_part[:2]
        _vhat = vhat.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.8, 5.8))
        _circle = plt.Circle((0, 0), 1.0, color="gray", fill=False, alpha=0.35, linestyle="--")
        _ax.add_patch(_circle)
        _ax.annotate("", xy=_v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.annotate("", xy=_vhat, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.plot([], [], color="steelblue", label="v")
        _ax.plot([], [], color="crimson", label="unit(v)")
        _ax.set_xlim(-5.5, 5.5)
        _ax.set_ylim(-5.5, 5.5)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Magnitude vs normalization")
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_normalization,)


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
    return alg, e1, e2


@app.cell
def _(mo):
    length = mo.ui.slider(0.2, 5.0, step=0.1, value=3.0, label="Vector length", show_value=True)
    angle = mo.ui.slider(0, 180, step=1, value=35, label="Vector angle", show_value=True)
    bivector_scale = mo.ui.slider(0.2, 3.0, step=0.1, value=1.4, label="Bivector scale", show_value=True)
    return angle, bivector_scale, length


@app.cell
def _(angle, bivector_scale, draw_normalization, e1, e2, gm, inverse, length, mo, norm, np, squared, unit):
    _theta = np.radians(angle.value)
    _vector = (length.value * np.cos(_theta) * e1 + length.value * np.sin(_theta) * e2).name("v")
    _unit_vector = unit(_vector).name(latex=r"\widehat{v}")
    _vector_square = squared(_vector).name(latex=r"v^2")
    _vector_norm = norm(_vector).name(latex=r"\|v\|")
    _vector_inverse = inverse(_vector).name(latex=r"v^{-1}")

    _bivector = (bivector_scale.value * (e1 ^ e2)).name("B")
    _unit_bivector = unit(_bivector).name(latex=r"\widehat{B}")
    _bivector_square = squared(_bivector).name(latex=r"B^2")
    _bivector_norm = norm(_bivector).name(latex=r"\|B\|")
    _bivector_inverse = inverse(_bivector).name(latex=r"B^{-1}")

    _md = t"""
    {_vector.display()} <br/>
    {_vector_square.display()} <br/>
    {_vector_norm.display()} <br/>
    {_unit_vector.display()} <br/>
    {_vector_inverse.display()} <br/>
    {_bivector.display()} <br/>
    {_bivector_square.display()} <br/>
    {_bivector_norm.display()} <br/>
    {_unit_bivector.display()} <br/>
    {_bivector_inverse.display()} <br/>
    The same object can have a square, a magnitude, a normalized version, and an inverse, but those are not interchangeable notions.
    """

    mo.vstack([length, angle, bivector_scale, gm.md(_md), draw_normalization(_vector, _unit_vector)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    `norm(...)` tells you how big something is. `unit(...)` rescales it. `inverse(...)` tells you what multiplies it back to $1$. Those are closely related operations, but each answers a different question.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
