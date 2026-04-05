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
def _(np, plt, s1, s2, s3):
    def draw_field_views(E_rel, B_rel, coeffs):
        _E = np.array(
            [
                (E_rel | (s1)).scalar_part / ((s1 | s1).scalar_part),
                (E_rel | (s2)).scalar_part / ((s2 | s2).scalar_part),
                (E_rel | (s3)).scalar_part / ((s3 | s3).scalar_part),
            ],
            dtype=float,
        )
        _B = np.array(
            [
                (B_rel | (s1)).scalar_part / ((s1 | s1).scalar_part),
                (B_rel | (s2)).scalar_part / ((s2 | s2).scalar_part),
                (B_rel | (s3)).scalar_part / ((s3 | s3).scalar_part),
            ],
            dtype=float,
        )
        _labels = [r"$\gamma_1\gamma_0$", r"$\gamma_2\gamma_0$", r"$\gamma_3\gamma_0$", r"$\gamma_2\gamma_3$", r"$\gamma_3\gamma_1$", r"$\gamma_1\gamma_2$"]
        _x = np.arange(len(_labels))

        _fig = plt.figure(figsize=(11.2, 5.4))
        _ax1 = _fig.add_subplot(121, projection="3d")
        _ax2 = _fig.add_subplot(122)

        _ax1.quiver(0, 0, 0, _E[0], _E[1], _E[2], color="crimson", linewidth=2.5)
        _ax1.quiver(0, 0, 0, _B[0], _B[1], _B[2], color="steelblue", linewidth=2.5)
        _ax1.set_xlim(-2.2, 2.2)
        _ax1.set_ylim(-2.2, 2.2)
        _ax1.set_zlim(-2.2, 2.2)
        _ax1.set_xlabel(r"$\sigma_1$")
        _ax1.set_ylabel(r"$\sigma_2$")
        _ax1.set_zlabel(r"$\sigma_3$")
        _ax1.set_title("Observer-relative E and B")
        _ax1.plot([], [], color="crimson", label="E")
        _ax1.plot([], [], color="steelblue", label="B")
        _ax1.legend(loc="upper left")

        _ax2.bar(_x, coeffs, color=["crimson", "crimson", "crimson", "steelblue", "steelblue", "steelblue"], alpha=0.8)
        _ax2.axhline(0, color="black", linewidth=0.8)
        _ax2.set_xticks(_x, _labels)
        _ax2.set_ylim(-2.2, 2.2)
        _ax2.grid(True, axis="y", alpha=0.25)
        _ax2.set_title("One bivector F in the STA bivector basis")

        plt.close(_fig)
        return _fig

    return (draw_field_views,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Electromagnetism as One Bivector

    In spacetime algebra, the electric and magnetic fields are not separate kinds of object. They are the timelike and spacelike parts of one bivector field $F$.

    This notebook follows [relative_vectors_sta.py](./relative_vectors_sta.py): that file explains the relative vectors $\sigma_i = \gamma_i\gamma_0$, while this one uses them to assemble the Faraday bivector.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    Relative to an observer $\gamma_0$, the spatial relative vectors are

    $$
    \sigma_i = \gamma_i\gamma_0.
    $$

    Then the Faraday bivector can be written as

    $$
    F = E + I B,
    $$

    where $E$ and $B$ are observer-relative vectors in the $\sigma_i$ basis.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build the Field

    The controls are intentionally simple: an electric field in the $\sigma_1$-$\sigma_2$ plane and a magnetic field along $\sigma_3$.

    That already shows the main point: one part of $F$ lives in timelike planes $\gamma_i\gamma_0$, and the other enters through the pseudoscalar-weighted spatial part $IB$.
    """)
    return


@app.cell
def _(mo):
    ex = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.2, label="E along σ1", show_value=True)
    ey = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.4, label="E along σ2", show_value=True)
    bz = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.8, label="B along σ3", show_value=True)
    return bz, ex, ey


@app.cell
def _(
    I,
    bz,
    draw_field_views,
    ex,
    ey,
    g0,
    g1,
    g2,
    g3,
    gm,
    grade,
    mo,
    np,
    s1,
    s2,
    s3,
):
    _E_rel = (ex.value * s1 + ey.value * s2).name("E")
    _B_rel = (bz.value * s3).name("B")
    _F = (_E_rel + I * _B_rel).name("F")

    _basis_bivectors = [
        (g1 * g0, r"\gamma_1\gamma_0"),
        (g2 * g0, r"\gamma_2\gamma_0"),
        (g3 * g0, r"\gamma_3\gamma_0"),
        (g2 * g3, r"\gamma_2\gamma_3"),
        (g3 * g1, r"\gamma_3\gamma_1"),
        (g1 * g2, r"\gamma_1\gamma_2"),
    ]

    _coeffs = np.array(
        [
            (_F | _basis).scalar_part / (_basis | _basis).scalar_part
            for _basis, _label in _basis_bivectors
        ],
        dtype=float,
    )

    _F2 = (_F * _F).name(latex=r"F^2")
    _scalar_invariant = grade(_F2, 0).name(latex=r"\langle F^2 \rangle_0")
    _pseudo_invariant = grade(_F2, 4).name(latex=r"\langle F^2 \rangle_4")

    _md = t"""
    {_E_rel.display()} <br/>
    {_B_rel.display()} <br/>
    {_F.display()} <br/>
    {_F2.display()} <br/>
    {_scalar_invariant.display()} <br/>
    {_pseudo_invariant.display()} <br/>
    The electric and magnetic pieces are not separate field types here. They are one bivector, split relative to the observer.
    """

    mo.vstack([ex, ey, bz, gm.md(_md), draw_field_views(_E_rel, _B_rel, _coeffs)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The payoff is conceptual. Once the field is one bivector $F$, the observer split into electric and magnetic parts becomes a decomposition of one geometric object, not a marriage of two unrelated fields.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
