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
    # 2D CGA: Point Pairs and Intersections

    In 2D CGA, lines and circles are built as outer products of conformal points.
    Their intersection is therefore another outer-product object. In a generic
    case, that intersection is a **point pair**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We keep the Euclidean picture explicit here:

    - a line comes from $A \wedge B \wedge e_\infty$
    - a circle comes from $C \wedge D \wedge E$
    - the Euclidean intersection is visible as the ordinary crossing points

    The full CGA meet machinery can package this elegantly, but the first useful
    thing to see is that intersections naturally come in pairs.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    line_height = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.2, label="Line height", show_value=True)
    circle_radius = mo.ui.slider(0.4, 1.8, step=0.05, value=1.0, label="Circle radius", show_value=True)
    return circle_radius, line_height


@app.cell
def _(alg, circle_radius, e1, e2, em, ep, gm, intersection_plot, line_height, mo, np):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    def up(vec, name):
        return (eo + vec + half * (vec | vec) * einf).name(latex=name)

    h = alg.scalar(line_height.value).name("h")
    r = alg.scalar(circle_radius.value).name("r")

    a = (-1.5 * e1 + h * e2).name("a")
    b = (1.5 * e1 + h * e2).name("b")
    c = (r * e1).name("c")
    d = (r * e2).name("d")
    e = (-r * e1).name("e")

    A = up(a, "A")
    B = up(b, "B")
    C = up(c, "C")
    D = up(d, "D")
    E = up(e, "E")

    line = (A ^ B ^ einf).name("L")
    circle = (C ^ D ^ E).name(latex=r"\mathcal C")
    pair = (line ^ circle).name(latex=r"L \wedge \mathcal C")

    _disc = max(circle_radius.value**2 - line_height.value**2, 0.0)
    _root = np.sqrt(_disc)
    _has_intersection = circle_radius.value >= abs(line_height.value)

    _md = t"""
    {einf.display()} <br/>
    {line.display()} <br/>
    {circle.display()} <br/>
    {pair.display()} <br/>
    If the Euclidean line meets the Euclidean circle, the conformal intersection
    is a point-pair object encoding the two crossing points together.
    """

    mo.vstack([
        line_height,
        circle_radius,
        gm.md(_md),
        intersection_plot(line_height.value, circle_radius.value, _root, _has_intersection),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In CGA, intersections are not an afterthought. The same outer-product
    language that builds lines and circles also builds their joint incidence
    structure. The first concrete form of that idea in 2D is the point pair.
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
    def intersection_plot(line_height, radius, root, has_intersection):
        _fig, _ax = plt.subplots(figsize=(5.6, 5.6))
        _t = np.linspace(0, 2 * np.pi, 240)
        _ax.plot(radius * np.cos(_t), radius * np.sin(_t), color="#2563eb", lw=2.0, label="circle")
        _ax.plot([-1.8, 1.8], [line_height, line_height], color="#d62828", lw=2.0, label="line")

        if has_intersection:
            _pts_x = np.array([-root, root])
            _pts_y = np.array([line_height, line_height])
            _ax.scatter(_pts_x, _pts_y, color="#059669", s=60, zorder=3, label="intersection pair")

        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.legend(loc="upper right")
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Euclidean view of the point pair")
        plt.close(_fig)
        return _fig

    return (intersection_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
