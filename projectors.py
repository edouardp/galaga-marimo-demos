import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, project, reject
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, project, reject


@app.cell
def _(np, plt):
    def draw_line_projection(a, p, r, v):
        a_xy = a.eval().vector_part[:2]
        v_xy = v.eval().vector_part[:2]
        p_xy = p.eval().vector_part[:2]
        r_xy = r.eval().vector_part[:2]

        fig, ax = plt.subplots(figsize=(5.8, 5.8))
        ax.plot([-2.5 * a_xy[0], 2.5 * a_xy[0]], [-2.5 * a_xy[1], 2.5 * a_xy[1]], color="gray", alpha=0.5)
        ax.annotate("", xy=v_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        ax.annotate("", xy=p_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        ax.annotate("", xy=(p_xy[0] + r_xy[0], p_xy[1] + r_xy[1]), xytext=(p_xy[0], p_xy[1]), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax.plot([], [], color="black", label="v")
        ax.plot([], [], color="steelblue", label="proj")
        ax.plot([], [], color="crimson", label="rej")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.25)
        ax.set_xlabel("e1")
        ax.set_ylabel("e2")
        ax.set_title("Projection onto a line")
        ax.legend(loc="upper left")
        plt.close(fig)
        return fig

    def draw_plane_projection(v, p_plane, r_plane, plane_angle_deg):
        v_xyz = v.eval().vector_part
        p_xyz = p_plane.eval().vector_part
        r_xyz = r_plane.eval().vector_part

        fig = plt.figure(figsize=(6.6, 5.4))
        ax = fig.add_subplot(111, projection="3d")

        angle = np.radians(plane_angle_deg)
        u = np.array([np.cos(angle), np.sin(angle), 0.0])
        w = np.array([0.0, 0.0, 1.0])
        s = np.linspace(-2.4, 2.4, 2)
        t = np.linspace(-2.4, 2.4, 2)
        ss, tt = np.meshgrid(s, t)
        xx = ss * u[0] + tt * w[0]
        yy = ss * u[1] + tt * w[1]
        zz = ss * u[2] + tt * w[2]

        ax.plot_surface(xx, yy, zz, alpha=0.12, color="steelblue")
        ax.quiver(0, 0, 0, v_xyz[0], v_xyz[1], v_xyz[2], color="black", linewidth=2.5, arrow_length_ratio=0.08)
        ax.quiver(0, 0, 0, p_xyz[0], p_xyz[1], p_xyz[2], color="steelblue", linewidth=2.5, arrow_length_ratio=0.08)
        ax.quiver(p_xyz[0], p_xyz[1], p_xyz[2], r_xyz[0], r_xyz[1], r_xyz[2], color="crimson", linewidth=2.5, arrow_length_ratio=0.08)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)
        ax.set_box_aspect((1, 1, 1))
        ax.set_xlabel("e1")
        ax.set_ylabel("e2")
        ax.set_zlabel("e3")
        ax.set_title("Projection into a plane")
        plt.close(fig)
        return fig

    return draw_line_projection, draw_plane_projection


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    Its basis vectors satisfy $e_1^2 = e_2^2 = e_3^2 = 1$. In this notebook the same named operations, `project(v, B)` and `reject(v, B)`, will act on two different kinds of blades: a vector for a line, and a bivector for a plane.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Projectors in Geometric Algebra

    Projection is one of the clearest places where GA unifies what are usually taught as separate tricks.

    For a vector $v$ and an invertible blade $B$,

    $$
    \operatorname{proj}_B(v) = (v \rfloor B) B^{-1},
    \qquad
    \operatorname{rej}_B(v) = (v \wedge B) B^{-1}.
    $$

    The important point is not the formula alone. It is that the same operation works whether $B$ represents a line or a plane.
    """)
    return


@app.cell
def _(mo):
    line_angle = mo.ui.slider(0, 180, step=1, value=30, label="Line angle", show_value=True)
    line_vx = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.6, label="v_x", show_value=True)
    line_vy = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.1, label="v_y", show_value=True)
    line_vz = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.8, label="v_z", show_value=True)
    return line_angle, line_vx, line_vy, line_vz


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Projection onto a Line

    A line is represented by a 1-blade. Here we rotate the reference direction $e_1$ inside the $e_1 e_2$ plane to define the line direction $a$.
    """)
    return


@app.cell
def _(
    draw_line_projection,
    e1,
    e2,
    e3,
    exp,
    gm,
    line_angle,
    line_vx,
    line_vy,
    line_vz,
    mo,
    np,
    project,
    reject,
):
    line_theta = np.radians(line_angle.value)
    line_R = exp(-(e1 * e2) * line_theta / 2).name("R")
    a = (line_R * e1 * ~line_R).name("a")
    line_v = (line_vx.value * e1 + line_vy.value * e2 + line_vz.value * e3).name("v")
    p = project(line_v, a).name("p")
    r = reject(line_v, a).name("r")

    _md = t"""
    {a.display()} <br/>
    {line_v.display()} <br/>
    {p.display()} <br/>
    {r.display()} <br/>
    Check: {(p + r).display()} = {line_v.eval()}
    """

    mo.vstack([
        line_angle,
        line_vx,
        line_vy,
        line_vz,
        gm.md(_md),
        draw_line_projection(a, p, r, line_v),
    ])
    return


@app.cell
def _(mo):
    plane_angle = mo.ui.slider(0, 180, step=1, value=30, label="Plane angle", show_value=True)
    plane_vx = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.6, label="v_x", show_value=True)
    plane_vy = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.1, label="v_y", show_value=True)
    plane_vz = mo.ui.slider(-3.0, 3.0, step=0.1, value=0.8, label="v_z", show_value=True)
    return plane_angle, plane_vx, plane_vy, plane_vz


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Projection into a Plane

    A plane is represented by a 2-blade. Starting from the reference plane $e_1 \wedge e_3$, we rotate that blade to get a new plane $B$. The same `project` and `reject` operations now keep the in-plane part and remove the normal part.
    """)
    return


@app.cell
def _(
    draw_plane_projection,
    e1,
    e2,
    e3,
    exp,
    gm,
    mo,
    np,
    plane_angle,
    plane_vx,
    plane_vy,
    plane_vz,
    project,
    reject,
):
    plane_theta = np.radians(plane_angle.value)
    plane_R = exp(-(e1 * e2) * plane_theta / 2).name("R")
    B = (plane_R * (e1 ^ e3) * ~plane_R).name("B")
    plane_v = (plane_vx.value * e1 + plane_vy.value * e2 + plane_vz.value * e3).name("v")
    p_plane = project(plane_v, B).name(latex="p_B")
    r_plane = reject(plane_v, B).name(latex="r_B")

    _md = t"""
    {B.display()} <br/>
    {plane_v.display()} <br/>
    {p_plane.display()} <br/>
    {r_plane.display()} <br/>
    Check: {(p_plane + r_plane).display()} $= v$
    """

    mo.vstack([
        plane_angle,
        plane_vx,
        plane_vy,
        plane_vz,
        gm.md(_md),
        draw_plane_projection(plane_v, p_plane, r_plane, plane_angle.value),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    In ordinary vector calculus, projecting onto a line and into a plane are often presented as different formulas. In geometric algebra they are the same construction against different blades. That is the real simplification.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
