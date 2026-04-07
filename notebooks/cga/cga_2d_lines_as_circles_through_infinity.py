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
    # Lines as Circles Through Infinity

    In the conformal picture, a line is not a totally different kind of object.
    It is the limiting case of a circle whose radius grows while one side of the
    circle runs through infinity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a horizontal line

    $$
    y = h,
    $$

    the lifted paraboloid points satisfy

    $$
    z = \frac12(x^2+h^2),
    $$

    which is a parabolic curve upstairs. This is the same lifted geometry you
    get by taking larger and larger circles that flatten toward a line.
    """)
    return


@app.cell
def _(mo):
    height = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.35, label="line height h", show_value=True)
    radius = mo.ui.slider(0.8, 6.0, step=0.05, value=1.5, label="comparison circle radius", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return height, radius, view_yaw


@app.cell
def _(gm, height, line_infinity_plot, mo, radius, view_yaw):
    _md = rf"""
    Line:

    $$
    y = {height.value:.2f}
    $$

    Comparison family of circles:

    $$
    x^2 + (y - ({height.value:.2f} - {radius.value:.2f}))^2 = {radius.value:.2f}^2
    $$

    As the radius grows, the lower part of the circle becomes harder to
    distinguish from the line.
    """
    mo.vstack([height, radius, view_yaw, gm.md(_md), line_infinity_plot(height.value, radius.value, view_yaw.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def line_infinity_plot(height, radius, view_yaw_deg):
        _x_line = np.linspace(-1.8, 1.8, 240)
        _y_line = np.full_like(_x_line, height)
        _z_line = 0.5 * (_x_line**2 + _y_line**2)

        _cx, _cy = 0.0, height - radius
        _t = np.linspace(0, 2 * np.pi, 240)
        _circle_x = _cx + radius * np.cos(_t)
        _circle_y = _cy + radius * np.sin(_t)
        _circle_z = 0.5 * (_circle_x**2 + _circle_y**2)

        _grid = np.linspace(-1.8, 1.8, 80)
        _gx, _gy = np.meshgrid(_grid, _grid)
        _gz = 0.5 * (_gx**2 + _gy**2)

        _fig = plt.figure(figsize=(11.4, 5.2))
        _ax0 = _fig.add_subplot(121)
        _ax1 = _fig.add_subplot(122, projection="3d")

        _ax0.plot(_x_line, _y_line, color="#2563eb", linewidth=2.2, label="line")
        _ax0.plot(_circle_x, _circle_y, color="#d62828", linewidth=1.5, alpha=0.65, label="comparison circle")
        _ax0.set_xlim(-1.9, 1.9)
        _ax0.set_ylim(-1.9, 1.9)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.18)
        _ax0.legend(loc="upper right")
        _ax0.set_xlabel(r"$\mathbf{e_1}$")
        _ax0.set_ylabel(r"$\mathbf{e_2}$")
        _ax0.set_title("Line and large-circle comparison")

        _ax1.plot_surface(_gx, _gy, _gz, color="#ddd6fe", alpha=0.24, linewidth=0, shade=False)
        _ax1.plot(_x_line, _y_line, _z_line, color="#2563eb", linewidth=2.4)
        _ax1.plot(_circle_x, _circle_y, _circle_z, color="#d62828", linewidth=1.5, alpha=0.6)
        _ax1.set_xlim(-1.9, 1.9)
        _ax1.set_ylim(-1.9, 1.9)
        _ax1.set_zlim(0, 4.0)
        _ax1.set_box_aspect((1, 1, 0.9))
        _ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        _ax1.set_xlabel(r"$\mathbf{e_1}$")
        _ax1.set_ylabel(r"$\mathbf{e_2}$")
        _ax1.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        _ax1.set_title("Lifted curves upstairs")

        plt.close(_fig)
        return _fig

    return (line_infinity_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
