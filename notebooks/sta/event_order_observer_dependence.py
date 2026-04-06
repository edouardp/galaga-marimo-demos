import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_sta, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Event Order Can Depend on the Observer

    In spacetime algebra, the order of two events is encoded in their separation
    vector. If that separation is spacelike, a boost can flip the sign of the
    time component and reverse which event happens first. If it is timelike or
    null, the time ordering does not flip.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    In this notebook we only use the $1+1$ slice spanned by $\gamma_0$ and
    $\gamma_1$, so every event separation is

    $$
    \Delta x = \Delta t\,\gamma_0 + \Delta x\,\gamma_1.
    $$

    The invariant interval is $\Delta x^2 = \Delta t^2 - \Delta x^2$, and a
    boost in the $\gamma_0\gamma_1$ plane changes the observed time component.
    """)
    return


@app.cell
def _(Algebra, b_sta):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, sta


@app.cell
def _(mo):
    dt_slider = mo.ui.slider(-2.5, 2.5, step=0.05, value=0.6, label="Δt from A to B", show_value=True)
    dx_slider = mo.ui.slider(-2.5, 2.5, step=0.05, value=1.4, label="Δx from A to B", show_value=True)
    phi_slider = mo.ui.slider(-2.5, 2.5, step=0.05, value=0.7, label="Observer rapidity φ", show_value=True)
    return dt_slider, dx_slider, phi_slider


@app.cell
def _(
    dt_slider,
    dx_slider,
    event_order_plot,
    exp,
    g0,
    g1,
    gm,
    mo,
    np,
    phi_slider,
    sta,
):
    half = sta.frac(1, 2)
    dt = sta.scalar(dt_slider.value).name(latex=r"\Delta t")
    dx = sta.scalar(dx_slider.value).name(latex=r"\Delta x")
    phi = sta.scalar(phi_slider.value).name(latex=r"\varphi")

    A = (sta.scalar(0) * g0).name("A", latex="A")
    delta = (dt * g0 + dx * g1).name(latex=r"\Delta x")
    B = (A + delta).name("B", latex="B")
    interval = (delta * delta).name(latex=r"\Delta x^2")

    boost_plane = (g0 * g1).name(latex=r"B")
    R = exp(half * phi * boost_plane).name(latex="R")
    delta_prime = (R * delta * ~R).name(latex=r"\Delta x'")
    B_prime = delta_prime.name(latex=r"B'")
    dt_prime = (delta_prime | g0).name(latex=r"\Delta t'")
    dx_prime = (-(delta_prime | g1)).name(latex=r"\Delta x'")

    beta = np.tanh(phi_slider.value)
    gamma = np.cosh(phi_slider.value)

    _interval_value = interval.scalar_part
    if _interval_value > 1e-9:
        _kind = "timelike"
    elif _interval_value < -1e-9:
        _kind = "spacelike"
    else:
        _kind = "null"

    def _order_label(_value):
        if _value > 1e-9:
            return "A happens before B"
        if _value < -1e-9:
            return "B happens before A"
        return "A and B are simultaneous"

    _rest_order = _order_label(dt.scalar_part)
    _boosted_order = _order_label(dt_prime.scalar_part)

    _extra = ""
    if _kind == "spacelike" and abs(dx.scalar_part) > 1e-9:
        _beta_flip = dt.scalar_part / dx.scalar_part
        if abs(_beta_flip) < 1.0:
            _extra = (
                f"$|\\beta_{{flip}}| = |\\Delta t / \\Delta x| = {abs(_beta_flip):.3f}$ "
                f"is the threshold where the boosted observer sees simultaneity."
            )

    _md = t"""
    {dt.display()} <br/>
    {dx.display()} <br/>
    {delta.display()} <br/>
    {interval.display()} $\\quad$ ({_kind}) <br/>
    {phi.display()} <br/>
    {R.display()} <br/>
    {delta_prime.display()} <br/>
    {dt_prime.display()} <br/>
    {dx_prime.display()} <br/>
    $\\beta = \\tanh\\varphi = {beta:.3f} \\quad \\gamma = \\cosh\\varphi = {gamma:.3f}$ <br/>
    Rest frame: {_rest_order}. <br/>
    Boosted frame: {_boosted_order}. <br/>
    {_extra}
    """

    mo.vstack(
        [
            dt_slider,
            dx_slider,
            phi_slider,
            gm.md(_md),
            event_order_plot(A, B, B_prime, _kind, _rest_order, _boosted_order),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The time ordering of events is encoded in the sign of the timelike component
    of their separation vector. A boost can change that sign only when the
    interval is spacelike. That is why spacelike-separated events can trade
    order between observers, while timelike and null-separated events cannot.
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
    def event_order_plot(A, B, B_prime, interval_kind, rest_order, boosted_order):
        _A = [A.vector_part[1], A.vector_part[0]]
        _B = [B.vector_part[1], B.vector_part[0]]
        _Bp = [B_prime.vector_part[1], B_prime.vector_part[0]]

        _extent = max(3.0, abs(_B[0]), abs(_B[1]), abs(_Bp[0]), abs(_Bp[1])) + 0.6
        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(10.8, 5.1), constrained_layout=True)

        for _ax, _point, _title, _order in [
            (_ax0, _B, "Rest frame", rest_order),
            (_ax1, _Bp, "Boosted frame", boosted_order),
        ]:
            _lc = np.linspace(-_extent, _extent, 200)
            _ax.plot(_lc, _lc, "--", color="#999999", alpha=0.25, lw=1.0)
            _ax.plot(_lc, -_lc, "--", color="#999999", alpha=0.25, lw=1.0)
            _ax.axhline(0, color="#333333", lw=1.0, alpha=0.7)
            _ax.axvline(0, color="#333333", lw=1.0, alpha=0.7)
            _ax.plot([_A[0], _point[0]], [_A[1], _point[1]], color="#6b7280", lw=1.8)
            _ax.scatter([_A[0]], [_A[1]], s=50, color="#2563eb", zorder=3)
            _ax.scatter([_point[0]], [_point[1]], s=58, color="#d62828", zorder=3)
            _ax.text(_A[0] + 0.06, _A[1] + 0.06, "A", color="#2563eb")
            _ax.text(_point[0] + 0.06, _point[1] + 0.06, "B", color="#d62828")
            _ax.set_xlim(-_extent, _extent)
            _ax.set_ylim(-_extent, _extent)
            _ax.set_aspect("equal")
            _ax.grid(True, alpha=0.18)
            _ax.set_xlabel("space (γ1)")
            _ax.set_ylabel("time (γ0)")
            _ax.set_title(f"{_title}\n{_order}")

        _fig.suptitle(f"Event ordering for a {interval_kind} separation", fontsize=13)
        plt.close(_fig)
        return _fig

    return (event_order_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
