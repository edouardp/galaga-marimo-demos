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
    # The Vector Derivative Unifies Vector Calculus

    In GA, gradient, divergence, and curl are not separate operators glued
    together afterward. They are grade-selected parts of one vector derivative.

    This notebook now focuses only on the vector-field side:

    $$
    \nabla v = \nabla \cdot v + \nabla \wedge v.
    $$

    The scalar-field story `\nabla f` is handled separately in
    `scalar_gradient_and_laplacian.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We work in $\mathrm{Cl}(2,0)$ so the routing is easy to see.

    The vector derivative is

    $$
    \nabla = e_1 \partial_x + e_2 \partial_y.
    $$

    Applied to a vector field $v$, it splits as

    $$
    \nabla v = \nabla \cdot v + \nabla \wedge v.
    $$

    In 2D that means one scalar channel and one bivector channel.
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
    a = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.0, label="Stretch a", show_value=True)
    b = mo.ui.slider(-2.0, 2.0, step=0.05, value=-0.6, label="Stretch b", show_value=True)
    c = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.8, label="Swirl c", show_value=True)
    return a, b, c, x0, y0


@app.cell
def _(a, alg, b, c, draw_vector_derivative, e1, e2, gm, mo, x0, y0):
    x = alg.scalar(x0.value).name(latex="x")
    y = alg.scalar(y0.value).name(latex="y")

    v = (
        (a.value * x.scalar_part - c.value * y.scalar_part) * e1
        + (c.value * x.scalar_part + b.value * y.scalar_part) * e2
    ).name(latex="v")
    div_v = alg.scalar(a.value + b.value).name(latex=r"\nabla \cdot v")
    curl_v = alg.scalar(2 * c.value).name(latex=r"\partial_x v_y - \partial_y v_x")
    wedge_v = (curl_v * (e1 * e2)).name(latex=r"\nabla \wedge v")
    nabla_v = (div_v + wedge_v).name(latex=r"\nabla v")
    _md = t"""
    {x.display()} <br/>
    {y.display()} <br/>
    {v.display()} <br/>
    {div_v.display()} <br/>
    {wedge_v.display()} <br/>
    {nabla_v.display()} <br/>
    In the plot, blue means the scalar source/sink channel $\\nabla \\cdot v$, and red means the bivector swirl channel $\\nabla \\wedge v$.
    """

    mo.vstack([x0, y0, a, b, c, gm.md(_md), draw_vector_derivative(x0.value, y0.value, a.value, b.value, c.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    GA does not add divergence and curl together as an afterthought. The
    geometric product with $\nabla$ already contains both pieces. Grade selection
    is what recovers the separate operators.
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
    def draw_vector_derivative(x0, y0, a, b, c):
        _xs = np.linspace(-2.0, 2.0, 17)
        _ys = np.linspace(-2.0, 2.0, 17)
        _X, _Y = np.meshgrid(_xs, _ys)
        _U = a * _X - c * _Y
        _V = c * _X + b * _Y

        _probe_v = np.array([a * x0 - c * y0, c * x0 + b * y0], dtype=float)
        _div = a + b
        _curl = 2 * c

        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.5, 4.9))

        _ax0.quiver(_X, _Y, _U, _V, color="#999999", alpha=0.5)
        _ax0.annotate(
            "",
            xy=(x0 + _probe_v[0], y0 + _probe_v[1]),
            xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="#222222", lw=2.3, mutation_scale=18),
        )
        _ax0.scatter([x0], [y0], color="#222222", s=35, zorder=4)

        _source_scale = 0.18 * abs(_div)
        if _source_scale > 1e-9:
            _source_sign = np.sign(_div) if abs(_div) > 1e-9 else 1.0
            for _dx, _dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                _start = np.array([x0 + 0.24 * _dx, y0 + 0.24 * _dy], dtype=float)
                _end = _start + _source_sign * _source_scale * np.array([_dx, _dy], dtype=float)
                _ax0.annotate(
                    "",
                    xy=_end,
                    xytext=_start,
                    arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.0, mutation_scale=15, alpha=0.9),
                )

        _swirl_scale = 0.18 * abs(_curl)
        if _swirl_scale > 1e-9:
            _swirl_r = 0.34 + 0.04 * min(abs(_curl), 3.0)
            _theta0 = np.deg2rad(40 if _curl >= 0 else 220)
            _theta1 = _theta0 + np.deg2rad(260 if _curl >= 0 else -260)
            _ts = np.linspace(_theta0, _theta1, 80)
            _xs_arc = x0 + _swirl_r * np.cos(_ts)
            _ys_arc = y0 + _swirl_r * np.sin(_ts)
            _ax0.plot(_xs_arc, _ys_arc, color="#d62828", lw=2.0, alpha=0.95)
            _ax0.annotate(
                "",
                xy=(_xs_arc[-1], _ys_arc[-1]),
                xytext=(_xs_arc[-3], _ys_arc[-3]),
                arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.0, mutation_scale=16, alpha=0.95),
            )

        _ax0.text(x0 + _probe_v[0] + 0.06, y0 + _probe_v[1] + 0.04, "v", color="#222222")
        _ax0.text(x0 + 0.52, y0 + 0.34, r"$\nabla\cdot v$", color="#2563eb")
        _ax0.text(x0 - 0.78, y0 - 0.60, r"$\nabla\wedge v$", color="#d62828")
        _ax0.set_aspect("equal")
        _ax0.set_xlim(-2.2, 2.2)
        _ax0.set_ylim(-2.2, 2.2)
        _ax0.grid(True, alpha=0.18)
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_title("Local field value, source/sink, and swirl at the probe")

        _x = np.arange(2)
        _ax1.bar(_x, [_div, _curl], color=["#2563eb", "#d62828"], alpha=0.84)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.5)
        _ax1.set_xticks(_x, [r"$\nabla \cdot v$", r"$\nabla \wedge v$"])
        _ax1.set_ylim(-4.2, 4.2)
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("The same blue/red channels in coefficient form")

        plt.close(_fig)
        return _fig

    return (draw_vector_derivative,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
