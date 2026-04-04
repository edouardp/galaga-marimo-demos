import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, unit, norm
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, norm, np, plt, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Why Bivectors Are Planes

    A bivector is not just an antisymmetric algebraic object. Geometrically, it represents an oriented plane element. In 2D that plane element looks like a signed area.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    Given two vectors $a$ and $b$, the wedge

    $$
    B = a \wedge b
    $$

    keeps only the plane-and-area part. Its magnitude tracks the spanned area, and its sign tracks orientation.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    opening = mo.ui.slider(5, 175, step=1, value=50, label="Opening angle", show_value=True)
    b_length = mo.ui.slider(0.2, 1.8, step=0.05, value=1.0, label="Length of b", show_value=True)
    return b_length, opening


@app.cell
def _(b_length, draw_plane_vectors, e1, e2, gm, mo, norm, np, opening, unit):
    _phi = np.radians(opening.value)
    _a = e1.name("a")
    _b = (b_length.value * np.cos(_phi) * e1 + b_length.value * np.sin(_phi) * e2).eval().name("b")
    _B = (_a ^ _b).name("B")
    _Bhat = unit(_B)
    _area = norm(_B).eval()

    _md = t"""
    {_a.display()} <br/>
    {_b.display()} <br/>
    {_B.display()} <br/>
    {_Bhat.display()} <br/>
    {norm(_B).display()} $, \\;$ so the bivector magnitude tracks the spanned area.
    """

    mo.vstack([opening, b_length, gm.md(_md), draw_plane_vectors(_a, _b)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The vectors span the plane, but the bivector is the plane object. Once normalized, it becomes the pure plane generator used in rotor exponentials.
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
    def draw_plane_vectors(a, b):
        _a = a.vector_part[:2]
        _b = b.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.8, 5.8))
        _ax.annotate("", xy=_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.annotate("", xy=_b, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.fill([0, _a[0], _a[0] + _b[0], _b[0]], [0, _a[1], _a[1] + _b[1], _b[1]], color="goldenrod", alpha=0.25)
        _ax.set_xlim(-2, 2)
        _ax.set_ylim(-2, 2)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("A bivector as an oriented area element")
        plt.close(_fig)
        return _fig

    return (draw_plane_vectors,)


if __name__ == "__main__":
    app.run()
