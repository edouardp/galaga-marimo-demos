import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, log, sandwich
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, log, mo, np, plt, sandwich


@app.cell
def _(np, plt):
    def draw_slerp(v0, v1, vt, R0, R1, Rt):
        fig, (ax_rot, ax_vec) = plt.subplots(1, 2, figsize=(10, 4.8))

        R0_eval = R0.eval()
        R1_eval = R1.eval()
        Rt_eval = Rt.eval()
        r0_xy = (R0_eval.data[0], R0_eval.data[3])
        r1_xy = (R1_eval.data[0], R1_eval.data[3])
        rt_xy = (Rt_eval.data[0], Rt_eval.data[3])

        t = np.linspace(0, 2 * np.pi, 200)
        ax_rot.plot(np.cos(t), np.sin(t), color="gray", alpha=0.25)
        ax_rot.annotate("", xy=r0_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        ax_rot.annotate("", xy=r1_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkorange", lw=2))
        ax_rot.annotate("", xy=rt_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax_rot.scatter([r0_xy[0], r1_xy[0], rt_xy[0]], [r0_xy[1], r1_xy[1], rt_xy[1]], color=["steelblue", "darkorange", "crimson"], zorder=3)
        ax_rot.plot([], [], color="steelblue", label="R0")
        ax_rot.plot([], [], color="darkorange", label="R1")
        ax_rot.plot([], [], color="crimson", label="R(t)")
        ax_rot.set_xlim(-1.15, 1.15)
        ax_rot.set_ylim(-1.15, 1.15)
        ax_rot.set_aspect("equal")
        ax_rot.grid(True, alpha=0.25)
        ax_rot.set_xlabel("scalar part")
        ax_rot.set_ylabel("e12 part")
        ax_rot.set_title("Rotor space")
        ax_rot.legend(loc="upper left")

        v0_xy = v0.vector_part[:2]
        v1_xy = v1.vector_part[:2]
        vt_xy = vt.vector_part[:2]
        ax_vec.annotate("", xy=v0_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        ax_vec.annotate("", xy=v1_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkorange", lw=2))
        ax_vec.annotate("", xy=vt_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax_vec.plot([], [], color="steelblue", label="R0 v R̃0")
        ax_vec.plot([], [], color="darkorange", label="R1 v R̃1")
        ax_vec.plot([], [], color="crimson", label="R(t) v R̃(t)")
        ax_vec.set_xlim(-1.4, 1.4)
        ax_vec.set_ylim(-1.4, 1.4)
        ax_vec.set_aspect("equal")
        ax_vec.grid(True, alpha=0.25)
        ax_vec.set_xlabel("e1")
        ax_vec.set_ylabel("e2")
        ax_vec.set_title("Vector space")
        ax_vec.legend(loc="upper left")

        plt.close(fig)
        return fig

    return (draw_slerp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Slerp with Rotors

    Slerp is spherical linear interpolation. For rotors, that means moving at constant angular speed along the unit circle in rotor space instead of linearly blending coefficients. The result stays normalized and gives a clean interpolated rotation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    In the plane, every rotor lies in the span of $1$ and $e_{12}$, so rotor space is a circle. That makes slerp easy to see: we move along that circle, then use the interpolated rotor to act on a vector.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor Slerp

    Given two rotors $R_0$ and $R_1$, define the relative rotor

    $$
    \Delta = \widetilde{R_0} R_1.
    $$

    Then the spherical interpolation is

    $$
    R(t) = R_0 \exp\!\bigl(t \log(\Delta)\bigr), \qquad 0 \le t \le 1.
    $$

    At $t=0$ we recover $R_0$, at $t=1$ we recover $R_1$, and for intermediate values we stay on the unit rotor manifold instead of cutting straight across it.
    """)
    return


@app.cell
def _(mo):
    start_angle = mo.ui.slider(0, 180, step=1, value=20, label="Start angle θ0", show_value=True)
    end_angle = mo.ui.slider(0, 180, step=1, value=110, label="End angle θ1", show_value=True)
    blend = mo.ui.slider(0.0, 1.0, step=0.01, value=0.5, label="Blend t", show_value=True)
    return blend, end_angle, start_angle


@app.cell
def _(
    alg,
    blend,
    draw_slerp,
    e1,
    e2,
    end_angle,
    exp,
    gm,
    log,
    mo,
    np,
    sandwich,
    start_angle,
):
    theta0 = alg.scalar(np.radians(start_angle.value)).name(latex=r"\theta_0")
    theta1 = alg.scalar(np.radians(end_angle.value)).name(latex=r"\theta_1")
    B = (e1 * e2).name("B")

    R0 = exp(-B * theta0 / 2).name("R_0")
    R1 = exp(-B * theta1 / 2).name("R_1")
    Delta = (~R0 * R1).name(r"\Delta")
    Rt = (R0 * exp(blend.value * log(Delta))).name("R(t)")

    v = e1.name("v")
    v0 = sandwich(R0, v).name("v_0")
    v1 = sandwich(R1, v).name("v_1")
    vt = sandwich(Rt, v).name("v_t")

    _md = t"""
    {B.display()} $\\quad with \\quad$ {(B**2).display(compact=True)} <br/>
    {R0.display()} <br/>
    {R1.display()} <br/>
    {Delta.display()} <br/>
    {log(Delta).display()} <br/>
    {Rt.display()} <br/>
    {(Rt * ~Rt).display()} <br/>
    $t = {blend.value:.2f}$ gives an interpolated rotation angle of about ${(1 - blend.value) * start_angle.value + blend.value * end_angle.value:.1f}^\\circ$
    """

    mo.vstack([start_angle, end_angle, blend, gm.md(_md), draw_slerp(v0, v1, vt, R0, R1, Rt)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why Slerp Instead of Linear Blending?

    Linear interpolation of rotor coefficients generally leaves the unit rotor manifold and distorts the angular speed. Slerp stays on the rotor circle, keeps the rotor normalized, and interpolates by composing a fractional relative rotation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    Slerp is a natural fit for geometric algebra: compute the relative rotor, take its logarithm, scale that generator, and exponentiate back. The interpolated rotor remains a true rotor the whole time, and the vector it acts on moves smoothly with it.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
