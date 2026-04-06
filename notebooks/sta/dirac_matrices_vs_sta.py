import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, b_sta, exp, gm, mo, np, plt, sandwich


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Dirac Matrices vs Spacetime Algebra

    This notebook compares two ways of expressing the same relativistic
    structure:

    - Dirac gamma matrices acting in a chosen matrix representation
    - STA basis vectors and multivectors inside the algebra itself

    The point is not that matrices are “wrong.” The point is that much of the
    matrix machinery is a representation of the spacetime Clifford algebra.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    The notebook keeps to two comparisons:

    - the gamma algebra itself
    - one boost and one on-shell momentum example
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before the comparison starts, it is worth fixing notation:

    - $\Gamma_\mu$ means a concrete $4\times4$ Dirac gamma matrix in one chosen matrix representation
    - $\gamma_\mu$ means the corresponding basis vector inside the spacetime algebra itself

    So the capital letter is the matrix representative, while the lowercase letter is the geometric algebra element being represented.
    """)
    return


@app.cell
def _(Algebra, b_sta):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, g2, g3


@app.cell
def _(np):
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    zero = np.zeros((2, 2), dtype=complex)
    eye2 = np.eye(2, dtype=complex)

    gamma0 = np.block([[eye2, zero], [zero, -eye2]])
    gamma1 = np.block([[zero, sigma_x], [-sigma_x, zero]])
    gamma2 = np.block([[zero, sigma_y], [-sigma_y, zero]])
    gamma3 = np.block([[zero, sigma_z], [-sigma_z, zero]])
    return gamma0, gamma1, gamma2, gamma3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Same Clifford Relation

    The Dirac matrices satisfy

    $$
    \{\Gamma_\mu,\Gamma_\nu\} = 2\eta_{\mu\nu} I_4.
    $$

    The STA basis vectors satisfy the same Clifford relation directly:

    $$
    \gamma_\mu\gamma_\nu + \gamma_\nu\gamma_\mu = 2\eta_{\mu\nu}.
    $$
    """)
    return


@app.cell
def _(g0, g1, g2, g3, gamma0, gamma1, gamma2, gamma3, gm, matrix_to_latex):
    _anticomm_01 = gamma0 @ gamma1 + gamma1 @ gamma0
    _sta_anticomm_01 = (g0 * g1 + g1 * g0).eval()

    _md = rf"""
    | Object | Matrix side | STA side |
    |---|---|---|
    | $\Gamma_0 / \gamma_0$ | ${matrix_to_latex(gamma0)}$ | ${g0.eval().latex()}$ |
    | $\Gamma_1 / \gamma_1$ | ${matrix_to_latex(gamma1)}$ | ${g1.eval().latex()}$ |
    | $\Gamma_2 / \gamma_2$ | ${matrix_to_latex(gamma2)}$ | ${g2.eval().latex()}$ |
    | $\Gamma_3 / \gamma_3$ | ${matrix_to_latex(gamma3)}$ | ${g3.eval().latex()}$ |
    | $\{{\Gamma_0,\Gamma_1\}} / \gamma_0\gamma_1 + \gamma_1\gamma_0$ | ${matrix_to_latex(_anticomm_01)}$ | ${_sta_anticomm_01.latex()}$ |
    """
    gm.md(_md)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Boost and One Momentum

    A boost in the $x$ direction is

    $$
    R = e^{(\varphi/2)\gamma_0\gamma_1}
    $$

    in STA, while the matrix side uses the corresponding Dirac boost operator.

    For momentum, the matrix formalism often uses the slashed operator
    $\Gamma^\mu p_\mu - m$. In STA, the same momentum is simply a spacetime
    vector with the on-shell condition $p^2 = m^2$.
    """)
    return


@app.cell
def _(mo):
    rapidity = mo.ui.slider(0.0, 3.0, step=0.02, value=0.9, label="Boost rapidity φ", show_value=True)
    mass = mo.ui.slider(0.1, 5.0, step=0.1, value=1.0, label="Mass m", show_value=True)
    px = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.8, label="Momentum p_x", show_value=True)
    py = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.0, label="Momentum p_y", show_value=True)
    pz = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.0, label="Momentum p_z", show_value=True)
    return mass, px, py, pz, rapidity


@app.cell
def _(
    draw_dirac_vs_sta,
    exp,
    g0,
    g1,
    g2,
    g3,
    gamma0,
    gamma1,
    gamma2,
    gamma3,
    gm,
    mass,
    matrix_to_latex,
    mo,
    np,
    px,
    py,
    pz,
    rapidity,
    sandwich,
):
    _phi = rapidity.value
    _R = exp((_phi / 2) * (g0 * g1)).name("R")
    _boosted_time_axis = sandwich(_R, g0).name(latex=r"\gamma_0'")
    _boosted_x_axis = sandwich(_R, g1).name(latex=r"\gamma_1'")

    _alpha1 = gamma0 @ gamma1
    _S = np.cosh(_phi / 2) * np.eye(4, dtype=complex) + np.sinh(_phi / 2) * _alpha1

    _m = mass.value
    _px = px.value
    _py = py.value
    _pz = pz.value
    _E = np.sqrt(_m**2 + _px**2 + _py**2 + _pz**2)
    _p = (_E * g0 + _px * g1 + _py * g2 + _pz * g3).eval().name("p")
    _slash = _E * gamma0 - _px * gamma1 - _py * gamma2 - _pz * gamma3
    _dirac_matrix = _slash - _m * np.eye(4, dtype=complex)

    _md = t"""
    {_R.display()} <br/>
    {_boosted_time_axis.display()} <br/>
    {_boosted_x_axis.display()} <br/>
    {_p.display()} <br/>
    $p^2 = {(_p * _p).eval().latex()}$ <br/>
    Dirac boost matrix:
    $$
    {matrix_to_latex(_S)}
    $$
    <br/>
    Slashed operator minus mass:
    $$
    {matrix_to_latex(_dirac_matrix)}
    $$
    """

    mo.vstack(
        [
            rapidity,
            mass,
            px,
            py,
            pz,
            gm.md(_md),
            draw_dirac_vs_sta(_boosted_time_axis.eval(), _boosted_x_axis.eval(), _E, _px, _py, _pz, _m),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The matrix side chooses a representation. STA keeps the geometry in the
    algebra itself. The boost and on-shell momentum are not different physics in
    the two languages; they are the same Clifford structure expressed in two ways.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _fmt_real(x):
        if abs(x) < 1e-10:
            return "0"
        if abs(x - round(x)) < 1e-10:
            return str(int(round(x)))
        return f"{x:.3f}"

    def _fmt_entry(z):
        z = complex(z)
        if abs(z.real) < 1e-10:
            z = complex(0.0, z.imag)
        if abs(z.imag) < 1e-10:
            return _fmt_real(z.real)
        if abs(z.real) < 1e-10:
            if abs(z.imag - 1.0) < 1e-10:
                return "i"
            if abs(z.imag + 1.0) < 1e-10:
                return "-i"
            return f"{_fmt_real(z.imag)}i"
        sign = "+" if z.imag >= 0 else "-"
        _imag = abs(z.imag)
        _imag_str = "i" if abs(_imag - 1.0) < 1e-10 else f"{_fmt_real(_imag)}i"
        return f"{_fmt_real(z.real)} {sign} {_imag_str}"

    def matrix_to_latex(M):
        _rows = []
        for _row in M:
            _rows.append(" & ".join(_fmt_entry(_entry) for _entry in _row))
        return r"\begin{pmatrix}" + r"\\".join(_rows) + r"\end{pmatrix}"

    def draw_dirac_vs_sta(boosted_time_axis, boosted_x_axis, E, px, py, pz, mass):
        _time = np.array(boosted_time_axis.vector_part[:2], dtype=float)
        _space = np.array(boosted_x_axis.vector_part[:2], dtype=float)
        _arrow_scale = 1.6
        _extent = max(4.0, _arrow_scale * np.max(np.abs(np.concatenate([_time, _space]))) + 0.6)
        _momentum_extent = max(4.0, np.max(np.abs([E, px, py, pz, mass])) + 0.6)

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.4, 5.0))
        _cone = np.linspace(-_extent, _extent, 300)
        _ax1.plot(_cone, _cone, "k--", alpha=0.25)
        _ax1.plot(_cone, -_cone, "k--", alpha=0.25)
        _ax1.annotate("", xy=(0, _arrow_scale), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.3))
        _ax1.annotate("", xy=(_arrow_scale, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.3))
        _ax1.annotate("", xy=(_arrow_scale * _time[0], _arrow_scale * _time[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.5))
        _ax1.annotate("", xy=(_arrow_scale * _space[0], _arrow_scale * _space[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#f59e0b", lw=2.5))
        _ax1.set_aspect("equal")
        _ax1.set_xlim(-_extent, _extent)
        _ax1.set_ylim(-_extent, _extent)
        _ax1.grid(True, alpha=0.25)
        _ax1.set_xlabel("x")
        _ax1.set_ylabel("t")
        _ax1.set_title("STA boost geometry")

        _ax2.bar(
            [0, 1, 2, 3, 4],
            [E, px, py, pz, mass],
            color=["#2563eb", "#d62828", "#d62828", "#d62828", "#222222"],
            alpha=0.82,
            width=0.6,
        )
        _ax2.set_xticks([0, 1, 2, 3, 4], ["E", "p_x", "p_y", "p_z", "m"])
        _ax2.set_ylim(-_momentum_extent, _momentum_extent)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title("On-shell momentum data")

        plt.close(_fig)
        return _fig

    return draw_dirac_vs_sta, matrix_to_latex


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
