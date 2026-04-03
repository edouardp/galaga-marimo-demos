import marimo

__generated_with = "0.22.0"
app = marimo.App()


@app.cell
def _():
    from galaga import Algebra, rev, complement, conjugate, dual, Notation, log
    import galaga_marimo as gm

    return Algebra, Notation, gm


@app.cell
def _(Algebra, Notation):
    alg = Algebra([1,1,1], notation=Notation().with_scientific(style="times"))
    e1,e2,e3 = alg.basis_vectors(lazy=True)
    return alg, e1


@app.cell
def _(alg, e1, gm):
    v = alg.pi * e1

    gm.md(t"""
    {(alg.c * alg.hbar).display():g} <br/>
    {(alg.pi).display():g} <br/>

    """)
    return


@app.cell
def _(alg):
    alg.c.display()
    return


@app.cell
def _():
    print(1/100000)
    return


@app.cell
def _(alg):
    alg.hbar.display()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
