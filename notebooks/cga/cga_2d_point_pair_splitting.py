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
    # 2D CGA: Splitting a Point Pair

    A point pair is one CGA object that encodes two Euclidean points together.
    This notebook makes that concrete in the simplest 2D case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For two conformal points $P_1$ and $P_2$, their point-pair object is

    $$
    \mathcal P = P_1 \wedge P_2.
    $$

    In an intersection problem, the meet gives a point pair first. The two
    Euclidean points are the two roots hidden inside that one bivector object.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    line_height = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.4, label="Line height", show_value=True)
    radius = mo.ui.slider(0.5, 1.8, step=0.05, value=1.2, label="Circle radius", show_value=True)
    return line_height, radius


@app.cell
def _(alg, e1, e2, em, ep, gm, line_height, mo, np, point_pair_plot, radius):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    def up(vec, name):
        return (eo + vec + half * (vec | vec) * einf).name(latex=name)

    h = alg.scalar(line_height.value).name("h")
    r = alg.scalar(radius.value).name("r")
    disc = (r * r - h * h).name(latex=r"r^2 - h^2")

    _disc_value = max(radius.value**2 - line_height.value**2, 0.0)
    _root_value = np.sqrt(_disc_value)

    p1 = (_root_value * e1 + h * e2).name(latex="p_1")
    p2 = ((-_root_value) * e1 + h * e2).name(latex="p_2")
    P1 = up(p1, "P_1")
    P2 = up(p2, "P_2")
    pair = (P1 ^ P2).name(latex=r"\mathcal P")
    incidence_1 = (P1 ^ pair).name(latex=r"P_1 \wedge \mathcal P")
    incidence_2 = (P2 ^ pair).name(latex=r"P_2 \wedge \mathcal P")

    _md = t"""
    {h.display()} <br/>
    {r.display()} <br/>
    {disc.display()} <br/>
    {p1.display()} <br/>
    {p2.display()} <br/>
    {P1.display()} <br/>
    {P2.display()} <br/>
    {pair.display()} <br/>
    {incidence_1.display()} <br/>
    {incidence_2.display()} <br/>
    The two Euclidean points are packed into one conformal point-pair object.
    """

    mo.vstack([line_height, radius, gm.md(_md), point_pair_plot(line_height.value, radius.value, _root_value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    A point pair is not just a list of two points. It is one CGA object whose
    algebraic incidence relations remember both points together.
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
    def point_pair_plot(line_height, radius, root):
        _fig, _ax = plt.subplots(figsize=(5.6, 5.6))
        _t = np.linspace(0, 2 * np.pi, 240)
        _ax.plot(radius * np.cos(_t), radius * np.sin(_t), color="#2563eb", lw=2.0, label="circle")
        _ax.plot([-1.8, 1.8], [line_height, line_height], color="#d62828", lw=2.0, label="line")
        _ax.scatter([-root, root], [line_height, line_height], color="#059669", s=65, zorder=3, label="split points")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.legend(loc="upper right")
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Euclidean split of the point pair")
        plt.close(_fig)
        return _fig

    return (point_pair_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
