import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, grade
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, grade, mo, np, plt


@app.cell
def _(np, plt):
    def draw_invariant_views(E_vec, B_vec, coeffs, scalar_inv, pseudo_inv):
        _fig = plt.figure(figsize=(11.4, 5.2))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _ax1.quiver(0, 0, 0, E_vec[0], E_vec[1], E_vec[2], color="crimson", linewidth=2.5)
        _ax1.quiver(0, 0, 0, B_vec[0], B_vec[1], B_vec[2], color="steelblue", linewidth=2.5)
        _ax1.set_xlim(-2.5, 2.5)
        _ax1.set_ylim(-2.5, 2.5)
        _ax1.set_zlim(-2.5, 2.5)
        _ax1.set_xlabel(r"$\sigma_1$")
        _ax1.set_ylabel(r"$\sigma_2$")
        _ax1.set_zlabel(r"$\sigma_3$")
        _ax1.set_title("Observer-relative E and B")
        _ax1.plot([], [], color="crimson", label="E")
        _ax1.plot([], [], color="steelblue", label="B")
        _ax1.legend(loc="upper left")

        _labels = [r"$\gamma_1\gamma_0$", r"$\gamma_2\gamma_0$", r"$\gamma_3\gamma_0$", r"$\gamma_2\gamma_3$", r"$\gamma_3\gamma_1$", r"$\gamma_1\gamma_2$"]
        _x = np.arange(len(_labels))
        _ax2.bar(_x, coeffs, color=["crimson", "crimson", "crimson", "steelblue", "steelblue", "steelblue"], alpha=0.82)
        _ax2.axhline(0, color="black", linewidth=0.8)
        _ax2.set_xticks(_x, _labels)
        _ax2.set_ylim(-2.5, 2.5)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title(rf"$\langle F^2 \rangle_0 = {scalar_inv:.3f},\;\; \langle F^2 \rangle_4 = {pseudo_inv:.3f}$")

        plt.close(_fig)
        return _fig

    return (draw_invariant_views,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Electromagnetic Invariants

    The square of the Faraday bivector carries the invariant content of the field. In spacetime algebra this is a direct algebraic statement, not a separate collection of memorized formulas.

    This notebook follows [electromagnetism_one_bivector.py](./electromagnetism_one_bivector.py): there the emphasis is on assembling $F$, while here the emphasis is on reading the field classification out of $F^2$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    For

    $$
    F = E + I B,
    $$

    the square

    $$
    F^2
    $$

    has:

    - a scalar part that distinguishes electric-dominated from magnetic-dominated configurations
    - a pseudoscalar part that measures the $E \cdot B$ coupling
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    I = sta.I.name("I")
    s1 = (g1 * g0).name(latex=r"\sigma_1")
    s2 = (g2 * g0).name(latex=r"\sigma_2")
    s3 = (g3 * g0).name(latex=r"\sigma_3")
    return I, g0, g1, g2, g3, s1, s2, s3


@app.cell
def _(mo):
    ex = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.2, label="E along σ1", show_value=True)
    ey = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="E along σ2", show_value=True)
    bx = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="B along σ1", show_value=True)
    bz = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.8, label="B along σ3", show_value=True)
    return bx, bz, ex, ey


@app.cell
def _(I, bx, bz, draw_invariant_views, ex, ey, g1, g2, g3, gm, grade, mo, np, s1, s2, s3):
    _E = (ex.value * s1 + ey.value * s2).name("E")
    _B = (bx.value * s1 + bz.value * s3).name("B")
    _F = (_E + I * _B).name("F")
    _F2 = (_F * _F).name(latex=r"F^2")
    _scalar = grade(_F2, 0).name(latex=r"\langle F^2 \rangle_0")
    _pseudo = grade(_F2, 4).name(latex=r"\langle F^2 \rangle_4")

    _scalar_value = float(_scalar.eval().scalar_part)
    _pseudo_value = float((_pseudo.eval() * ~I.eval()).scalar_part) if np.any(np.abs(_pseudo.eval().data) > 1e-12) else 0.0

    if abs(_scalar_value) < 1e-9:
        _class = "balanced / null-like threshold"
    elif _scalar_value > 0:
        _class = "electric-dominated"
    else:
        _class = "magnetic-dominated"

    _basis_bivectors = [g1 * g0, g2 * g0, g3 * g0, g2 * g3, g3 * g1, g1 * g2]
    _coeffs = np.array(
        [(_F | _basis).scalar_part / (_basis | _basis).scalar_part for _basis in _basis_bivectors],
        dtype=float,
    )
    _E_vec = np.array([ex.value, ey.value, 0.0], dtype=float)
    _B_vec = np.array([bx.value, 0.0, bz.value], dtype=float)

    _md = t"""
    {_E.display()} <br/>
    {_B.display()} <br/>
    {_F.display()} <br/>
    {_F2.display()} <br/>
    {_scalar.display()} <br/>
    {_pseudo.display()} <br/>
    Classification: **{_class}**
    """

    mo.vstack([ex, ey, bx, bz, gm.md(_md), draw_invariant_views(_E_vec, _B_vec, _coeffs, _scalar_value, _pseudo_value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The invariant content is encoded in one algebraic object, $F^2$. That is one of the clearest examples of STA turning several familiar formulas into one geometric statement.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
