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
    # Conformal STA: Null Rays

    The simplest useful conformal-spacetime notebook is probably a notebook about
    null rays. A spacetime event together with a null direction already points
    toward the incidence picture that twistor theory later reorganizes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We work in a 1+1 visual slice of conformal spacetime.

    Start with a spacetime event $x$ and a null direction $k$ with $k^2 = 0$.
    Then points on the null ray are

    $$
    x(\lambda) = x + \lambda k.
    $$

    Their conformal lifts are

    $$
    X(\lambda) = e_o + x(\lambda) + \frac{1}{2} x(\lambda)^2 e_\infty.
    $$

    The same ray can then be treated as a conformal incidence object rather than
    just as an affine parameterization.
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
    t0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=0.0, label="Initial time", show_value=True)
    x0 = mo.ui.slider(-2.0, 2.0, step=0.05, value=-1.0, label="Initial space", show_value=True)
    lam = mo.ui.slider(0.0, 3.0, step=0.05, value=1.2, label="Ray parameter λ", show_value=True)
    probe = mo.ui.slider(0.0, 3.0, step=0.05, value=2.0, label="Probe parameter μ", show_value=True)
    direction = mo.ui.dropdown(options={"Right-moving": "right", "Left-moving": "left"}, value="Right-moving", label="Null direction")
    return direction, lam, probe, t0, x0


@app.cell
def _(csta, conformal_null_ray_plot, direction, em, ep, g0, g1, gm, lam, mo, probe, t0, x0):
    half = csta.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (t0.value * g0 + x0.value * g1).name(latex="x")
    k = ((g0 + g1) if direction.value == "right" else (g0 - g1)).name(latex="k")
    x_lam = (x + csta.scalar(lam.value).name(latex=r"\lambda") * k).name(latex=r"x(\lambda)")
    x_mu = (x + csta.scalar(probe.value).name(latex=r"\mu") * k).name(latex=r"x(\mu)")

    X = (eo + x + half * (x | x) * einf).name(latex="X")
    X_lam = (eo + x_lam + half * (x_lam | x_lam) * einf).name(latex=r"X(\lambda)")
    X_mu = (eo + x_mu + half * (x_mu | x_mu) * einf).name(latex=r"X(\mu)")

    k_sq = (k * k).name(latex=r"k^2")
    X_sq = (X * X).name(latex=r"X^2")
    X_lam_sq = (X_lam * X_lam).name(latex=r"X(\lambda)^2")
    ray_object = (X ^ X_lam ^ einf).name(latex=r"\mathcal R")
    incidence = (X_mu ^ ray_object).name(latex=r"X(\mu) \wedge \mathcal R")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {x.display()} <br/>
    {k.display()} <br/>
    {k_sq.display()} <br/>
    {x_lam.display()} <br/>
    {x_mu.display()} <br/>
    {X.display()} <br/>
    {X_sq.display()} <br/>
    {X_lam.display()} <br/>
    {X_lam_sq.display()} <br/>
    {ray_object.display()} <br/>
    {incidence.display()} <br/>
    The probe event on the same null ray wedges to zero with the conformal ray object.
    """

    mo.vstack([t0, x0, direction, lam, probe, gm.md(_md), conformal_null_ray_plot(x, x_lam, x_mu)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    In ordinary STA, a null ray is "an event plus a null direction". In conformal
    STA, the same ray can be treated as an incidence object built from conformal
    points and infinity. That is a small but real step toward the kind of geometry
    twistor theory cares about.
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
    def conformal_null_ray_plot(x, x_lam, x_mu):
        _x = [x.vector_part[0], x.vector_part[1]]
        _xl = [x_lam.vector_part[0], x_lam.vector_part[1]]
        _xm = [x_mu.vector_part[0], x_mu.vector_part[1]]

        _fig, _ax = plt.subplots(figsize=(6.2, 5.4))
        _ax.plot([_x[1], _xm[1]], [_x[0], _xm[0]], color="#555555", lw=1.8)
        _ax.scatter([_x[1], _xl[1], _xm[1]], [_x[0], _xl[0], _xm[0]], color=["#2563eb", "#7c3aed", "#d62828"], s=55)
        _ax.text(_x[1] + 0.05, _x[0] + 0.05, "x", color="#2563eb")
        _ax.text(_xl[1] + 0.05, _xl[0] + 0.05, "x(λ)", color="#7c3aed")
        _ax.text(_xm[1] + 0.05, _xm[0] + 0.05, "x(μ)", color="#d62828")
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
        _ax.set_title("Null ray in a 1+1 spacetime slice")
        plt.close(_fig)
        return _fig

    return (conformal_null_ray_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
