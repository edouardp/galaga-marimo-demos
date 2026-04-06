import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA: Inversion in a Circle

    Circle inversion is one of the classic conformal actions. In CGA it becomes a
    sandwich action by the circle object itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a normalized circle object $\mathcal C$, the conformal image of a point
    $P$ under inversion is

    $$
    P' = \mathcal C P \mathcal C.
    $$

    In the unit circle centered at the origin, points move along the same radial
    line and the radius inverts.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 360, step=1, value=20, label="Point angle", show_value=True)
    radius = mo.ui.slider(0.2, 1.8, step=0.05, value=0.6, label="Point radius", show_value=True)
    return angle, radius


@app.cell
def _(alg, angle, e1, e2, em, ep, gm, inversion_plot, mo, np, radius):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    def up(vec, name):
        return (eo + vec + half * (vec | vec) * einf).name(latex=name)

    theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
    r = alg.scalar(radius.value).name("r")
    p = (radius.value * np.cos(theta.scalar_part) * e1 + radius.value * np.sin(theta.scalar_part) * e2).name("p")
    P = up(p, "P")

    A = up(e1, "A")
    B = up(e2, "B")
    C = up((-1) * e1, "C")
    circle = (A ^ B ^ C).name(latex=r"\mathcal C")
    Pp = (circle * P * circle).name(latex=r"P'")
    p_prime = (((Pp | e1) * e1) + ((Pp | e2) * e2)).name(latex=r"p'")

    _md = t"""
    {theta.display()} <br/>
    {r.display()} <br/>
    {P.display()} <br/>
    {circle.display()} <br/>
    {Pp.display()} <br/>
    {p_prime.display()} <br/>
    In the unit circle, the conformal sandwich reproduces ordinary Euclidean circle inversion.
    """

    mo.vstack([angle, radius, gm.md(_md), inversion_plot(p, p_prime)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    This is a good example of why CGA is called conformal. A classical nonlinear
    Euclidean transformation becomes a uniform sandwich action in the larger algebra.
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
    def inversion_plot(p, p_prime):
        _p = p.vector_part[:2]
        _pp = p_prime.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.6, 5.6))
        _t = np.linspace(0, 2 * np.pi, 240)
        _ax.plot(np.cos(_t), np.sin(_t), color="#2563eb", lw=2.0, label="unit circle")
        _ax.plot([0, _pp[0]], [0, _pp[1]], color="#555555", lw=1.0, alpha=0.5)
        _ax.scatter([_p[0], _pp[0]], [_p[1], _pp[1]], color=["#d62828", "#059669"], s=60)
        _ax.text(_p[0] + 0.05, _p[1] + 0.05, "p", color="#d62828")
        _ax.text(_pp[0] + 0.05, _pp[1] + 0.05, "p'", color="#059669")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.2, 2.2)
        _ax.set_ylim(-2.2, 2.2)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.legend(loc="upper right")
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Inversion in the unit circle")
        plt.close(_fig)
        return _fig

    return (inversion_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
