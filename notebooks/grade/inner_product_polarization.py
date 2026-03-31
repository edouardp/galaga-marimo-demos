import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_polarization(u, v):
        _u = np.array(u.eval().vector_part[:2], dtype=float)
        _v = np.array(v.eval().vector_part[:2], dtype=float)
        _sum = _u + _v

        _fig, _ax = plt.subplots(figsize=(7.2, 5.4))

        _ax.annotate(
            "",
            xy=_u,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=3, mutation_scale=22),
        )
        _ax.annotate(
            "",
            xy=_u + _v,
            xytext=_u,
            arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=3, mutation_scale=22),
        )
        _ax.annotate(
            "",
            xy=_sum,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=3, mutation_scale=22),
        )

        _ax.text(_u[0] * 0.5, _u[1] * 0.5 - 0.12, "u", color="#d62828", fontsize=13)
        _mid_v = _u + 0.5 * _v
        _ax.text(_mid_v[0] + 0.06, _mid_v[1] + 0.03, "v", color="#2563eb", fontsize=13)
        _mid_sum = 0.5 * _sum
        _ax.text(_mid_sum[0] - 0.28, _mid_sum[1] + 0.12, "u + v", color="#7c3aed", fontsize=13)

        _ax.set_xlim(-0.5, 3.0)
        _ax.set_ylim(-1.0, 1.5)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Build the sum vector tip-to-tail")

        plt.close(_fig)
        return _fig

    return (draw_polarization,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Inner Product from Squared Lengths

    The inner product does not have to be introduced as a projection first. It can also be recovered from squared lengths:

    $$
    u \cdot v = \frac{1}{2}\left((u+v)^2 - u^2 - v^2\right).
    $$

    This formula is called the **polarization identity**. It recovers the bilinear inner product from the quadratic notion of squaring a vector.

    This notebook is inspired by [this short video](https://www.youtube.com/shorts/2d3A5x6Mwc4) by `@sudgylacmoe`.

    It complements [grade_routing_products.py](./grade_routing_products.py): there the dot product appears as one grade channel of the geometric product, while here it is reconstructed from the geometry of three vectors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    In Euclidean signature, the square of a vector is its squared length. That makes the polarization identity especially visual:

    - $u^2$ is the squared length of the fixed horizontal vector
    - $v^2$ is the squared length of the rotating vector
    - $(u+v)^2$ is the squared length of the diagonal sum

    Their signed combination recovers the inner product.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    turn = mo.ui.slider(0, 180, step=1, value=90, label="Turn v from opposite to aligned", show_value=True)
    v_length = mo.ui.slider(0.4, 1.2, step=0.05, value=1.0, label="Length of v", show_value=True)
    return turn, v_length


@app.cell
def _(alg, draw_polarization, e1, e2, gm, mo, np, turn, v_length):
    _half = alg.scalar(1/2).name(latex=r"\frac{1}{2}")
    _u = (1.5 * e1).name("u")
    _theta = np.radians(180 - turn.value)
    _v = (v_length.value * np.cos(_theta) * e1 + v_length.value * np.sin(_theta) * e2).name("v")
    _sum = (_u + _v).name(latex=r"u + v")

    _u_sq = (_u * _u).scalar_part
    _v_sq = (_v * _v).scalar_part
    _sum_sq = (_sum * _sum).scalar_part
    _dot_by_identity = 0.5 * (_sum_sq - _u_sq - _v_sq)
    _dot_direct = (_u | _v).scalar_part

    _md = t"""
    {_u.display()} <br/>
    {_v.display()} <br/>
    {_sum.display()} <br/>
    {(_u**2).display():.3f} <br/>
    {(_v**2).display():.3f} <br/>
    {((_u+_v)**2).display():.3f} <br/>
    {(_half*((_u+_v)**2 - _u**2 - _v**2)).display():.3f} <br/>
    $compared\\;to: \\quad$ {(_u | _v).display():.3f}
    """

    mo.vstack(
        [
            turn,
            v_length,
            gm.md(_md),
            draw_polarization(_u, _v),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The inner product can be reconstructed from metric information alone. In Euclidean GA, the squares of the three visible vectors already contain the dot product.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
