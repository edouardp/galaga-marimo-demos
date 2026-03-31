import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, grade
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, grade, mo, np, plt


@app.cell
def _(plt):
    def draw_grade_blades(a, b, c):
        _a = a.vector_part[:3]
        _b = b.vector_part[:3]
        _c = c.vector_part[:3]
        _fig = plt.figure(figsize=(6.2, 5.8))
        _ax = _fig.add_subplot(111, projection="3d")
        _ax.quiver(0, 0, 0, _a[0], _a[1], _a[2], color="crimson", linewidth=2)
        _ax.quiver(0, 0, 0, _b[0], _b[1], _b[2], color="steelblue", linewidth=2)
        _ax.quiver(0, 0, 0, _c[0], _c[1], _c[2], color="darkorange", linewidth=2)
        _ax.set_xlim(-1.5, 1.5)
        _ax.set_ylim(-1.5, 1.5)
        _ax.set_zlim(-1.5, 1.5)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Vectors spanning higher-grade objects")
        plt.close(_fig)
        return _fig

    return (draw_grade_blades,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Grade as Geometric Dimension

    Grade is not just bookkeeping. It tracks the geometric dimension of the part of a multivector you are looking at.

    This notebook pairs naturally with [bivectors_are_planes.py](./bivectors_are_planes.py): that file zooms in on grade 2, while this one shows how all grades fit together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    In three dimensions:

    - grade 0: scalar
    - grade 1: vector
    - grade 2: bivector, an oriented plane element
    - grade 3: trivector, an oriented volume element

    The wedge product raises grade when the vectors span genuinely new directions.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    b_angle = mo.ui.slider(10, 170, step=1, value=70, label="Angle of b in e1-e2 plane", show_value=True)
    c_tilt = mo.ui.slider(-80, 80, step=1, value=35, label="Tilt of c toward e3", show_value=True)
    return b_angle, c_tilt


@app.cell
def _(b_angle, c_tilt, draw_grade_blades, e1, e2, e3, gm, grade, mo, np):
    _phi = np.radians(b_angle.value)
    _psi = np.radians(c_tilt.value)
    _a = e1.name("a")
    _b = (np.cos(_phi) * e1 + np.sin(_phi) * e2).name("b")
    _c = (0.7 * np.cos(_psi) * e1 + 0.4 * e2 + np.sin(_psi) * e3).name("c")
    _scalar_part = (_a | _b).name(latex=r"\langle ab \rangle_0")
    _vector_example = (_a + _b).name(latex=r"a + b")
    _plane_blade = (_a ^ _b).name(latex=r"a \wedge b")
    _volume_blade = (_a ^ _b ^ _c).name(latex=r"a \wedge b \wedge c")
    _geometric_product = (_a * _b).name("ab")
    _grade_0_part = grade(_geometric_product, 0).name(latex=r"\langle ab \rangle_0")
    _grade_2_part = grade(_geometric_product, 2).name(latex=r"\langle ab \rangle_2")

    _md = t"""
    {_a.display()} <br/>
    {_b.display()} <br/>
    {_c.display()} <br/>
    {_scalar_part.display()} <br/>
    {_vector_example.display()} <br/>
    {_plane_blade.display()} <br/>
    {_volume_blade.display()} <br/>
    {_geometric_product.display()} splits into {_grade_0_part.display()} and {_grade_2_part.display()}.
    """

    mo.vstack([b_angle, c_tilt, gm.md(_md), draw_grade_blades(_a, _b, _c)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    Grade tells you what geometric kind of thing you have. That is why GA can combine several geometric meanings inside one product without losing track of them.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
