import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA Power of a Point

    For a Euclidean circle, the power of a point tells you whether the point is
    inside, on, or outside the circle. Upstairs, the same quantity becomes the
    vertical gap between the lifted paraboloid and the circle's slicing plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the circle

    $$
    (x-c_x)^2 + (y-c_y)^2 = r^2,
    $$

    the power at a probe point $p$ is

    $$
    P(p) = (p-c)^2 - r^2.
    $$

    After writing the paraboloid as $z=\tfrac12(x^2+y^2)$, the circle becomes a
    plane upstairs, and $P(p)$ is proportional to the signed vertical gap between
    the lifted point and that plane.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    cx = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.2, label="centre along e1", show_value=True)
    cy = mo.ui.slider(-1.2, 1.2, step=0.05, value=-0.15, label="centre along e2", show_value=True)
    radius = mo.ui.slider(0.2, 1.5, step=0.05, value=0.9, label="radius", show_value=True)
    px = mo.ui.slider(-1.8, 1.8, step=0.05, value=1.1, label="probe along e1", show_value=True)
    py = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.55, label="probe along e2", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return cx, cy, px, py, radius, view_yaw


@app.cell
def _(
    alg,
    cx,
    cy,
    e1,
    e2,
    em,
    ep,
    gm,
    mo,
    power_of_point_plot,
    px,
    py,
    radius,
    view_yaw,
):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    c = (cx.value * e1 + cy.value * e2).name(latex="c")
    p = (px.value * e1 + py.value * e2).name(latex="p")
    P = (eo + p + half * (p | p) * einf).name(latex=r"P = \operatorname{up}(p)")

    circle_plane = (c + half * (alg.scalar(radius.value**2) - (c | c)) * einf).name(latex=r"\Pi_C")
    power_mv = (((p - c) | (p - c)) - alg.scalar(radius.value**2)).name(latex=r"\operatorname{pow}_C(p)")

    power = power_mv.scalar_part
    if abs(power) < 1e-8:
        status = "on the circle"
    elif power < 0:
        status = "inside the circle"
    else:
        status = "outside the circle"

    plane_height = cx.value * px.value + cy.value * py.value + 0.5 * (
        radius.value**2 - cx.value**2 - cy.value**2
    )
    paraboloid_height = 0.5 * (px.value**2 + py.value**2)
    gap = paraboloid_height - plane_height

    gap_mv = alg.scalar(2 * gap).name(latex=r"2\,(z_{\mathrm{paraboloid}}-z_{\mathrm{plane}})")

    _md = t"""
    {c.display()} <br/>
    {P.display()} <br/>
    {circle_plane.display()} <br/>
    {power_mv.display()} <br/>
    {gap_mv.display()} <br/>
    Status: **{status}**
    <br/><br/>
    For this circle, the signed upstairs gap is half the Euclidean power.
    """

    mo.vstack(
        [cx, cy, radius, px, py, gm.md(_md), power_of_point_plot(cx.value, cy.value, radius.value, px.value, py.value, view_yaw.value), view_yaw]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def power_of_point_plot(cx, cy, radius, px, py, view_yaw_deg):
        t = np.linspace(0, 2 * np.pi, 240)
        circle_x = cx + radius * np.cos(t)
        circle_y = cy + radius * np.sin(t)
        circle_z = 0.5 * (circle_x**2 + circle_y**2)

        grid = np.linspace(-1.8, 1.8, 90)
        gx, gy = np.meshgrid(grid, grid)
        gz = 0.5 * (gx**2 + gy**2)
        plane_z = cx * gx + cy * gy + 0.5 * (radius**2 - cx**2 - cy**2)

        probe_base_z = 0.0
        probe_lift_z = 0.5 * (px**2 + py**2)
        probe_plane_z = cx * px + cy * py + 0.5 * (radius**2 - cx**2 - cy**2)

        fig = plt.figure(figsize=(11.8, 5.3))
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122, projection="3d")

        ax0.plot(circle_x, circle_y, color="#2563eb", lw=2.2)
        ax0.scatter([cx], [cy], color="#2563eb", s=38)
        ax0.scatter([px], [py], color="#7c3aed", s=50)
        ax0.plot([cx, px], [cy, py], color="#7c3aed", alpha=0.25, lw=1.4)
        ax0.set_xlim(-1.9, 1.9)
        ax0.set_ylim(-1.9, 1.9)
        ax0.set_aspect("equal")
        ax0.grid(True, alpha=0.18)
        ax0.set_xlabel(r"$\mathbf{e_1}$")
        ax0.set_ylabel(r"$\mathbf{e_2}$")
        ax0.set_title("Circle and probe point")

        ax1.plot_surface(gx, gy, gz, color="#ddd6fe", alpha=0.25, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, plane_z, color="#bfdbfe", alpha=0.18, linewidth=0, shade=False)
        ax1.plot(circle_x, circle_y, circle_z, color="#2563eb", lw=2.2)
        ax1.scatter([px], [py], [probe_lift_z], color="#7c3aed", s=54)
        ax1.scatter([px], [py], [probe_plane_z], color="#111111", s=30, alpha=0.75)
        ax1.plot([px, px], [py, py], [probe_plane_z, probe_lift_z], color="#7c3aed", alpha=0.55, lw=2.0)
        ax1.plot([px, px], [py, py], [probe_base_z, probe_lift_z], color="#7c3aed", alpha=0.18, lw=1.2)
        ax1.set_xlim(-1.9, 1.9)
        ax1.set_ylim(-1.9, 1.9)
        ax1.set_zlim(-1.2, 3.3)
        ax1.set_box_aspect((1, 1, 0.85))
        ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        ax1.set_xlabel(r"$\mathbf{e_1}$")
        ax1.set_ylabel(r"$\mathbf{e_2}$")
        ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        ax1.set_title("Lifted point vs circle plane")

        plt.close(fig)
        return fig

    return (power_of_point_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
