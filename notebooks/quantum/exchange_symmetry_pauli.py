import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, simplify
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exchange Symmetry and Pauli Exclusion

    The Pauli exclusion principle is not the same thing as the single-particle
    spinor sign under a $2\pi$ rotation. Exclusion is a two-particle statement:
    identical fermions must occupy an antisymmetric joint state under exchange.

    This notebook shows that directly for two spin-$1/2$ states.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ only to keep contact with the Bloch-sphere picture.

    Particle A is fixed in the reference direction $e_3$. Particle B is prepared
    by a rotor and then read through its direction vector.

    For one-particle rotor states $R_A$ and $R_B$, the corresponding observable
    directions are

    $$
    s_A = R_A e_3 \widetilde R_A,
    \qquad
    s_B = R_B e_3 \widetilde R_B.
    $$

    The two-particle combinations are then read through the symmetric and
    antisymmetric exchange sectors

    $$
    |\Psi_{\pm}\rangle = \frac{1}{\sqrt{2}}\left(|a\rangle\otimes|b\rangle \pm |b\rangle\otimes|a\rangle\right).
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    e12 = (e1 * e2).eval()
    e31 = (e3 * e1).eval()
    return alg, e12, e3, e31


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pure GA Antisymmetrization

    First read this as an algebraic statement, not yet as a story about two
    physical particles.

    Given two one-particle states $|a\rangle$ and $|b\rangle$, form

    $$
    |\Psi_{\pm}\rangle = \frac{1}{\sqrt{2}}\left(|a\rangle\otimes|b\rangle \pm |b\rangle\otimes|a\rangle\right).
    $$

    The antisymmetric combination vanishes exactly when the two one-particle
    states are identical. The key point here is just the algebra of
    symmetrizing and antisymmetrizing.
    """)
    return


@app.cell
def _(mo):
    theta_b = mo.ui.slider(0, 180, step=1, value=60, label="Particle B polar angle θ", show_value=True)
    phi_b = mo.ui.slider(0, 360, step=1, value=40, label="Particle B azimuth φ", show_value=True)
    return phi_b, theta_b


@app.cell
def _(alg, e12, e3, e31, exp, np, phi_b, theta_b):
    _theta = alg.scalar(np.radians(theta_b.value)).name(latex=r"\theta")
    _phi = alg.scalar(np.radians(phi_b.value)).name(latex=r"\phi")

    R_A = (1 + 0 * e12).name(latex=r"R_A")
    R_B = (exp(-_phi * e12 / 2) * exp(-_theta * e31 / 2)).name(latex=r"R_B")
    bloch_A = (R_A * e3 * ~R_A).name(latex=r"s_A")
    bloch_B = (R_B * e3 * ~R_B).name(latex=r"s_B")
    overlap_sq = (1.0 + (bloch_A | bloch_B)) / 2.0
    sym_norm = 1.0 + overlap_sq
    anti_norm = 1.0 - overlap_sq
    return R_A, R_B, anti_norm, bloch_A, bloch_B, overlap_sq, sym_norm


@app.cell
def _(bloch_A):
    bloch_A.display()
    return


@app.cell
def _(
    R_A,
    R_B,
    anti_norm,
    bloch_A,
    bloch_B,
    gm,
    mo,
    overlap_sq,
    phi_b,
    sym_norm,
    theta_b,
):
    _md = t"""
    Take the reference rotor <br/>
    {R_A.display()} <br/>
    and the varied rotor <br/>
    {R_B.display()}

    These determine the observable directions <br/>
    {bloch_A.display()} <br/> {bloch_B.display()}

    In this notebook we use the GA overlap magnitude
    $|\\langle a|b\\rangle|^2 =$  {overlap_sq.display():.4f}

    So the exchange sectors have norms

    $\\lVert \\Psi_+ \\rVert^2 =$ {sym_norm:.4f}, $\\qquad \\lVert \\Psi_- \\rVert^2 =$ {anti_norm:.4f}

    When the two one-particle directions coincide, $s_B = s_A$, the overlap
    magnitude becomes $1$ and the antisymmetric sector collapses to zero.
    That is the algebraic cancellation we reinterpret physically below.
    """

    mo.vstack([theta_b, phi_b, gm.md(_md)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Physical Interpretation

    Now read the same antisymmetrization as a physical two-particle statement.
    Nothing in the algebra changes; only the interpretation changes.

    Particle A is fixed along $e_3$. Particle B is varied on the Bloch sphere.

    For identical fermions, the antisymmetric exchange sector is the physically
    relevant one. When the one-particle states become identical, that allowed
    antisymmetric state disappears. That is the exclusion point.
    """)
    return


@app.cell
def _(
    anti_norm,
    bloch_B,
    draw_exchange_symmetry,
    gm,
    mo,
    phi_b,
    sym_norm,
    theta_b,
):
    _md = rf"""
    Fixed particle A:
    $$|a\rangle = \begin{{pmatrix}}1\\0\end{{pmatrix}}, \qquad s_A = e_3.$$

    The second particle moves over the Bloch sphere.

    The symmetric two-particle sector has norm
    $$\lVert \Psi_+ \rVert^2 = {sym_norm:.4f},$$

    while the antisymmetric sector has norm
    $$\lVert \Psi_- \rVert^2 = {anti_norm:.4f}.$$

    For identical fermions, that antisymmetric sector is the relevant one.
    """

    mo.vstack([gm.md(_md), draw_exchange_symmetry(bloch_B, sym_norm.scalar_part, anti_norm.scalar_part, theta_b.value, phi_b.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_exchange_symmetry(bloch_B, sym_norm, anti_norm, theta_deg, phi_deg):
        _B = np.array(bloch_B.vector_part[:3], dtype=float)

        _fig = plt.figure(figsize=(12.4, 5.0))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _u = np.linspace(0, 2 * np.pi, 32)
        _v = np.linspace(0, np.pi, 16)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax1.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08)
        _ax1.quiver(0, 0, 0, 0, 0, 1, color="#2563eb", linewidth=2.8, arrow_length_ratio=0.1)
        _ax1.quiver(0, 0, 0, _B[0], _B[1], _B[2], color="#d62828", linewidth=2.5, arrow_length_ratio=0.1)
        _ax1.set_xlim(-1, 1)
        _ax1.set_ylim(-1, 1)
        _ax1.set_zlim(-1, 1)
        _ax1.set_box_aspect((1, 1, 1))
        _ax1.set_title("One-particle Bloch directions")

        _ax2.bar([0, 1], [sym_norm, anti_norm], color=["#2563eb", "#d62828"], alpha=0.82, width=0.6)
        _ax2.set_xticks([0, 1], [r"$\|\Psi_+\|^2$", r"$\|\Psi_-\|^2$"])
        _ax2.set_ylim(0, 2.05)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title(f"Exchange sectors for θ={theta_deg}°, φ={phi_deg}°")

        plt.close(_fig)
        return _fig

    return (draw_exchange_symmetry,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
