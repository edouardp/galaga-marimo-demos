import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, norm, sandwich
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, norm, np, plt, sandwich


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Kepler Orbits with Geometric Algebra

    The Kepler problem is planar. Geometric algebra makes that plane explicit:
    the radial direction, tangential direction, and angular-momentum bivector are
    all organized by one orbit plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use $\mathrm{Cl}(3,0)$, but keep the orbit in the $e_1$-$e_2$ plane.

    The point of doing that is not to make the orbit 3D. It is to let the
    angular momentum live naturally as a bivector plane element instead of
    hiding it inside a cross-product normal vector.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Orbit and Hodograph

    For a Kepler orbit with eccentricity $e$ and semilatus rectum $p$,

    $$
    r(\theta) = \frac{p}{1 + e\cos\theta}.
    $$

    A rotor in the orbital plane builds the radial and tangential unit vectors at
    the current true anomaly.
    """)
    return


@app.cell
def _(mo):
    eccentricity = mo.ui.slider(0.0, 0.95, step=0.01, value=0.45, label="Eccentricity", show_value=True)
    semilatus = mo.ui.slider(1.0, 10.0, step=0.1, value=4.0, label="Semilatus rectum", show_value=True)
    anomaly = mo.ui.slider(0, 360, step=1, value=80, label="True anomaly", show_value=True)
    return anomaly, eccentricity, semilatus


@app.cell
def _(
    alg,
    anomaly,
    draw_kepler_orbit,
    e1,
    e2,
    eccentricity,
    exp,
    gm,
    mo,
    norm,
    np,
    sandwich,
    semilatus,
):
    _theta = alg.scalar(np.radians(anomaly.value)).name(latex=r"\theta")
    _plane = (e1 ^ e2).name(latex=r"B_{\mathrm{orb}}")
    _R = exp(-(_theta / 2) * _plane)
    _radial = sandwich(_R, e1).name(latex=r"\hat r")
    _tangent = sandwich(_R, e2).name(latex=r"\hat \theta")
    _r = semilatus.value / (1 + eccentricity.value * np.cos(_theta.scalar_part))
    _position = (_r * _radial).name("x")
    _hodograph_center = ((eccentricity.value / np.sqrt(semilatus.value)) * e2).name(latex=r"c_h")
    _velocity = (_hodograph_center + _tangent / np.sqrt(semilatus.value)).name("v")
    _angular_momentum = (_position ^ _velocity).name("L")

    _md = t"""
    {_theta.display()} radians $\\qquad$ ({anomaly.value} degrees) <br/>
    {_plane.display()} <br/>
    {_radial.display()} <br/>
    {_tangent.display()} <br/>
    {_position.display()} <br/>
    {_velocity.display()} <br/>
    {_angular_momentum.display()} <br/>
    {norm(_angular_momentum).display()} $,\\;$ so the orbit stays in one fixed bivector plane.
    """

    mo.vstack(
        [
            eccentricity,
            semilatus,
            anomaly,
            gm.md(_md),
            draw_kepler_orbit(
                eccentricity.value,
                semilatus.value,
                anomaly.value,
                _position.eval(),
                _velocity.eval(),
                _hodograph_center.eval(),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The orbit is not “just a curve in coordinates.” The rotor gives the moving
    radial/tangential frame, and the angular momentum bivector keeps the orbit
    locked to one plane throughout the motion.
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
    def draw_kepler_orbit(eccentricity, semilatus, anomaly_deg, position, velocity, hodograph_center):
        _ths = np.linspace(0, 2 * np.pi, 500)
        _r = semilatus / (1 + eccentricity * np.cos(_ths))
        _x = _r * np.cos(_ths)
        _y = _r * np.sin(_ths)

        _position_xy = np.array(position.vector_part[:2], dtype=float)
        _velocity_xy = np.array(velocity.vector_part[:2], dtype=float)
        _center_xy = np.array(hodograph_center.vector_part[:2], dtype=float)
        _vxs = _center_xy[0] - np.sin(_ths) / np.sqrt(semilatus)
        _vys = _center_xy[1] + np.cos(_ths) / np.sqrt(semilatus)

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.4, 4.8))

        _ax1.plot(_x, _y, color="#2563eb", linewidth=2.5)
        _ax1.plot([0], [0], "o", color="#f59e0b", ms=9)
        _ax1.plot([_position_xy[0]], [_position_xy[1]], "o", color="#222222", ms=7)
        _ax1.set_aspect("equal")
        _ax1.grid(True, alpha=0.25)
        _ax1.set_xlabel("e1")
        _ax1.set_ylabel("e2")
        _ax1.set_title("Configuration-space orbit")

        _ax2.plot(_vxs, _vys, color="#d62828", linewidth=2.5)
        _ax2.plot([_center_xy[0]], [_center_xy[1]], "o", color="#f59e0b", ms=8)
        _ax2.plot([_velocity_xy[0]], [_velocity_xy[1]], "o", color="#222222", ms=7)
        _ax2.set_aspect("equal")
        _ax2.grid(True, alpha=0.25)
        _ax2.set_xlabel("v1")
        _ax2.set_ylabel("v2")
        _ax2.set_title("Velocity-space hodograph")

        plt.close(_fig)
        return _fig

    return (draw_kepler_orbit,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
