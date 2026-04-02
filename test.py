import marimo

__generated_with = "0.22.0"
app = marimo.App()


@app.cell
def _():
    from galaga import Algebra, rev, complement, conjugate, dual, Notation

    return Algebra, Notation


@app.cell
def _(Algebra):
    sta = Algebra([1,-1,-1,-1], names="gamma")
    y0,y1,y2,y3 = sta.basis_vectors(lazy=True)
    return y0, y1, y2


@app.cell
def _(Algebra, Notation):

    alg = Algebra([1,1,1], notation=Notation().hestenes())
    e1,e2,e3 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(e1, e2):
    B = e1^e2
    return (B,)


@app.cell
def _(B):
    B**2
    return


@app.cell
def _(B):
    (B*B).display()
    return


@app.cell
def _(B):
    (B*~B).display()
    return


@app.cell
def _(y0, y1, y2):
    C = y0^y1
    D = y1^y2
    return


@app.cell
def _(B):
    ~B
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
