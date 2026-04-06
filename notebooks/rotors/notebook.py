import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import (
        Algebra, exp
    )
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    Its basis vectors satisfy $e_1^2 = e_2^2 = 1$, so lengths and angles behave like the usual plane, and the bivector $e_1 e_2$ generates ordinary rotations.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1,1))
    e1,e2 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotations with Rotors in Geometric Algebra

    In geometric algebra, we rotate vectors using **rotors** — objects built from bivectors via the exponential map.

    Given a bivector $B = e_1 \wedge e_2$ (representing the plane of rotation) and an angle $\theta$, the rotor is:

    $$R = e^{-B \theta/2}$$

    To rotate a vector $\mathbf{v}$, we apply the **sandwich product**:

    $$\mathbf{v'} = R\mathbf{v}\tilde{R}$$

    where $\tilde{R}$ is the reverse of $R$. The half-angle in the exponential is what makes this work — the double-sided product produces a full rotation by $\theta$.

    Use the slider below to explore how the rotation angle affects the transformed vector $\mathbf{v'}$.
    """)
    return


@app.cell
def _(mo):
    theta_slider = mo.ui.slider(0, 360, value=45, label="θ (degrees)", show_value=True)
    return (theta_slider,)


@app.cell
def _(alg, draw_rotation, e1, e2, exp, gm, mo, np, theta_slider):
    theta = alg.scalar(np.radians(theta_slider.value)).name(latex=r"\theta")
    half = alg.frac(1, 2)
    B = (e1 ^ e2).name(latex="B")
    R = exp(-B * theta * half).name(latex="R")
    v = (e1 + e2).name(latex="v")
    vp = (R * v * ~R).name(latex=r"v'")

    _md = t"""
    {theta.display()} radians $\\quad = \\quad {theta_slider.value}\\degree$ <br/>
    {B.display()} <br/>
    {R.display()} <br/>
    {v.display()} <br/>
    {vp.display()}
    """

    mo.vstack([theta_slider, gm.md(_md), draw_rotation(v, vp)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(plt):
    def draw_rotation(v, vp):
        _v_xy = v.vector_part[:2].tolist()
        _vp_xy = vp.vector_part[:2].tolist()
        _fig, _ax = plt.subplots(figsize=(4, 4))
        _ax.annotate('', xy=_v_xy, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='blue', lw=2))
        _ax.annotate('', xy=_vp_xy, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        _ax.plot([], [], color='blue', label='v')
        _ax.plot([], [], color='red', label="v'")
        _ax.set_xlim(-1.8, 1.8)
        _ax.set_ylim(-1.8, 1.8)
        _ax.set_aspect('equal')
        _ax.grid(True)
        _ax.legend()
        _ax.set_title('Rotation')
        plt.close(_fig)
        return _fig

    return (draw_rotation,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
