import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, even_grades, grade, involute, odd_grades, reverse
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return (
        Algebra,
        even_grades,
        gm,
        grade,
        involute,
        mo,
        np,
        odd_grades,
        plt,
        reverse,
    )


@app.cell
def _(np, plt):
    def draw_grade_products(before, after_left, after_right):
        _labels = ["grade 0", "grade 1", "grade 2", "grade 3"]
        _x = np.arange(len(_labels))
        _w = 0.25
        _fig, _ax = plt.subplots(figsize=(7.4, 4.8))
        _ax.bar(_x - _w, before, width=_w, color="black", alpha=0.8, label="x")
        _ax.bar(_x, after_left, width=_w, color="steelblue", alpha=0.8, label="I x")
        _ax.bar(_x + _w, after_right, width=_w, color="darkorange", alpha=0.8, label="x I")
        _ax.set_xticks(_x, _labels)
        _ax.grid(True, axis="y", alpha=0.25)
        _ax.set_title("How multiplication by I reorganizes grade signs")
        _ax.legend(loc="upper right")
        plt.close(_fig)
        return _fig

    return (draw_grade_products,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Grade Structure

    Geometric algebra is not just “one product on one space.” It is stratified by grade, and many of its cleanest patterns come from how operations respect, flip, or regroup grades.

    This notebook extends [grade_and_dimension.py](./grade_and_dimension.py) and [involutions_and_grade_ops.py](./involutions_and_grade_ops.py): those explain what grades are and how involutions act on them, while this one focuses on the larger grade structure itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We begin with a quick parity comparison between $\mathrm{Cl}(2,0)$ and $\mathrm{Cl}(3,0)$.

    The pseudoscalar behavior depends on dimension parity:

    - in even dimensions, the pseudoscalar anticommutes with odd grades
    - in odd dimensions, the pseudoscalar commutes with all grades

    That is one reason grade structure is bigger than any single algebra example.
    """)
    return


@app.cell
def _(Algebra):
    alg2 = Algebra((1, 1))
    f1, f2 = alg2.basis_vectors(lazy=True)
    return alg2, f1, f2


@app.cell
def _(alg2, f1, f2, gm):
    _I2 = (f1 * f2).name("I_2")
    _left_vector = (_I2 * f1).name(latex=r"I_2 e_1")
    _right_vector = (f1 * _I2).name(latex=r"e_1 I_2")
    _left_scalar = (_I2 * alg2.scalar(1)).name(latex=r"I_2 1")
    _right_scalar = (alg2.scalar(1) * _I2).name(latex=r"1 I_2")

    gm.md(t"""
    {_I2.display()} <br/>
    {_left_scalar.display()} <br/>
    {_right_scalar.display()} <br/>
    {_left_vector.display()} <br/>
    {_right_vector.display()} <br/>
    In $\\mathrm{{Cl}}(2,0)$, the pseudoscalar commutes with even grades but anticommutes with vectors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    In three dimensions, the grades are:

    - grade 0: scalar
    - grade 1: vector
    - grade 2: bivector
    - grade 3: trivector

    The even subalgebra contains grades $0$ and $2$. The odd subalgebra contains grades $1$ and $3$.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Multivector, Split by Grade

    Start with one mixed multivector and peel it apart. That is the basic move behind almost every named symmetry and subalgebra statement in GA.
    """)
    return


@app.cell
def _(mo):
    scalar_coeff = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Scalar coeff", show_value=True)
    vector_coeff = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.1, label="Vector coeff", show_value=True)
    bivector_coeff = mo.ui.slider(-2.0, 2.0, step=0.1, value=-0.9, label="Bivector coeff", show_value=True)
    trivector_coeff = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.7, label="Trivector coeff", show_value=True)
    return bivector_coeff, scalar_coeff, trivector_coeff, vector_coeff


@app.cell
def _(
    bivector_coeff,
    e1,
    e2,
    e3,
    even_grades,
    gm,
    grade,
    mo,
    odd_grades,
    scalar_coeff,
    trivector_coeff,
    vector_coeff,
):
    _x = (
        scalar_coeff.value
        + vector_coeff.value * e1
        + bivector_coeff.value * (e1 ^ e2)
        + trivector_coeff.value * (e1 ^ e2 ^ e3)
    ).eval().name("x")
    _grade_0 = grade(_x, 0)
    _grade_1 = grade(_x, 1)
    _grade_2 = grade(_x, 2)
    _grade_3 = grade(_x, 3)
    _x_even = even_grades(_x)
    _x_odd = odd_grades(_x)

    _md = t"""
    {_x.display()} <br/>
    {_grade_0.display()} <br/>
    {_grade_1.display()} <br/>
    {_grade_2.display()} <br/>
    {_grade_3.display()} <br/>
    {_x_even.display()} <br/>
    {_x_odd.display()} <br/>
    Grade decomposition is the cleanest way to see what kind of geometric content is present.
    """

    mo.vstack([scalar_coeff, vector_coeff, bivector_coeff, trivector_coeff, gm.md(_md)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Even and Odd Multiplication

    The even grades form a subalgebra: even times even stays even. Odd times odd lands back in the even sector. Mixed parity gives odd output.
    """)
    return


@app.cell
def _(
    bivector_coeff,
    e1,
    e2,
    e3,
    even_grades,
    gm,
    mo,
    odd_grades,
    scalar_coeff,
    trivector_coeff,
    vector_coeff,
):
    _x = (
        scalar_coeff.value
        + vector_coeff.value * e1
        + bivector_coeff.value * (e1 ^ e2)
        + trivector_coeff.value * (e1 ^ e2 ^ e3)
    )
    _even = even_grades(_x).name("E")
    _odd = odd_grades(_x).name("O")
    _ee = (_even * _even).name("EE")
    _eo = (_even * _odd).name("EO")
    _oe = (_odd * _even).name("OE")
    _oo = (_odd * _odd).name("OO")

    _md = t"""
    {_even.display()} <br/>
    {_odd.display()} <br/>
    {_ee.display()} <br/>
    {_eo.display()} <br/>
    {_oe.display()} <br/>
    {_oo.display()} <br/>
    Even-even and odd-odd products land in the even sector. Mixed parity products land in the odd sector.
    """

    mo.vstack([gm.md(_md)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Pseudoscalar and Grade Parity in 3D

    In $\mathrm{Cl}(3,0)$, the pseudoscalar $I = e_1 e_2 e_3$ is odd. Multiplying by it does not preserve individual grade, but it does relate complementary grades:

    - scalar $\leftrightarrow$ trivector
    - vector $\leftrightarrow$ bivector

    In odd dimension it also commutes with every grade, which is why the 3D pseudoscalar behaves more like a central orientation element.
    """)
    return


@app.cell
def _(
    bivector_coeff,
    draw_grade_products,
    e1,
    e2,
    e3,
    gm,
    grade,
    mo,
    np,
    scalar_coeff,
    trivector_coeff,
    vector_coeff,
):
    _I = (e1 * e2 * e3).name("I")
    _x = (
        scalar_coeff.value
        + vector_coeff.value * e1
        + bivector_coeff.value * (e1 ^ e2)
        + trivector_coeff.value * (e1 ^ e2 ^ e3)
    ).name("x")
    _Ix = (_I * _x).name("Ix")
    _xI = (_x * _I).name("xI")

    _before = np.array([
        grade(_x, 0).scalar_part,
        grade(_x, 1).vector_part[0],
        grade(_x, 2).eval().data[3],
        grade(_x, 3).eval().data[7],
    ])
    _after_left = np.array([
        grade(_Ix, 0).scalar_part,
        grade(_Ix, 1).vector_part[0],
        grade(_Ix, 2).eval().data[3],
        grade(_Ix, 3).eval().data[7],
    ])
    _after_right = np.array([
        grade(_xI, 0).scalar_part,
        grade(_xI, 1).vector_part[0],
        grade(_xI, 2).eval().data[3],
        grade(_xI, 3).eval().data[7],
    ])

    _md = t"""
    {_I.display()} <br/>
    {_x.display()} <br/>
    {_Ix.display()} <br/>
    {_xI.display()} <br/>
    Multiplication by the pseudoscalar swaps complementary grades.
    """

    mo.vstack([gm.md(_md), draw_grade_products(_before, _after_left, _after_right)])
    return


@app.cell
def _(e1, e2, e3, gm):
    _I = (e1 * e2 * e3).name("I")
    _left_vector = (_I * e1).name(latex=r"I e_1")
    _right_vector = (e1 * _I).name(latex=r"e_1 I")
    _left_bivector = (_I * (e1 ^ e2)).name(latex=r"I (e_1 \wedge e_2)")
    _right_bivector = ((e1 ^ e2) * _I).name(latex=r"(e_1 \wedge e_2) I")

    gm.md(t"""
    {_I.display()} <br/>
    {_left_vector.display()} <br/>
    {_right_vector.display()} <br/>
    {_left_bivector.display()} <br/>
    {_right_bivector.display()} <br/>
    In $\\mathrm{{Cl}}(3,0)$, left and right multiplication by the pseudoscalar agree on both odd and even grades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reverse and Involute Revisited

    Reverse and involute are good sanity checks on the grade structure:

    - `reverse(...)` changes sign by grade order
    - `involute(...)` changes sign by grade parity

    The second one is exactly why even and odd subalgebras matter so much.
    """)
    return


@app.cell
def _(
    bivector_coeff,
    e1,
    e2,
    e3,
    gm,
    involute,
    mo,
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
    ).eval().name("x")
    _x_reverse = reverse(_x)
    _x_involute = involute(_x)

    _md = t"""
    {_x.display()} <br/>
    {_x_reverse.display()} <br/>
    {_x_involute.display()} <br/>
    Reverse and involute are grade-structured operations, not arbitrary symbol manipulations.
    """

    mo.vstack([gm.md(_md)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Grade structure is one of the reasons GA stays organized. It tells you what kind of geometric object you have, how parity behaves under multiplication, and why duality and involutions take the forms they do.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
