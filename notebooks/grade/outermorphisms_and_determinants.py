import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, gm, mo, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Outermorphisms and Determinants

    A linear map on vectors automatically extends to lines, areas, and higher-grade
    objects. That extension is the outermorphism. One of its cleanest payoffs is
    that the determinant is just the scale factor on the pseudoscalar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(2,0)$ so the whole story fits in one picture.

    If a linear map sends

    $$
    e_1 \mapsto f(e_1), \qquad e_2 \mapsto f(e_2),
    $$

    then the extension of that map to wedges, written here as $f_{\mathrm{ext}}$,
    sends

    $$
    e_{12} = e_1 \wedge e_2
    \mapsto
    f_{\mathrm{ext}}(e_{12}) = f(e_1) \wedge f(e_2).
    $$

    The coefficient of that transformed area element is the determinant.
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    a = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.2, label="Matrix entry a", show_value=True)
    b = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.6, label="Matrix entry b", show_value=True)
    c = mo.ui.slider(-2.0, 2.0, step=0.05, value=-0.4, label="Matrix entry c", show_value=True)
    d = mo.ui.slider(-2.0, 2.0, step=0.05, value=1.1, label="Matrix entry d", show_value=True)
    return a, b, c, d


@app.cell
def _(a, alg, b, c, d, draw_outermorphism, e1, e2, gm, mo):
    e12 = (e1 ^ e2).name(latex=r"e_{12}")
    matrix_f = alg.scalar(0).name(
        latex=rf"f \sim \begin{{pmatrix}} {a.value:.2f} & {b.value:.2f} \\ {c.value:.2f} & {d.value:.2f} \end{{pmatrix}}"
    )
    fe1 = (a.value * e1 + c.value * e2).name(latex=r"f(e_1)")
    fe2 = (b.value * e1 + d.value * e2).name(latex=r"f(e_2)")
    fe12 = (fe1 ^ fe2).name(latex=r"f_{\mathrm{ext}}(e_{12})")
    det_f = alg.scalar(a.value * d.value - b.value * c.value).name(latex=r"\det f")
    det_times_e12 = (det_f * e12).name(latex=r"(\det f)e_{12}")

    _orientation = "orientation-preserving" if det_f.scalar_part > 1e-9 else "orientation-reversing" if det_f.scalar_part < -1e-9 else "area-collapsing"

    _md = t"""
    {matrix_f.display()} <br/>
    {fe1.display()} <br/>
    {fe2.display()} <br/>
    {e12.display()} <br/>
    {fe12.display()} <br/>
    {det_f.display()} <br/>
    {det_times_e12.display()} <br/>
    This map is {_orientation}. The determinant is exactly the signed scale on the unit area element.
    """

    mo.vstack([a, b, c, d, gm.md(_md), draw_outermorphism(fe1, fe2, det_f.scalar_part)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The determinant is not an arbitrary scalar cooked up from coordinates. It is
    the coefficient telling you how the linear map acts on the top-grade blade.
    In 2D, that means the signed scale factor on the oriented area element.
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
    def draw_outermorphism(fe1, fe2, det_value):
        _f1 = fe1.vector_part[:2]
        _f2 = fe2.vector_part[:2]
        _fill = "#d62828" if det_value < 0 else "#f59e0b"

        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.2, 4.8))

        _ax0.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#222222", lw=2.3))
        _ax0.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#555555", lw=2.3))
        _ax0.fill([0, 1, 1, 0], [0, 0, 1, 1], color="#999999", alpha=0.15)
        _ax0.annotate("", xy=_f1, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.5))
        _ax0.annotate("", xy=_f2, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#10b981", lw=2.5))
        _ax0.fill([0, _f1[0], _f1[0] + _f2[0], _f2[0]], [0, _f1[1], _f1[1] + _f2[1], _f2[1]], color=_fill, alpha=0.35)
        _ax0.text(1.05, 0.05, r"$e_1$", color="#222222")
        _ax0.text(0.05, 1.05, r"$e_2$", color="#555555")
        _ax0.text(_f1[0] + 0.06, _f1[1] + 0.05, r"$f(e_1)$", color="#2563eb")
        _ax0.text(_f2[0] + 0.06, _f2[1] + 0.05, r"$f(e_2)$", color="#10b981")
        _ax0.set_xlim(-2.6, 2.6)
        _ax0.set_ylim(-2.6, 2.6)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.18)
        _ax0.set_title("Vectors determine the outermorphism")

        _ax1.bar([0], [1.0], color="#999999", alpha=0.45, width=0.5, label=r"$e_{12}$")
        _ax1.bar([1], [det_value], color=_fill, alpha=0.82, width=0.5, label=r"$f_\wedge(e_{12})$")
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.45)
        _ax1.set_xticks([0, 1], [r"$e_{12}$", r"$f_\wedge(e_{12})$"])
        _ax1.set_ylim(min(-2.6, det_value - 0.4), max(2.6, det_value + 0.4))
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("Determinant as top-grade scale")
        _ax1.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_outermorphism,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
