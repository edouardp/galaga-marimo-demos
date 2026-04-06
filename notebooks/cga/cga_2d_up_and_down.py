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
    # 2D CGA: `up(...)` and `down(...)`

    The conformal lift sends an ordinary Euclidean point into the larger conformal
    model. To use CGA comfortably, you also need the reverse direction: recover
    the Euclidean point from its conformal representative.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this notebook we use

    $$
    \operatorname{up}(x) = e_o + x + \frac{1}{2} x^2 e_\infty.
    $$

    For a normalized conformal point $X$ with $X \cdot e_\infty = -1$, the
    Euclidean point is recovered by

    $$
    \operatorname{down}(X) = X - e_o - \frac{1}{2}(X^2)e_\infty,
    $$

    which, for a true point, simply leaves the Euclidean $e_1,e_2$ part.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    px = mo.ui.slider(-1.7, 1.7, step=0.05, value=0.9, label="Point x", show_value=True)
    py = mo.ui.slider(-1.7, 1.7, step=0.05, value=-0.4, label="Point y", show_value=True)
    return px, py


@app.cell
def _(alg, down_up_plot, e1, e2, em, ep, gm, mo, px, py):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (px.value * e1 + py.value * e2).name(latex="x")
    X = (eo + x + half * (x | x) * einf).name(latex=r"\operatorname{up}(x)")
    down_X = (X - eo - half * (X * X) * einf).name(latex=r"\operatorname{down}(X)")
    euclid_part = ((down_X | e1) * e1 + (down_X | e2) * e2).name(latex=r"\pi_E(\operatorname{down}(X))")
    null_sq = (X * X).name(latex=r"\operatorname{up}(x)^2")
    normalizing = (X | einf).name(latex=r"\operatorname{up}(x)\cdot e_\infty")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {x.display()} <br/>
    {X.display()} <br/>
    {null_sq.display()} <br/>
    {normalizing.display()} <br/>
    {down_X.display()} <br/>
    {euclid_part.display()} <br/>
    The Euclidean point survives inside the conformal point and can be recovered.
    """

    mo.vstack([px, py, gm.md(_md), down_up_plot(x, euclid_part)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    CGA is not abandoning Euclidean geometry. It is embedding Euclidean points in
    a larger algebra where more geometry becomes linear and uniform. The
    `down(...)` step is what makes that embedding feel reversible and concrete.
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
    def down_up_plot(x, recovered):
        _x = x.vector_part[:2]
        _r = recovered.vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(5.4, 5.4))
        _ax.scatter([_x[0]], [_x[1]], color="#7c3aed", s=65, label="input x")
        _ax.scatter([_r[0]], [_r[1]], color="#059669", marker="x", s=80, label="down(up(x))")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-2.0, 2.0)
        _ax.set_ylim(-2.0, 2.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.legend(loc="upper left")
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Up to CGA, back down to the plane")
        plt.close(_fig)
        return _fig

    return (down_up_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
