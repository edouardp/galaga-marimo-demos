import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, dual
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, dual, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hodge Star vs GA Duality

    Readers coming from differential geometry often meet the Hodge star first.
    GA duality is closely related, but it is phrased directly in the Clifford
    algebra rather than through forms and a separate star operator.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use Euclidean $\mathrm{Cl}(3,0)$, where the pseudoscalar is invertible.

    In this setting, duality is

    $$
    A^\star = A I^{-1}.
    $$

    That has the same geometric effect as the familiar Hodge-star mapping:

    - vectors $\leftrightarrow$ bivectors
    - scalars $\leftrightarrow$ pseudoscalars

    The main difference is that GA keeps everything in one product algebra.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    I = alg.I.name("I")
    one = alg.scalar(1).name("1")
    return e1, e2, one


app._unparsable_cell(
    r"""
    1angle = mo.ui.slider(0, 180, step=1, value=40, label="Opening angle", show_value=True)
    scale = mo.ui.slider(0.2, 1.8, step=0.05, value=1.0, label="Second-vector length", show_value=True)
    """,
    name="_"
)


@app.cell
def _(angle, draw_hodge_vs_duality, dual, e1, e2, gm, mo, np, one, scale):
    a = e1.name(latex="a")
    b = (scale.value * (np.cos(np.radians(angle.value)) * e1 + np.sin(np.radians(angle.value)) * e2)).name(latex="b")
    B = (a ^ b).name(latex=r"B = a \wedge b")
    B_star = dual(B).name(latex=r"B^\star")
    e1_star = dual(e1).name(latex=r"e_1^\star")
    scalar_star = dual(one).name(latex=r"1^\star")

    _md = t"""
    {a.display()} <br/>
    {b.display()} <br/>
    {B.display()} <br/>
    {B_star.display()} <br/>
    {e1_star.display()} <br/>
    {scalar_star.display()} <br/>
    In Euclidean 3D, duality sends the plane element $a \\wedge b$ to its perpendicular axial direction.
    """

    mo.vstack([angle, scale, gm.md(_md), draw_hodge_vs_duality(a, b, B_star)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In Euclidean signature, Hodge-star intuition and GA duality line up well. The
    benefit of the GA version is that the dual is still just another multivector
    inside the same algebraic language, rather than a separate external operator
    on differential forms.
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
    def draw_hodge_vs_duality(a, b, dual_bivector):
        _a = a.vector_part[:3]
        _b = b.vector_part[:3]
        _d = dual_bivector.vector_part[:3]

        _fig = plt.figure(figsize=(11.6, 5.2))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        _ax0.quiver(0, 0, 0, _a[0], _a[1], _a[2], color="#d62828", linewidth=2.5, arrow_length_ratio=0.1)
        _ax0.quiver(0, 0, 0, _b[0], _b[1], _b[2], color="#2563eb", linewidth=2.5, arrow_length_ratio=0.1)
        _ax0.quiver(0, 0, 0, _d[0], _d[1], _d[2], color="#10b981", linewidth=2.7, arrow_length_ratio=0.1)
        _ax0.text(_a[0] + 0.05, _a[1] + 0.05, _a[2] + 0.05, "a", color="#d62828")
        _ax0.text(_b[0] + 0.05, _b[1] + 0.05, _b[2] + 0.05, "b", color="#2563eb")
        _ax0.text(_d[0] + 0.05, _d[1] + 0.05, _d[2] + 0.05, r"$B^\star$", color="#10b981")
        _ax0.set_xlim(-1.5, 1.5)
        _ax0.set_ylim(-1.5, 1.5)
        _ax0.set_zlim(-1.5, 1.5)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_title("Plane element and its dual direction")
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_zlabel("e3")

        _ax1.text(0.05, 0.78, r"$\star(dx \wedge dy)$", fontsize=16)
        _ax1.text(0.60, 0.78, r"$\leftrightarrow$", fontsize=16)
        _ax1.text(0.75, 0.78, r"$dz$", fontsize=16, color="#10b981")
        _ax1.text(0.05, 0.52, r"$(e_1 \wedge e_2)^\star$", fontsize=16)
        _ax1.text(0.60, 0.52, r"$=$", fontsize=16)
        _ax1.text(0.75, 0.52, r"$e_3$", fontsize=16, color="#10b981")
        _ax1.text(0.05, 0.20, "Hodge-star language and GA duality agree here", fontsize=12)
        _ax1.axis("off")
        _ax1.set_title("Same geometry, different language")

        plt.close(_fig)
        return _fig

    return (draw_hodge_vs_duality,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
