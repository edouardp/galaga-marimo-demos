import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, hestenes_inner, doran_lasenby_inner
    from galaga.notation import Notation
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo

    return Algebra, Notation, exp, gm, mo, np


@app.cell
def _(Algebra, Notation):
    alg = Algebra([1,1,1], notation=Notation.doran_lasenby())
    e1,e2,e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2


@app.cell
def _(mo):
    slider = mo.ui.slider(0,180, show_value=True)
    return (slider,)


@app.cell
def _(alg, e1, e2, exp, gm, mo, np, slider):
    theta = alg.scalar(np.radians(slider.value)).name(latex=r"\theta")
    v = (e1+e2).name("v")
    B = (e1^e2).name("B")
    R = exp(-B*theta/2).name("R")
    vp = (R * v * ~R).name("v'")

    _md = gm.md(t"""
    {theta.display()} <br/>
    {v.display()} <br/>
    {B.display()} <br/>
    {R.display()} <br/>
    {vp.display()} <br/>
    """)

    mo.vstack([slider, _md])
    return


@app.cell
def _(e1, e2):
    e1^e2
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
