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
def _(np, plt):
    def draw_null_geometry(v, v_boosted, k_plus):
        _vx, _vy = v.vector_part[1], v.vector_part[0]
        _bx, _by = v_boosted.vector_part[1], v_boosted.vector_part[0]
        _kx, _ky = k_plus.vector_part[1], k_plus.vector_part[0]

        _extent = max(2.2, abs(_vx), abs(_vy), abs(_bx), abs(_by), abs(_kx), abs(_ky)) * 1.15
        _fig, _ax = plt.subplots(figsize=(6.4, 6.4))
        _lc = np.linspace(-_extent, _extent, 200)
        _ax.plot(_lc, _lc, "k--", alpha=0.3, label="light cone")
        _ax.plot(_lc, -_lc, "k--", alpha=0.3)
        _ax.annotate("", xy=(_vx, _vy), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        _ax.annotate("", xy=(_bx, _by), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.annotate("", xy=(_kx, _ky), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.plot([], [], color="black", label="v")
        _ax.plot([], [], color="crimson", label="boosted v")
        _ax.plot([], [], color="steelblue", label=r"$k_+ = \gamma_0 + \gamma_1$")
        _ax.set_xlim(-_extent, _extent)
        _ax.set_ylim(-_extent, _extent)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("x (space)")
        _ax.set_ylabel("t (time)")
        _ax.set_title("Timelike, spacelike, and null vectors in STA")
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_null_geometry,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Null Vectors in STA

    In spacetime algebra, vectors split into three geometric classes:

    - **timelike** if $v^2 > 0$
    - **null** or **lightlike** if $v^2 = 0$
    - **spacelike** if $v^2 < 0$

    The null case is the boundary between the other two. Those vectors lie on the light cone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    That gives one timelike basis vector, $\gamma_0^2 = +1$, and three spacelike basis vectors, $\gamma_i^2 = -1$. In the reduced $t$-$x$ picture used here, a vector $v = t \gamma_0 + x \gamma_1$ has square

    $$
    v^2 = t^2 - x^2.
    $$

    So the sign of $t^2 - x^2$ tells us the geometric type immediately.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Vector, Three Possible Geometries

    Move the coefficients of $v = t\gamma_0 + x\gamma_1$ and watch how the sign of $v^2$ changes. Then apply a boost and check that the classification is preserved.
    """)
    return


@app.cell
def _(mo):
    time_coeff = mo.ui.slider(0.0, 2.0, step=0.05, value=1.0, label="Time coefficient t", show_value=True)
    space_coeff = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.8, label="Space coefficient x", show_value=True)
    rapidity = mo.ui.slider(0.0, 2.5, step=0.05, value=0.6, label="Boost rapidity φ", show_value=True)
    return rapidity, space_coeff, time_coeff


@app.cell
def _(
    draw_null_geometry,
    exp,
    g0,
    g1,
    gm,
    mo,
    rapidity,
    sandwich,
    space_coeff,
    time_coeff,
):
    _t = time_coeff.value
    _x = space_coeff.value
    _phi = rapidity.value

    _v = (_t * g0 + _x * g1).name("v")
    _R = exp((_phi / 2) * (g0 * g1)).name("R")
    _v_boosted = sandwich(_R, _v).name("v'")
    _k_plus = (g0 + g1).name(latex=r"k_+")

    _square = (_v ** 2)
    _boosted_square = (_v_boosted ** 2)

    if _square.scalar_part > 1e-9:
        _kind = "timelike"
    elif _square.scalar_part < -1e-9:
        _kind = "spacelike"
    else:
        _kind = "null (lightlike)"

    _md = t"""
    {_v.display()} <br/>
    {_square.display():.4f} $\\quad$ so {_square} is **{_kind}**. <br/>
    {_R.display()} <br/>
    {_v_boosted.display()} <br/>
    {_boosted_square.display():.4f}, so the boost preserves the classification. <br/>
    {_k_plus.display()} $\\quad with \\quad$ {(_k_plus ** 2).display()}
    """

    mo.vstack([
        time_coeff,
        space_coeff,
        rapidity,
        gm.md(_md),
        draw_null_geometry(_v, _v_boosted, _k_plus),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why Null Means Lightlike

    A null vector is nonzero, but its Minkowski square vanishes. In the $t$-$x$ plane that means $t = \pm x$, exactly the light-cone directions. Timelike vectors stay inside the cone; spacelike vectors stay outside it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    In STA, null, timelike, and spacelike vectors are not three unrelated labels. They are the three sign-classes of the same quadratic form. Null vectors sit on the boundary of causal structure, which is why lightlike motion is geometrically special.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
