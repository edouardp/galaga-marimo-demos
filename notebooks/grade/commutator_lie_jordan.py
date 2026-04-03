import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, anticommutator, commutator, jordan_product, lie_bracket
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return (
        Algebra,
        anticommutator,
        commutator,
        gm,
        jordan_product,
        lie_bracket,
        mo,
        np,
        plt,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Commutator, Lie Bracket, and Jordan Product

    The geometric product splits naturally into antisymmetric and symmetric parts. The commutator and Lie bracket isolate the rotation-generating structure; the anticommutator and Jordan product isolate the complementary symmetric structure.

    This notebook extends [bivector_commutators.py](./bivector_commutators.py): that file focuses on why bivectors form a Lie algebra, while this one contrasts that antisymmetric structure with the symmetric Jordan side.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    For bivectors $A$ and $B$, the commutator captures order-sensitive structure and the Jordan product captures order-insensitive structure. Together they show how the geometric product splits into two meaningful parts.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(mo):
    plane_A = mo.ui.dropdown(
        options=["e12 plane", "e13 plane", "e23 plane"],
        value="e12 plane",
        label="Plane for A",
    )
    plane_B = mo.ui.dropdown(
        options=["e12 plane", "e13 plane", "e23 plane"],
        value="e23 plane",
        label="Plane for B",
    )
    scale_A = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Scale of A", show_value=True)
    scale_B = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Scale of B", show_value=True)
    return plane_A, plane_B, scale_A, scale_B


@app.cell
def _(
    anticommutator,
    commutator,
    draw_bivector_coeffs,
    e1,
    e2,
    e3,
    gm,
    jordan_product,
    lie_bracket,
    mo,
    plane_A,
    plane_B,
    scale_A,
    scale_B,
):
    _planes = {
        "e12 plane": e1 ^ e2,
        "e13 plane": e1 ^ e3,
        "e23 plane": e2 ^ e3,
    }
    _A = (scale_A.value * _planes[plane_A.value]).name("A")
    _B = (scale_B.value * _planes[plane_B.value]).name("B")
    _comm = commutator(_A, _B).name(latex=r"[A,B]")
    _anticomm = anticommutator(_A, _B).name(latex=r"\{A,B\}")
    _lie = lie_bracket(_A, _B).name(latex=r"[A,B]_{\mathrm{Lie}}")
    _jordan = jordan_product(_A, _B).name(latex=r"A \circ B")

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_comm.display()} <br/>
    {_anticomm.display()} <br/>
    {_lie.display()} <br/>
    {_jordan.display()} <br/>
    The antisymmetric and symmetric splits expose different algebraic structure inside the same geometric product.
    """

    mo.vstack([plane_A, plane_B, scale_A, scale_B, gm.md(_md), draw_bivector_coeffs(_A, _B, _comm)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The commutator is about order-sensitive structure and generators. The Jordan product is about the symmetric side. Both come from the same geometric product, but they answer different questions.
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_bivector_coeffs(A, B, comm):
        _labels = ["e12", "e13", "e23"]
        _x = np.arange(3)
        _fig, _ax = plt.subplots(figsize=(6.8, 4.8))

        def _coeffs(mv):
            _mv = mv.eval()
            return np.array([_mv.data[3], _mv.data[5], _mv.data[6]])

        _ax.bar(_x - 0.25, _coeffs(A), width=0.25, color="steelblue", alpha=0.8, label="A")
        _ax.bar(_x, _coeffs(B), width=0.25, color="darkorange", alpha=0.8, label="B")
        _ax.bar(_x + 0.25, _coeffs(comm), width=0.25, color="crimson", alpha=0.8, label="[A,B]")
        _ax.set_xticks(_x, _labels)
        _ax.grid(True, axis="y", alpha=0.25)
        _ax.set_title("Commutator structure in the bivector basis")
        _ax.legend(loc="upper right")
        plt.close(_fig)
        return _fig

    return (draw_bivector_coeffs,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
