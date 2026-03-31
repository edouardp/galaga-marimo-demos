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
def _(np, plt):
    def draw_grade_routing(a, b, vv_coeffs, vv_inner_coeffs, vv_outer_coeffs):
        _labels = ["grade 0", "grade 1", "grade 2"]
        _x = np.arange(len(_labels))
        _w = 0.25
        _a = a.vector_part[:2]
        _b = b.vector_part[:2]
        _cross = _a[0] * _b[1] - _a[1] * _b[0]
        _fill_color = "darkorange" if _cross >= 0 else "crimson"

        _fig, (_ax_left, _ax_right) = plt.subplots(1, 2, figsize=(11.0, 4.8))

        _ax_left.annotate("", xy=_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        _ax_left.annotate("", xy=_b, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax_left.fill(
            [0, _a[0], _a[0] + _b[0], _b[0]],
            [0, _a[1], _a[1] + _b[1], _b[1]],
            color=_fill_color,
            alpha=0.5,
        )
        _ax_left.plot([], [], color="black", label="a")
        _ax_left.plot([], [], color="steelblue", label="b")
        _ax_left.plot([], [], color=_fill_color, alpha=0.5, linewidth=6, label="a ^ b")
        _extent = max(1.6, np.max(np.abs(np.concatenate([_a, _b, _a + _b]))) + 0.3)
        _ax_left.set_xlim(-_extent, _extent)
        _ax_left.set_ylim(-_extent, _extent)
        _ax_left.set_aspect("equal")
        _ax_left.grid(True, alpha=0.25)
        _ax_left.set_xlabel("e1")
        _ax_left.set_ylabel("e2")
        _ax_left.set_title("Vectors and the oriented area element")
        _ax_left.legend(loc="upper left")

        _ax_right.bar(_x - _w, vv_coeffs, width=_w, color="black", alpha=0.8, label="ab")
        _ax_right.bar(_x, vv_inner_coeffs, width=_w, color="steelblue", alpha=0.8, label="a | b")
        _ax_right.bar(_x + _w, vv_outer_coeffs, width=_w, color="darkorange", alpha=0.8, label="a ^ b")
        _ax_right.set_xticks(_x, _labels)
        _ax_right.set_ylim(-2.5, 2.5)
        _ax_right.grid(True, axis="y", alpha=0.25)
        _ax_right.set_title("Signed grade routing")
        _ax_right.legend(loc="upper right")
        plt.close(_fig)
        return _fig

    return (draw_grade_routing,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Grade Routing by Product

    Grade structure is not just about decomposing multivectors after the fact. The products themselves route information between grades in systematic ways.

    This notebook follows [grade_structure.py](./grade_structure.py): that file explains the grade stratification, while this one shows how the main products move information through that stratification.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$ here on purpose.

    In 2D, the cleanest routing story is already visible:

    - vector times vector splits into scalar and bivector parts
    - the inner product selects the scalar route
    - the outer product selects the bivector route

    This makes grades 0 and 2 the main actors instead of introducing grade 3 just to have one more bar.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vector Times Vector

    The central routing identity is

    $$
    ab = a \cdot b + a \wedge b.
    $$

    In $\mathrm{Cl}(2,0)$, that means the geometric product routes into grade 0 and grade 2, with no extra grades to distract from the split.
    """)
    return


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 360, step=1, value=50, label="Angle between a and b", show_value=True)
    b_length = mo.ui.slider(0.2, 2.0, step=0.05, value=1.0, label="Length of b", show_value=True)
    return angle, b_length


@app.cell
def _(angle, b_length, draw_grade_routing, e1, e2, gm, grade, mo, np):
    _theta = np.radians(angle.value)
    _a = e1.name("a")
    _b = (b_length.value * np.cos(_theta) * e1 + b_length.value * np.sin(_theta) * e2).name("b")
    _gp = (_a * _b).name("ab")
    _inner = (_a | _b).name(latex=r"a \cdot b")
    _outer = (_a ^ _b).name(latex=r"a \wedge b")

    def _grade_coeffs(_mv):
        _g0 = grade(_mv, 0).scalar_part
        _g1 = 0.0
        _g2 = grade(_mv, 2).eval().data[3]
        return np.array([_g0, _g1, _g2], dtype=float)

    _gp_coeffs = _grade_coeffs(_gp)
    _inner_coeffs = _grade_coeffs(_inner)
    _outer_coeffs = _grade_coeffs(_outer)

    _md = t"""
    {_a.display()} <br/>
    {_b.display()} <br/>
    {_gp.display()} <br/>
    {_inner.display()} <br/>
    {_outer.display()} <br/>
    Here the geometric product really does split into a scalar channel and a bivector channel.
    """

    mo.vstack([angle, b_length, gm.md(_md), draw_grade_routing(_a, _b, _gp_coeffs, _inner_coeffs, _outer_coeffs)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Grade-Routing Summary

    In this 2D setting the routing is explicit and signed:

    - geometric product keeps both routes
    - inner product keeps the scalar route
    - outer product keeps the bivector route

    This is the cleanest first example of products acting like grade selectors.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
