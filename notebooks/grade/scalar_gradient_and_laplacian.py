import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scalar Gradient and Laplacian

    Before the vector-derivative split `\nabla v = \nabla \cdot v + \nabla \wedge v`,
    there is the simpler scalar-field story:

    $$
    \nabla f
    \qquad \text{and} \qquad
    \nabla^2 f.
    $$

    The gradient is the vector direction of fastest increase, and the Laplacian
    measures how the field bends overall around a point.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We work in $\mathrm{Cl}(2,0)$ with

    $$
    \nabla = e_1 \partial_x + e_2 \partial_y.
    $$

    For the quadratic scalar field

    $$
    f(x,y) = a x^2 + b xy + c y^2,
    $$

    the gradient is a vector field and the Laplacian is a scalar.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    x0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.9, label="Probe x", show_value=True)
    y0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.6, label="Probe y", show_value=True)
    a = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.0, label="Quadratic a", show_value=True)
    b = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.0, label="Mixed b", show_value=True)
    c = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.0, label="Quadratic c", show_value=True)
    return a, b, c, x0, y0


@app.cell
def _(a, alg, b, c, draw_scalar_gradient, e1, e2, gm, mo, x0, y0):
    x = alg.scalar(x0.value).name(latex="x")
    y = alg.scalar(y0.value).name(latex="y")

    f = (a.value * x * x + b.value * x * y + c.value * y * y).name(latex="f")
    grad_f = (((2 * a.value * x + b.value * y) * e1) + ((b.value * x + 2 * c.value * y) * e2)).name(latex=r"\nabla f")
    lap_f = alg.scalar(2 * a.value + 2 * c.value).name(latex=r"\nabla^2 f")

    _md = t"""
    {x.display()} <br/>
    {y.display()} <br/>
    {f.display()} <br/>
    {grad_f.display()} <br/>
    {lap_f.display()} <br/>
    The gradient is the local direction of steepest increase. The Laplacian is the scalar curvature-like summary of the same field.
    """

    mo.vstack([x0, y0, a, b, c, gm.md(_md), draw_scalar_gradient(x0.value, y0.value, a.value, b.value, c.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    For a scalar field, `\nabla` already gives geometry: a vector pointing uphill.
    Applying `\nabla` again contracts that local change into the scalar Laplacian.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_scalar_gradient(x0, y0, a, b, c):
        _xs = np.linspace(-2.0, 2.0, 120)
        _ys = np.linspace(-2.0, 2.0, 120)
        _X, _Y = np.meshgrid(_xs, _ys)
        _F = a * _X**2 + b * _X * _Y + c * _Y**2

        _grad = np.array([2 * a * x0 + b * y0, b * x0 + 2 * c * y0], dtype=float)
        _lap = 2 * a + 2 * c

        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.4, 4.9))

        _cont = _ax0.contourf(_X, _Y, _F, levels=18, cmap="viridis", alpha=0.9)
        _ax0.contour(_X, _Y, _F, levels=10, colors="white", alpha=0.35, linewidths=0.7)
        _ax0.annotate(
            "",
            xy=(x0 + 0.22 * _grad[0], y0 + 0.22 * _grad[1]),
            xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.5, mutation_scale=18),
        )
        _ax0.scatter([x0], [y0], color="#111111", s=36, zorder=4)
        _ax0.text(x0 + 0.08, y0 + 0.08, r"$\nabla f$", color="#d62828")
        _ax0.set_aspect("equal")
        _ax0.set_xlim(-2.1, 2.1)
        _ax0.set_ylim(-2.1, 2.1)
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_title("Scalar field contours and the gradient")

        _ax1.bar([0], [_lap], color="#2563eb", alpha=0.84, width=0.5)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.5)
        _ax1.set_xticks([0], [r"$\nabla^2 f$"])
        _ax1.set_ylim(min(-4.2, _lap - 0.5), max(4.2, _lap + 0.5))
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("Laplacian at the probe")

        plt.close(_fig)
        return _fig

    return (draw_scalar_gradient,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
