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
    # Circles as Plane Slices of the Paraboloid

    In the Euclidean plane, a circle is curved. After the conformal lift, that
    same circle becomes a planar slice of the paraboloid.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a circle

    $$
    (x-c_x)^2 + (y-c_y)^2 = r^2,
    $$

    write

    $$
    z = \frac12(x^2+y^2).
    $$

    Substituting gives

    $$
    z = c_x x + c_y y + \frac12(r^2 - c_x^2 - c_y^2),
    $$

    which is a plane equation in the lifted coordinates.
    """)
    return


@app.cell
def _(mo):
    cx = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.4, label="centre along e1", show_value=True)
    cy = mo.ui.slider(-1.2, 1.2, step=0.05, value=-0.2, label="centre along e2", show_value=True)
    radius = mo.ui.slider(0.2, 1.4, step=0.05, value=0.8, label="radius", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return cx, cy, radius, view_yaw


@app.cell
def _(circle_slice_plot, cx, cy, gm, mo, radius, view_yaw):
    _const = 0.5 * (radius.value**2 - cx.value**2 - cy.value**2)
    _md = rf"""
    Circle in the plane:

    $$
    (x-{cx.value:.2f})^2 + (y-{cy.value:.2f})^2 = {radius.value:.2f}^2
    $$

    Corresponding plane upstairs:

    $$
    z = {cx.value:.2f}x + {cy.value:.2f}y + {_const:.3f}
    $$
    """
    mo.vstack([cx, cy, radius, gm.md(_md), circle_slice_plot(cx.value, cy.value, radius.value, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def circle_slice_plot(cx, cy, radius, view_yaw_deg):
        _t = np.linspace(0, 2 * np.pi, 240)
        _circle_x = cx + radius * np.cos(_t)
        _circle_y = cy + radius * np.sin(_t)
        _circle_z = 0.5 * (_circle_x**2 + _circle_y**2)

        _grid = np.linspace(-1.8, 1.8, 80)
        _gx, _gy = np.meshgrid(_grid, _grid)
        _gz = 0.5 * (_gx**2 + _gy**2)
        _plane_z = cx * _gx + cy * _gy + 0.5 * (radius**2 - cx**2 - cy**2)

        _fig = plt.figure(figsize=(11.4, 5.2))
        _ax0 = _fig.add_subplot(121)
        _ax1 = _fig.add_subplot(122, projection="3d")

        _ax0.plot(_circle_x, _circle_y, color="#2563eb", linewidth=2.2)
        _ax0.scatter([cx], [cy], color="#d62828", s=45)
        _ax0.set_xlim(-1.9, 1.9)
        _ax0.set_ylim(-1.9, 1.9)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.18)
        _ax0.set_xlabel(r"$\mathbf{e_1}$")
        _ax0.set_ylabel(r"$\mathbf{e_2}$")
        _ax0.set_title("Circle in the Euclidean plane")

        _ax1.plot_surface(_gx, _gy, _gz, color="#ddd6fe", alpha=0.24, linewidth=0, shade=False)
        _ax1.plot_surface(_gx, _gy, _plane_z, color="#bfdbfe", alpha=0.22, linewidth=0, shade=False)
        _ax1.plot(_circle_x, _circle_y, _circle_z, color="#7c3aed", linewidth=2.4)
        _ax1.set_xlim(-1.9, 1.9)
        _ax1.set_ylim(-1.9, 1.9)
        _ax1.set_zlim(-1.0, 3.4)
        _ax1.set_box_aspect((1, 1, 0.85))
        _ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        _ax1.set_xlabel(r"$\mathbf{e_1}$")
        _ax1.set_ylabel(r"$\mathbf{e_2}$")
        _ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        _ax1.set_title("Planar slice upstairs")

        plt.close(_fig)
        return _fig

    return (circle_slice_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
