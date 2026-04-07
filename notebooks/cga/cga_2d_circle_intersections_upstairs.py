import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Two-Circle Intersections Upstairs

    Two Euclidean circles meet in zero, one, or two points. Upstairs, their two
    slicing planes meet the paraboloid in exactly the same shared lifted points.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each circle becomes a plane slice of the paraboloid:

    $$
    z = c_x x + c_y y + \frac12(r^2-c_x^2-c_y^2).
    $$

    So circle-circle intersections become points that lie on:

    - the paraboloid
    - the first circle plane
    - the second circle plane
    """)
    return


@app.cell
def _(mo):
    c2x = mo.ui.slider(0.3, 2.0, step=0.05, value=1.1, label="circle 2 centre along e1", show_value=True)
    c2y = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.35, label="circle 2 centre along e2", show_value=True)
    r1 = mo.ui.slider(0.3, 1.5, step=0.05, value=0.9, label="circle 1 radius", show_value=True)
    r2 = mo.ui.slider(0.3, 1.5, step=0.05, value=0.95, label="circle 2 radius", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return c2x, c2y, r1, r2, view_yaw


@app.cell
def _(c2x, c2y, circle_intersections_plot, gm, mo, r1, r2, view_yaw):
    d = float((c2x.value**2 + c2y.value**2) ** 0.5)
    if d < 1e-8:
        status = "concentric"
        y_sq = None
    else:
        x = (d**2 + r1.value**2 - r2.value**2) / (2 * d)
        y_sq = r1.value**2 - x**2
        if y_sq > 1e-8:
            status = "two intersections"
        elif abs(y_sq) <= 1e-8:
            status = "tangent"
        else:
            status = "no real intersections"

    y_sq_text = "undefined" if y_sq is None else f"{y_sq:.4f}"
    _md = rf"""
    Circle 1:

    $$
    x^2 + y^2 = {r1.value:.2f}^2
    $$

    Circle 2:

    $$
    (x-{c2x.value:.2f})^2 + (y-{c2y.value:.2f})^2 = {r2.value:.2f}^2
    $$

    Shared-point test:

    $$
    y^2 = {y_sq_text}
    $$

    Status: **{status}**
    """

    mo.vstack([c2x, c2y, r1, r2, gm.md(_md), circle_intersections_plot(c2x.value, c2y.value, r1.value, r2.value, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def circle_intersections_plot(c2x, c2y, r1, r2, view_yaw_deg):
        c1 = np.array([0.0, 0.0], dtype=float)
        c2 = np.array([c2x, c2y], dtype=float)
        t = np.linspace(0, 2 * np.pi, 240)

        fig = plt.figure(figsize=(11.8, 5.3))
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122, projection="3d")

        x1 = r1 * np.cos(t)
        y1 = r1 * np.sin(t)
        x2 = c2x + r2 * np.cos(t)
        y2 = c2y + r2 * np.sin(t)
        z1 = 0.5 * (x1**2 + y1**2)
        z2 = 0.5 * (x2**2 + y2**2)

        ax0.plot(x1, y1, color="#2563eb", lw=2.2)
        ax0.plot(x2, y2, color="#d62828", lw=2.2)
        ax0.scatter([0, c2x], [0, c2y], color=["#2563eb", "#d62828"], s=40)

        d = float(np.linalg.norm(c2))
        points = []
        if d > 1e-8:
            ex = c2 / d
            ey = np.array([-ex[1], ex[0]])
            x = (d**2 + r1**2 - r2**2) / (2 * d)
            y_sq = r1**2 - x**2
            if y_sq >= -1e-8:
                y = np.sqrt(max(y_sq, 0.0))
                points = [x * ex + y * ey] if y < 1e-6 else [x * ex + y * ey, x * ex - y * ey]
                ax0.scatter([p[0] for p in points], [p[1] for p in points], color="#111111", s=42, zorder=5)

        ax0.set_xlim(-1.9, 2.2)
        ax0.set_ylim(-1.9, 1.9)
        ax0.set_aspect("equal")
        ax0.grid(True, alpha=0.18)
        ax0.set_xlabel(r"$\mathbf{e_1}$")
        ax0.set_ylabel(r"$\mathbf{e_2}$")
        ax0.set_title("Two circles in the plane")

        grid_x = np.linspace(-1.8, 2.1, 90)
        grid_y = np.linspace(-1.8, 1.8, 90)
        gx, gy = np.meshgrid(grid_x, grid_y)
        gz = 0.5 * (gx**2 + gy**2)
        plane1 = 0.5 * (r1**2)
        plane2 = c2x * gx + c2y * gy + 0.5 * (r2**2 - c2x**2 - c2y**2)

        ax1.plot_surface(gx, gy, gz, color="#ddd6fe", alpha=0.22, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, np.full_like(gx, plane1), color="#bfdbfe", alpha=0.16, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, plane2, color="#fecaca", alpha=0.16, linewidth=0, shade=False)
        ax1.plot(x1, y1, z1, color="#2563eb", lw=2.2)
        ax1.plot(x2, y2, z2, color="#d62828", lw=2.2)
        for p in points:
            pz = 0.5 * float(np.dot(p, p))
            ax1.scatter([p[0]], [p[1]], [pz], color="#111111", s=44)

        ax1.set_xlim(-1.9, 2.1)
        ax1.set_ylim(-1.9, 1.9)
        ax1.set_zlim(-1.0, 3.6)
        ax1.set_box_aspect((1.1, 1.0, 0.85))
        ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        ax1.set_xlabel(r"$\mathbf{e_1}$")
        ax1.set_ylabel(r"$\mathbf{e_2}$")
        ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        ax1.set_title("Shared lifted points on two slice planes")

        plt.close(fig)
        return fig

    return (circle_intersections_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
