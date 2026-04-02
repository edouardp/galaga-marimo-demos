import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt, sandwich


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotor Space

    Rotors are the objects we use to rotate vectors, but rotors are also geometric objects in their own right. This notebook separates those two roles: vectors rotate by a sandwich product, while rotors themselves move naturally by single-sided multiplication.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    Its basis vectors satisfy $e_1^2 = e_2^2 = 1$, and the bivector $e_{12} = e_1 e_2$ squares to $-1$. That means rotors in the plane live in the two-dimensional span of $1$ and $e_{12}$, which is exactly the rotor space we can plot.
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
    ## One Rotor Acting on a Vector

    For a plane bivector $B = e_{12}$, a rotor is

    $$
    R = e^{-B\theta/2}.
    $$

    It rotates a vector $v$ by the sandwich product

    $$
    v' = R v \widetilde{R}.
    $$

    But if we want to move the rotor itself, we do not sandwich it. A rotor is already an operator, so multiplying by another rotor composes actions directly:

    $$
    R_{\text{new}} = S R.
    $$

    Then the new rotor acts on vectors in the usual way:

    $$
    v'' = R_{\text{new}} v \widetilde{R_{\text{new}}}.
    $$
    """)
    return


app._unparsable_cell(
    r"""
    theta = mo.ui.slider(0, 360, step=1, value=45, label="Base rotor angle θ", show_value=True)
    alpha = mo.ui.slider(0, 360, step=1, value=30, label="Rotor-space shift α", show_value=True)
    beta = mo.ui```python
    .slider(0, 360, step=1, value=60, label="Stator-space shift β", show_value=True)

    ```
    """,
    name="_"
)


@app.cell
def _(alg, alpha, draw_rotor_space, e1, e2, exp, gm, mo, np, sandwich, theta):
    theta_rad = alg.scalar(np.radians(theta.value)).name(latex=r"\theta")
    alpha_rad = alg.scalar(np.radians(alpha.value)).name(latex=r"\alpha")

    B = (e1 ^ e2).name("B")
    R = exp(-B * theta_rad / 2).name("R")
    S = exp(-B * alpha_rad / 2).name("S")
    R_new = (S * R).name("S R")

    v = e1.copy_as("v")
    v_rot = sandwich(R, v).name("v'")
    v_rotated_rotor = sandwich(R_new, v).name("v''")

    total_angle = theta.value + alpha.value

    _md = t"""
    {B.display()} $\\quad with \\quad$ {(B**2).display(compact=True)} <br/>
    {R.display()} <br/>
    {S.display()} <br/>
    {R_new.display()} <br/>
    {v.display()} <br/>
    {v_rot.display()} <br/>
    {v_rotated_rotor.display()} <br/>
    Single-sided multiplication adds the rotor actions: $\\theta_{{\\mathrm{{total}}}} =$ {theta.value}$^\\circ + {alpha.value}^\\circ =$ {total_angle}$^\\circ$
    """

    mo.vstack([theta, alpha, gm.md(_md), draw_rotor_space(v, v_rot, v_rotated_rotor, R, R_new)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why Single-Sided Multiplication?

    The sandwich product is designed to keep vectors inside vector space. A rotor is different: it already lives in the even subalgebra, and left multiplication by another rotor means "do this extra rotation as well." In 2D rotor space that is visible as motion around the unit circle of rotor coefficients.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    Rotors act on vectors by sandwiches, but rotors themselves transform most naturally by composition. That is the reason for the single-sided update: first move the rotor in rotor space, then use the new rotor to rotate the vector.
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
    def draw_rotor_space(v, v_rot, v_rotated_rotor, R, R_rot):
        fig, (ax_rot, ax_vec) = plt.subplots(1, 2, figsize=(10, 4.8))

        v_xy = v.vector_part[:2]
        vr_xy = v_rot.vector_part[:2]
        vrr_xy = v_rotated_rotor.vector_part[:2]

        ax_vec.annotate("", xy=v_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        ax_vec.annotate("", xy=vr_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        ax_vec.annotate("", xy=vrr_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax_vec.plot([], [], color="black", label="input vector")
        ax_vec.plot([], [], color="steelblue", label=(R*v*~R).latex(wrap="$"))  #"R v R̃")
        ax_vec.plot([], [], color="crimson", label=(R_rot*v*~R_rot).latex(wrap="$"))  #"(S R) v (S R)̃")
        ax_vec.set_xlim(-1.4, 1.4)
        ax_vec.set_ylim(-1.4, 1.4)
        ax_vec.set_aspect("equal")
        ax_vec.grid(True, alpha=0.25)
        ax_vec.set_xlabel("e1")
        ax_vec.set_ylabel("e2")
        ax_vec.set_title("Vector space")
        ax_vec.legend(loc="upper left")

        R_eval = R.eval()
        R_rot_eval = R_rot.eval()
        r_xy = (R_eval.data[0], R_eval.data[3])
        rr_xy = (R_rot_eval.data[0], R_rot_eval.data[3])

        t = np.linspace(0, 2 * np.pi, 200)
        ax_rot.plot(np.cos(t), np.sin(t), color="gray", alpha=0.25)
        ax_rot.annotate("", xy=r_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        ax_rot.annotate("", xy=rr_xy, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax_rot.scatter([r_xy[0], rr_xy[0]], [r_xy[1], rr_xy[1]], color=["steelblue", "crimson"], zorder=3)
        ax_rot.plot([], [], color="steelblue", label="R")
        ax_rot.plot([], [], color="crimson", label="S R")
        ax_rot.set_xlim(-1.15, 1.15)
        ax_rot.set_ylim(-1.15, 1.15)
        ax_rot.set_aspect("equal")
        ax_rot.grid(True, alpha=0.25)
        ax_rot.set_xlabel("scalar part")
        ax_rot.set_ylabel("e12 part")
        ax_rot.set_title("Rotor space")
        ax_rot.legend(loc="upper left")

        plt.close(fig)
        return fig

    return (draw_rotor_space,)


if __name__ == "__main__":
    app.run()
