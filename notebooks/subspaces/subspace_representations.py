import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, complement, dual, uncomplement, undual
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, complement, dual, gm, mo, np, plt, uncomplement, undual


@app.cell
def _(np, plt):
    def draw_subspace_views(angle_deg):
        _theta = np.radians(angle_deg)
        _a = np.array([1.0, 0.0])
        _b = np.array([np.cos(_theta), np.sin(_theta)])
        _normal = np.array([-np.sin(_theta), np.cos(_theta)])

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.0, 5.2))

        _ax1.annotate("", xy=_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax1.annotate("", xy=_b, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax1.fill([0, _a[0], _a[0] + _b[0], _b[0]], [0, _a[1], _a[1] + _b[1], _b[1]], color="goldenrod", alpha=0.25)
        _ax1.set_aspect("equal")
        _ax1.set_xlim(-1.3, 2.0)
        _ax1.set_ylim(-1.3, 2.0)
        _ax1.set_title("OPNS: the spanned area")
        _ax1.grid(True, alpha=0.25)

        _ax2.annotate("", xy=_normal, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkgreen", lw=2))
        _ax2.plot([-1.8 * _b[0], 1.8 * _b[0]], [-1.8 * _b[1], 1.8 * _b[1]], color="gray", alpha=0.35)
        _ax2.set_aspect("equal")
        _ax2.set_xlim(-1.3, 2.0)
        _ax2.set_ylim(-1.3, 2.0)
        _ax2.set_title("Dual view: the perpendicular normal")
        _ax2.grid(True, alpha=0.25)

        plt.close(_fig)
        return _fig

    return (draw_subspace_views,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Same Subspace, Different Representation

    A blade can describe a subspace in more than one way. The underlying geometry stays the same, but the representation changes what is easiest to read off.

    This notebook is the representation-side companion to [duality_and_complements.py](./duality_and_complements.py): that file emphasizes when `dual(...)` and `complement(...)` differ, while this one emphasizes what they are both doing when they agree.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    A bivector like $a \wedge b$ describes a plane element directly. Its dual describes the complementary normal direction. Those are different algebraic objects, but they refer to the same geometric plane.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    opening = mo.ui.slider(5, 175, step=1, value=55, label="Opening angle", show_value=True)
    return (opening,)


@app.cell
def _(
    complement,
    draw_subspace_views,
    dual,
    e1,
    e2,
    gm,
    mo,
    np,
    opening,
    uncomplement,
    undual,
):
    _theta = np.radians(opening.value)
    _a = e1.name("a")
    _b = (np.cos(_theta) * e1 + np.sin(_theta) * e2).name("b")
    _plane_blade = (_a ^ _b).name(latex=r"a \wedge b")
    _dual_normal = dual(_plane_blade).name(latex=r"(a \wedge b)^\star")
    _complementary_blade = complement(_plane_blade).name(latex=r"(a \wedge b)^\complement")
    _recovered_from_dual = undual(_dual_normal).name(latex=r"undual((a \wedge b)^\star)")
    _recovered_from_comp = uncomplement(_complementary_blade).name(latex=r"uncomplement((a \wedge b)^\complement)")

    _md = t"""
    {_a.display()} <br/>
    {_b.display()} <br/>
    {_plane_blade.display()} <br/>
    {_dual_normal.display()} <br/>
    {_complementary_blade.display()} <br/>
    {_recovered_from_dual.display()} <br/>
    {_recovered_from_comp.display()} <br/>
    The blade, its dual, and its complement are different representations around the same subspace story.
    """

    mo.vstack([opening, gm.md(_md), draw_subspace_views(opening.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    OPNS and dual-style descriptions are not competing meanings. They are different coordinate systems for the same geometry. The right representation is the one that makes the next operation simplest.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
