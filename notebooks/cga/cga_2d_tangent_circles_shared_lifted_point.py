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
    # Tangent Circles as a Shared Lifted Point

    Two Euclidean circles are tangent when their two intersections collapse to
    one. Upstairs, their two slicing planes still meet the paraboloid, but now
    they share exactly one lifted point.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With one circle centred at the origin and a second on the $e_1$ axis, outer
    tangency happens when the centre spacing equals the sum of the radii:

    $$
    d = r_1 + r_2.
    $$

    For $d < r_1+r_2$ the circles intersect twice. At $d = r_1+r_2$ those two
    points merge into one touching point.
    """)
    return


@app.cell
def _(mo):
    r1 = mo.ui.slider(0.3, 1.4, step=0.05, value=0.8, label="circle 1 radius", show_value=True)
    r2 = mo.ui.slider(0.3, 1.4, step=0.05, value=0.55, label="circle 2 radius", show_value=True)
    offset = mo.ui.slider(-0.6, 0.6, step=0.01, value=0.0, label="distance offset", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return offset, r1, r2, view_yaw


@app.cell
def _(gm, mo, offset, r1, r2, tangent_circles_plot, view_yaw):
    d = r1.value + r2.value + offset.value
    discriminant = ((d**2 + r1.value**2 - r2.value**2) / (2 * d)) ** 2 if abs(d) > 1e-8 else 0.0
    root_sq = max(r1.value**2 - discriminant, 0.0) if abs(d) > 1e-8 else 0.0

    if offset.value < -1e-6:
        status = "two intersections"
    elif abs(offset.value) <= 1e-6:
        status = "tangent"
    else:
        status = "separate"

    _md = rf"""
    Centres:

    $$
    c_1=(0,0), \qquad c_2=({d:.2f}, 0)
    $$

    Outer tangency test:

    $$
    d - (r_1+r_2) = {offset.value:.3f}
    $$

    Vertical intersection offset:

    $$
    y^2 = {root_sq:.4f}
    $$

    Status: **{status}**
    """

    mo.vstack([r1, r2, offset, gm.md(_md), tangent_circles_plot(r1.value, r2.value, d, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def tangent_circles_plot(r1, r2, d, view_yaw_deg):
        c1 = np.array([0.0, 0.0], dtype=float)
        c2 = np.array([d, 0.0], dtype=float)
        t = np.linspace(0, 2 * np.pi, 240)

        fig = plt.figure(figsize=(11.8, 5.3))
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122, projection="3d")

        x1 = c1[0] + r1 * np.cos(t)
        y1 = c1[1] + r1 * np.sin(t)
        x2 = c2[0] + r2 * np.cos(t)
        y2 = c2[1] + r2 * np.sin(t)
        z1 = 0.5 * (x1**2 + y1**2)
        z2 = 0.5 * (x2**2 + y2**2)

        ax0.plot(x1, y1, color="#2563eb", lw=2.2)
        ax0.plot(x2, y2, color="#d62828", lw=2.2)
        ax0.scatter([c1[0], c2[0]], [c1[1], c2[1]], color=["#2563eb", "#d62828"], s=40)

        if abs(d) > 1e-8:
            x = (d**2 + r1**2 - r2**2) / (2 * d)
            y_sq = r1**2 - x**2
            if y_sq >= -1e-8:
                y = np.sqrt(max(y_sq, 0.0))
                pts = [(x, y)] if y < 1e-6 else [(x, y), (x, -y)]
                ax0.scatter([p[0] for p in pts], [p[1] for p in pts], color="#111111", s=42, zorder=5)
        ax0.set_xlim(-1.9, 2.6)
        ax0.set_ylim(-1.9, 1.9)
        ax0.set_aspect("equal")
        ax0.grid(True, alpha=0.18)
        ax0.set_xlabel(r"$\mathbf{e_1}$")
        ax0.set_ylabel(r"$\mathbf{e_2}$")
        ax0.set_title("Euclidean circles")

        grid_x = np.linspace(-1.8, 2.5, 90)
        grid_y = np.linspace(-1.8, 1.8, 90)
        gx, gy = np.meshgrid(grid_x, grid_y)
        gz = 0.5 * (gx**2 + gy**2)
        plane1 = c1[0] * gx + c1[1] * gy + 0.5 * (r1**2 - c1[0] ** 2 - c1[1] ** 2)
        plane2 = c2[0] * gx + c2[1] * gy + 0.5 * (r2**2 - c2[0] ** 2 - c2[1] ** 2)

        ax1.plot_surface(gx, gy, gz, color="#ddd6fe", alpha=0.22, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, plane1, color="#bfdbfe", alpha=0.16, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, plane2, color="#fecaca", alpha=0.16, linewidth=0, shade=False)
        ax1.plot(x1, y1, z1, color="#2563eb", lw=2.2)
        ax1.plot(x2, y2, z2, color="#d62828", lw=2.2)

        if abs(d) > 1e-8:
            x = (d**2 + r1**2 - r2**2) / (2 * d)
            y_sq = r1**2 - x**2
            if y_sq >= -1e-8:
                y = np.sqrt(max(y_sq, 0.0))
                pts = [(x, y)] if y < 1e-6 else [(x, y), (x, -y)]
                for px, py in pts:
                    pz = 0.5 * (px**2 + py**2)
                    ax1.scatter([px], [py], [pz], color="#111111", s=44)

        ax1.set_xlim(-1.9, 2.5)
        ax1.set_ylim(-1.9, 1.9)
        ax1.set_zlim(-1.2, 4.0)
        ax1.set_box_aspect((1.2, 1.0, 0.9))
        ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        ax1.set_xlabel(r"$\mathbf{e_1}$")
        ax1.set_ylabel(r"$\mathbf{e_2}$")
        ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        ax1.set_title("Two slice planes sharing lifted points")

        plt.close(fig)
        return fig

    return (tangent_circles_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
