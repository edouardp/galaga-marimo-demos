import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, project, reject, unit
    from galaga.blade_convention import b_default
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_default, gm, mo, np, plt, project, reject, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Reflection and Refraction from Subspaces

    At an interface, the incoming direction naturally splits into the part
    parallel to the surface and the part perpendicular to it. Reflection flips
    the perpendicular part. Refraction keeps the same surface direction but
    changes how steeply the ray leans into the new medium.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use $\mathrm{Cl}(2,0)$ and a flat interface aligned with $e_1$.

    - the interface tangent is the line direction $t = e_1$
    - the interface normal is $n = e_2$

    Then an incoming unit direction $d$ splits as

    $$
    d = d_{\parallel} + d_{\perp},
    \qquad
    d_{\parallel} = \mathrm{project}(d, t),
    \qquad
    d_{\perp} = \mathrm{reject}(d, t).
    $$
    """
    )
    return


@app.cell
def _(Algebra, b_default):
    alg = Algebra((1, 1), blades=b_default())
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## One Decomposition, Two Outcomes

    Reflection is the simpler case:

    $$
    d_{\mathrm{refl}} = d_{\parallel} - d_{\perp}.
    $$

    Refraction is constrained by Snell's law

    $$
    n_1 \sin\theta_i = n_2 \sin\theta_t,
    $$

    so the tangential direction stays the same while the new normal component is
    chosen to give the transmitted angle.
    """
    )
    return


@app.cell
def _(mo):
    incidence = mo.ui.slider(0, 80, step=1, value=35, label="Incidence angle from the normal", show_value=True)
    n1 = mo.ui.slider(1.0, 2.0, step=0.01, value=1.0, label="Upper index n₁", show_value=True)
    n2 = mo.ui.slider(1.0, 2.5, step=0.01, value=1.5, label="Lower index n₂", show_value=True)
    return incidence, n1, n2


@app.cell
def _(alg, draw_interface_split, e1, e2, gm, incidence, mo, n1, n2, np, project, reject, unit):
    theta_i = alg.scalar(np.radians(incidence.value)).name(latex=r"\theta_i")
    index_1 = alg.scalar(n1.value).name(latex=r"n_1")
    index_2 = alg.scalar(n2.value).name(latex=r"n_2")

    tangent = e1.name(latex="t")
    normal = e2.name(latex="n")

    incoming = unit(np.sin(theta_i.scalar_part) * e1 - np.cos(theta_i.scalar_part) * e2).name(latex=r"d")
    d_parallel = project(incoming, tangent).name(latex=r"d_{\parallel}")
    d_perp = reject(incoming, tangent).name(latex=r"d_{\perp}")

    reflected = (d_parallel - d_perp).name(latex=r"d_{\mathrm{refl}}")

    _sin_t = np.clip(n1.value * np.sin(theta_i.scalar_part) / n2.value, -1.0, 1.0)
    _tir = abs(_sin_t) > 1 - 1e-12 and n1.value > n2.value and np.sin(theta_i.scalar_part) > n2.value / n1.value if n1.value > n2.value else False
    if abs(_sin_t) >= 1.0:
        _theta_t = np.pi / 2
    else:
        _theta_t = float(np.arcsin(_sin_t))
    theta_t = alg.scalar(_theta_t).name(latex=r"\theta_t")

    refracted = unit(np.sin(theta_t.scalar_part) * e1 - np.cos(theta_t.scalar_part) * e2).name(latex=r"d_{\mathrm{refr}}")

    _note = ""
    if _tir:
        _note = "For these indices and this angle, Snell's law has no real transmitted direction: this is total internal reflection."

    _md = rt"""
    {tangent.display()} <br/>
    {normal.display()} <br/>
    {index_1.display()} <br/>
    {index_2.display()} <br/>
    {incoming.display()} <br/>
    {d_parallel.display()} <br/>
    {d_perp.display()} <br/>
    {reflected.display()} <br/>
    {theta_t.display()} <br/>
    {refracted.display()} <br/>
    $n_1 \sin(\theta_i) = {n1.value * np.sin(theta_i.scalar_part):.3f}$ <br/>
    $n_2 \sin(\theta_t) = {n2.value * np.sin(theta_t.scalar_part):.3f}$ <br/>
    {_note}
    """

    mo.vstack([incidence, n1, n2, gm.md(_md), draw_interface_split(incoming, d_parallel, d_perp, reflected, refracted, theta_i.scalar_part, theta_t.scalar_part, n1.value, n2.value, _tir)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    The same project/reject split explains both outcomes. Reflection just flips
    the perpendicular channel. Refraction keeps the direction along the interface
    but changes how much of the ray points into the second medium.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Appendum: Plotting Code
    """
    )
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_interface_split(incoming, d_parallel, d_perp, reflected, refracted, theta_i, theta_t, n1, n2, tir):
        _fig, (_ax0, _ax1) = plt.subplots(1, 2, figsize=(11.6, 4.9))

        def _xy(_v):
            return np.array(_v.vector_part[:2], dtype=float)

        _d = _xy(incoming)
        _dp = _xy(d_parallel)
        _dn = _xy(d_perp)
        _dr = _xy(reflected)
        _dt = _xy(refracted)

        _ax0.axhline(0, color="#333333", lw=1.2, alpha=0.8)
        _ax0.axvline(0, color="#666666", lw=1.0, alpha=0.45, linestyle="--")
        _ax0.fill_between([-1.8, 1.8], 0, 1.8, color="#dbeafe", alpha=0.30)
        _ax0.fill_between([-1.8, 1.8], -1.8, 0, color="#fee2e2", alpha=0.24)

        _start_in = np.array([0.0, 0.0]) - 1.15 * _d
        _start_out = np.array([0.0, 0.0])
        _ax0.annotate("", xy=(0, 0), xytext=_start_in, arrowprops=dict(arrowstyle="-|>", color="#222222", lw=2.6, mutation_scale=18))
        _ax0.annotate("", xy=_dp, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.0, mutation_scale=15, alpha=0.9))
        _ax0.annotate("", xy=_dn, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.0, mutation_scale=15, alpha=0.9))
        _ax0.annotate("", xy=1.15 * _dr, xytext=_start_out, arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2.6, mutation_scale=18))

        if tir:
            _ax0.text(-1.65, -1.55, "total internal reflection", color="#b91c1c")
        else:
            _ax0.annotate("", xy=1.15 * _dt, xytext=_start_out, arrowprops=dict(arrowstyle="-|>", color="#16a34a", lw=2.6, mutation_scale=18))

        _ax0.text(_dp[0] + 0.05, _dp[1] + 0.05, r"$d_{\parallel}$", color="#2563eb")
        _ax0.text(_dn[0] + 0.05, _dn[1] + 0.05, r"$d_{\perp}$", color="#d62828")
        _ax0.text(_dr[0] * 1.15 + 0.05, _dr[1] * 1.15 + 0.05, r"$d_{\mathrm{refl}}$", color="#7c3aed")
        if not tir:
            _ax0.text(_dt[0] * 1.15 + 0.05, _dt[1] * 1.15 - 0.08, r"$d_{\mathrm{refr}}$", color="#16a34a")

        _ax0.set_xlim(-1.8, 1.8)
        _ax0.set_ylim(-1.8, 1.8)
        _ax0.set_aspect("equal")
        _ax0.grid(True, alpha=0.15)
        _ax0.set_xlabel("tangent direction e1")
        _ax0.set_ylabel("normal direction e2")
        _ax0.set_title("Interface geometry from one split")

        _labels = ["tangent", "normal"]
        _x = np.arange(2)
        _width = 0.18
        _incoming_vals = [_d[0], _d[1]]
        _reflected_vals = [_dr[0], _dr[1]]
        _refracted_vals = [_dt[0], _dt[1]]
        _ax1.bar(_x - 1.5 * _width, _incoming_vals, width=_width, color="#222222", alpha=0.9, label="incoming")
        _ax1.bar(_x - 0.5 * _width, [_dp[0], _dn[1]], width=_width, color=["#2563eb", "#d62828"], alpha=0.85, label="split pieces")
        _ax1.bar(_x + 0.5 * _width, _reflected_vals, width=_width, color="#7c3aed", alpha=0.85, label="reflected")
        if tir:
            _ax1.bar(_x + 1.5 * _width, [0, 0], width=_width, color="#16a34a", alpha=0.25, label="refracted")
        else:
            _ax1.bar(_x + 1.5 * _width, _refracted_vals, width=_width, color="#16a34a", alpha=0.85, label="refracted")

        _ax1.axhline(0, color="#333333", lw=1.0, alpha=0.5)
        _ax1.set_xticks(_x, _labels)
        _ax1.set_ylim(-1.1, 1.1)
        _ax1.grid(True, axis="y", alpha=0.15)
        _ax1.set_ylabel("component coefficient")
        _ax1.set_title("Parallel and perpendicular channels")
        _ax1.legend(loc="upper right")

        _ax1.text(
            0.02,
            0.04,
            rf"$\theta_i = {np.degrees(theta_i):.1f}^\circ$" + "\n" + rf"$\theta_t = {np.degrees(theta_t):.1f}^\circ$" + "\n" + rf"$n_1={n1:.2f},\; n_2={n2:.2f}$",
            transform=_ax1.transAxes,
            ha="left",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#999999", alpha=0.9),
        )

        plt.close(_fig)
        return _fig

    return (draw_interface_split,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
