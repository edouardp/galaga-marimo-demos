import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(plt):
    def draw_reflections(normal1, normal2, x, x1, x2):
        a = normal1.vector_part[:2]
        b = normal2.vector_part[:2]
        m1 = [-a[1], a[0]]
        m2 = [-b[1], b[0]]
        xv = x.vector_part[:2]
        x1v = x1.vector_part[:2]
        x2v = x2.vector_part[:2]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot([-2.5 * m1[0], 2.5 * m1[0]], [-2.5 * m1[1], 2.5 * m1[1]], color="steelblue", alpha=0.45)
        ax.plot([-2.5 * m2[0], 2.5 * m2[0]], [-2.5 * m2[1], 2.5 * m2[1]], color="darkorange", alpha=0.45)
        ax.annotate("", xy=a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.2, alpha=0.35, linestyle="--"))
        ax.annotate("", xy=b, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="darkorange", lw=1.2, alpha=0.35, linestyle="--"))
        ax.annotate("", xy=xv, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        ax.annotate("", xy=x1v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2, alpha=0.5))
        ax.annotate("", xy=x2v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        ax.plot([], [], color="steelblue", label="first mirror line")
        ax.plot([], [], color="darkorange", label="second mirror line")
        ax.plot([], [], color="black", label="input vector")
        ax.plot([], [], color="black", alpha=0.5, label="after first reflection")
        ax.plot([], [], color="crimson", label="after two reflections")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.25)
        ax.set_xlabel("e1")
        ax.set_ylabel("e2")
        ax.set_title("Two reflections compose to a rotation")
        ax.legend(loc="upper left")
        plt.close(fig)
        return fig

    return (draw_reflections,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotors from Reflections

    This is the third notebook in the reflection-to-rotor sequence. [reflections_ga.py](./reflections_ga.py) shows one reflection, [versor_composition.py](./versor_composition.py) packages two reflections into a versor, and this notebook makes the rotor interpretation explicit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    Its basis vectors satisfy $e_1^2 = e_2^2 = 1$, so reflections preserve lengths, and composing two reflections produces a rotation in the plane.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotors from Reflections

    A rotor can be built from two mirror directions. If $n_1$ and $n_2$ are unit vectors normal to the two reflection lines, then reflecting a vector $x$ twice gives

    $$x' = (-n_2)(-n_1)x n_1 n_2 = (n_2 n_1)\, x \,\widetilde{(n_2 n_1)}.$$

    So the product $R = n_2 n_1$ acts like a rotor. The angle between the mirrors controls the rotation angle of the final vector.
    """)
    return


@app.cell
def _(mo):
    alpha = mo.ui.slider(0, 360, step=1, value=20, label="First mirror line angle", show_value=True)
    beta = mo.ui.slider(0, 360, step=1, value=65, label="Second mirror line angle", show_value=True)
    vector_angle = mo.ui.slider(0, 180, step=1, value=15, label="Input vector angle", show_value=True)
    return alpha, beta, vector_angle


@app.cell
def _(alpha, beta, draw_reflections, e1, e2, gm, mo, np, vector_angle):
    _a = np.radians(alpha.value)
    _b = np.radians(beta.value)
    _v = np.radians(vector_angle.value)

    _line1 = np.cos(_a) * e1 + np.sin(_a) * e2
    _line2 = np.cos(_b) * e1 + np.sin(_b) * e2
    n1 = ((-_line1 | e2) * e1 + (_line1 | e1) * e2).eval().name(latex=r"n_1")
    n2 = ((-_line2 | e2) * e1 + (_line2 | e1) * e2).eval().name(latex=r"n_2")
    x = (np.cos(_v) * e1 + np.sin(_v) * e2).name("x")
    x1 = (-n1 * x * n1).name(latex=r"x_1")
    x2 = (-n2 * x1 * n2).name(latex=r"x_2")
    R = (n2 * n1).name("R")
    x_R = (R * x * ~R).name(latex=r"x'")

    _md = t"""
    {n1.display()} <br/>
    {n2.display()} <br/>
    {x.display()} <br/>
    {x1.display()} <br/>
    {x2.display()} <br/>
    {R.display()} <br/>
    {x_R.display()} <br/>
    Rotation angle: $\\theta = 2(\\beta - \\alpha) = {2 * (beta.value - alpha.value)}^\\circ$
    """

    mo.vstack([alpha, beta, vector_angle, gm.md(_md), draw_reflections(n1, n2, x, x1, x2)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    A rotor is not a mysterious new kind of object. In this 2D Euclidean setting it is the compressed record of two reflections, and the angle between the mirrors determines the final rotation.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
