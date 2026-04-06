import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Density Matrices and the Bloch Ball

    Pure qubit states lie on the Bloch sphere. Mixed states live inside it. The
    missing ingredient is purity: once the state is no longer fully coherent, the
    Bloch vector shrinks away from the surface.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$ and keep the state description geometric.

    A pure-state direction is

    $$
    s = R e_3 \widetilde R.
    $$

    A mixed state can be represented by a Bloch vector of length at most one:

    $$
    \rho = \frac{1 + r}{2},
    \qquad
    |r| \le 1.
    $$

    The purity is

    $$
    \mathrm{Tr}(\rho^2) = \frac{1 + |r|^2}{2}.
    $$
    """)
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1, 1), blades=b_default())
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    theta = mo.ui.slider(0, 180, step=1, value=55, label="Polar angle θ", show_value=True)
    phi = mo.ui.slider(0, 360, step=1, value=35, label="Azimuth φ", show_value=True)
    purity_mix = mo.ui.slider(0.0, 1.0, step=0.01, value=1.0, label="Bloch radius |r|", show_value=True)
    return phi, purity_mix, theta


@app.cell
def _(alg, density_bloch_plot, e1, e2, e3, exp, gm, mo, np, phi, purity_mix, theta):
    half = alg.frac(1, 2)
    _theta = np.radians(theta.value)
    _phi = np.radians(phi.value)

    R = (exp(-(_phi / 2) * (e1 * e2)) * exp(-(_theta / 2) * (e3 * e1))).name(latex="R")
    s = (R * e3 * ~R).name(latex="s")
    r = (purity_mix.value * s).name(latex="r")
    rho = (half * (alg.scalar(1).name(latex="1") + r)).name(latex=r"\rho")
    purity = (half * (alg.scalar(1).name(latex="1") + (r | r))).name(latex=r"\mathrm{Tr}(\rho^2)")
    p0 = (half * (alg.scalar(1).name(latex="1") + (r | e3))).name(latex=r"P(0)")
    p1 = (half * (alg.scalar(1).name(latex="1") - (r | e3))).name(latex=r"P(1)")

    _state_kind = "pure" if abs(purity_mix.value - 1.0) < 1e-9 else "mixed" if purity_mix.value > 1e-9 else "maximally mixed"
    _md = t"""
    {R.display()} <br/>
    {s.display()} <br/>
    {r.display()} <br/>
    {rho.display()} <br/>
    {purity.display()} <br/>
    {p0.display()} <br/>
    {p1.display()} <br/>
    This is a {_state_kind} state. As $|r|$ shrinks, the state moves from the Bloch sphere into the Bloch ball.
    """

    mo.vstack([theta, phi, purity_mix, gm.md(_md), density_bloch_plot(r, purity.scalar_part, p0.scalar_part, p1.scalar_part)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The Bloch sphere is only the pure-state boundary. The full state space is the
    Bloch ball, and the radius of the Bloch vector directly measures how mixed the
    state is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def density_bloch_plot(r, purity, p0, p1):
        _r = np.array(r.eval().vector_part, dtype=float)
        _fig = plt.figure(figsize=(12.0, 5.3))
        _ax0 = _fig.add_subplot(121, projection="3d")
        _ax1 = _fig.add_subplot(122)

        _u = np.linspace(0, 2 * np.pi, 36)
        _v = np.linspace(0, np.pi, 18)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax0.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08, linewidth=0.6)
        _ax0.quiver(0, 0, 0, _r[0], _r[1], _r[2], color="#7c3aed", linewidth=3.0, arrow_length_ratio=0.1)
        _ax0.set_xlim(-1, 1)
        _ax0.set_ylim(-1, 1)
        _ax0.set_zlim(-1, 1)
        _ax0.set_box_aspect((1, 1, 1))
        _ax0.set_xlabel("e1")
        _ax0.set_ylabel("e2")
        _ax0.set_zlabel("e3")
        _ax0.set_title("Bloch ball: mixed states live inside")

        _ax1.bar([0, 1, 2], [np.linalg.norm(_r), purity, p0 - p1], color=["#7c3aed", "#2563eb", "#d62828"], alpha=0.84)
        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.45)
        _ax1.set_xticks([0, 1, 2], [r"$|r|$", r"$\mathrm{Tr}(\rho^2)$", r"$P(0)-P(1)$"])
        _ax1.set_ylim(-1.05, 1.05)
        _ax1.grid(True, axis="y", alpha=0.18)
        _ax1.set_title("Radius, purity, and z-bias")

        plt.close(_fig)
        return _fig

    return (density_bloch_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
