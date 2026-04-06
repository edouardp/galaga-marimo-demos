import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, left_contraction, right_contraction
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, left_contraction, mo, np, plt, right_contraction


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Inner, Left, and Right Contraction

    These three products often agree in simple cases, which makes them easy to
    conflate. They are not the same operation.

    This notebook compares them in two settings:

    - same grade: bivector with bivector
    - mixed grade: vector with bivector, in both operand orders
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean algebra $\mathrm{Cl}(3,0)$.

    That gives us:

    - vectors for directions
    - bivectors for planes
    - a trivector pseudoscalar $I = e_1 e_2 e_3$

    The same-grade example uses two planes. The mixed-grade example uses a
    vector and a plane chosen from the same $e_1$-$e_3$ family so the output is
    easy to read.
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
    ## Same Grade: Bivector with Bivector

    For equal grades, these three products collapse to the same scalar overlap
    in this library. That is why they can seem interchangeable at first.
    """)
    return


@app.cell
def _(mo):
    same_grade_angle = mo.ui.slider(
        0, 180, step=1, value=35, label="Second plane angle", show_value=True
    )
    return (same_grade_angle,)


@app.cell
def _(
    draw_same_grade_contractions,
    e1,
    e2,
    e3,
    gm,
    left_contraction,
    mo,
    np,
    right_contraction,
    same_grade_angle,
):
    _theta = np.radians(same_grade_angle.value)
    _I = (e1 ^ e2 ^ e3).name("I")

    _A = (e1 ^ e2).name("A")
    _nA = e3.name(latex=r"n_A")
    _nB = (np.sin(_theta) * e1 + np.cos(_theta) * e3).name(latex=r"n_B")
    _B = (_I * _nB).eval().name("B")

    _inner = (_A | _B).eval().name(latex=r"A \cdot B")
    _left = left_contraction(_A, _B).eval().name(latex=r"A \,\lrcorner\, B")
    _right = right_contraction(_A, _B).eval().name(latex=r"A \,\llcorner\, B")

    _inner_value = _inner.scalar_part
    _left_value = _left.scalar_part
    _right_value = _right.scalar_part

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_inner.display()} <br/>
    {_left.display()} <br/>
    {_right.display()} <br/>
    Here all three reduce to the same scalar overlap because the operands have the same grade.
    """

    mo.vstack(
        [
            same_grade_angle,
            gm.md(_md),
            draw_same_grade_contractions(
                _nA.eval(), _nB.eval(), _inner_value, _left_value, _right_value
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mixed Grade: Vector with Bivector

    Now the difference matters. We keep the vector and the plane-normal in the
    $e_1$-$e_3$ plane. In this restricted family, every nonzero contraction
    lands along $e_2$, so a single signed coefficient is enough to show what is
    happening.

    The pattern to watch:

    - $a \cdot B$ matches the left contraction $a \,\lrcorner\, B$
    - $B \cdot a$ matches the right contraction $B \,\llcorner\, a$
    - the opposite-sided contraction vanishes in each order
    """)
    return


@app.cell
def _(mo):
    vector_angle = mo.ui.slider(0, 360, step=1, value=30, label="Vector angle for $a$", show_value=True)
    plane_angle = mo.ui.slider(0, 180, step=1, value=60, label="Plane angle for $B$", show_value=True)
    return plane_angle, vector_angle


@app.cell
def _(
    draw_mixed_grade_contractions,
    e1,
    e2,
    e3,
    gm,
    left_contraction,
    mo,
    np,
    plane_angle,
    right_contraction,
    vector_angle,
):
    _phi = np.radians(vector_angle.value)
    _theta = np.radians(plane_angle.value)
    _I = (e1 ^ e2 ^ e3).name("I")

    _a = (np.cos(_phi) * e1 + np.sin(_phi) * e3).eval().name("a")
    _n = (np.sin(_theta) * e1 + np.cos(_theta) * e3).eval().name("n")
    _B = (_I * _n).eval().name("B")

    _inner_ab = (_a | _B).eval().name(latex=r"a \cdot B")
    _left_ab = left_contraction(_a, _B).eval().name(latex=r"a \,\lrcorner\, B")
    _right_ab = right_contraction(_a, _B).eval().name(latex=r"a \,\llcorner\, B")

    _inner_ba = (_B | _a).eval().name(latex=r"B \cdot a")
    _left_ba = left_contraction(_B, _a).eval().name(latex=r"B \,\lrcorner\, a")
    _right_ba = right_contraction(_B, _a).eval().name(latex=r"B \,\llcorner\, a")

    _md_def = t"""
    {_a.display()} <br/>
    {_B.display()} <br/>
    """
    _md_aB = t"""
    {_inner_ab.display()} <br/>
    {_left_ab.display()} <br/>
    {_right_ab.display()} <br/>
    """
    _md_Ba = t"""
    {_inner_ba.display()} <br/>
    {_left_ba.display()} <br/>
    {_right_ba.display()} <br/>
    """


    mo.vstack([vector_angle,
               plane_angle,
               gm.md(_md_def),
               mo.hstack([gm.md(_md_aB), gm.md(_md_Ba)], justify="center", widths="equal", gap=0),
               "Mixed grades make the order-sensitivity visible: the nonzero contraction lives on only one side of the product.",
               draw_mixed_grade_contractions(_a.eval(), _n.eval(), _inner_ab.eval(),
                _left_ab.eval(), _right_ab.eval(), _inner_ba.eval(), _left_ba.eval(),
                _right_ba.eval() ) ] )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Same-grade examples hide the distinction because inner, left contraction,
    and right contraction collapse to the same scalar overlap.

    Mixed-grade examples expose the real structure:

    - left contraction favors the left operand when the grades descend that way
    - right contraction favors the right operand in the opposite order
    - the inner product tracks the nonzero side for these vector-bivector examples
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _xz_components(_vec):
        _parts = np.array(_vec.vector_part[:3], dtype=float)
        return np.array([_parts[0], _parts[2]], dtype=float)

    def draw_same_grade_contractions(nA, nB, inner_value, left_value, right_value):
        _labels = [r"$A \cdot B$", r"$A \,\lrcorner\, B$", r"$A \,\llcorner\, B$"]
        _values = np.array([inner_value, left_value, right_value], dtype=float)
        _nA = _xz_components(nA)
        _nB = _xz_components(nB)

        _fig, (_ax_left, _ax_right) = plt.subplots(1, 2, figsize=(11.0, 4.6))

        _ax_left.annotate(
            "",
            xy=_nA,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.8, mutation_scale=18),
        )
        _ax_left.annotate(
            "",
            xy=_nB,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.8, mutation_scale=18),
        )
        _ax_left.text(_nA[0] + 0.05, _nA[1] + 0.04, r"$n_A$", color="#2563eb")
        _ax_left.text(_nB[0] + 0.05, _nB[1] + 0.04, r"$n_B$", color="#d62828")
        _ax_left.axhline(0, color="#555555", lw=1.0, alpha=0.45)
        _ax_left.axvline(0, color="#555555", lw=1.0, alpha=0.45)
        _ax_left.set_xlim(-1.1, 1.1)
        _ax_left.set_ylim(-1.1, 1.1)
        _ax_left.set_aspect("equal")
        _ax_left.grid(True, alpha=0.25)
        _ax_left.set_xlabel("e1")
        _ax_left.set_ylabel("e3")
        _ax_left.set_title("Dual normals of the two planes")

        _x = np.arange(len(_labels))
        _ax_right.bar(_x, _values, color=["#222222", "#2563eb", "#d62828"], alpha=0.82)
        _ax_right.set_xticks(_x, _labels)
        _ax_right.set_ylim(-1.1, 1.1)
        _ax_right.grid(True, axis="y", alpha=0.25)
        _ax_right.set_title("Scalar outputs")

        plt.close(_fig)
        return _fig

    def draw_mixed_grade_contractions(a, n, inner_ab, left_ab, right_ab, inner_ba, left_ba, right_ba):
        _a = _xz_components(a)
        _n = _xz_components(n)
        _labels = [r"$\cdot$", r"$\lrcorner$", r"$\llcorner$"]
        _x = np.arange(len(_labels))

        def _coeff_e2(_mv):
            return _mv.vector_part[1]

        _ab_values = np.array(
            [_coeff_e2(inner_ab), _coeff_e2(left_ab), _coeff_e2(right_ab)],
            dtype=float,
        )
        _ba_values = np.array(
            [_coeff_e2(inner_ba), _coeff_e2(left_ba), _coeff_e2(right_ba)],
            dtype=float,
        )

        _fig, (_ax_left, _ax_mid, _ax_right) = plt.subplots(1, 3, figsize=(14.0, 4.6))

        _ax_left.annotate(
            "",
            xy=_a,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2.8, mutation_scale=18),
        )
        _ax_left.annotate(
            "",
            xy=_n,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.8, mutation_scale=18),
        )
        _ax_left.text(_a[0] + 0.05, _a[1] + 0.04, r"$a$", color="#7c3aed")
        _ax_left.text(_n[0] + 0.05, _n[1] + 0.04, r"$n$", color="#d62828")
        _ax_left.axhline(0, color="#555555", lw=1.0, alpha=0.45)
        _ax_left.axvline(0, color="#555555", lw=1.0, alpha=0.45)
        _ax_left.set_xlim(-1.1, 1.1)
        _ax_left.set_ylim(-1.1, 1.1)
        _ax_left.set_aspect("equal")
        _ax_left.grid(True, alpha=0.25)
        _ax_left.set_xlabel("e1")
        _ax_left.set_ylabel("e3")
        _ax_left.set_title(r"Vector $a$ and plane normal $n$")

        _ax_mid.bar(_x, _ab_values, color=["#222222", "#2563eb", "#d62828"], alpha=0.82)
        _ax_mid.set_xticks(_x, _labels)
        _ax_mid.set_ylim(-1.1, 1.1)
        _ax_mid.grid(True, axis="y", alpha=0.25)
        _ax_mid.set_title(r"$e_2$ coefficient of $a$ with $B$")

        _ax_right.bar(_x, _ba_values, color=["#222222", "#2563eb", "#d62828"], alpha=0.82)
        _ax_right.set_xticks(_x, _labels)
        _ax_right.set_ylim(-1.1, 1.1)
        _ax_right.grid(True, axis="y", alpha=0.25)
        _ax_right.set_title(r"$e_2$ coefficient of $B$ with $a$")

        plt.close(_fig)
        return _fig

    return draw_mixed_grade_contractions, draw_same_grade_contractions


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
