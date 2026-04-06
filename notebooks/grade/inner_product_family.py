import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import (
        Algebra,
        doran_lasenby_inner,
        hestenes_inner,
        left_contraction,
        right_contraction,
        scalar_product,
    )
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return (
        Algebra,
        doran_lasenby_inner,
        gm,
        hestenes_inner,
        left_contraction,
        mo,
        np,
        plt,
        right_contraction,
        scalar_product,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Inner Product Family

    Geometric algebra has several inner-like products because different
    grade-selection rules solve different geometric tasks. In easy examples they
    agree. In mixed-grade examples they separate sharply.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use $\mathrm{Cl}(3,0)$.

    This notebook compares five named products:

    - Doran-Lasenby inner
    - Hestenes inner
    - left contraction
    - right contraction
    - scalar product
    """
    )
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Same Grade and Mixed Grade

    The same-grade comparison uses two bivectors. The mixed-grade comparison uses
    a vector and a bivector in both operand orders, which is where the family
    really starts to diverge.
    """
    )
    return


@app.cell
def _(mo):
    same_angle = mo.ui.slider(0, 180, step=1, value=35, label="Same-grade plane angle", show_value=True)
    vector_angle = mo.ui.slider(0, 360, step=1, value=25, label="Mixed-grade vector angle", show_value=True)
    plane_angle = mo.ui.slider(0, 180, step=1, value=60, label="Mixed-grade plane angle", show_value=True)
    return plane_angle, same_angle, vector_angle


@app.cell
def _(
    doran_lasenby_inner,
    draw_inner_product_family,
    e1,
    e2,
    e3,
    gm,
    hestenes_inner,
    left_contraction,
    mo,
    np,
    plane_angle,
    right_contraction,
    same_angle,
    scalar_product,
    vector_angle,
):
    _ops = [
        ("DL", doran_lasenby_inner),
        ("H", hestenes_inner),
        ("LC", left_contraction),
        ("RC", right_contraction),
        ("SP", scalar_product),
    ]

    _theta = np.radians(same_angle.value)
    _A = (e1 ^ e2).name("A")
    _B_same = (np.cos(_theta) * (e1 ^ e2) + np.sin(_theta) * (e2 ^ e3)).eval().name("B")

    _phi = np.radians(vector_angle.value)
    _psi = np.radians(plane_angle.value)
    _a = (np.cos(_phi) * e1 + np.sin(_phi) * e3).eval().name("a")
    _B_mix = (np.cos(_psi) * (e1 ^ e2) + np.sin(_psi) * (e2 ^ e3)).eval().name(latex=r"B_m")

    _same_results = [(label, fn(_A, _B_same).eval()) for label, fn in _ops]
    _mixed_ab = [(label, fn(_a, _B_mix).eval()) for label, fn in _ops]
    _mixed_ba = [(label, fn(_B_mix, _a).eval()) for label, fn in _ops]

    _md = t"""
    {_A.display()} <br/>
    {_B_same.display()} <br/>
    {_a.display()} <br/>
    {_B_mix.display()} <br/>
    Same-grade bivectors mostly agree. Mixed-grade inputs expose the real difference between the family members.
    """

    mo.vstack(
        [
            same_angle,
            vector_angle,
            plane_angle,
            gm.md(_md),
            draw_inner_product_family(_same_results, _mixed_ab, _mixed_ba),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    The names are not redundant. They encode different grade-selection rules.
    Same-grade examples can hide that, but mixed-grade examples make the family
    structure visible immediately.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_inner_product_family(same_results, mixed_ab, mixed_ba):
        _labels = [label for label, _ in same_results]

        def _scalar_or_e2(_mv):
            _parts = np.array(_mv.vector_part[:3], dtype=float)
            if np.max(np.abs(_parts)) > 1e-9:
                return _parts[1]
            return _mv.scalar_part

        _same_vals = np.array([_scalar_or_e2(_mv) for _, _mv in same_results], dtype=float)
        _ab_vals = np.array([_scalar_or_e2(_mv) for _, _mv in mixed_ab], dtype=float)
        _ba_vals = np.array([_scalar_or_e2(_mv) for _, _mv in mixed_ba], dtype=float)
        _x = np.arange(len(_labels))

        _fig, (_ax1, _ax2, _ax3) = plt.subplots(1, 3, figsize=(14.4, 4.8))
        for _ax, _vals, _title in [
            (_ax1, _same_vals, "Same-grade: bivector with bivector"),
            (_ax2, _ab_vals, "Mixed-grade: vector with bivector"),
            (_ax3, _ba_vals, "Mixed-grade: bivector with vector"),
        ]:
            _ax.bar(_x, _vals, color=["#222222", "#2563eb", "#16a34a", "#d62828", "#f59e0b"], alpha=0.82)
            _ax.set_xticks(_x, _labels)
            _ax.set_ylim(-2.2, 2.2)
            _ax.axhline(0, color="#555555", lw=1.0, alpha=0.45)
            _ax.grid(True, axis="y", alpha=0.25)
            _ax.set_title(_title)

        plt.close(_fig)
        return _fig

    return (draw_inner_product_family,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
