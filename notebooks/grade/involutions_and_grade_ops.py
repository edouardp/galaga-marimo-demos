import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, conjugate, even_grades, grade, involute, odd_grades, reverse
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, conjugate, even_grades, gm, grade, involute, mo, np, odd_grades, plt, reverse


@app.cell
def _(np, plt):
    def draw_grade_coefficients(coeffs_before, coeffs_after, title_after):
        _labels = ["grade 0", "grade 1", "grade 2", "grade 3"]
        _x = np.arange(len(_labels))
        _w = 0.35
        _fig, _ax = plt.subplots(figsize=(7.0, 4.8))
        _ax.bar(_x - _w / 2, coeffs_before, width=_w, color="steelblue", alpha=0.8, label="x")
        _ax.bar(_x + _w / 2, coeffs_after, width=_w, color="darkorange", alpha=0.8, label=title_after)
        _ax.set_xticks(_x, _labels)
        _ax.grid(True, axis="y", alpha=0.25)
        _ax.set_title("How the involution changes grade signs")
        _ax.legend(loc="upper right")
        plt.close(_fig)
        return _fig

    return (draw_grade_coefficients,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Involutions and Grade Operations

    Reverse, involute, and conjugate are different symmetries of the algebra. Grade projections and even/odd decompositions let you peel a multivector apart to see exactly what those symmetries are acting on.

    This notebook complements [grade_and_dimension.py](./grade_and_dimension.py): that file explains what the grades mean geometrically, while this one shows how algebraic symmetries respond to those grades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    A general multivector mixes grades. Reverse, involute, and conjugate do not change the underlying coefficients arbitrarily: they flip signs according to grade parity and grade order.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    scalar_coeff = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.0, label="Scalar coeff", show_value=True)
    vector_coeff = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.2, label="Vector coeff", show_value=True)
    bivector_coeff = mo.ui.slider(-3.0, 3.0, step=0.1, value=-0.8, label="Bivector coeff", show_value=True)
    trivector_coeff = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.6, label="Trivector coeff", show_value=True)
    operation = mo.ui.dropdown(
        options=["reverse", "involute", "conjugate"],
        value="reverse",
        label="Involution",
    )
    return bivector_coeff, operation, scalar_coeff, trivector_coeff, vector_coeff


@app.cell
def _(
    bivector_coeff,
    conjugate,
    draw_grade_coefficients,
    e1,
    e2,
    e3,
    even_grades,
    gm,
    grade,
    involute,
    mo,
    odd_grades,
    operation,
    reverse,
    scalar_coeff,
    trivector_coeff,
    vector_coeff,
):
    _x = (
        scalar_coeff.value
        + vector_coeff.value * e1
        + bivector_coeff.value * (e1 ^ e2)
        + trivector_coeff.value * (e1 ^ e2 ^ e3)
    ).name("x")

    _operations = {
        "reverse": reverse,
        "involute": involute,
        "conjugate": conjugate,
    }
    _transformed = _operations[operation.value](_x).name(operation.value)
    _grade0 = grade(_x, 0).name(latex=r"\langle x \rangle_0")
    _grade1 = grade(_x, 1).name(latex=r"\langle x \rangle_1")
    _grade2 = grade(_x, 2).name(latex=r"\langle x \rangle_2")
    _grade3 = grade(_x, 3).name(latex=r"\langle x \rangle_3")
    _even = even_grades(_x).name(latex=r"x_{\mathrm{even}}")
    _odd = odd_grades(_x).name(latex=r"x_{\mathrm{odd}}")

    _before = np.array([
        grade(_x, 0).scalar_part,
        grade(_x, 1).vector_part[0],
        grade(_x, 2).eval().data[3],
        grade(_x, 3).eval().data[7],
    ])
    _after = np.array([
        grade(_transformed, 0).scalar_part,
        grade(_transformed, 1).vector_part[0],
        grade(_transformed, 2).eval().data[3],
        grade(_transformed, 3).eval().data[7],
    ])

    _md = t"""
    {_x.display()} <br/>
    {_transformed.display()} <br/>
    {_grade0.display()} <br/>
    {_grade1.display()} <br/>
    {_grade2.display()} <br/>
    {_grade3.display()} <br/>
    {_even.display()} <br/>
    {_odd.display()} <br/>
    The grade split explains exactly which parts change sign under {operation.value}.
    """

    mo.vstack(
        [
            scalar_coeff,
            vector_coeff,
            bivector_coeff,
            trivector_coeff,
            operation,
            gm.md(_md),
            draw_grade_coefficients(_before, _after, operation.value),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Involutions are not mysterious global rewrites. They are grade-sensitive symmetries. Once the multivector is decomposed by grade, their action becomes transparent.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
