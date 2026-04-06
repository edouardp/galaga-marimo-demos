import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_default, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Celestial Circle at an Event

    At a spacetime event, future null directions form a sphere in 3+1 dimensions.
    In a 2+1 teaching slice, that becomes a circle. This is one of the cleanest
    real geometric precursors to twistor theory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In a 2+1 slice with basis vectors $\gamma_0, \gamma_1, \gamma_2$, choose a
    unit spatial direction

    $$
    n = \cos\phi \, \gamma_1 + \sin\phi \, \gamma_2.
    $$

    Then the corresponding future null direction is

    $$
    k = \gamma_0 + n,
    \qquad
    k^2 = 0.
    $$

    As $\phi$ changes, the null direction sweeps the celestial circle of the event.
    """)
    return


@app.cell
def _(Algebra, b_default):
    sta = Algebra((1, -1, -1), blades=b_default(prefix="e", start=0))
    e0, e1, e2 = sta.basis_vectors(lazy=True)
    g0 = e0.name(latex=r"\gamma_0")
    g1 = e1.name(latex=r"\gamma_1")
    g2 = e2.name(latex=r"\gamma_2")
    return g0, g1, g2, sta


@app.cell
def _(mo):
    phi = mo.ui.slider(0, 360, step=1, value=35, label="Spatial direction angle", show_value=True)
    return (phi,)


@app.cell
def _(celestial_circle_plot, g0, g1, g2, gm, mo, np, phi, sta):
    phi_mv = sta.scalar(np.radians(phi.value)).name(latex=r"\phi")
    n = (np.cos(phi_mv.scalar_part) * g1 + np.sin(phi_mv.scalar_part) * g2).name(latex="n")
    k = (g0 + n).name(latex="k")
    k_sq = (k * k).name(latex=r"k^2")

    _md = t"""
    {phi_mv.display()} <br/>
    {n.display()} <br/>
    {k.display()} <br/>
    {k_sq.display()} <br/>
    As the spatial unit vector runs around the ordinary circle, the future null
    direction runs around the celestial circle.
    """

    mo.vstack([phi, gm.md(_md), celestial_circle_plot(n)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Twistor theory is much deeper than this notebook, but the celestial sphere
    idea starts here: an event naturally comes with a family of null directions.
    In 2+1 dimensions that family is a circle, and in 3+1 it becomes a sphere.
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
    def celestial_circle_plot(n):
        _n = n.vector_part[:2]
        _t = np.linspace(0, 2 * np.pi, 240)

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10.2, 4.8))

        _ax1.plot(np.cos(_t), np.sin(_t), color="#999999", lw=1.0, alpha=0.35)
        _ax1.annotate("", xy=_n, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2.2))
        _ax1.set_xlim(-1.2, 1.2)
        _ax1.set_ylim(-1.2, 1.2)
        _ax1.set_aspect("equal")
        _ax1.grid(True, alpha=0.18)
        _ax1.set_xlabel("γ1")
        _ax1.set_ylabel("γ2")
        _ax1.set_title("Spatial unit direction")

        _ax2.plot(np.cos(_t), np.sin(_t), color="#999999", lw=1.0, alpha=0.35)
        _ax2.scatter([_n[0]], [_n[1]], color="#7c3aed", s=65)
        _ax2.text(_n[0] + 0.05, _n[1] + 0.05, "k", color="#7c3aed")
        _ax2.set_xlim(-1.2, 1.2)
        _ax2.set_ylim(-1.2, 1.2)
        _ax2.set_aspect("equal")
        _ax2.grid(True, alpha=0.18)
        _ax2.set_xlabel("celestial x")
        _ax2.set_ylabel("celestial y")
        _ax2.set_title("Celestial circle")

        plt.close(_fig)
        return _fig

    return (celestial_circle_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
