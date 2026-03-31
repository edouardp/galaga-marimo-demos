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
    def draw_barycentric_areas(A, B, C, P, weights):
        _A = A.vector_part[:2]
        _B = B.vector_part[:2]
        _C = C.vector_part[:2]
        _P = P.vector_part[:2]
        _alpha, _beta, _gamma = weights

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.2, 5.2))

        for _ax in [_ax1, _ax2]:
            _ax.plot([_A[0], _B[0], _C[0], _A[0]], [_A[1], _B[1], _C[1], _A[1]], color="black", linewidth=1.8)
            _ax.scatter([_A[0], _B[0], _C[0], _P[0]], [_A[1], _B[1], _C[1], _P[1]], color=["black", "black", "black", "darkgreen"], zorder=3)
            for _label, _pt in zip(["A", "B", "C", "P"], [_A, _B, _C, _P]):
                _ax.text(_pt[0] + 0.05, _pt[1] + 0.05, _label)
            _ax.set_aspect("equal")
            _ax.set_xlim(-2.2, 2.2)
            _ax.set_ylim(-1.6, 2.2)
            _ax.grid(True, alpha=0.25)
            _ax.set_xlabel("e1")
            _ax.set_ylabel("e2")

        _ax1.fill([_P[0], _B[0], _C[0]], [_P[1], _B[1], _C[1]], color="crimson", alpha=0.28)
        _ax1.fill([_P[0], _C[0], _A[0]], [_P[1], _C[1], _A[1]], color="steelblue", alpha=0.28)
        _ax1.fill([_P[0], _A[0], _B[0]], [_P[1], _A[1], _B[1]], color="darkorange", alpha=0.28)
        _ax1.set_title("Subtriangle areas")

        _labels = [r"$\alpha$", r"$\beta$", r"$\gamma$"]
        _vals = np.array([_alpha, _beta, _gamma], dtype=float)
        _colors = ["crimson", "steelblue", "darkorange"]
        _x = np.arange(3)
        _ax2.bar(_x, _vals, color=_colors, alpha=0.82)
        _ax2.axhline(0, color="black", linewidth=0.8)
        _ax2.axhline(1, color="gray", linewidth=0.8, alpha=0.4, linestyle="--")
        _ax2.set_xticks(_x, _labels)
        _ax2.set_ylim(-0.6, 1.4)
        _ax2.set_title("Barycentric weights from oriented areas")
        _ax2.grid(True, axis="y", alpha=0.25)

        plt.close(_fig)
        return _fig

    return (draw_barycentric_areas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Barycentric Coordinates from Oriented Areas

    Barycentric coordinates are a geometric area story before they are a coordinate recipe. Each weight is the ratio of a signed subtriangle area to the signed area of the whole triangle.

    This notebook spins out one of the key ideas from [line_triangle_intersection.py](./line_triangle_intersection.py): there the barycentric weights were part of an intersection test, while here they are the main object of study.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    For a point $P$ in the plane of triangle $ABC$, the oriented triangle areas give

    $$
    \alpha = \frac{(B-P)\wedge(C-P)}{(B-A)\wedge(C-A)},
    \qquad
    \beta = \frac{(C-P)\wedge(A-P)}{(B-A)\wedge(C-A)},
    \qquad
    \gamma = \frac{(A-P)\wedge(B-P)}{(B-A)\wedge(C-A)}.
    $$

    The signs matter. Negative weight means the point has crossed an edge.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Constrained Point Motion

    The triangle stays fixed. The point moves in a slightly larger neighborhood so you can see both inside and outside cases without losing the geometry.
    """)
    return


@app.cell
def _(mo):
    px = mo.ui.slider(-1.2, 1.5, step=0.05, value=0.0, label="Point x", show_value=True)
    py = mo.ui.slider(-0.8, 1.6, step=0.05, value=0.5, label="Point y", show_value=True)
    return px, py


@app.cell
def _(draw_barycentric_areas, e1, e2, gm, mo, px, py):
    _A = (-1.2 * e1 - 0.5 * e2).name("A")
    _B = (1.3 * e1 - 0.3 * e2).name("B")
    _C = (-0.2 * e1 + 1.4 * e2).name("C")
    _P = (px.value * e1 + py.value * e2).name("P")

    _area_total = ((_B - _A) ^ (_C - _A)).eval().data[3]
    _alpha = (((_B - _P) ^ (_C - _P)).eval().data[3]) / _area_total
    _beta = (((_C - _P) ^ (_A - _P)).eval().data[3]) / _area_total
    _gamma = (((_A - _P) ^ (_B - _P)).eval().data[3]) / _area_total
    _inside = (_alpha >= -1e-9) and (_beta >= -1e-9) and (_gamma >= -1e-9)
    _status = "inside triangle" if _inside else "outside triangle"

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_C.display()} <br/>
    {_P.display()} <br/>
    $\\alpha = {_alpha:.3f},\\quad \\beta = {_beta:.3f},\\quad \\gamma = {_gamma:.3f}$ <br/>
    $\\alpha + \\beta + \\gamma = {_alpha + _beta + _gamma:.3f}$ <br/>
    Classification: **{_status}**
    """

    mo.vstack([px, py, gm.md(_md), draw_barycentric_areas(_A, _B, _C, _P, (_alpha, _beta, _gamma))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Barycentric coordinates are signed area fractions. The sum stays at $1$, and the signs tell you immediately whether the point is still inside the triangle or has crossed an edge.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
