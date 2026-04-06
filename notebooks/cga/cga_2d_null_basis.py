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

    return Algebra, b_cga, gm, mo, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA: Null Basis and Lifted Points

    Conformal geometric algebra adds two extra directions to the Euclidean plane.
    In the beginning, the important idea is not "higher dimension" by itself. The
    important idea is that these extra directions let ordinary Euclidean points be
    represented as **null vectors**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start from the 2D conformal model with Euclidean basis vectors $e_1, e_2$
    and an orthogonal $(+,-)$ pair $e_+, e_-$. From that pair we build the null
    directions

    $$
    e_o = \frac{e_- - e_+}{2},
    \qquad
    e_\infty = e_+ + e_-.
    $$

    Then a Euclidean point $x$ is lifted to the conformal point

    $$
    X = e_o + x + \frac{1}{2} x^2 e_\infty.
    $$
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    x_coord = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.8, label="Point x", show_value=True)
    y_coord = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.6, label="Point y", show_value=True)
    return x_coord, y_coord


@app.cell
def _(alg, e1, e2, em, ep, gm, lift_point_plot, mo, x_coord, y_coord):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (x_coord.value * e1 + y_coord.value * e2).name(latex="x")
    x_sq = (x | x).name(latex=r"x^2")
    X = (eo + x + half * x_sq * einf).name(latex="X")
    eo_sq = (eo * eo).name(latex=r"e_o^2")
    einf_sq = (einf * einf).name(latex=r"e_\infty^2")
    null_pair = (eo | einf).name(latex=r"e_o \cdot e_\infty")
    X_sq = (X * X).name(latex=r"X^2")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {eo_sq.display()} <br/>
    {einf_sq.display()} <br/>
    {null_pair.display()} <br/>
    {x.display()} <br/>
    {x_sq.display()} <br/>
    {X.display()} <br/>
    {X_sq.display()} <br/>
    The lift $X$ is null: that is the first key structural fact in CGA.
    """

    mo.vstack([x_coord, y_coord, gm.md(_md), lift_point_plot(x)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The Euclidean point $x$ and the conformal point $X$ are not the same kind of
    object. The Euclidean point lives in the ordinary plane. The conformal point
    lives in the larger conformal model and is null there. That nullness is what
    later makes distances, lines, and circles fit into one algebraic language.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(plt):
    def lift_point_plot(x):
        _xy = x.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.3, 5.3))
        _ax.annotate("", xy=_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2.3))
        _ax.scatter([_xy[0]], [_xy[1]], color="#7c3aed", s=45)
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Euclidean point before lifting")
        plt.close(_fig)
        return _fig

    return (lift_point_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
