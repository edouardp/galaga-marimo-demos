import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pauli Matrices vs Geometric Algebra

    This notebook compares two descriptions of the same spin-$1/2$ structure:

    - Pauli matrices and 2-component spinors
    - $\mathrm{Cl}(3,0)$ vectors, bivectors, and rotors

    The goal is not to hide the matrix side. The goal is to show how much of it
    is just the Pauli/Clifford algebra written in a particular representation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ and compare it with the Pauli matrices.

    The dictionary used here is:

    $$
    e_1 \leftrightarrow \sigma_x,
    \qquad
    e_2 \leftrightarrow \sigma_y,
    \qquad
    e_3 \leftrightarrow \sigma_z,
    $$

    and for bivectors:

    $$
    e_{23} \leftrightarrow i\sigma_x,
    \qquad
    e_{31} \leftrightarrow i\sigma_y,
    \qquad
    e_{12} \leftrightarrow i\sigma_z.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    e23 = (e2 * e3).name(latex=r"e_{23}")
    e31 = (e3 * e1).name(latex=r"e_{31}")
    e12 = (e1 * e2).name(latex=r"e_{12}")
    return e12, e23, e3, e31


@app.cell
def _(np):
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    eye2 = np.eye(2, dtype=complex)
    return eye2, sigma_x, sigma_y, sigma_z


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One State and One Rotation

    The state rotor is

    $$
    \psi = e^{-(\phi/2)e_{12}} e^{-(\theta/2)e_{31}},
    $$

    which rotates the reference direction $e_3$ into the Bloch vector

    $$
    s = \psi e_3 \tilde\psi.
    $$

    Then we compare a further $z$-axis rotation on both sides.
    """)
    return


@app.cell
def _(mo):
    theta = mo.ui.slider(0, 180, step=1, value=55, label="Polar angle θ", show_value=True)
    phi = mo.ui.slider(0, 360, step=1, value=35, label="Azimuth φ", show_value=True)
    alpha = mo.ui.slider(0, 360, step=1, value=70, label="Rotation angle α about z", show_value=True)
    return alpha, phi, theta


@app.cell
def _(
    alpha,
    draw_pauli_vs_ga,
    e12,
    e3,
    e31,
    exp,
    ga_rotor_to_su2,
    gm,
    matrix_to_latex,
    mo,
    np,
    pauli_observable_from_vector,
    phi,
    sigma_z,
    spinor_to_latex,
    theta,
    vector_operator_latex,
):
    _theta = np.radians(theta.value)
    _phi = np.radians(phi.value)
    _alpha = np.radians(alpha.value)

    _psi = (exp((-_phi / 2) * e12) * exp((-_theta / 2) * e31)).name(latex=r"\psi")
    _spin = (_psi * e3 * ~_psi).name("s")

    _U_state = ga_rotor_to_su2(_psi.eval())
    _ket = _U_state @ np.array([[1.0], [0.0]], dtype=complex)
    _sigma_s = pauli_observable_from_vector(_spin.eval())

    _Rz = exp((-_alpha / 2) * e12).name(latex=r"R_z")
    _U_z = np.cos(_alpha / 2) * np.eye(2, dtype=complex) - 1j * np.sin(_alpha / 2) * sigma_z
    _spin_rot = (_Rz * _spin * ~_Rz).name(latex=r"s'")
    _sigma_s_rot = pauli_observable_from_vector(_spin_rot.eval())
    _ket_rot = _U_z @ _ket

    _md = rf"""
    ### Basis and Generators

    GA vector observable:
    ${_spin.eval().latex()}$

    Pauli operator:
    {vector_operator_latex(_sigma_s)}

    GA state rotor:
    ${_psi.eval().latex()}$

    Matching SU(2) matrix:
    {matrix_to_latex(_U_state)}

    Matching 2-spinor on $\lvert 0 \rangle$:
    {spinor_to_latex(_ket)}

    ### After the $z$ Rotation

    GA rotor:
    ${_Rz.eval().latex()}$

    Pauli matrix:
    {matrix_to_latex(_U_z)}

    Rotated GA observable:
    ${_spin_rot.eval().latex()}$

    Rotated Pauli operator:
    {vector_operator_latex(_sigma_s_rot)}

    Rotated 2-spinor:
    {spinor_to_latex(_ket_rot)}
    """

    mo.vstack([theta, phi, alpha, gm.md(_md), draw_pauli_vs_ga(_spin.eval(), _spin_rot.eval())])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    On the matrix side, vectors become Hermitian operators and rotations become
    unitary conjugations. On the GA side, vectors stay vectors and rotations stay
    rotor sandwiches. The structures match because they are two representations of
    the same Pauli/Clifford algebra.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(e12, e23, e31, eye2, np, plt, sigma_x, sigma_y, sigma_z):
    def _fmt_real(x):
        if abs(x) < 1e-10:
            x = 0.0
        return f"{x:.3f}"

    def _fmt_complex(z):
        if abs(z.real) < 1e-10:
            z = complex(0.0, z.imag)
        if abs(z.imag) < 1e-10:
            return _fmt_real(z.real)
        if abs(z.real) < 1e-10:
            return f"{_fmt_real(z.imag)}i"
        sign = "+" if z.imag >= 0 else "-"
        return f"{_fmt_real(z.real)} {sign} {_fmt_real(abs(z.imag))}i"

    def matrix_to_latex(M):
        _rows = []
        for _row in M:
            _rows.append(" & ".join(_fmt_complex(complex(_entry)) for _entry in _row))
        return r"$$\begin{pmatrix}" + r"\\".join(_rows) + r"\end{pmatrix}$$"

    def spinor_to_latex(psi):
        return matrix_to_latex(psi)

    def ga_rotor_to_su2(rotor):
        _scalar = rotor.scalar_part
        _b23 = (rotor | e23).scalar_part / ((e23 | e23).scalar_part)
        _b31 = (rotor | e31).scalar_part / ((e31 | e31).scalar_part)
        _b12 = (rotor | e12).scalar_part / ((e12 | e12).scalar_part)
        return _scalar * eye2 + 1j * (_b23 * sigma_x + _b31 * sigma_y + _b12 * sigma_z)

    def pauli_observable_from_vector(v):
        _parts = np.array(v.vector_part[:3], dtype=float)
        return _parts[0] * sigma_x + _parts[1] * sigma_y + _parts[2] * sigma_z

    def vector_operator_latex(M):
        return matrix_to_latex(M)

    def draw_pauli_vs_ga(spin, rotated_spin):
        _spin = np.array(spin.vector_part[:3], dtype=float)
        _rot = np.array(rotated_spin.vector_part[:3], dtype=float)

        _fig = plt.figure(figsize=(7.0, 6.2))
        _ax = _fig.add_subplot(111, projection="3d")
        _u = np.linspace(0, 2 * np.pi, 32)
        _v = np.linspace(0, np.pi, 16)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08)
        _ax.quiver(0, 0, 0, _spin[0], _spin[1], _spin[2], color="#2563eb", linewidth=2.5, arrow_length_ratio=0.1)
        _ax.quiver(0, 0, 0, _rot[0], _rot[1], _rot[2], color="#d62828", linewidth=2.5, arrow_length_ratio=0.1)
        _ax.set_xlim(-1, 1)
        _ax.set_ylim(-1, 1)
        _ax.set_zlim(-1, 1)
        _ax.set_box_aspect((1, 1, 1))
        _ax.set_title("One Bloch sphere, two languages")
        plt.close(_fig)
        return _fig

    return (
        draw_pauli_vs_ga,
        ga_rotor_to_su2,
        matrix_to_latex,
        pauli_observable_from_vector,
        spinor_to_latex,
        vector_operator_latex,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
