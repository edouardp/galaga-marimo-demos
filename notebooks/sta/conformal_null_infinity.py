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

    return Algebra, b_default, gm, mo, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conformal STA: Null Infinity

    In conformal spacetime, null directions are special. Along a null ray, the
    conformal lift grows differently than it does for timelike or spacelike
    directions. This is the simplest useful hint of why null infinity matters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Write a ray through an event $x$ as

    $$
    x(\lambda) = x + \lambda v.
    $$

    Its conformal lift is

    $$
    X(\lambda) = e_o + x(\lambda) + \frac{1}{2} x(\lambda)^2 e_\infty.
    $$

    The crucial distinction is that

    - if $v^2 \neq 0$, then $x(\lambda)^2$ grows quadratically in $\lambda$
    - if $v^2 = 0$, then the quadratic term disappears and the growth becomes linear

    Null directions are therefore singled out at conformal infinity.
    """)
    return


@app.cell
def _(Algebra, b_default):
    csta = Algebra((1, -1, 1, -1), blades=b_default(prefix="e", start=0))
    e0, e1, e2, e3 = csta.basis_vectors(lazy=True)
    g0 = e0.name(latex=r"\gamma_0")
    g1 = e1.name(latex=r"\gamma_1")
    ep = e2.name(latex=r"e_+")
    em = e3.name(latex=r"e_-")
    return csta, em, ep, g0, g1


@app.cell
def _(mo):
    direction_type = mo.ui.dropdown(
        options={"Timelike": "timelike", "Null": "null", "Spacelike": "spacelike"},
        value="Null",
        label="Direction type",
    )
    t0 = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.0, label="Initial time", show_value=True)
    x0 = mo.ui.slider(-1.5, 1.5, step=0.05, value=-0.6, label="Initial space", show_value=True)
    lam = mo.ui.slider(0.0, 3.0, step=0.05, value=2.0, label="Ray parameter λ", show_value=True)
    return direction_type, lam, t0, x0


@app.cell
def _(conformal_infinity_plot, csta, direction_type, em, ep, g0, g1, gm, lam, mo, t0, x0):
    half = csta.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (t0.value * g0 + x0.value * g1).name(latex="x")
    if direction_type.value == "timelike":
        v = (g0 + csta.scalar(0.4) * g1).name(latex="v")
    elif direction_type.value == "null":
        v = (g0 + g1).name(latex="v")
    else:
        v = (csta.scalar(0.4) * g0 + g1).name(latex="v")

    lam_mv = csta.scalar(lam.value).name(latex=r"\lambda")
    x_lam = (x + lam_mv * v).name(latex=r"x(\lambda)")
    v_sq = (v * v).name(latex=r"v^2")
    x_lam_sq = (x_lam | x_lam).name(latex=r"x(\lambda)^2")
    X_lam = (eo + x_lam + half * x_lam_sq * einf).name(latex=r"X(\lambda)")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {x.display()} <br/>
    {v.display()} <br/>
    {v_sq.display()} <br/>
    {x_lam.display()} <br/>
    {x_lam_sq.display()} <br/>
    {X_lam.display()} <br/>
    When $v^2 = 0$, the quadratic growth disappears. That is the special conformal behavior of null directions.
    """

    mo.vstack([direction_type, t0, x0, lam, gm.md(_md), conformal_infinity_plot(x, x_lam, direction_type.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Null rays are not just one more family of spacetime directions. In the
    conformal lift, they sit exactly at the boundary between quadratic and
    linear growth. That is one of the cleanest first signs that null infinity
    deserves special attention.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(plt):
    def conformal_infinity_plot(x, x_lam, direction_type):
        _x = [x.vector_part[0], x.vector_part[1]]
        _xl = [x_lam.vector_part[0], x_lam.vector_part[1]]
        _color = {"timelike": "#2563eb", "null": "#7c3aed", "spacelike": "#d62828"}[direction_type]

        _fig, _ax = plt.subplots(figsize=(6.0, 5.2))
        _ax.plot([_x[1], _xl[1]], [_x[0], _xl[0]], color=_color, lw=2.0)
        _ax.scatter([_x[1], _xl[1]], [_x[0], _xl[0]], color=[_color, _color], s=55)
        _ax.text(_x[1] + 0.05, _x[0] + 0.05, "x", color=_color)
        _ax.text(_xl[1] + 0.05, _xl[0] + 0.05, "x(λ)", color=_color)
        _ax.plot([-3, 3], [-3, 3], color="#999999", lw=0.8, alpha=0.25)
        _ax.plot([-3, 3], [3, -3], color="#999999", lw=0.8, alpha=0.25)
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.set_xlim(-3.0, 3.0)
        _ax.set_ylim(-3.0, 3.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("space (γ1)")
        _ax.set_ylabel("time (γ0)")
        _ax.set_title("Timelike, null, and spacelike rays")
        plt.close(_fig)
        return _fig

    return (conformal_infinity_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
