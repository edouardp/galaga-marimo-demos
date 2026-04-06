import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, b_default, exp, gm, mo, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conformal STA: Translations as Conformal Rotations

    One of the first dramatic payoffs of conformal spacetime is that translations
    become versor actions too. They are no longer a separate affine operation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given a spacetime translation vector $a$, define

    $$
    T = \exp\!\left(-\frac{1}{2} a e_\infty\right).
    $$

    Then a conformal event $X$ translates by

    $$
    X' = T X \widetilde T.
    $$

    This has the same sandwich form as the familiar rotor action. That is the
    first clear taste of why the conformal model is structurally appealing.
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
    t0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=-0.5, label="Event time", show_value=True)
    x0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.8, label="Event space", show_value=True)
    dt = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.7, label="Translation time", show_value=True)
    dx = mo.ui.slider(-1.5, 1.5, step=0.05, value=-0.4, label="Translation space", show_value=True)
    return dt, dx, t0, x0


@app.cell
def _(conformal_translation_plot, csta, dt, dx, em, ep, exp, g0, g1, gm, mo, t0, x0):
    half = csta.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (t0.value * g0 + x0.value * g1).name(latex="x")
    X = (eo + x + half * (x | x) * einf).name(latex="X")

    a = (dt.value * g0 + dx.value * g1).name(latex="a")
    T = exp(-half * a * einf).name(latex="T")
    Xp = (T * X * ~T).name(latex=r"X'")
    x_prime = (((Xp | g0) * g0) + ((Xp | g1) * g1)).name(latex=r"x'")
    Xp_sq = (Xp * Xp).name(latex=r"{X'}^2")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {x.display()} <br/>
    {X.display()} <br/>
    {a.display()} <br/>
    {T.display()} <br/>
    {Xp.display()} <br/>
    {Xp_sq.display()} <br/>
    {x_prime.display()} <br/>
    The translated conformal event is still null, and the Euclidean spacetime part has shifted by the translation vector.
    """

    mo.vstack([t0, x0, dt, dx, gm.md(_md), conformal_translation_plot(x, a, x_prime)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In conformal spacetime, translations join the same sandwich-action language
    as rotations and boosts. That is the simplest concrete reason to care about
    the extra null directions.
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
    def conformal_translation_plot(x, a, x_prime):
        _x = [x.vector_part[0], x.vector_part[1]]
        _a = [a.vector_part[0], a.vector_part[1]]
        _xp = [x_prime.vector_part[0], x_prime.vector_part[1]]

        _fig, _ax = plt.subplots(figsize=(6.2, 5.4))
        _ax.scatter([_x[1], _xp[1]], [_x[0], _xp[0]], color=["#2563eb", "#d62828"], s=60)
        _ax.annotate("", xy=(_xp[1], _xp[0]), xytext=(_x[1], _x[0]), arrowprops=dict(arrowstyle="->", color="#555555", lw=1.8))
        _ax.annotate("", xy=(_a[1], _a[0]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2.0))
        _ax.text(_x[1] + 0.05, _x[0] + 0.05, "x", color="#2563eb")
        _ax.text(_xp[1] + 0.05, _xp[0] + 0.05, "x'", color="#d62828")
        _ax.text(_a[1] + 0.05, _a[0] + 0.05, "a", color="#7c3aed")
        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
        _ax.plot([-3, 3], [-3, 3], color="#999999", lw=0.8, alpha=0.25)
        _ax.plot([-3, 3], [3, -3], color="#999999", lw=0.8, alpha=0.25)
        _ax.set_xlim(-3.0, 3.0)
        _ax.set_ylim(-3.0, 3.0)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.18)
        _ax.set_xlabel("space (γ1)")
        _ax.set_ylabel("time (γ0)")
        _ax.set_title("Translation in a 1+1 spacetime slice")
        plt.close(_fig)
        return _fig

    return (conformal_translation_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
