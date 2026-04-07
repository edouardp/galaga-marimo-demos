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
    # Conics from a Veronese-Style Lift

    This is not standard CGA. It is a restricted projective lift for axis-aligned
    conics. The point is the same, though: a curved Euclidean object downstairs
    can come from one linear equation upstairs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lift an affine point $(x,y)$ to

    $$
    V(x,y) = (x,\ y,\ u=x^2,\ v=y^2).
    $$

    Then any conic with no $xy$ term,

    $$
    A x^2 + C y^2 + D x + E y + F = 0,
    $$

    becomes the hyperplane equation

    $$
    A u + C v + D x + E y + F = 0
    $$

    on the lifted surface $u=x^2,\ v=y^2$.
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
def _(a, b, conic_veronese_plot, family, gm, h, k, mo, view_yaw):
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
    Downstairs conic:

    $$
    {eq_text}
    $$

    Lifted hyperplane equation:

    $$
    {A:.3f}u + {C:.3f}v + {D:.3f}x + {E:.3f}y + {F:.3f} = 0
    $$

    This notebook only covers the no-$xy$ family, so one hyperplane in the
    lifted $(x,y,u,v)$ space is enough.
    """

    mo.vstack(
        [
            family,
            a,
            b,
            h,
            k,
            gm.md(_md),
            conic_veronese_plot(family_key, a.value, b.value, h.value, k.value, view_yaw.value),
            view_yaw,
        ]
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

    def conic_veronese_plot(family_key, a, b, h, k, view_yaw_deg):
        A, C, D, E, F = _coefficients(family_key, a, b, h, k)

        xs = np.linspace(-2.2, 2.2, 280)
        ys = np.linspace(-2.2, 2.2, 280)
        gx, gy = np.meshgrid(xs, ys)
        gu = gx**2
        eq = A * gu + C * (gy**2) + D * gx + E * gy + F

        fig = plt.figure(figsize=(12.2, 5.2))
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122, projection="3d")

        ax0.contour(gx, gy, eq, levels=[0], colors=["#7c3aed"], linewidths=2.4)
        ax0.set_xlim(-2.2, 2.2)
        ax0.set_ylim(-2.2, 2.2)
        ax0.set_aspect("equal")
        ax0.grid(True, alpha=0.18)
        ax0.set_xlabel(r"$\mathbf{e_1}$")
        ax0.set_ylabel(r"$\mathbf{e_2}$")
        ax0.set_title("Conic in the Euclidean plane")

        hyperplane_u = -(C * (gy**2) + D * gx + E * gy + F) / A
        mask = np.abs(eq) < 0.02
        ax1.plot_surface(gx, gy, gu, color="#ddd6fe", alpha=0.22, linewidth=0, shade=False)
        ax1.plot_surface(gx, gy, hyperplane_u, color="#bfdbfe", alpha=0.18, linewidth=0, shade=False)
        ax1.scatter(gx[mask], gy[mask], gu[mask], color="#7c3aed", s=3, alpha=0.8)
        ax1.set_xlim(-2.2, 2.2)
        ax1.set_ylim(-2.2, 2.2)
        ax1.set_zlim(-6.0, 6.0)
        ax1.set_box_aspect((1, 1, 0.8))
        ax1.view_init(elev=22, azim=-58 + view_yaw_deg)
        ax1.set_xlabel(r"$x$")
        ax1.set_ylabel(r"$y$")
        ax1.set_zlabel(r"$u$")
        ax1.set_title(r"Chart of the lift: $u=x^2$ and the hyperplane")

        plt.close(fig)
        return fig

    return (conic_veronese_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
