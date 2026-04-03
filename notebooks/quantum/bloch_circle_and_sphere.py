import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, grade, norm, grade,scalar_sqrt
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, grade, mo, norm, np, plt, scalar_sqrt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloch Circle and Bloch Sphere

    A spin-$\tfrac12$ pure state can be represented by a rotor, but the thing we usually draw is its **observable direction**:

    $$
    s = R e_k \tilde R.
    $$

    In 2D that direction lives on a circle. In 3D it lives on the full Bloch sphere.

    This notebook puts the two views next to each other conceptually:

    - a 2D Bloch-circle demonstration
    - a 3D Bloch-sphere demonstration
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean algebra $\mathrm{Cl}(2,0)$.

    In 2D the even subalgebra is spanned by $1$ and $e_{12}$, so one rotor already sweeps out every possible observable direction in the plane:

    $$
    R(\phi) = e^{-(\phi/2)e_{12}},
    \qquad
    s = R e_1 \tilde R.
    $$

    This is the simplest possible Bloch picture: the observable state moves around a circle.
    """)
    return


@app.cell
def _(Algebra):
    alg2 = Algebra((1, 1))
    a1, a2 = alg2.basis_vectors(lazy=True)
    a12 = a1 ^ a2
    return a1, a2


@app.cell
def _(Algebra):
    alg3 = Algebra((1, 1, 1))
    e1, e2, e3 = alg3.basis_vectors(lazy=True)
    return alg3, e1, e2, e3


@app.cell
def _(mo):
    circle_angle = mo.ui.slider(0, 360, step=1, value=45, label="2D physical angle φ", show_value=True)
    return (circle_angle,)


@app.cell
def _(a1, a2, circle_angle, draw_bloch_circle, exp, gm, mo, np):
    _phi = np.radians(circle_angle.value)
    _R = exp((-_phi / 2) * (a1 * a2)).name(latex=r"R_{2D}")
    _s = (_R * a1 * ~_R).name(latex=r"s_{2D}")
    _xy = _s.eval().vector_part[:2]

    _md = t"""
    {_R.display()} <br/>
    {_s.display()} <br/>
    Bloch-circle direction: $({_xy[0]:.3f}, {_xy[1]:.3f})$ <br/>
    Physical angle on the circle: ${circle_angle.value}^\\circ$
    """

    mo.vstack([circle_angle, gm.md(_md), draw_bloch_circle(_s)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now switch to the 3D Euclidean algebra $\mathrm{Cl}(3,0)$.

    Here a rotor can move the reference axis $e_3$ to any point on the sphere:

    $$
    s = R e_3 \tilde R.
    $$

    The usual Bloch-sphere angles are:

    $$
    R(\theta,\phi) = e^{-(\phi/2)e_{12}} e^{-(\theta/2)e_{31}}.
    $$

    This is the full qubit-state picture: polar angle $\theta$ controls how far we move from the poles, and azimuth $\phi$ controls the phase around the equator.
    """)
    return


@app.cell
def _(mo):
    theta = mo.ui.slider(0, 180, step=1, value=60, label="3D polar angle θ", show_value=True)
    phi = mo.ui.slider(0, 360, step=1, value=30, label="3D azimuth φ", show_value=True)
    return phi, theta


@app.cell
def _(alg3, draw_bloch_sphere, e1, e2, e3, exp, gm, mo, np, phi, theta):
    _half = alg3.frac(1,2)

    _theta = alg3.scalar(np.radians(theta.value)).name(latex=r"\theta")
    _phi = alg3.scalar(np.radians(phi.value)).name(latex=r"\phi")

    _B_azimuth = (e1 ^ e2).name(latex=r"B_{az}")
    _B_polar = (e3 ^ e1).name(latex=r"B_{plr}")

    _R = (exp(-_phi * _B_azimuth / 2) * exp(-_theta * _B_polar / 2)).name(latex=r"R")

    _s = (_R * e3 * ~_R).name(latex=r"s")
    _xyz = _s.vector_part

    _p0 = (_half * (1 + (_s | e3))).name("P(0)")
    _p1 = (_half * (1 - (_s | e3))).name("P(1)")

    _md = t"""
    {_R.display()} <br/>
    {_s.display()} <br/>
    Bloch-sphere direction: $({_xyz[0]:.3f}, {_xyz[1]:.3f}, {_xyz[2]:.3f})$ <br/>
    {_p0.display()} </br>
    {_p1.display()} </br>
    Polar angle: ${theta.value}^\\circ, \\qquad$ azimuth: ${phi.value}^\\circ$
    """

    mo.vstack([theta, phi, gm.md(_md), draw_bloch_sphere(_s)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The Bloch circle is the 2D version of the same idea as the Bloch sphere: a pure spin state is represented by a rotor, but what we draw is the observable direction that rotor produces.
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
    def draw_bloch_circle(state):
        _s = np.array(state.eval().vector_part[:2], dtype=float)

        _fig = plt.figure(figsize=(6.2, 5.6))
        _ax = _fig.add_subplot(111)
        _circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", alpha=0.25, linewidth=1.2)
        _ax.add_patch(_circle)
        _ax.axhline(0, color="gray", alpha=0.15, linewidth=0.8)
        _ax.axvline(0, color="gray", alpha=0.15, linewidth=0.8)
        _ax.annotate(
            "",
            xy=_s,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2.8, mutation_scale=18, alpha=0.95),
        )
        _ax.text(1.08 * _s[0], 1.08 * _s[1], r"$s_{2D}$", color="#7c3aed", ha="center", va="center")
        _ax.text(1.12, 0, r"$e_1$", color="#444444", ha="center", va="center", fontsize=12)
        _ax.text(-1.12, 0, r"$-e_1$", color="#444444", ha="center", va="center", fontsize=12)
        _ax.text(0, 1.14, r"$e_2$", color="#444444", ha="center", va="center", fontsize=12)
        _ax.text(0, -1.14, r"$-e_2$", color="#444444", ha="center", va="center", fontsize=12)
        _ax.set_xlim(-1.25, 1.25)
        _ax.set_ylim(-1.25, 1.25)
        _ax.set_aspect("equal")
        _ax.set_xticks([])
        _ax.set_yticks([])
        _ax.set_title("Bloch Circle", fontsize=12)
        plt.close(_fig)
        return _fig

    def draw_bloch_sphere(state):
        _s = np.array(state.eval().vector_part, dtype=float)

        _fig = plt.figure(figsize=(7.0, 6.2))
        _ax = _fig.add_subplot(111, projection="3d")

        _u = np.linspace(0, 2 * np.pi, 48)
        _v = np.linspace(0, np.pi, 28)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax.plot_wireframe(_x, _y, _z, color="gray", alpha=0.10, linewidth=0.6)

        _ax.quiver(0, 0, 0, 1, 0, 0, color="#2563eb", linewidth=1.8, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, -1, 0, 0, color="#2563eb", linewidth=1.2, alpha=0.30, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 1, 0, color="#16a34a", linewidth=1.8, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, -1, 0, color="#16a34a", linewidth=1.2, alpha=0.30, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 0, 1, color="#d62828", linewidth=2.2, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, 0, 0, -1, color="#d62828", linewidth=1.5, alpha=0.35, arrow_length_ratio=0.08)
        _ax.quiver(0, 0, 0, _s[0], _s[1], _s[2], color="#7c3aed", linewidth=3.0, arrow_length_ratio=0.10)

        _ax.text(1.12, 0, 0, r"$+e_1$", color="#2563eb")
        _ax.text(-1.22, 0, 0, r"$-e_1$", color="#2563eb")
        _ax.text(0, 1.12, 0, r"$+e_2$", color="#16a34a")
        _ax.text(0, -1.22, 0, r"$-e_2$", color="#16a34a")
        _ax.text(0, 0, 1.14, r"$+e_3\;( |0\rangle )$", color="#d62828")
        _ax.text(0, 0, -1.25, r"$-e_3\;( |1\rangle )$", color="#d62828")

        _ax.set_xlim(-1.1, 1.1)
        _ax.set_ylim(-1.1, 1.1)
        _ax.set_zlim(-1.1, 1.1)
        _ax.set_box_aspect((1, 1, 1))
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Bloch Sphere", fontsize=12)
        plt.close(_fig)
        return _fig

    return draw_bloch_circle, draw_bloch_sphere


@app.cell
def _():
    return


@app.cell
def _(alg3, e1, e2, e3, exp, gm, grade, norm, np, scalar_sqrt):
    _v = (0+e3).name("v")
    _theta = alg3.scalar(np.radians(45)).name(latex=r"\theta")
    _B = (e1 ^ e2).name("B")
    _R = exp(_theta * _B / 2).name("R")

    gm.md(t"""
    {_v.display()} <br/>
    {_R.display()} <br/>
    {(~_R).display()} <br/>
    {(_R*~_R).display()} <br/>
    {(_R * _v).display()} <br/>
    {norm(_R * _v).display()} <br/>
    {scalar_sqrt(grade((_R*_v) * (_v * ~_R), 0)).display()} <br/>
    {(_v * ~_R).display()} <br/>
    """)
    return


@app.cell
def _(np):
    np.sqrt(0.92388**2 + 0.382683**2)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
