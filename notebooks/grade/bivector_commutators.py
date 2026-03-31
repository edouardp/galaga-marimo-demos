import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, commutator, lie_bracket
    import galaga_marimo as gm
    import marimo as mo

    return Algebra, commutator, gm, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bivector Commutators

    Bivectors are not just plane elements. Under the commutator they form the Lie algebra of infinitesimal rotations. That is why bivectors are the natural generators for rotors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We work in the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$.

    The commutator of two bivectors tells you how their infinitesimal rotation generators fail to commute.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(commutator, e1, e2, e3, gm):
    _A = (e1 ^ e2).name("A")
    _B = (e2 ^ e3).name("B")
    _C = (e1 ^ e3).name("C")
    _AB = commutator(_A, _B)
    _BC = commutator(_B, _C)
    _CA = commutator(_C, _A)

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_C.display()} <br/>
    {_AB.display()} <br/>
    {_BC.display()} <br/>
    {_CA.display()} <br/>
    The commutator closes on bivectors again, which is the Lie-algebra structure behind 3D rotations.
    """

    gm.md(_md)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    Rotor exponentials come from bivectors because bivectors already carry the infinitesimal rotation algebra. The commutator shows that this is not an accident of notation; it is the structural reason rotors work.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
