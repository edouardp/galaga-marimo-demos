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
    # Conics as Cone Slices

    This is the classical projective picture of a conic. It is not CGA. Instead
    of lifting points onto a Veronese surface, we treat the conic as a quadratic
    cone in homogeneous coordinates and recover the ordinary Euclidean conic as
    the slice $z=1$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In homogeneous coordinates $(x,y,z)$, an axis-aligned affine conic becomes a
    quadratic cone:

    $$
    A x^2 + C y^2 + D xz + E yz + F z^2 = 0.
    $$

    The visible Euclidean conic is the plane section

    $$
    z = 1.
    $$

    So the downstairs curve is literally the slice of the upstairs cone by one
    affine chart plane.
    """)
    return


@app.cell
def _(mo):
    family = mo.ui.dropdown(
        options={
            "Ellipse": "ellipse",
            "Parabola": "parabola",
            "Hyperbola": "hyperbola",
        },
        value="Ellipse",
        label="Family",
    )
    a = mo.ui.slider(0.3, 1.8, step=0.05, value=1.0, label="a / opening scale", show_value=True)
    b = mo.ui.slider(0.3, 1.8, step=0.05, value=0.7, label="b / secondary scale", show_value=True)
    h = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.2, label="centre / vertex along e1", show_value=True)
    k = mo.ui.slider(-1.2, 1.2, step=0.05, value=-0.1, label="centre / vertex along e2", show_value=True)
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return a, b, family, h, k, view_yaw


@app.cell
def _(a, b, cone_slice_plot, family, gm, h, k, mo, view_yaw):
    family_key = family.value

    if family_key == "ellipse":
        A = 1.0 / (a.value**2)
        C = 1.0 / (b.value**2)
        D = -2.0 * h.value / (a.value**2)
        E = -2.0 * k.value / (b.value**2)
        F = h.value**2 / (a.value**2) + k.value**2 / (b.value**2) - 1.0
        eq_text = (
            rf"\frac{{(x-{h.value:.2f})^2}}{{{a.value:.2f}^2}} + "
            rf"\frac{{(y-{k.value:.2f})^2}}{{{b.value:.2f}^2}} = 1"
        )
    elif family_key == "hyperbola":
        A = 1.0 / (a.value**2)
        C = -1.0 / (b.value**2)
        D = -2.0 * h.value / (a.value**2)
        E = 2.0 * k.value / (b.value**2)
        F = h.value**2 / (a.value**2) - k.value**2 / (b.value**2) - 1.0
        eq_text = (
            rf"\frac{{(x-{h.value:.2f})^2}}{{{a.value:.2f}^2}} - "
            rf"\frac{{(y-{k.value:.2f})^2}}{{{b.value:.2f}^2}} = 1"
        )
    else:
        p = a.value
        A = p
        C = 0.0
        D = -2.0 * p * h.value
        E = -1.0
        F = p * h.value**2 + k.value
        eq_text = rf"y - {k.value:.2f} = {p:.2f}(x-{h.value:.2f})^2"

    _md = rf"""
    Euclidean conic:

    $$
    {eq_text}
    $$

    Homogeneous cone:

    $$
    {A:.3f}x^2 + {C:.3f}y^2 + {D:.3f}xz + {E:.3f}yz + {F:.3f}z^2 = 0
    $$

    Affine chart:

    $$
    z = 1
    $$
    """

    mo.vstack([family, a, b, h, k, gm.md(_md), cone_slice_plot(family_key, a.value, b.value, h.value, k.value, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _coefficients(family_key, a, b, h, k):
        if family_key == "ellipse":
            A = 1.0 / (a**2)
            C = 1.0 / (b**2)
            D = -2.0 * h / (a**2)
            E = -2.0 * k / (b**2)
            F = h**2 / (a**2) + k**2 / (b**2) - 1.0
        elif family_key == "hyperbola":
            A = 1.0 / (a**2)
            C = -1.0 / (b**2)
            D = -2.0 * h / (a**2)
            E = 2.0 * k / (b**2)
            F = h**2 / (a**2) - k**2 / (b**2) - 1.0
        else:
            p = a
            A = p
            C = 0.0
            D = -2.0 * p * h
            E = -1.0
            F = p * h**2 + k
        return A, C, D, E, F

    def cone_slice_plot(family_key, a, b, h, k, view_yaw_deg):
        A, C, D, E, F = _coefficients(family_key, a, b, h, k)

        xs = np.linspace(-2.2, 2.2, 280)
        ys = np.linspace(-2.2, 2.2, 280)
        gx, gy = np.meshgrid(xs, ys)
        conic_eq = A * gx**2 + C * gy**2 + D * gx + E * gy + F

        fig = plt.figure(figsize=(12.2, 5.2))
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122, projection="3d")

        ax0.contour(gx, gy, conic_eq, levels=[0], colors=["#7c3aed"], linewidths=2.4)
        ax0.set_xlim(-2.2, 2.2)
        ax0.set_ylim(-2.2, 2.2)
        ax0.set_aspect("equal")
        ax0.grid(True, alpha=0.18)
        ax0.set_xlabel(r"$\mathbf{e_1}$")
        ax0.set_ylabel(r"$\mathbf{e_2}$")
        ax0.set_title("Conic in the Euclidean plane")

        z_vals = np.linspace(0.3, 2.0, 36)
        z_grid = np.broadcast_to(z_vals[:, None, None], (len(z_vals),) + gx.shape)
        x_grid = np.broadcast_to(gx, z_grid.shape)
        y_grid = np.broadcast_to(gy, z_grid.shape)
        cone_eq = A * x_grid**2 + C * y_grid**2 + D * x_grid * z_grid + E * y_grid * z_grid + F * z_grid**2
        cone_mask = np.abs(cone_eq) < 0.05

        ax1.scatter(x_grid[cone_mask], y_grid[cone_mask], z_grid[cone_mask], color="#7c3aed", s=0.8, alpha=0.18)
        ax1.plot_surface(gx, gy, np.ones_like(gx), color="#bfdbfe", alpha=0.20, linewidth=0, shade=False)
        slice_mask = np.abs(conic_eq) < 0.02
        ax1.scatter(gx[slice_mask], gy[slice_mask], np.ones_like(gx[slice_mask]), color="#111111", s=3, alpha=0.95)

        ax1.set_xlim(-2.2, 2.2)
        ax1.set_ylim(-2.2, 2.2)
        ax1.set_zlim(0.0, 2.1)
        ax1.set_box_aspect((1, 1, 0.8))
        ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        ax1.set_xlabel(r"$x$")
        ax1.set_ylabel(r"$y$")
        ax1.set_zlabel(r"$z$")
        ax1.set_title(r"Homogeneous cone sliced by $z=1$")

        plt.close(fig)
        return fig

    return (cone_slice_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
