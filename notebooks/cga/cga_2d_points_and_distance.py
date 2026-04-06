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
    # 2D CGA: Points and Distance

    Once Euclidean points are lifted to null conformal points, the distance
    between them appears inside their inner product.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For lifted conformal points $X$ and $Y$,

    $$
    X^2 = Y^2 = 0,
    \qquad
    X \cdot Y = -\frac{1}{2} d(x,y)^2.
    $$

    So CGA does not treat Euclidean distance as an extra formula bolted on after
    the fact. Distance is already encoded in the conformal inner product.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    ax = mo.ui.slider(-1.6, 1.6, step=0.05, value=-0.7, label="A x", show_value=True)
    ay = mo.ui.slider(-1.4, 1.4, step=0.05, value=0.2, label="A y", show_value=True)
    bx = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.9, label="B x", show_value=True)
    by = mo.ui.slider(-1.4, 1.4, step=0.05, value=0.8, label="B y", show_value=True)
    return ax, ay, bx, by


@app.cell
def _(alg, ax, ay, bx, by, distance_plot, e1, e2, em, ep, gm, mo):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    a = (ax.value * e1 + ay.value * e2).name("a")
    b = (bx.value * e1 + by.value * e2).name("b")

    a_sq = (a | a).name(latex=r"a^2")
    b_sq = (b | b).name(latex=r"b^2")
    A = (eo + a + half * a_sq * einf).name("A")
    B = (eo + b + half * b_sq * einf).name("B")
    A_sq = (A * A).name(latex=r"A^2")
    B_sq = (B * B).name(latex=r"B^2")
    AB = (A | B).name(latex=r"A \cdot B")
    dist_sq = ((alg.scalar(-2) * AB)).name(latex=r"d(a,b)^2")
    sep = (b - a).name(latex=r"b-a")
    sep_sq = (sep | sep).name(latex=r"\|b-a\|^2")

    _md = t"""
    {A.display()} <br/>
    {B.display()} <br/>
    {A_sq.display()} <br/>
    {B_sq.display()} <br/>
    {AB.display()} <br/>
    {dist_sq.display()} <br/>
    {sep_sq.display()} <br/>
    In CGA, the conformal inner product already knows the Euclidean distance.
    """

    mo.vstack([ax, ay, bx, by, gm.md(_md), distance_plot(a, b, dist_sq)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The lifted points are null, but they are not orthogonal to each other. Their
    inner product records the Euclidean distance between the original points. That
    is one of the central reasons CGA is useful.
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
    def distance_plot(a, b, dist_sq):
        _a = a.vector_part[:2]
        _b = b.vector_part[:2]
        _d = dist_sq.scalar_part if hasattr(dist_sq, "scalar_part") else float(dist_sq)
        _fig, _ax = plt.subplots(figsize=(5.5, 5.5))
        _ax.scatter([_a[0], _b[0]], [_a[1], _b[1]], color=["#2563eb", "#d62828"], s=55)
        _ax.plot([_a[0], _b[0]], [_a[1], _b[1]], color="#555555", lw=1.6, alpha=0.85)
        _ax.text(_a[0] + 0.04, _a[1] + 0.05, "a", color="#2563eb")
        _ax.text(_b[0] + 0.04, _b[1] + 0.05, "b", color="#d62828")
        _mid = (_a + _b) / 2
        _ax.text(_mid[0] + 0.05, _mid[1] + 0.05, f"d² = {_d:.3f}", color="#333333")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-1.8, 1.8)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Euclidean points and their distance")
        plt.close(_fig)
        return _fig

    return (distance_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
