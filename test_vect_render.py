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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Vector Rendering Test

    This is a small rendering notebook for a single `Cl(3,0)` vector.

    The main vector is shown in 3D, and its shadows are also drawn onto the three background coordinate walls:

    - the `xy` wall
    - the `xz` wall
    - the `yz` wall

    The goal is just to make the 3D position easier to read by eye.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean algebra $\mathrm{Cl}(3,0)$ with basis vectors $e_1, e_2, e_3$.

    The sliders control spherical-style angles:

    - azimuth: turn around the vertical axis
    - elevation: tip up and down from the `xy` plane
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(mo):
    azimuth = mo.ui.slider(0, 360, step=1, value=35, label="Azimuth", show_value=True)
    elevation = mo.ui.slider(-90, 90, step=1, value=25, label="Elevation", show_value=True)
    return azimuth, elevation


@app.cell
def _(azimuth, draw_vector_walls, e1, e2, e3, elevation, gm, mo, np):
    _az = np.radians(azimuth.value)
    _el = np.radians(elevation.value)

    _x = np.cos(_el) * np.cos(_az)
    _y = np.cos(_el) * np.sin(_az)
    _z = np.sin(_el)

    v = (_x * e1 + _y * e2 + _z * e3).name(latex=r"v")

    _md = t"""
    {v.display()} <br/>
    Cartesian coordinates: $({_x:.3f}, {_y:.3f}, {_z:.3f})$
    """

    mo.vstack([azimuth, elevation, gm.md(_md), draw_vector_walls(v)])
    return (v,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A second render draws the actual projected arrows on the three walls, not just the dropped shadow points. This is a more literal “flatten the vector onto each wall” view.
    """)
    return


@app.cell
def _(azimuth, draw_vector_wall_arrows, elevation, mo, v):
    mo.vstack([azimuth, elevation,draw_vector_wall_arrows(v)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A third vector render keeps the same vector, but drops the component lines to the central coordinate axes instead of the walls.
    """)
    return


@app.cell
def _(mo):
    show_axis_dots = mo.ui.checkbox(value=True, label="Show axis dots")
    show_axis_lines = mo.ui.checkbox(value=True, label="Show axis projection lines")
    show_wall_projections = mo.ui.checkbox(value=False, label="Show wall-projected arrows")
    return show_axis_dots, show_axis_lines, show_wall_projections


@app.cell
def _(
    azimuth,
    draw_vector_axis_projections,
    elevation,
    mo,
    show_axis_dots,
    show_axis_lines,
    show_wall_projections,
    v,
):
    mo.vstack([azimuth, elevation, show_axis_dots, show_axis_lines, show_wall_projections, draw_vector_axis_projections(v, show_axis_dots.value, show_axis_lines.value, show_wall_projections.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A third render treats the controlled direction as a plane normal instead. The plane itself is drawn as a disk patch, and its projected shadow is drawn onto each wall. If the plane is perpendicular to a wall, that shadow collapses to a line.
    """)
    return


@app.cell
def _(mo):
    plane_azimuth = mo.ui.slider(0, 360, step=1, value=35, label="Plane azimuth", show_value=True)
    plane_elevation = mo.ui.slider(-90, 90, step=1, value=25, label="Plane elevation", show_value=True)
    show_plane_guides = mo.ui.checkbox(value=True, label="Show in-plane guide diameters")
    show_positive_normal = mo.ui.checkbox(value=True, label="Show positive normal")
    return (
        plane_azimuth,
        plane_elevation,
        show_plane_guides,
        show_positive_normal,
    )


@app.cell
def _(
    draw_plane_wall_shadows,
    e1,
    e2,
    e3,
    gm,
    mo,
    np,
    plane_azimuth,
    plane_elevation,
    show_plane_guides,
    show_positive_normal,
):
    _az = np.radians(plane_azimuth.value)
    _el = np.radians(plane_elevation.value)

    _nx = np.cos(_el) * np.cos(_az)
    _ny = np.cos(_el) * np.sin(_az)
    _nz = np.sin(_el)

    n = (_nx * e1 + _ny * e2 + _nz * e3).eval().name(latex=r"n")

    _md = t"""
    {n.display()} <br/>
    Plane normal coordinates: $({_nx:.3f}, {_ny:.3f}, {_nz:.3f})$
    """

    mo.vstack([plane_azimuth, plane_elevation, show_plane_guides, show_positive_normal, gm.md(_md), draw_plane_wall_shadows(n, show_plane_guides.value)])
    return (n,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A fourth render rebuilds the plane from scratch using the tangent directions of the spherical parameterization itself. This gives the patch a control-aligned in-plane orientation, which may match intuition better as you move the azimuth and elevation sliders.
    """)
    return


@app.cell
def _(
    draw_plane_wall_shadows_tangent,
    mo,
    n,
    plane_azimuth,
    plane_elevation,
    show_plane_guides,
    show_positive_normal,
):
    mo.vstack([plane_azimuth, plane_elevation, show_plane_guides, show_positive_normal, draw_plane_wall_shadows_tangent(n, plane_azimuth.value, plane_elevation.value, show_plane_guides.value, show_positive_normal.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_vector_walls(v):
        _vec = np.array(v.eval().vector_part[:3], dtype=float)
        _x, _y, _z = _vec

        _bound = 1.1

        def _style_grid(_ax):
            _ax.grid(True)
            _ticks = np.arange(-1.0, 1.01, 0.25)
            _ax.set_xticks(_ticks)
            _ax.set_yticks(_ticks)
            _ax.set_zticks(_ticks)
            for _axis in (_ax.xaxis, _ax.yaxis, _ax.zaxis):
                _axis._axinfo["grid"]["color"] = (0.2, 0.2, 0.2, 0.08)
                _axis._axinfo["grid"]["linewidth"] = 0.6
                _axis._axinfo["grid"]["linestyle"] = "-"

        _fig = plt.figure(figsize=(8.0, 7.0))
        _ax = _fig.add_subplot(111, projection="3d")

        _s = np.linspace(-_bound, _bound, 2)
        _u, _w = np.meshgrid(_s, _s)

        _ax.plot_surface(_u, _w, -_bound * np.ones_like(_u), color="#dbeafe", alpha=0.12, shade=False)
        _ax.plot_surface(_u, _bound * np.ones_like(_u), _w, color="#dcfce7", alpha=0.12, shade=False)
        _ax.plot_surface(-_bound * np.ones_like(_u), _u, _w, color="#fee2e2", alpha=0.12, shade=False)

        _ax.quiver(0, 0, 0, _x, _y, _z, color="#7c3aed", linewidth=3.0, arrow_length_ratio=0.08)

        _ax.plot([_x, _x], [_y, _y], [-_bound, _z], color="#2563eb", alpha=0.55, linewidth=2.0)
        _ax.plot([_x, _x], [_bound, _y], [_z, _z], color="#16a34a", alpha=0.55, linewidth=2.0)
        _ax.plot([-_bound, _x], [_y, _y], [_z, _z], color="#dc2626", alpha=0.55, linewidth=2.0)

        _ax.scatter([_x], [_y], [-_bound], color="#2563eb", s=30, alpha=0.8)
        _ax.scatter([_x], [_bound], [_z], color="#16a34a", s=30, alpha=0.8)
        _ax.scatter([-_bound], [_y], [_z], color="#dc2626", s=30, alpha=0.8)

        _ax.text(_x, _y, _z, r"$v$", color="#7c3aed")
        _ax.text(_x, _y, -_bound - 0.08, r"$xy$", color="#2563eb")
        _ax.text(_x, _bound + 0.08, _z, r"$xz$", color="#16a34a")
        _ax.text(-_bound - 0.08, _y, _z, r"$yz$", color="#dc2626")

        _ax.set_xlim(-_bound, _bound)
        _ax.set_ylim(-_bound, _bound)
        _ax.set_zlim(-_bound, _bound)
        _ax.set_box_aspect((1, 1, 1))
        _style_grid(_ax)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Vector with projections onto the three coordinate walls")
        plt.close(_fig)
        return _fig

    def draw_vector_wall_arrows(v):
        _vec = np.array(v.eval().vector_part[:3], dtype=float)
        _x, _y, _z = _vec

        _bound = 1.1
        _purple = "#7c3aed"
        _tick_color = "#333333"

        def _style_grid(_ax):
            _ax.grid(True)
            _ticks = np.arange(-1.0, 1.01, 0.25)
            _ax.set_xticks(_ticks)
            _ax.set_yticks(_ticks)
            _ax.set_zticks(_ticks)
            for _axis in (_ax.xaxis, _ax.yaxis, _ax.zaxis):
                _axis._axinfo["grid"]["color"] = (0.2, 0.2, 0.2, 0.08)
                _axis._axinfo["grid"]["linewidth"] = 0.6
                _axis._axinfo["grid"]["linestyle"] = "-"

        _fig = plt.figure(figsize=(8.0, 7.0))
        _ax = _fig.add_subplot(111, projection="3d")

        _s = np.linspace(-_bound, _bound, 2)
        _u, _w = np.meshgrid(_s, _s)

        _ax.plot_surface(_u, _w, -_bound * np.ones_like(_u), color="#dbeafe", alpha=0.10, shade=False)
        _ax.plot_surface(_u, _bound * np.ones_like(_u), _w, color="#dcfce7", alpha=0.10, shade=False)
        _ax.plot_surface(-_bound * np.ones_like(_u), _u, _w, color="#fee2e2", alpha=0.10, shade=False)

        _ax.plot([-_bound, _bound], [0, 0], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [-_bound, _bound], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [0, 0], [-_bound, _bound], color=_tick_color, alpha=0.75, linewidth=1.3)

        _tick_positions = np.arange(-1.0, 1.01, 0.25)
        _tick_half = 0.03
        for _t in _tick_positions:
            if abs(_t) < 1e-9:
                continue
            _ax.plot([_t, _t], [-_tick_half, _tick_half], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [_t, _t], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [0, 0], [_t, _t], color=_tick_color, alpha=0.75, linewidth=1.0)

        _ax.quiver(0, 0, 0, _x, _y, _z, color=_purple, linewidth=3.0, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, -_bound, _x, _y, 0.0, color=_purple, linewidth=2.4, arrow_length_ratio=0.10, alpha=0.35)
        _ax.quiver(0, _bound, 0, _x, 0.0, _z, color=_purple, linewidth=2.4, arrow_length_ratio=0.10, alpha=0.35)
        _ax.quiver(-_bound, 0, 0, 0.0, _y, _z, color=_purple, linewidth=2.4, arrow_length_ratio=0.10, alpha=0.35)

        _ax.set_xlim(-_bound, _bound)
        _ax.set_ylim(-_bound, _bound)
        _ax.set_zlim(-_bound, _bound)
        _ax.set_box_aspect((1, 1, 1))
        _style_grid(_ax)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Vector with actual projected arrows on the three walls")
        plt.close(_fig)
        return _fig

    def draw_vector_axis_projections(v, show_axis_dots, show_axis_lines, show_wall_projections):
        _vec = np.array(v.eval().vector_part[:3], dtype=float)
        _x, _y, _z = _vec

        _bound = 1.1
        _purple = "#7c3aed"
        _tick_color = "#333333"

        def _style_grid(_ax):
            _ax.grid(True)
            _ticks = np.arange(-1.0, 1.01, 0.25)
            _ax.set_xticks(_ticks)
            _ax.set_yticks(_ticks)
            _ax.set_zticks(_ticks)
            for _axis in (_ax.xaxis, _ax.yaxis, _ax.zaxis):
                _axis._axinfo["grid"]["color"] = (0.2, 0.2, 0.2, 0.08)
                _axis._axinfo["grid"]["linewidth"] = 0.6
                _axis._axinfo["grid"]["linestyle"] = "-"

        _fig = plt.figure(figsize=(8.0, 7.0))
        _ax = _fig.add_subplot(111, projection="3d")

        _s = np.linspace(-_bound, _bound, 2)
        _u, _w = np.meshgrid(_s, _s)

        _ax.plot_surface(_u, _w, -_bound * np.ones_like(_u), color="#dbeafe", alpha=0.08, shade=False)
        _ax.plot_surface(_u, _bound * np.ones_like(_u), _w, color="#dcfce7", alpha=0.08, shade=False)
        _ax.plot_surface(-_bound * np.ones_like(_u), _u, _w, color="#fee2e2", alpha=0.08, shade=False)

        _ax.plot([-_bound, _bound], [0, 0], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [-_bound, _bound], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [0, 0], [-_bound, _bound], color=_tick_color, alpha=0.75, linewidth=1.3)

        _tick_positions = np.arange(-1.0, 1.01, 0.25)
        _tick_half = 0.03
        for _t in _tick_positions:
            if abs(_t) < 1e-9:
                continue
            _ax.plot([_t, _t], [-_tick_half, _tick_half], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [_t, _t], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [0, 0], [_t, _t], color=_tick_color, alpha=0.75, linewidth=1.0)

        _ax.quiver(0, 0, 0, _x, _y, _z, color=_purple, linewidth=3.0, arrow_length_ratio=0.08)

        if show_axis_lines:
            _ax.plot([_x, _x], [_y, _y], [_z, 0], color=_purple, alpha=0.35, linewidth=2.0)
            _ax.plot([_x, _x], [_y, 0], [0, 0], color=_purple, alpha=0.35, linewidth=2.0)
            _ax.plot([_x, 0], [_y, _y], [0, 0], color=_purple, alpha=0.35, linewidth=2.0)

        if show_wall_projections:
            _ax.quiver(0, 0, -_bound, _x, _y, 0.0, color=_purple, linewidth=2.2, arrow_length_ratio=0.10, alpha=0.22)
            _ax.quiver(0, _bound, 0, _x, 0.0, _z, color=_purple, linewidth=2.2, arrow_length_ratio=0.10, alpha=0.22)
            _ax.quiver(-_bound, 0, 0, 0.0, _y, _z, color=_purple, linewidth=2.2, arrow_length_ratio=0.10, alpha=0.22)

        if show_axis_dots:
            _ax.scatter([_x], [0], [0], color=_purple, s=24, alpha=0.45)
            _ax.scatter([0], [_y], [0], color=_purple, s=24, alpha=0.45)
            _ax.scatter([0], [0], [_z], color=_purple, s=24, alpha=0.45)

        _ax.set_xlim(-_bound, _bound)
        _ax.set_ylim(-_bound, _bound)
        _ax.set_zlim(-_bound, _bound)
        _ax.set_box_aspect((1, 1, 1))
        _style_grid(_ax)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Vector with component lines dropped to the central axes")
        plt.close(_fig)
        return _fig

    def draw_plane_wall_shadows(n, show_guides):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        _normal = np.array(n.eval().vector_part[:3], dtype=float)
        _norm = np.linalg.norm(_normal)
        if _norm < 1e-9:
            _normal = np.array([0.0, 0.0, 1.0])
        else:
            _normal = _normal / _norm

        _bound = 1.1
        _purple = "#7c3aed"
        _tick_color = "#333333"

        def _style_grid(_ax):
            _ax.grid(True)
            _ticks = np.arange(-1.0, 1.01, 0.25)
            _ax.set_xticks(_ticks)
            _ax.set_yticks(_ticks)
            _ax.set_zticks(_ticks)
            for _axis in (_ax.xaxis, _ax.yaxis, _ax.zaxis):
                _axis._axinfo["grid"]["color"] = (0.2, 0.2, 0.2, 0.08)
                _axis._axinfo["grid"]["linewidth"] = 0.6
                _axis._axinfo["grid"]["linestyle"] = "-"

        def _disk_frame_from_normal(_normal_vec):
            _nx, _ny, _nz = _normal_vec
            if _nz < -0.999999:
                _u = np.array([0.0, -1.0, 0.0])
                _v = np.array([-1.0, 0.0, 0.0])
            else:
                _a = 1.0 / (1.0 + _nz)
                _b = -_nx * _ny * _a
                _u = np.array([1.0 - _nx * _nx * _a, _b, -_nx])
                _v = np.array([_b, 1.0 - _ny * _ny * _a, -_ny])

            _u = _u / np.linalg.norm(_u)
            _v = _v / np.linalg.norm(_v)
            return _u, _v

        def _guide_frame_from_tangent_convention(_normal_vec):
            _az = np.arctan2(_normal_vec[1], _normal_vec[0])
            _xy_norm = np.hypot(_normal_vec[0], _normal_vec[1])

            if _xy_norm < 1e-8:
                _guide_u = np.array([0.0, 1.0, 0.0])
            else:
                _guide_u = np.array([-np.sin(_az), np.cos(_az), 0.0], dtype=float)
                _guide_u = _guide_u / np.linalg.norm(_guide_u)

            _guide_v = np.cross(_normal_vec, _guide_u)
            _guide_v = _guide_v / np.linalg.norm(_guide_v)
            return _guide_u, _guide_v

        def _disk_points_from_frame(_u, _v, _radius=0.62, _num=120):
            _angles = np.linspace(0, 2 * np.pi, _num, endpoint=False)
            return np.array([_radius * (np.cos(_a) * _u + np.sin(_a) * _v) for _a in _angles])

        def _project_points(_points, _wall):
            _proj = _points.copy()
            if _wall == "xy":
                _proj[:, 2] = -_bound
            elif _wall == "xz":
                _proj[:, 1] = _bound
            elif _wall == "yz":
                _proj[:, 0] = -_bound
            return _proj

        def _draw_shadow(_ax, _points, _wall, _alpha):
            _proj = _project_points(_points, _wall)

            if _wall == "xy":
                _pts2 = _proj[:, :2]
            elif _wall == "xz":
                _pts2 = _proj[:, [0, 2]]
            else:
                _pts2 = _proj[:, 1:]

            _centered = _pts2 - _pts2.mean(axis=0)
            _rank = np.linalg.matrix_rank(_centered, tol=1e-8)

            if _rank <= 1:
                _spread = np.sum(_centered**2, axis=1)
                _i0 = int(np.argmin(_spread))
                _direction = _centered[np.argmax(_spread)]
                _direction_norm = np.linalg.norm(_direction)
                if _direction_norm < 1e-9:
                    return
                _direction = _direction / _direction_norm
                _scores = _centered @ _direction
                _p0 = _proj[np.argmin(_scores)]
                _p1 = _proj[np.argmax(_scores)]
                _ax.plot(
                    [_p0[0], _p1[0]],
                    [_p0[1], _p1[1]],
                    [_p0[2], _p1[2]],
                    color=_purple,
                    alpha=_alpha,
                    linewidth=2.2,
                )
            else:
                _ax.add_collection3d(
                    Poly3DCollection(
                        [_proj],
                        facecolors=_purple,
                        edgecolors="none",
                        alpha=_alpha,
                    )
                )

        _u_vec, _v_vec = _disk_frame_from_normal(_normal)
        _guide_u, _guide_v = _guide_frame_from_tangent_convention(_normal)
        _disk_points = _disk_points_from_frame(_u_vec, _v_vec)

        _fig = plt.figure(figsize=(8.2, 7.2))
        _ax = _fig.add_subplot(111, projection="3d")

        _s = np.linspace(-_bound, _bound, 2)
        _u, _w = np.meshgrid(_s, _s)

        _ax.plot_surface(_u, _w, -_bound * np.ones_like(_u), color="#dbeafe", alpha=0.10, shade=False)
        _ax.plot_surface(_u, _bound * np.ones_like(_u), _w, color="#dcfce7", alpha=0.10, shade=False)
        _ax.plot_surface(-_bound * np.ones_like(_u), _u, _w, color="#fee2e2", alpha=0.10, shade=False)

        _ax.plot([-_bound, _bound], [0, 0], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [-_bound, _bound], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [0, 0], [-_bound, _bound], color=_tick_color, alpha=0.75, linewidth=1.3)

        _tick_positions = np.arange(-1.0, 1.01, 0.25)
        _tick_half = 0.03
        for _t in _tick_positions:
            if abs(_t) < 1e-9:
                continue
            _ax.plot([_t, _t], [-_tick_half, _tick_half], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [_t, _t], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [0, 0], [_t, _t], color=_tick_color, alpha=0.75, linewidth=1.0)

        _ax.add_collection3d(
            Poly3DCollection(
                [_disk_points],
                facecolors=_purple,
                edgecolors="none",
                alpha=0.28,
            )
        )
        _ax.plot(_disk_points[:, 0], _disk_points[:, 1], _disk_points[:, 2], color=_purple, alpha=0.55, linewidth=1.2)

        if show_guides:
            _radius = 0.62
            _guide_1 = np.vstack([-_radius * _guide_u, _radius * _guide_u])
            _guide_2 = np.vstack([-_radius * _guide_v, _radius * _guide_v])
            _ax.plot(_guide_1[:, 0], _guide_1[:, 1], _guide_1[:, 2], color=_purple, alpha=0.42, linewidth=1.4)
            _ax.plot(_guide_2[:, 0], _guide_2[:, 1], _guide_2[:, 2], color=_purple, alpha=0.42, linewidth=1.4)

        _draw_shadow(_ax, _disk_points, "xy", 0.10)
        _draw_shadow(_ax, _disk_points, "xz", 0.10)
        _draw_shadow(_ax, _disk_points, "yz", 0.10)

        _ax.quiver(0, 0, 0, 0.25 * _normal[0], 0.25 * _normal[1], 0.25 * _normal[2], color=_purple, linewidth=2.6, arrow_length_ratio=0.16, alpha=0.95)

        _ax.set_xlim(-_bound, _bound)
        _ax.set_ylim(-_bound, _bound)
        _ax.set_zlim(-_bound, _bound)
        _ax.set_box_aspect((1, 1, 1))
        _style_grid(_ax)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Plane patch with projected shadows on the three walls")
        plt.close(_fig)
        return _fig

    def draw_plane_wall_shadows_tangent(n, azimuth_deg, elevation_deg, show_guides, show_positive_normal):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        _normal = np.array(n.eval().vector_part[:3], dtype=float)
        _norm = np.linalg.norm(_normal)
        if _norm < 1e-9:
            _normal = np.array([0.0, 0.0, 1.0])
        else:
            _normal = _normal / _norm

        _az = np.radians(azimuth_deg)
        _el = np.radians(elevation_deg)

        _bound = 1.1
        _purple = "#7c3aed"
        _tick_color = "#333333"

        def _style_grid(_ax):
            _ax.grid(True)
            _ticks = np.arange(-1.0, 1.01, 0.25)
            _ax.set_xticks(_ticks)
            _ax.set_yticks(_ticks)
            _ax.set_zticks(_ticks)
            for _axis in (_ax.xaxis, _ax.yaxis, _ax.zaxis):
                _axis._axinfo["grid"]["color"] = (0.2, 0.2, 0.2, 0.08)
                _axis._axinfo["grid"]["linewidth"] = 0.6
                _axis._axinfo["grid"]["linestyle"] = "-"

        def _polygon_points(_u_vec, _v_vec, _half_u=0.72, _half_v=0.48):
            return np.array(
                [
                    -_half_u * _u_vec - _half_v * _v_vec,
                    _half_u * _u_vec - _half_v * _v_vec,
                    _half_u * _u_vec + _half_v * _v_vec,
                    -_half_u * _u_vec + _half_v * _v_vec,
                ]
            )

        def _project_points(_points, _wall):
            _proj = _points.copy()
            if _wall == "xy":
                _proj[:, 2] = -_bound
            elif _wall == "xz":
                _proj[:, 1] = _bound
            elif _wall == "yz":
                _proj[:, 0] = -_bound
            return _proj

        def _draw_shadow(_ax, _points, _wall, _alpha):
            _proj = _project_points(_points, _wall)

            if _wall == "xy":
                _pts2 = _proj[:, :2]
            elif _wall == "xz":
                _pts2 = _proj[:, [0, 2]]
            else:
                _pts2 = _proj[:, 1:]

            _centered = _pts2 - _pts2.mean(axis=0)
            _rank = np.linalg.matrix_rank(_centered, tol=1e-8)

            if _rank <= 1:
                _cov = _centered.T @ _centered
                _eigvals, _eigvecs = np.linalg.eigh(_cov)
                _dir2 = _eigvecs[:, np.argmax(_eigvals)]
                _scores = _centered @ _dir2
                _p0 = _proj[np.argmin(_scores)]
                _p1 = _proj[np.argmax(_scores)]
                _ax.plot(
                    [_p0[0], _p1[0]],
                    [_p0[1], _p1[1]],
                    [_p0[2], _p1[2]],
                    color=_purple,
                    alpha=_alpha,
                    linewidth=2.2,
                )
            else:
                _ax.add_collection3d(
                    Poly3DCollection(
                        [_proj],
                        facecolors=_purple,
                        edgecolors="none",
                        alpha=_alpha,
                    )
                )

        # Tangent frame from the azimuth/elevation parameterization.
        _u_vec = np.array([-np.sin(_az), np.cos(_az), 0.0], dtype=float)
        _u_vec = _u_vec / np.linalg.norm(_u_vec)
        _v_vec = np.cross(_normal, _u_vec)
        _v_vec = _v_vec / np.linalg.norm(_v_vec)

        _plane_poly = _polygon_points(_u_vec, _v_vec)

        _fig = plt.figure(figsize=(8.2, 7.2))
        _ax = _fig.add_subplot(111, projection="3d")

        _s = np.linspace(-_bound, _bound, 2)
        _u_mesh, _w_mesh = np.meshgrid(_s, _s)

        _ax.plot_surface(_u_mesh, _w_mesh, -_bound * np.ones_like(_u_mesh), color="#dbeafe", alpha=0.10, shade=False)
        _ax.plot_surface(_u_mesh, _bound * np.ones_like(_u_mesh), _w_mesh, color="#dcfce7", alpha=0.10, shade=False)
        _ax.plot_surface(-_bound * np.ones_like(_u_mesh), _u_mesh, _w_mesh, color="#fee2e2", alpha=0.10, shade=False)

        _ax.plot([-_bound, _bound], [0, 0], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [-_bound, _bound], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.3)
        _ax.plot([0, 0], [0, 0], [-_bound, _bound], color=_tick_color, alpha=0.75, linewidth=1.3)

        _tick_positions = np.arange(-1.0, 1.01, 0.25)
        _tick_half = 0.03
        for _t in _tick_positions:
            if abs(_t) < 1e-9:
                continue
            _ax.plot([_t, _t], [-_tick_half, _tick_half], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [_t, _t], [0, 0], color=_tick_color, alpha=0.75, linewidth=1.0)
            _ax.plot([-_tick_half, _tick_half], [0, 0], [_t, _t], color=_tick_color, alpha=0.75, linewidth=1.0)

        _ax.add_collection3d(
            Poly3DCollection(
                [_plane_poly],
                facecolors=_purple,
                edgecolors="none",
                alpha=0.24,
            )
        )
        _outline = np.vstack([_plane_poly, _plane_poly[:1]])
        _ax.plot(_outline[:, 0], _outline[:, 1], _outline[:, 2], color=_purple, alpha=0.58, linewidth=1.3)

        if show_guides:
            _guide_1 = np.vstack([-0.72 * _u_vec, 0.72 * _u_vec])
            _guide_2 = np.vstack([-0.48 * _v_vec, 0.48 * _v_vec])
            _ax.plot(_guide_1[:, 0], _guide_1[:, 1], _guide_1[:, 2], color=_purple, alpha=0.42, linewidth=1.4)
            _ax.plot(_guide_2[:, 0], _guide_2[:, 1], _guide_2[:, 2], color=_purple, alpha=0.42, linewidth=1.4)

        _draw_shadow(_ax, _plane_poly, "xy", 0.10)
        _draw_shadow(_ax, _plane_poly, "xz", 0.10)
        _draw_shadow(_ax, _plane_poly, "yz", 0.10)

        if show_positive_normal:
            _ax.quiver(0, 0, 0, 0.25 * _normal[0], 0.25 * _normal[1], 0.25 * _normal[2], color=_purple, linewidth=2.6, arrow_length_ratio=0.16, alpha=0.95)

        _ax.set_xlim(-_bound, _bound)
        _ax.set_ylim(-_bound, _bound)
        _ax.set_zlim(-_bound, _bound)
        _ax.set_box_aspect((1, 1, 1))
        _style_grid(_ax)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Plane polygon from tangent-frame construction")
        plt.close(_fig)
        return _fig

    return (
        draw_plane_wall_shadows,
        draw_plane_wall_shadows_tangent,
        draw_vector_axis_projections,
        draw_vector_wall_arrows,
        draw_vector_walls,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
