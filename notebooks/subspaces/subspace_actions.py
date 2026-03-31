import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, project, reflect, reject
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt, project, reflect, reject


@app.cell
def _(np, plt):
    def draw_subspace_actions(a, v, p, r, vr):
        _a = a.eval().vector_part[:2]
        _v = v.eval().vector_part[:2]
        _p = p.eval().vector_part[:2]
        _r = r.eval().vector_part[:2]
        _vr = vr.eval().vector_part[:2]
        _fig, _ax = plt.subplots(figsize=(6, 6))
        _ax.plot([-2.5 * _a[0], 2.5 * _a[0]], [-2.5 * _a[1], 2.5 * _a[1]], color="gray", alpha=0.5)
        _ax.annotate("", xy=_v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
        _ax.annotate("", xy=_p, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2))
        _ax.annotate("", xy=(_p[0] + _r[0], _p[1] + _r[1]), xytext=(_p[0], _p[1]), arrowprops=dict(arrowstyle="->", color="darkorange", lw=2))
        _ax.annotate("", xy=_vr, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2))
        _ax.plot([], [], color="black", label="v")
        _ax.plot([], [], color="steelblue", label="proj")
        _ax.plot([], [], color="darkorange", label="rej")
        _ax.plot([], [], color="crimson", label="reflect")
        _ax.set_xlim(-3, 3)
        _ax.set_ylim(-3, 3)
        _ax.set_aspect("equal")
        _ax.grid(True, alpha=0.25)
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_title("Projection, rejection, and reflection")
        _ax.legend(loc="upper left")
        plt.close(_fig)
        return _fig

    return (draw_subspace_actions,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Projection, Rejection, and Reflection

    These are three closely related subspace actions. Projection keeps the part parallel to a subspace, rejection keeps the complementary part, and reflection flips the rejected part while leaving the projected part alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    A unit vector $a$ defines a line. Relative to that line:

    - `project(v, a)` keeps the parallel part
    - `reject(v, a)` keeps the perpendicular part
    - `reflect(v, a)` keeps one part and flips the other
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    line_angle = mo.ui.slider(0, 180, step=1, value=35, label="Line angle", show_value=True)
    vector_angle = mo.ui.slider(0, 180, step=1, value=70, label="Vector angle", show_value=True)
    vector_length = mo.ui.slider(0.3, 2.0, step=0.05, value=1.3, label="Vector length", show_value=True)
    return line_angle, vector_angle, vector_length


@app.cell
def _(draw_subspace_actions, e1, e2, gm, line_angle, mo, np, project, reflect, reject, vector_angle, vector_length):
    _a = np.radians(line_angle.value)
    _v = np.radians(vector_angle.value)
    _line = (np.cos(_a) * e1 + np.sin(_a) * e2).name("a")
    _vec = (vector_length.value * np.cos(_v) * e1 + vector_length.value * np.sin(_v) * e2).name("v")
    _p = project(_vec, _line).name("p")
    _r = reject(_vec, _line).name("r")
    _vr = reflect(_vec, _line).name("v'")

    _md = t"""
    {_line.display()} <br/>
    {_vec.display()} <br/>
    {_p.display()} <br/>
    {_r.display()} <br/>
    {_vr.display()} <br/>
    Check: ${((_p + _r).eval()).latex()} = {(_vec.eval()).latex()}$
    """

    mo.vstack([line_angle, vector_angle, vector_length, gm.md(_md), draw_subspace_actions(_line, _vec, _p, _r, _vr)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Family of Ideas

    These are not unrelated formulas. They are the same geometric decomposition used in three different ways. That is one of the recurring themes of GA: one subspace object supports several clean actions.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
