import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_bloch_state(state):
        _s = np.array(state.eval().vector_part, dtype=float)

        _fig = plt.figure(figsize=(8.0, 6.0))
        _ax = _fig.add_subplot(111, projection="3d")

        _u = np.linspace(0, 2 * np.pi, 40)
        _v = np.linspace(0, np.pi, 24)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax.plot_wireframe(_x, _y, _z, color="gray", alpha=0.10, linewidth=0.6)

        _ax.quiver(0, 0, 0, 1, 0, 0, color="#2563eb", linewidth=1.8, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 1, 0, color="#16a34a", linewidth=1.8, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 0, 1, color="#d62828", linewidth=2.2, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 0, -1, color="#d62828", linewidth=1.5, alpha=0.35, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, _s[0], _s[1], _s[2], color="#7c3aed", linewidth=3.0, arrow_length_ratio=0.10)

        _ax.text(1.08, 0, 0, r"$+e_1\;( |+\rangle )$", color="#2563eb")
        _ax.text(0, 1.08, 0, r"$+e_2$", color="#16a34a")
        _ax.text(0, 0, 1.10, r"$+e_3\;( |0\rangle )$", color="#d62828")
        _ax.text(0, 0, -1.18, r"$-e_3\;( |1\rangle )$", color="#d62828")

        _ax.set_xlim(-1.1, 1.1)
        _ax.set_ylim(-1.1, 1.1)
        _ax.set_zlim(-1.1, 1.1)
        _ax.set_box_aspect((1, 1, 1))
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Superposition as a Bloch-sphere direction")
        plt.close(_fig)
        return _fig

    return (draw_bloch_state,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Qubit Superposition in Geometric Algebra

    In ordinary quantum notation, a qubit is written as

    $$
    |\psi\rangle = \alpha |0\rangle + \beta |1\rangle,
    \qquad |\alpha|^2 + |\beta|^2 = 1.
    $$

    In geometric algebra, the same pure state can be represented by a rotor. The key observable is the Bloch vector

    $$
    s = \psi e_3 \tilde{\psi}.
    $$

    The point of this notebook is that **superposition is not a separate mysterious ingredient**. It is just a pure state whose Bloch vector is not sitting at either pole.

    This reimplements the idea of the upstream `qubits_and_superposition_ga.py` example, but in the shorter concept-first style used in this repo.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    A qubit rotor can rotate the reference axis $e_3$ into any point on the Bloch sphere. Relative to the computational basis:

    - $|0\rangle$ sits at $+e_3$
    - $|1\rangle$ sits at $-e_3$
    - equal superpositions live away from those poles

    The notebook keeps the standard qubit angles:

    $$
    \psi = e^{-(\phi/2)e_{12}} e^{-(\theta/2)e_{31}},
    \qquad
    \alpha = \cos(\theta/2), \quad
    \beta = e^{i\phi}\sin(\theta/2).
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(mo):
    theta = mo.ui.slider(0, 180, step=1, value=60, label="Weight angle θ", show_value=True)
    phi = mo.ui.slider(0, 360, step=1, value=30, label="Relative phase φ", show_value=True)
    return phi, theta


@app.cell
def _(draw_bloch_state, e1, e2, e3, exp, gm, mo, np, phi, theta):
    _theta = np.radians(theta.value)
    _phi = np.radians(phi.value)

    _psi = (exp((-_phi / 2) * (e1 * e2)) * exp((-_theta / 2) * (e3 * e1))).name(latex=r"\psi")
    _s = (_psi * e3 * ~_psi).name("s")
    _s_xyz = _s.eval().vector_part

    _alpha_real = np.cos(_theta / 2)
    _beta_mag = np.sin(_theta / 2)
    _beta_real = _beta_mag * np.cos(_phi)
    _beta_imag = _beta_mag * np.sin(_phi)
    _p0 = 0.5 * (1 + _s_xyz[2])
    _p1 = 0.5 * (1 - _s_xyz[2])

    _state_label = (
        "computational basis state |0⟩"
        if np.isclose(_p0, 1.0) else
        "computational basis state |1⟩"
        if np.isclose(_p1, 1.0) else
        "genuine superposition of |0⟩ and |1⟩"
    )

    _md = t"""
    {_psi.display()} <br/>
    {_s.display()} <br/>
    Bloch vector: $({_s_xyz[0]:.3f}, {_s_xyz[1]:.3f}, {_s_xyz[2]:.3f})$ <br/>
    $\\alpha = {_alpha_real:.3f}$ <br/>
    $\\beta = {_beta_real:+.3f} {_beta_imag:+.3f} i$ <br/>
    $P(0) = {_p0:.3f}, \\qquad P(1) = {_p1:.3f}$ <br/>
    Interpretation: {_state_label}.
    """

    mo.vstack(
        [
            theta,
            phi,
            gm.md(_md),
            draw_bloch_state(_s),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In the GA picture, a pure qubit state is a rotor and its observable content is a direction on the Bloch sphere. Superposition means that the direction is not pinned to one of the computational-basis poles.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
