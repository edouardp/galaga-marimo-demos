import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, complement, dual, uncomplement, undual
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, complement, dual, gm, mo, np, plt, uncomplement, undual


@app.cell
def _(np, plt):
    def draw_area_vectors(angle_deg):
        _theta = np.radians(angle_deg)
        _a = np.array([1.0, 0.0])
        _b = np.array([np.cos(_theta), np.sin(_theta)])

        _fig, _ax = plt.subplots(figsize=(6, 6))
        _ax.annotate("", xy=_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.annotate("", xy=_b, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.fill([0, _a[0], _a[0] + _b[0], _b[0]], [0, _a[1], _a[1] + _b[1], _b[1]], color="goldenrod", alpha=0.25)
        _ax.set_aspect("equal")
        _ax.set_xlim(-1.5, 2.0)
        _ax.set_ylim(-1.2, 2.0)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("A bivector as an oriented area element")
        _ax.grid(True, alpha=0.25)
        plt.close(_fig)
        return _fig

    return (draw_area_vectors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Duality and Complements

    `dual(...)` and `complement(...)` often look the same in ordinary Euclidean examples, so it is easy to think they are interchangeable. They are not. This notebook compares them in Euclidean 3D and then shows why the distinction matters in a degenerate algebra.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We first build the Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    Its basis vectors satisfy $e_1^2 = e_2^2 = e_3^2 = 1$, so the pseudoscalar is invertible. In that setting, metric duality is well-defined and often agrees with complement on simple basis blades.
    """)
    return


@app.cell
def _(Algebra):
    cl3 = Algebra((1, 1, 1))
    e1, e2, e3 = cl3.basis_vectors(lazy=True)
    return e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Euclidean 3D

    In Euclidean 3D, the dual of a bivector is an axial vector. The complement of a basis blade often lands on the same basis element, but the meanings are different:

    - `dual(...)` uses the metric and the pseudoscalar inverse
    - `complement(...)` is combinatorial and tracks missing basis directions
    """)
    return


@app.cell
def _(complement, dual, e1, e2, gm, uncomplement, undual):
    _bivector = (e1 ^ e2).name("B")
    _dual_b = dual(_bivector).name(latex=r"B^\star")
    _comp_b = complement(_bivector).name(latex=r"B^\complement")
    _undual_b = undual(_dual_b).name(latex=r"(B^\star)^{\star^{-1}}")
    _uncomp_b = uncomplement(_comp_b).name(latex=r"(B^\complement)^{\complement^{-1}}")

    gm.md(t"""
    {_bivector.display()} <br/>
    {_dual_b.display()} <br/>
    {_comp_b.display()} <br/>
    {_undual_b.display()} <br/>
    {_uncomp_b.display()}
    """)
    return


@app.cell
def _(mo):
    area_angle = mo.ui.slider(0, 180, step=1, value=35, label="Opening angle", show_value=True)
    return (area_angle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive Area Element

    Let $a$ and $b$ span an oriented area element $a \wedge b$. In Euclidean 3D, `dual(a \wedge b)` gives the perpendicular axial vector. `complement(a \wedge b)` matches it here on basis structure, but that agreement is contingent on the Euclidean metric.
    """)
    return


@app.cell
def _(area_angle, complement, draw_area_vectors, dual, e1, e2, gm, mo, np):
    _theta = np.radians(area_angle.value)
    _a = e1.name("a")
    _b = (np.cos(_theta) * e1 + np.sin(_theta) * e2).name("b")
    _area = (_a ^ _b).name(latex=r"a \wedge b")
    _dual_area = dual(_area).name(latex=r"(a \wedge b)^\star")
    _comp_area = complement(_area).name(latex=r"(a \wedge b)^\complement")

    _md = t"""
    {_a.display()} <br/>
    {_b.display()} <br/>
    {_area.display()} <br/>
    {_dual_area.display()} <br/>
    {_comp_area.display()}
    """

    mo.vstack([
        area_angle,
        gm.md(_md),
        draw_area_vectors(area_angle.value),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now build projective geometric algebra with signature $(1,1,1,0)$.

    This algebra is degenerate: the pseudoscalar is not invertible. That is exactly the setting where complement remains available while metric duality is no longer the right operation.
    """)
    return


@app.cell
def _(Algebra):
    pga = Algebra((1, 1, 1, 0))
    p1, p2, p3, p0 = pga.basis_vectors(lazy=True)
    return p0, p1, p2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Degenerate Metric: PGA

    In PGA, complement still converts between complementary basis structure without needing a pseudoscalar inverse. That makes it robust in a way that Euclidean-style duality is not.
    """)
    return


@app.cell
def _(mo):
    plane_a = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Plane e1 coeff", show_value=True)
    plane_b = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.7, label="Plane e2 coeff", show_value=True)
    plane_d = mo.ui.slider(-2.0, 2.0, step=0.1, value=-1.2, label="Plane e0 coeff", show_value=True)
    return plane_a, plane_b, plane_d


@app.cell
def _(complement, gm, mo, p0, p1, p2, plane_a, plane_b, plane_d):
    _plane = (plane_a.value * p1 + plane_b.value * p2 + plane_d.value * p0).name(latex=r"\pi")
    _ideal_line = complement(_plane).name(latex=r"\pi^\complement")

    _md = t"""
    {_plane.display()} <br/>
    {_ideal_line.display()} <br/>
    Here the complement is still well-defined because it is basis-combinatorial rather than metric-inverse based.
    """

    mo.vstack([
        plane_a,
        plane_b,
        plane_d,
        gm.md(_md),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    In Euclidean examples, dual and complement can look deceptively similar. The difference becomes important once the metric changes or becomes degenerate. `dual(...)` is metric-dependent; `complement(...)` is a basis-combinatorial operation that remains available in settings like PGA.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
