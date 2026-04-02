import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_polygon_area(vertices, point, wedge_terms):
        _verts = np.array(vertices, dtype=float)
        _p = np.array(point, dtype=float)
        _terms = np.array(wedge_terms, dtype=float)

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.8, 5.4))

        _closed = np.vstack([_verts, _verts[0]])
        _ax1.plot(_closed[:, 0], _closed[:, 1], color="black", linewidth=1.8)
        _ax1.scatter(_verts[:, 0], _verts[:, 1], color="black", s=28, zorder=3)
        _ax1.scatter([_p[0]], [_p[1]], color="darkgreen", s=50, zorder=4)
        _ax1.text(_p[0] + 0.05, _p[1] + 0.05, "P", color="darkgreen")

        for _i, _v in enumerate(_verts):
            _ax1.text(_v[0] + 0.05, _v[1] + 0.05, f"v{_i+1}")

        for _i in range(len(_verts)):
            _a = _verts[_i]
            _b = _verts[(_i + 1) % len(_verts)]
            _color = "crimson" if _terms[_i] >= 0 else "steelblue"
            _ax1.fill([_p[0], _a[0], _b[0]], [_p[1], _a[1], _b[1]], color=_color, alpha=0.22)
            _ax1.plot([_p[0], _a[0]], [_p[1], _a[1]], color="gray", alpha=0.35, linewidth=1)
            _ax1.plot([_p[0], _b[0]], [_p[1], _b[1]], color="gray", alpha=0.35, linewidth=1)

        _ax1.set_aspect("equal")
        _ax1.set_xlim(-2.8, 2.8)
        _ax1.set_ylim(-2.4, 2.4)
        _ax1.grid(True, alpha=0.25)
        _ax1.set_xlabel("e1")
        _ax1.set_ylabel("e2")
        _ax1.set_title("Signed fan of wedge triangles")

        _x = np.arange(len(_terms))
        _colors = ["#222222" if _t >= 0 else "crimson" for _t in _terms]
        _ax2.bar(_x, _terms, color=_colors, alpha=0.82)
        _ax2.axhline(0, color="black", linewidth=0.8)
        _ax2.set_xticks(_x, [f"$v_{i+1}\\wedge v_{(i+1)%len(_terms)+1}$" for i in range(len(_terms))])
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_ylim(-4.0, 4.0)
        _ax2.set_title("Signed bivector contributions")

        plt.close(_fig)
        return _fig

    return (draw_polygon_area,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Polygon Area from Bivector Sums

    The area of a polygon can be recovered from a sum of signed wedge terms. Moving the reference point changes the individual bivectors, but the total bivector area stays the same.

    This notebook extends [barycentric_from_areas.py](./barycentric_from_areas.py): there the wedge areas belong to one triangle, while here a whole polygon is decomposed into a fan of signed subareas.

    Inspired by [this short video](https://www.youtube.com/shorts/S3ICGDfWqJs) by `@sudgylacmoe`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    If the polygon vertices are $v_1, \dots, v_n$ and $P$ is any reference point, then

    $$
    B_{\mathrm{poly}} = \frac{1}{2}\sum_{k=1}^n (v_k - P)\wedge(v_{k+1} - P)
    $$

    is the signed area bivector of the polygon.

    The individual terms can be positive or negative. That is not a bug. Their signed sum is the geometric content.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    polygon = mo.ui.dropdown(
        options=["triangle", "convex pentagon", "concave pentagon", "concave hexagon"],
        value="concave pentagon",
        label="Polygon",
    )
    px = mo.ui.slider(-1.5, 1.8, step=0.05, value=0.1, label="Reference point x", show_value=True)
    py = mo.ui.slider(-1.5, 1.8, step=0.05, value=0.2, label="Reference point y", show_value=True)
    return polygon, px, py


@app.cell
def _(e1, e2):
    polygons = {
        "triangle": [(-1.2, -0.6), (1.4, -0.2), (-0.1, 1.4)],
        "convex pentagon": [(-1.5, -0.2), (-0.6, -1.1), (1.0, -0.8), (1.5, 0.5), (-0.1, 1.5)],
        "concave pentagon": [(-1.6, -0.1), (-0.4, -1.0), (1.3, -0.2), (0.2, 0.3), (-0.2, 1.4)],
        "concave hexagon": [(-1.6, 0.1), (-0.8, -1.0), (0.7, -1.1), (1.5, 0.1), (0.2, 0.2), (-0.3, 1.4)],
    }

    def to_mv(points):
        return [x * e1 + y * e2 for x, y in points]

    return polygons, to_mv


@app.cell
def _(
    alg,
    draw_polygon_area,
    e1,
    e2,
    gm,
    mo,
    polygon,
    polygons,
    px,
    py,
    to_mv,
):
    _verts_xy = polygons[polygon.value]
    _verts = to_mv(_verts_xy)
    _P = (px.value * e1 + py.value * e2).name("P")

    _terms = []
    _term_lines = []
    _sum_biv = alg.scalar(0)
    for _i in range(len(_verts)):
        _a = (_verts[_i] - _P).name(latex=rf"r_{_i+1}")
        _b = (_verts[(_i + 1) % len(_verts)] - _P).name(latex=rf"r_{(_i+1)%len(_verts)+1}")
        _term = (_a ^ _b).name(latex=rf"r_{_i+1}\wedge r_{(_i+1)%len(_verts)+1}")
        _term_value = _term.eval().data[3]
        _terms.append(_term_value)
        _sum_biv = _sum_biv + _term
        if _term_value < 0:
            _term_lines.append(
                rf"${_term.latex()} = {{\color{{red}} {_term.eval().latex()}}}$"
            )
        else:
            _term_lines.append(rf"${_term.latex()} = {_term.eval().latex()}$")

    _area_bivector = (0.5 * _sum_biv).name(latex=r"B_{\mathrm{poly}}")
    _signed_area = 0.5 * _sum_biv.eval().data[3]
    _abs_area = abs(_signed_area)
    _orientation = "counterclockwise" if _signed_area >= 0 else "clockwise"
    _term_block = "<br/>".join(_term_lines)

    _md = t"""
    {_P.display()} <br/>
    {_area_bivector.display()} <br/>
    Signed scalar area: ${_signed_area:.3f}$ <br/>
    Absolute area: ${_abs_area:.3f}$ <br/>
    Orientation: **{_orientation}** <br/><br/>
    Individual wedge terms:<br/>
    """

    mo.vstack([polygon, px, py,
    gm.md(_md), gm.md(_term_block), draw_polygon_area(_verts_xy, (px.value, py.value), _terms)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The reference point can make some triangle contributions negative, especially for concave polygons. That does not break the method. The signed bivector sum is exactly what keeps the total area correct.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
