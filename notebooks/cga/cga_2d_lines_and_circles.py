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
    # 2D CGA: Lines and Circles

    In 2D conformal GA, lines and circles arise from the same outer-product
    pattern. That is one of the early conceptual payoffs of the conformal model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three conformal points determine a circle:

    $$
    \mathcal C = A \wedge B \wedge C.
    $$

    Two conformal points together with infinity determine a line:

    $$
    L = A \wedge B \wedge e_\infty.
    $$

    A probe point $P$ lies on the object when the corresponding outer product
    vanishes.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    object_mode = mo.ui.dropdown(
        options={"Line through A and B": "line", "Circle through A, B, C": "circle"},
        value="Line through A and B",
        label="Object",
    )
    px = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.1, label="Probe x", show_value=True)
    py = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.2, label="Probe y", show_value=True)
    return object_mode, px, py


@app.cell
def _(alg, e1, e2, em, ep, gm, line_circle_plot, mo, object_mode, px, py):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    def up(vec, name):
        _vec_sq = (vec | vec)
        return (eo + vec + half * _vec_sq * einf).name(latex=name)

    a = (1.0 * e1).name("a")
    b = (-0.2 * e1 + 1.0 * e2).name("b")
    c = (-1.0 * e1).name("c")
    p = (px.value * e1 + py.value * e2).name("p")

    A = up(a, "A")
    B = up(b, "B")
    C = up(c, "C")
    P = up(p, "P")

    line = (A ^ B ^ einf).name("L")
    circle = (A ^ B ^ C).name(latex=r"\mathcal C")
    incidence_line = (P ^ line).name(latex=r"P \wedge L")
    incidence_circle = (P ^ circle).name(latex=r"P \wedge \mathcal C")

    if object_mode.value == "line":
        _md = t"""
        {A.display()} <br/>
        {B.display()} <br/>
        {P.display()} <br/>
        {einf.display()} <br/>
        {line.display()} <br/>
        {incidence_line.display()} <br/>
        Zero means the probe point lies on the line.
        """
    else:
        _md = t"""
        {A.display()} <br/>
        {B.display()} <br/>
        {C.display()} <br/>
        {P.display()} <br/>
        {circle.display()} <br/>
        {incidence_circle.display()} <br/>
        Zero means the probe point lies on the circle.
        """

    mo.vstack([object_mode, px, py, gm.md(_md), line_circle_plot(a, b, c, p, object_mode.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In ordinary Euclidean treatments, lines and circles often look like different
    families of formulas. In CGA they are both outer-product constructions of
    conformal points. The difference is just whether one of those points is
    infinity.
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
    def line_circle_plot(a, b, c, p, mode):
        _a = a.vector_part[:2]
        _b = b.vector_part[:2]
        _c = c.vector_part[:2]
        _p = p.vector_part[:2]

        _fig, _ax = plt.subplots(figsize=(5.6, 5.6))

        if mode == "line":
            _dir = _b - _a
            _pts = np.vstack([_a - 2.5 * _dir, _a + 2.5 * _dir])
            _ax.plot(_pts[:, 0], _pts[:, 1], color="#2563eb", lw=2.0)
            _ax.scatter([_a[0], _b[0]], [_a[1], _b[1]], color="#2563eb", s=45)
        else:
            x1, y1 = _a
            x2, y2 = _b
            x3, y3 = _c
            _d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            _ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / _d
            _uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / _d
            _r = np.hypot(x1 - _ux, y1 - _uy)
            _t = np.linspace(0, 2 * np.pi, 240)
            _ax.plot(_ux + _r * np.cos(_t), _uy + _r * np.sin(_t), color="#2563eb", lw=2.0)
            _ax.scatter([_a[0], _b[0], _c[0]], [_a[1], _b[1], _c[1]], color="#2563eb", s=45)

        _ax.scatter([_p[0]], [_p[1]], color="#d62828", s=60)
        _ax.text(_p[0] + 0.05, _p[1] + 0.05, "p", color="#d62828")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Line or circle in the Euclidean picture")
        plt.close(_fig)
        return _fig

    return (line_circle_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
