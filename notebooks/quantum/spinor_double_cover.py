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
    mo.md(r"""
    # Spinor Double Cover

    A measured spin direction can be shown as an ordinary vector. But the underlying spin state is not just that vector.

    In geometric algebra, the spin state is a rotor in the even subalgebra. The observable direction is derived from it:

    $$
    s = R e_1 \tilde{R}.
    $$

    The key point is that `Spin(2)` double-covers `SO(2)`: the rotors $R$ and $-R$ give the same physical direction $s$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean algebra $\mathrm{Cl}(2,0)$.

    The even subalgebra is spanned by

    $$
    1, \qquad e_{12},
    $$

    so a rotor lives in a separate 2D rotor space:

    $$
    R = \cos(\phi/2) - e_{12}\sin(\phi/2).
    $$

    The measured direction rotates by the full angle $\phi$, while the rotor itself only moves by the half-angle $\phi/2$.

    In this notebook we choose $e_1$ as the reference direction, so when $\phi = 0^\circ$ the rotor-space point and the measured direction both start on the positive horizontal axis.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    e12 = e1 * e2
    return alg, e1, e12, e2


@app.cell
def _(mo):
    physical_angle = mo.ui.slider(0, 720, step=1, value=20, label="Physical direction angle φ", show_value=True)
    return (physical_angle,)


@app.cell
def _(alg, draw_double_cover, e1, e12, e2, exp, gm, mo, np, physical_angle):
    _phi = alg.scalar(np.radians(physical_angle.value)).name(latex=r"\phi")
    _R = exp((-_phi) * (e1 ^ e2) / 2).name(latex=r"R")
    _minus_R = (-_R)#.name(latex=r"-R")
    _spin = (_R * e1 * ~_R).name(latex=r"s_+")
    _spin_neg = (_minus_R * e1 * ~_minus_R).name(latex=r"s_-")

    _rotor_scalar = _R.eval().scalar_part
    _rotor_bivector = -(_R.eval() | e12).scalar_part
    _spin_xy = _spin.eval().vector_part[:2]

    _md = t"""
    {_R.display()} <br/>
    {_minus_R.display()} <br/>
    {_spin.display()} <br/>
    {_spin_neg.display()} <br/>
    Physical angle: ${physical_angle.value:.1f}^\\circ$ <br/>
    Rotor angle in rotor space: ${physical_angle.value / 2:.1f}^\\circ$
    """

    mo.vstack(
        [
            physical_angle,
            gm.md(_md),
            draw_double_cover(_R, _minus_R, _spin, e12),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The physical spin direction lives in ordinary vector space, but the spinor that generates it lives in rotor space. That is why opposite rotor-space points $R$ and $-R$ can represent the same measured direction.
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
    def draw_double_cover(rotor, neg_rotor, spin_direction, basis_bivector):
        _rotor_scalar = rotor.eval().scalar_part
        _rotor_bivector = -(-(rotor.eval() | basis_bivector).scalar_part)
        _neg_scalar = neg_rotor.eval().scalar_part
        _neg_bivector = -(-(neg_rotor.eval() | basis_bivector).scalar_part)
        _spin = np.array(spin_direction.eval().vector_part[:2], dtype=float)

        _fig = plt.figure(figsize=(12.0, 5.8))
        _gs = _fig.add_gridspec(1, 2, width_ratios=[1.0, 1.1])
        _rotor_ax = _fig.add_subplot(_gs[0, 0])
        _spin_ax = _fig.add_subplot(_gs[0, 1])

        def _setup(_ax):
            _circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", alpha=0.25, linewidth=1.2)
            _ax.add_patch(_circle)
            _ax.axhline(0, color="gray", alpha=0.15, linewidth=0.8)
            _ax.axvline(0, color="gray", alpha=0.15, linewidth=0.8)
            _ax.set_xlim(-1.35, 1.35)
            _ax.set_ylim(-1.35, 1.35)
            _ax.set_aspect("equal")
            _ax.set_xticks([])
            _ax.set_yticks([])

        _setup(_rotor_ax)
        _setup(_spin_ax)

        _rotor_ax.annotate(
            "",
            xy=(_rotor_scalar, _rotor_bivector),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2.5, mutation_scale=18, alpha=0.95),
        )
        _rotor_ax.annotate(
            "",
            xy=(_neg_scalar, _neg_bivector),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#16a34a", lw=2.5, mutation_scale=18, alpha=0.95),
        )
        _rotor_ax.text(1.08 * _rotor_scalar, 1.08 * _rotor_bivector, r"$R$", color="#7c3aed", ha="center", va="center")
        _rotor_ax.text(1.08 * _neg_scalar, 1.08 * _neg_bivector, r"$-R$", color="#16a34a", ha="center", va="center")
        _rotor_ax.text(1.18, 0, r"$1$", color="#444444", ha="center", va="center", fontsize=13)
        _rotor_ax.text(-1.18, 0, r"$-1$", color="#444444", ha="center", va="center", fontsize=13)
        _rotor_ax.text(0, 1.20, r"$-e_{12}$", color="#444444", ha="center", va="center", fontsize=13)
        _rotor_ax.text(0, -1.20, r"$e_{12}$", color="#444444", ha="center", va="center", fontsize=13)
        _rotor_ax.set_title("Rotor Space: Spin(2)", fontsize=12)

        _spin_ax.annotate(
            "",
            xy=_spin,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.8, mutation_scale=18, alpha=0.95),
        )
        _spin_ax.text(1.08 * _spin[0], 1.08 * _spin[1], "$s_+$\n$s_-$", color="#d62828", ha="center", va="center")
        _spin_ax.text(1.18, 0, r"$e_1$", color="#444444", ha="center", va="center", fontsize=13)
        _spin_ax.text(-1.18, 0, r"$-e_1$", color="#444444", ha="center", va="center", fontsize=13)
        _spin_ax.text(0, 1.20, r"$e_2$", color="#444444", ha="center", va="center", fontsize=13)
        _spin_ax.text(0, -1.20, r"$-e_2$", color="#444444", ha="center", va="center", fontsize=13)
        _spin_ax.set_title("Measured Direction: SO(2)", fontsize=12)

        _fig.suptitle("Two opposite rotor-space points map to the same physical direction", fontsize=13)
        _fig.tight_layout()
        plt.close(_fig)
        return _fig

    return (draw_double_cover,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
