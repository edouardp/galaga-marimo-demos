import marimo

__generated_with = "0.22.0"
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
    def draw_celestial_views(event, null_vector, boosted_null):
        _event = event.eval().vector_part
        _k = null_vector.eval().vector_part
        _kb = boosted_null.eval().vector_part

        _fig = plt.figure(figsize=(12.4, 5.8))
        _ax1 = _fig.add_subplot(121)
        _ax2 = _fig.add_subplot(122, projection="3d")

        _ax1.plot([-3, 3], [-3, 3], color="gray", linestyle="--", alpha=0.35)
        _ax1.plot([-3, 3], [3, -3], color="gray", linestyle="--", alpha=0.35)
        _ax1.scatter([_event[1]], [_event[0]], color="#111111", s=40, zorder=4)
        _ax1.annotate(
            "",
            xy=(_event[1] + 1.5 * _k[1], _event[0] + 1.5 * _k[0]),
            xytext=(_event[1], _event[0]),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.6, mutation_scale=18),
        )
        _ax1.annotate(
            "",
            xy=(_event[1] + 1.5 * _kb[1], _event[0] + 1.5 * _kb[0]),
            xytext=(_event[1], _event[0]),
            arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.4, mutation_scale=18, alpha=0.9),
        )
        _ax1.text(_event[1] + 0.08, _event[0] + 0.08, "x", color="#111111")
        _ax1.text(_event[1] + 1.55 * _k[1], _event[0] + 1.55 * _k[0], "k", color="#d62828")
        _ax1.text(_event[1] + 1.55 * _kb[1], _event[0] + 1.55 * _kb[0], "k'", color="#2563eb")
        _ax1.set_xlim(-3, 3)
        _ax1.set_ylim(-3, 3)
        _ax1.set_aspect("equal")
        _ax1.grid(True, alpha=0.2)
        _ax1.set_xlabel("space x")
        _ax1.set_ylabel("time t")
        _ax1.set_title("Null ray through one event")

        _u = np.linspace(0, 2 * np.pi, 40)
        _v = np.linspace(0, np.pi, 24)
        _xs = np.outer(np.cos(_u), np.sin(_v))
        _ys = np.outer(np.sin(_u), np.sin(_v))
        _zs = np.outer(np.ones_like(_u), np.cos(_v))
        _ax2.plot_wireframe(_xs, _ys, _zs, color="gray", alpha=0.10, linewidth=0.6)

        def _spatial_unit(_mv):
            _vec = np.array(_mv.eval().vector_part[1:4], dtype=float)
            _norm = np.linalg.norm(_vec)
            return _vec / _norm if _norm > 1e-12 else _vec

        _n = _spatial_unit(null_vector)
        _nb = _spatial_unit(boosted_null)
        _ax2.quiver(0, 0, 0, _n[0], _n[1], _n[2], color="#d62828", linewidth=2.6, arrow_length_ratio=0.08)
        _ax2.quiver(0, 0, 0, _nb[0], _nb[1], _nb[2], color="#2563eb", linewidth=2.4, arrow_length_ratio=0.08)
        _ax2.text(1.08 * _n[0], 1.08 * _n[1], 1.08 * _n[2], "observer 1", color="#d62828")
        _ax2.text(1.08 * _nb[0], 1.08 * _nb[1], 1.08 * _nb[2], "observer 2", color="#2563eb")
        _ax2.set_xlim(-1.1, 1.1)
        _ax2.set_ylim(-1.1, 1.1)
        _ax2.set_zlim(-1.1, 1.1)
        _ax2.set_box_aspect((1, 1, 1))
        _ax2.set_xlabel("x")
        _ax2.set_ylabel("y")
        _ax2.set_zlabel("z")
        _ax2.set_title("Celestial sphere of null directions")

        plt.close(_fig)
        return _fig

    return (draw_celestial_views,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Null Directions and the Celestial Sphere

    This is not full twistor theory. It is a **real geometric precursor** to it.

    A key twistor idea is that null structure matters more deeply than ordinary point-by-point Euclidean intuition suggests. At any spacetime event, the null directions form a sphere of lightlike directions: the **celestial sphere** seen by an observer at that event.

    This notebook keeps everything real and uses only spacetime algebra. The goal is to isolate one clean ingredient that twistor theory later organizes in a richer way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use spacetime algebra with signature $(+, -, -, -)$:

    $$
    \mathrm{Cl}(1,3), \qquad
    \gamma_0^2 = 1, \quad
    \gamma_1^2 = \gamma_2^2 = \gamma_3^2 = -1.
    $$

    A future null vector satisfies

    $$
    k^2 = 0.
    $$

    If we write one as

    $$
    k = \gamma_0 + \hat{n},
    $$

    where $\hat{n}$ is a unit spatial direction, then the possible directions $\hat{n}$ fill out a sphere. That sphere is the observer's celestial sphere.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, g2, g3, sta


@app.cell
def _(mo):
    azimuth = mo.ui.slider(0, 360, step=1, value=30, label="Null direction azimuth", show_value=True)
    elevation = mo.ui.slider(-80, 80, step=1, value=20, label="Null direction elevation", show_value=True)
    rapidity = mo.ui.slider(-1.5, 1.5, step=0.05, value=0.5, label="Observer 2 rapidity along x", show_value=True)
    event_t = mo.ui.slider(-1.5, 1.5, step=0.1, value=0.0, label="Event time", show_value=True)
    event_x = mo.ui.slider(-1.5, 1.5, step=0.1, value=0.0, label="Event x", show_value=True)
    return azimuth, elevation, event_t, event_x, rapidity


@app.cell
def _(
    azimuth,
    draw_celestial_views,
    elevation,
    event_t,
    event_x,
    exp,
    g0,
    g1,
    g2,
    g3,
    gm,
    mo,
    np,
    rapidity,
    sandwich,
    sta,
):
    _az = np.radians(azimuth.value)
    _el = np.radians(elevation.value)
    _rap = sta.scalar(rapidity.value).name(latex=r"\phi")

    _nx = np.cos(_el) * np.cos(_az)
    _ny = np.cos(_el) * np.sin(_az)
    _nz = np.sin(_el)

    _n = (_nx * g1 + _ny * g2 + _nz * g3).name(latex=r"\hat{n}")
    _k = (g0 + _n).name("k")
    _event = (event_t.value * g0 + event_x.value * g1).name("x")

    _B = (g0 * g1).name(latex=r"\gamma_0\gamma_1")
    _R = exp(-_rap * _B / 2).name("R")
    _k_boosted = sandwich(_R, _k).name(latex=r"k'")

    _k_sq = (_k * _k).scalar_part
    _k_boosted_sq = (_k_boosted * _k_boosted).scalar_part

    _md = t"""
    {_event.display()} <br/>
    {_n.display()} <br/>
    {_k.display()} <br/>
    {_R.display()} <br/>
    {_k_boosted.display()} <br/>
    $k^2 = {_k_sq:.3f}$ <br/>
    $(k')^2 = {_k_boosted_sq:.3f}$ <br/>
    The red and blue arrows are the same null ray described by two observers. Their spacetime components differ, but the ray remains null, and its spatial direction lands on each observer's celestial sphere.
    """

    mo.vstack(
        [
            azimuth,
            elevation,
            rapidity,
            event_t,
            event_x,
            gm.md(_md),
            draw_celestial_views(_event, _k, _k_boosted),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The real geometric idea here is that a spacetime event comes with a sphere of null directions. Twistor theory reorganizes this null and conformal structure in a deeper way, but this celestial-sphere picture is one of the simplest real ingredients to understand first.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
