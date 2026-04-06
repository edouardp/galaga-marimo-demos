import marimo

__generated_with = "0.22.0"
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
    mo.md(
        r"""
    # Measurement and Interference in GA

    A useful single-qubit story is:

    1. start in $|0\rangle$
    2. create a superposition
    3. add a relative phase
    4. recombine and measure

    In GA, the phase is a rotor around the measurement axis. Interference appears
    when the final recombination turns that hidden phase back into a measurable
    population difference.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We work in $\mathrm{Cl}(3,0)$ and use the Bloch-vector picture.

    The sequence is Hadamard-like preparation, then a phase rotor around $e_3$,
    then the same Hadamard-like recombination again.
    """
    )
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    phase = mo.ui.slider(0.0, 360.0, step=1.0, value=60.0, label="Relative phase φ", show_value=True)
    return (phase,)


@app.cell
def _(draw_interference, e1, e2, e3, exp, gm, mo, np, phase):
    _phi = np.radians(phase.value)
    _ket0 = (1 + 0 * e1).name(latex=r"\psi_0")
    _hadamard = exp((-(np.pi) / 2) * ((e2 * e3 + e1 * e2) / np.sqrt(2))).name("H")
    _phase_rotor = exp((-_phi / 2) * (e1 * e2)).name(latex=r"R_\phi")

    _after_h = (_hadamard * _ket0).name(latex=r"\psi_1")
    _after_phase = (_phase_rotor * _after_h).name(latex=r"\psi_2")
    _final_state = (_hadamard * _after_phase).name(latex=r"\psi_f")
    _final_bloch = (_final_state * e3 * ~_final_state).eval().vector_part

    _p0 = 0.5 * (1 + _final_bloch[2])
    _p1 = 0.5 * (1 - _final_bloch[2])

    _md = t"""
    {_ket0.display()} <br/>
    {_hadamard.display()} <br/>
    {_phase_rotor.display()} <br/>
    {_after_h.display()} <br/>
    {_after_phase.display()} <br/>
    {_final_state.display()} <br/>
    $P(0) = {_p0:.4f}, \\qquad P(1) = {_p1:.4f}$ <br/>
    The middle phase rotor does not change the computational-basis measurement by itself. The final recombination is what converts that phase into interference.
    """

    mo.vstack([phase, gm.md(_md), draw_interference(_final_bloch, _p0, _p1, phase.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    Interference here is not a mysterious extra effect. The phase rotor stores
    information geometrically around the equator, and the final recombination
    turns it into a measurable $z$-population oscillation.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_interference(final_bloch, p0, p1, phase_deg):
        _fig = plt.figure(figsize=(11.2, 4.8))
        _ax1 = _fig.add_subplot(121)
        _ax2 = _fig.add_subplot(122, projection="3d")

        _phis = np.linspace(0, 2 * np.pi, 400)
        _curve = 0.5 * (1 + np.cos(_phis))
        _ax1.plot(np.degrees(_phis), _curve, color="#2563eb", linewidth=2.5)
        _ax1.plot([phase_deg], [p0], "o", color="#222222", ms=7)
        _ax1.set_xlabel("phase φ (degrees)")
        _ax1.set_ylabel("P(0)")
        _ax1.set_ylim(-0.05, 1.05)
        _ax1.grid(True, alpha=0.25)
        _ax1.set_title("Interference curve")

        _u = np.linspace(0, 2 * np.pi, 32)
        _v = np.linspace(0, np.pi, 16)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax2.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08)
        _ax2.quiver(0, 0, 0, final_bloch[0], final_bloch[1], final_bloch[2], color="#d62828", linewidth=2.6, arrow_length_ratio=0.1)
        _ax2.set_xlim(-1, 1)
        _ax2.set_ylim(-1, 1)
        _ax2.set_zlim(-1, 1)
        _ax2.set_box_aspect((1, 1, 1))
        _ax2.set_title(f"Final Bloch vector\nP(0)={p0:.3f}, P(1)={p1:.3f}")

        plt.close(_fig)
        return _fig

    return (draw_interference,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
