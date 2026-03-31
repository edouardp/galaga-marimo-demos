import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, log, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo

    return Algebra, exp, gm, log, mo, np, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotor Logarithms

    The exponential builds a rotor from a bivector generator. The logarithm runs that process backward and recovers the generator when the rotor lies on the supported branch.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start with the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    A unit bivector $\widehat{B}$ defines a rotation plane, and

    $$
    R = e^{-\theta \widehat{B}/2}
    $$

    is the corresponding rotor. The logarithm should recover the half-angle generator:

    $$
    \log R = -\frac{\theta}{2}\widehat{B}.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 170, step=1, value=55, label="Rotation angle", show_value=True)
    plane = mo.ui.dropdown(
        options=["e12 plane", "e23 plane", "e13 plane"],
        value="e12 plane",
        label="Rotation plane",
    )
    return angle, plane


@app.cell
def _(alg, angle, e1, e2, e3, exp, gm, log, mo, np, plane, unit):
    _planes = {
        "e12 plane": (e1 * e2).name("B"),
        "e23 plane": (e2 * e3).name("B"),
        "e13 plane": (e1 * e3).name("B"),
    }
    _B = unit(_planes[plane.value]).name(latex=r"\widehat{B}")
    _theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
    _half_generator = ((-_theta / 2) * _B).name(latex=r"-\theta \widehat{B}/2")
    _R = exp(_half_generator).name("R")
    _logR = log(_R).name(latex=r"\log R")

    _md = t"""
    {_B.display()} <br/>
    {_theta.display()} <br/>
    {_half_generator.display()} <br/>
    {_R.display()} <br/>
    {_logR.display()} <br/>
    The logarithm recovers the bivector generator that produced the rotor.
    """

    mo.vstack([plane, angle, gm.md(_md)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    Rotor interpolation, fractional rotations, and generator recovery all rely on the same idea: a rotor is not just an operator, it also carries the bivector plane-and-angle information that `log(...)` can expose.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
