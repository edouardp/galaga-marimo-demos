import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3D CGA: Spheres and Planes

    After the 2D line/circle story, the 3D analogue is sphere/plane. The conformal
    model treats them in a very similar way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In 3D CGA, a dual sphere centered at $c$ with radius $r$ can be written

    $$
    S = C - \frac{1}{2} r^2 e_\infty,
    $$

    where $C = \operatorname{up}(c)$.

    A plane with Euclidean normal $n$ and offset $d$ can be written

    $$
    \Pi = n + d e_\infty.
    $$

    A conformal point $X$ lies on the object when the corresponding inner product
    vanishes.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(4, 1, blades=b_cga(euclidean=3, null_basis="plus_minus"))
    e1, e2, e3, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3, em, ep


@app.cell
def _(mo):
    mode = mo.ui.dropdown(options={"Sphere": "sphere", "Plane": "plane"}, value="Sphere", label="Object")
    probe_x = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.8, label="Probe x", show_value=True)
    probe_y = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.0, label="Probe y", show_value=True)
    probe_z = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.0, label="Probe z", show_value=True)
    radius = mo.ui.slider(0.4, 1.6, step=0.05, value=1.0, label="Sphere radius", show_value=True)
    plane_z = mo.ui.slider(-1.2, 1.2, step=0.05, value=0.5, label="Plane z offset", show_value=True)
    return mode, plane_z, probe_x, probe_y, probe_z, radius


@app.cell
def _(alg, e1, e2, e3, em, ep, gm, mode, mo, plane_z, probe_x, probe_y, probe_z, radius, sphere_plane_plot):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    def up(vec, name):
        return (eo + vec + half * (vec | vec) * einf).name(latex=name)

    c = alg.scalar(0) * e1
    center = (c + alg.scalar(0) * e2 + alg.scalar(0) * e3).name("c")
    C = up(center, "C")
    r = alg.scalar(radius.value).name("r")
    sphere = (C - half * (r * r) * einf).name("S")

    d = alg.scalar(plane_z.value).name("d")
    plane = (e3 + d * einf).name(latex=r"\Pi")

    p = (probe_x.value * e1 + probe_y.value * e2 + probe_z.value * e3).name("p")
    P = up(p, "P")
    sphere_test = (P | sphere).name(latex=r"P \cdot S")
    plane_test = (P | plane).name(latex=r"P \cdot \Pi")

    if mode.value == "sphere":
        _md = t"""
        {center.display()} <br/>
        {C.display()} <br/>
        {r.display()} <br/>
        {sphere.display()} <br/>
        {P.display()} <br/>
        {sphere_test.display()} <br/>
        Zero means the probe point lies on the sphere.
        """
    else:
        _md = t"""
        {d.display()} <br/>
        {plane.display()} <br/>
        {P.display()} <br/>
        {plane_test.display()} <br/>
        Zero means the probe point lies on the plane.
        """

    mo.vstack([
        mode,
        probe_x,
        probe_y,
        probe_z,
        radius,
        plane_z,
        gm.md(_md),
        sphere_plane_plot(mode.value, probe_x.value, probe_y.value, probe_z.value, radius.value, plane_z.value),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The 3D sphere/plane story is the direct analogue of the 2D circle/line story.
    Once points are conformal, these classical Euclidean objects become simple
    conformal objects tested by one incidence condition.
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
    def sphere_plane_plot(mode, px, py, pz, radius, plane_z):
        _fig = plt.figure(figsize=(7.0, 6.0))
        _ax = _fig.add_subplot(111, projection="3d")

        if mode == "sphere":
            _u = np.linspace(0, 2 * np.pi, 36)
            _v = np.linspace(0, np.pi, 20)
            _x = radius * np.outer(np.cos(_u), np.sin(_v))
            _y = radius * np.outer(np.sin(_u), np.sin(_v))
            _z = radius * np.outer(np.ones_like(_u), np.cos(_v))
            _ax.plot_wireframe(_x, _y, _z, color="#2563eb", alpha=0.18)
        else:
            _g = np.linspace(-1.5, 1.5, 2)
            _X, _Y = np.meshgrid(_g, _g)
            _Z = np.full_like(_X, plane_z)
            _ax.plot_surface(_X, _Y, _Z, color="#2563eb", alpha=0.16)

        _ax.scatter([px], [py], [pz], color="#d62828", s=60)
        _ax.text(px + 0.05, py + 0.05, pz + 0.05, "p", color="#d62828")
        _ax.set_xlim(-1.8, 1.8)
        _ax.set_ylim(-1.8, 1.8)
        _ax.set_zlim(-1.8, 1.8)
        _ax.set_box_aspect((1, 1, 1))
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Euclidean view of the CGA object")
        plt.close(_fig)
        return _fig

    return (sphere_plane_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
