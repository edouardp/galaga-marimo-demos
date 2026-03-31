import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, dual, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    return Algebra, Poly3DCollection, dual, gm, mo, np, plt, unit


@app.cell
def _(Poly3DCollection, np, plt):
    def draw_line_triangle(A, B, C, origin, direction, hit, hit_inside):
        _A = A.vector_part[:3]
        _B = B.vector_part[:3]
        _C = C.vector_part[:3]
        _origin = origin.vector_part[:3]
        _direction = direction.vector_part[:3]
        _hit = hit.vector_part[:3]

        _fig = plt.figure(figsize=(7.2, 6.0))
        _ax = _fig.add_subplot(111, projection="3d")

        _tri = Poly3DCollection([[list(_A), list(_B), list(_C)]], alpha=0.28, facecolor="goldenrod", edgecolor="black")
        _ax.add_collection3d(_tri)

        _ray_len = 2.8
        _ray_end = _origin + _ray_len * _direction
        _ax.plot([_origin[0], _ray_end[0]], [_origin[1], _ray_end[1]], [_origin[2], _ray_end[2]], color="crimson", linewidth=2.5)
        _ax.scatter([_origin[0]], [_origin[1]], [_origin[2]], color="crimson", s=50)

        _color = "darkgreen" if hit_inside else "gray"
        _ax.scatter([_hit[0]], [_hit[1]], [_hit[2]], color=_color, s=60)
        _ax.text(_hit[0] + 0.05, _hit[1] + 0.05, _hit[2] + 0.05, "hit", color=_color)

        for _label, _pt in zip(["A", "B", "C"], [_A, _B, _C]):
            _ax.scatter([_pt[0]], [_pt[1]], [_pt[2]], color="black", s=35)
            _ax.text(_pt[0] + 0.05, _pt[1] + 0.05, _pt[2] + 0.05, _label)

        _all_pts = np.vstack([_A, _B, _C, _origin, _ray_end, _hit])
        _mins = _all_pts.min(axis=0) - 0.3
        _maxs = _all_pts.max(axis=0) + 0.3
        _ax.set_xlim(_mins[0], _maxs[0])
        _ax.set_ylim(_mins[1], _maxs[1])
        _ax.set_zlim(min(-0.2, _mins[2]), max(1.8, _maxs[2]))
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Ray-triangle intersection in Cl(3,0)")
        plt.close(_fig)
        return _fig

    return (draw_line_triangle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Line-Triangle Intersection

    A ray-triangle intersection can be built from ordinary Euclidean GA objects in $\mathrm{Cl}(3,0)$. The line meets the triangle's plane first; then the same plane bivector gives an oriented-area test for whether the hit point lies inside the triangle.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    The triangle determines a plane bivector

    $$
    B_\triangle = (B - A) \wedge (C - A),
    $$

    and its dual gives the plane normal. A ray

    $$
    x(t) = O + t d
    $$

    meets the plane where that normal equation is satisfied.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Constrained Setup

    The triangle is fixed and the controls are intentionally narrow, so most slider choices still aim near or through the triangle. That keeps the geometry legible while still allowing misses near the boundary.
    """)
    return


@app.cell
def _(mo):
    origin_x = mo.ui.slider(-0.4, 0.7, step=0.05, value=0.1, label="Origin x", show_value=True)
    origin_y = mo.ui.slider(-0.5, 0.6, step=0.05, value=0.0, label="Origin y", show_value=True)
    aim_x = mo.ui.slider(-0.9, 0.9, step=0.05, value=0.1, label="Aim x on z=0", show_value=True)
    aim_y = mo.ui.slider(-0.7, 1.0, step=0.05, value=0.1, label="Aim y on z=0", show_value=True)
    return aim_x, aim_y, origin_x, origin_y


@app.cell
def _(
    aim_x,
    aim_y,
    draw_line_triangle,
    dual,
    e1,
    e2,
    e3,
    gm,
    mo,
    np,
    origin_x,
    origin_y,
    unit,
):
    _A = (-1.0 * e1 - 0.8 * e2).name("A")
    _B = (1.2 * e1 - 0.4 * e2).name("B")
    _C = (-0.2 * e1 + 1.1 * e2).name("C")

    _origin = (origin_x.value * e1 + origin_y.value * e2 + 1.6 * e3).name("O")
    _aim_point = (aim_x.value * e1 + aim_y.value * e2).name("P_{aim}")
    _direction = unit((_aim_point - _origin)).name("d")

    _triangle_plane = ((_B - _A) ^ (_C - _A)).name(latex=r"B_\triangle")
    _normal = dual(_triangle_plane).name("n")

    _denom = (_direction | _normal).scalar_part
    _numer = ((_A - _origin) | _normal).scalar_part
    _t_value = _numer / _denom if abs(_denom) > 1e-9 else np.nan
    _hit = (_origin + _t_value * _direction).name("H")

    _area_total = (_triangle_plane | _triangle_plane).scalar_part
    _alpha = (((_B - _hit) ^ (_C - _hit)) | _triangle_plane).scalar_part / _area_total
    _beta = (((_C - _hit) ^ (_A - _hit)) | _triangle_plane).scalar_part / _area_total
    _gamma = (((_A - _hit) ^ (_B - _hit)) | _triangle_plane).scalar_part / _area_total
    _inside = bool(
        np.isfinite(_t_value)
        and _t_value >= 0.0
        and _alpha >= -1e-9
        and _beta >= -1e-9
        and _gamma >= -1e-9
    )
    _status = "inside triangle" if _inside else "outside triangle"

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_C.display()} <br/>
    {_origin.display()} <br/>
    {_direction.display()} <br/>
    {_triangle_plane.display()} <br/>
    {_normal.display()} <br/>
    Ray parameter: $t = {_t_value:.3f}$ <br/>
    {_hit.display()} <br/>
    Oriented-area barycentric weights: $({ _alpha:.3f}, { _beta:.3f}, { _gamma:.3f})$ <br/>
    Classification: **{_status}**
    """

    mo.vstack(
        [
            origin_x,
            origin_y,
            aim_x,
            aim_y,
            gm.md(_md),
            draw_line_triangle(_A, _B, _C, _origin, _direction, _hit, _inside),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Nothing projective was needed here. In $\mathrm{Cl}(3,0)$, the triangle plane, the ray direction, and the oriented sub-areas already give a clean intersection test. PGA would make incidence more primary, but Euclidean GA is enough for the core computation.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
