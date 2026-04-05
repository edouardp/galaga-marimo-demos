import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, sandwich


@app.cell
def _(np, plt, s1, s2, s3):
    def _rel_components(_mv):
        return np.array(
            [
                (_mv | s1).scalar_part / ((s1 | s1).scalar_part),
                (_mv | s2).scalar_part / ((s2 | s2).scalar_part),
                (_mv | s3).scalar_part / ((s3 | s3).scalar_part),
            ],
            dtype=float,
        )

    def draw_boosted_field(E_before, B_before, E_after, B_after, coeffs_before, coeffs_after):
        _Eb = _rel_components(E_before)
        _Bb = _rel_components(B_before)
        _Ea = _rel_components(E_after)
        _Ba = _rel_components(B_after)

        _fig = plt.figure(figsize=(14.0, 5.2))
        _ax1 = _fig.add_subplot(131, projection="3d")
        _ax2 = _fig.add_subplot(132, projection="3d")
        _ax3 = _fig.add_subplot(133)

        for _ax, _E, _B, _title in [
            (_ax1, _Eb, _Bb, "Before boost"),
            (_ax2, _Ea, _Ba, "After boost"),
        ]:
            _ax.quiver(0, 0, 0, _E[0], _E[1], _E[2], color="crimson", linewidth=2.5)
            _ax.quiver(0, 0, 0, _B[0], _B[1], _B[2], color="steelblue", linewidth=2.5)
            _ax.set_xlim(-2.5, 2.5)
            _ax.set_ylim(-2.5, 2.5)
            _ax.set_zlim(-2.5, 2.5)
            _ax.set_xlabel(r"$\sigma_1$")
            _ax.set_ylabel(r"$\sigma_2$")
            _ax.set_zlabel(r"$\sigma_3$")
            _ax.set_title(_title)
            _ax.plot([], [], color="crimson", label="E")
            _ax.plot([], [], color="steelblue", label="B")
            _ax.legend(loc="upper left")

        _labels = [r"$\gamma_1\gamma_0$", r"$\gamma_2\gamma_0$", r"$\gamma_3\gamma_0$", r"$\gamma_2\gamma_3$", r"$\gamma_3\gamma_1$", r"$\gamma_1\gamma_2$"]
        _x = np.arange(len(_labels))
        _w = 0.36
        _ax3.bar(_x - _w / 2, coeffs_before, width=_w, color="gray", alpha=0.75, label="before")
        _ax3.bar(_x + _w / 2, coeffs_after, width=_w, color="darkorange", alpha=0.82, label="after")
        _ax3.axhline(0, color="black", linewidth=0.8)
        _ax3.set_xticks(_x, _labels)
        _ax3.set_ylim(-2.5, 2.5)
        _ax3.grid(True, axis="y", alpha=0.25)
        _ax3.set_title("Bivector coefficients before and after")
        _ax3.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_boosted_field,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Boosting the Electromagnetic Field

    A Lorentz boost does not separately transform electric and magnetic fields. It transforms one bivector $F$, and the observer-relative split into $E$ and $B$ changes with the frame.

    This notebook follows [electromagnetism_one_bivector.py](./electromagnetism_one_bivector.py): there the goal is to see one bivector, while here the goal is to watch that bivector change its observer split under a boost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    The field is

    $$
    F = E + I B,
    $$

    and a boost rotor

    $$
    R = e^{-\varphi \gamma_0 n / 2}
    $$

    carries it to

    $$
    F' = R F \widetilde{R}.
    $$

    The point of the notebook is that the boost acts on $F$ once, and the new $E'$ and $B'$ are read off afterward.
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
    return I, g0, g1, g2, g3, s1, s2, s3, sta


@app.cell
def _(mo):
    ex = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.2, label="E along σ1", show_value=True)
    ey = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="E along σ2", show_value=True)
    bz = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.9, label="B along σ3", show_value=True)
    rapidity = mo.ui.slider(0.0, 2.0, step=0.05, value=0.75, label="Boost rapidity φ", show_value=True)
    boost_dir = mo.ui.dropdown(
        options=["along σ1", "along σ2", "along σ3"],
        value="along σ1",
        label="Boost direction",
    )
    return boost_dir, bz, ex, ey, rapidity


@app.cell
def _(
    I,
    boost_dir,
    bz,
    draw_boosted_field,
    ex,
    exp,
    ey,
    g0,
    g1,
    g2,
    g3,
    gm,
    mo,
    np,
    rapidity,
    s1,
    s2,
    s3,
    sandwich,
    sta,
):
    _E_before = (ex.value * s1 + ey.value * s2).name(latex=r"E")
    _B_before = (bz.value * s3).name(latex=r"B")
    _F_before = (_E_before + I * _B_before).name("F")

    _dirs = {
        "along σ1": g1,
        "along σ2": g2,
        "along σ3": g3,
    }
    _n = _dirs[boost_dir.value].name("n")
    _phi = sta.scalar(rapidity.value).name(latex=r"\varphi")
    _R = exp((-( _phi) / 2) * (g0 * _n)).name("R")
    _F_after = sandwich(_R, _F_before).name(latex=r"F'")

    _E_after = (_F_after | g0).name(latex=r"E'")
    _B_after = (
        ((_F_after | (I * s1)).scalar_part / ((I * s1) | (I * s1)).scalar_part) * s1
        + ((_F_after | (I * s2)).scalar_part / ((I * s2) | (I * s2)).scalar_part) * s2
        + ((_F_after | (I * s3)).scalar_part / ((I * s3) | (I * s3)).scalar_part) * s3
    ).name(latex=r"B'")

    _basis_bivectors = [g1 * g0, g2 * g0, g3 * g0, g2 * g3, g3 * g1, g1 * g2]
    _coeffs_before = np.array(
        [(_F_before | _basis).scalar_part / (_basis | _basis).scalar_part for _basis in _basis_bivectors],
        dtype=float,
    )
    _coeffs_after = np.array(
        [(_F_after | _basis).scalar_part / (_basis | _basis).scalar_part for _basis in _basis_bivectors],
        dtype=float,
    )

    _md = t"""
    {_E_before.display()} <br/>
    {_B_before.display()} <br/>
    {_F_before.display()} <br/>
    {_n.display()} <br/>
    {_phi.display()} <br/>
    {_R.display()} <br/>
    {_F_after.display()} <br/>
    {_E_after.display()} <br/>
    {_B_after.display()} <br/>
    One boost acts on one bivector, and the electric/magnetic split is read off afterward in the new frame.
    """

    mo.vstack(
        [
            ex,
            ey,
            bz,
            boost_dir,
            rapidity,
            gm.md(_md),
            draw_boosted_field(_E_before, _B_before, _E_after, _B_after, _coeffs_before, _coeffs_after),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    A boost can create magnetic components from a field that looked mostly electric, or vice versa, because the boost is not acting on two separate fields. It is acting on one spacetime bivector.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
