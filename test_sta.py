import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, sandwich
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, b_sta


@app.cell
def _(Algebra, b_sta):
    sta = Algebra((1, -1, -1, -1), blades=b_sta(sigmas=True, pss="I"))
    g0, g1, g2, g3 = sta.basis_vectors()
    return g0, g1, sta


@app.cell
def _(g0, g1):
    g1*g0
    return


@app.cell
def _(sta):
    sta.locals(grades=[2], lazy=True)
    return


@app.cell
def _(sta):
    locals().update(sta.locals())
    return


@app.cell
def _():
    return


@app.cell
def _(b_sta):
    b_sta()
    return


if __name__ == "__main__":
    app.run()
