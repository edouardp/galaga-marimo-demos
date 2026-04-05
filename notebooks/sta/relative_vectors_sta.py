import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_sta
    import galaga_marimo as gm
    import marimo as mo

    return Algebra, gm, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Relative Vectors in STA

    The spatial vectors of ordinary 3D geometry live naturally inside spacetime algebra. The key objects are the relative vectors

    $$
    \sigma_i = \gamma_i \gamma_0.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build the spacetime algebra $\mathrm{Cl}(1,3)$ with signature $(+,-,-,-)$.

    The relative vectors are bivectors in STA, but they form a subalgebra isomorphic to the Pauli algebra. That is how Euclidean 3D vector geometry appears inside spacetime geometry.
    """)
    return


@app.cell
def _(Algebra):
    sta = Algebra((1, -1, -1, -1), blades=b_sta())
    g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
    return g0, g1, g2, g3


@app.cell
def _(g0, g1, g2, g3, gm):
    _s1 = (g1 * g0).name(latex=r"\sigma_1")
    _s2 = (g2 * g0).name(latex=r"\sigma_2")
    _s3 = (g3 * g0).name(latex=r"\sigma_3")

    _md = t"""
    {_s1.display()} <br/>
    {_s2.display()} <br/>
    {_s3.display()} <br/>
    {(_s1**2).display()}, $\\quad$ {(_s2**2).display()}, $\\quad$ {(_s3**2).display()} <br/>
    {(_s1 * _s2).display()}, $\\quad$ {(_s2 * _s1).display()}
    """

    gm.md(_md)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    This is one of the cleanest conceptual bridges in GA: the familiar 3D Pauli algebra is not separate from spacetime algebra. It is already sitting inside STA as the algebra of relative spatial directions.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
