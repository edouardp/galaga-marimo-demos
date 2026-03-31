import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, complement
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, complement, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_incidence(points, lines, meet_point):
        _fig, _ax = plt.subplots(figsize=(6.5, 6.5))

        _xs = np.linspace(-3.0, 3.0, 200)
        _colors = ["steelblue", "crimson"]
        for (_a, _b, _c), _color in zip(lines, _colors):
            if abs(_b) > 1e-12:
                _ys = (-_a * _xs - _c) / _b
                _ax.plot(_xs, _ys, color=_color, linewidth=2.5)
            else:
                _x = -_c / _a if abs(_a) > 1e-12 else 0.0
                _ax.plot([_x, _x], [-3, 3], color=_color, linewidth=2.5)

        _pts = np.array(points)
        _ax.scatter(_pts[:, 0], _pts[:, 1], color="black", zorder=3)
        for _label, (_x, _y) in zip(["A", "B", "C", "D"], points):
            _ax.text(_x + 0.08, _y + 0.08, _label)

        _mx, _my = meet_point
        _ax.scatter([_mx], [_my], color="darkgreen", s=60, zorder=4)
        _ax.text(_mx + 0.08, _my + 0.08, "meet", color="darkgreen")

        _ax.set_aspect("equal")
        _ax.set_xlim(-3, 3)
        _ax.set_ylim(-3, 3)
        _ax.set_xlabel("x")
        _ax.set_ylabel("y")
        _ax.set_title("Joins of points and the meet of lines")
        _ax.grid(True, alpha=0.25)
        plt.close(_fig)
        return _fig

    return (draw_incidence,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Meets and Joins in PGA

    In projective geometric algebra, the outer product builds joins: two points determine a line. The dual viewpoint then lets us talk about meets: two lines determine a point. This notebook keeps the geometry concrete by working in the projective plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build 2D projective geometric algebra with signature $(1,1,1,0)$.

    This algebra is degenerate, which is one reason complement operations are useful here. Points can be represented as trivectors, while line joins are built by taking complements into the dual representation and then using the outer product.
    """)
    return


@app.cell
def _(Algebra):
    pga = Algebra((1, 1, 1, 0))
    e1, e2, e3, e0 = pga.basis_vectors(lazy=True)
    e123 = e1 ^ e2 ^ e3
    E1 = e2 ^ e3 ^ e0
    E2 = -(e1 ^ e3 ^ e0)
    E3 = e1 ^ e2 ^ e0
    return E1, E2, E3, e1, e2, e0, e123


@app.cell
def _(E1, E2, E3, e0, e1, e2, e123, np):
    def point(x, y, z=0.0):
        return (e123 + x * E1 + y * E2 + z * E3).name(latex=rf"P({x:.1f},{y:.1f},{z:.1f})")

    def coords(P):
        _P = P.eval()
        _w = _P.data[7]
        return np.array([_P.data[14] / _w, -_P.data[13] / _w, _P.data[11] / _w])

    def blade_coefficient(mv, blade):
        _mv = mv.eval()
        _blade = blade.eval()
        _nz = np.flatnonzero(np.abs(_blade.data) > 1e-12)
        _idx = int(_nz[0])
        return _mv.data[_idx] / _blade.data[_idx]

    def line_equation(line):
        _c = blade_coefficient(line, e1 ^ e2)
        _a = blade_coefficient(line, e2 ^ e0)
        _b = -blade_coefficient(line, e1 ^ e0)
        return _a, _b, -_c

    return blade_coefficient, coords, line_equation, point


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Join Two Point Pairs, Then Find Their Meet

    In this notebook, the joins are the GA-native step:

    $$
    \ell_{AB} = A^\complement \wedge B^\complement,
    \qquad
    \ell_{CD} = C^\complement \wedge D^\complement.
    $$

    To keep the geometry readable in a 2D plot, we then extract the affine line equations and solve for the intersection point of those two joined lines.
    """)
    return


@app.cell
def _(mo):
    ax = mo.ui.slider(-2.5, 2.5, step=0.1, value=-1.2, label="A_x", show_value=True)
    ay = mo.ui.slider(-2.5, 2.5, step=0.1, value=-0.4, label="A_y", show_value=True)
    bx = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.8, label="B_x", show_value=True)
    by = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.2, label="B_y", show_value=True)
    cx = mo.ui.slider(-2.5, 2.5, step=0.1, value=-1.0, label="C_x", show_value=True)
    cy = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.8, label="C_y", show_value=True)
    dx = mo.ui.slider(-2.5, 2.5, step=0.1, value=2.0, label="D_x", show_value=True)
    dy = mo.ui.slider(-2.5, 2.5, step=0.1, value=-0.8, label="D_y", show_value=True)
    return ax, ay, bx, by, cx, cy, dx, dy


@app.cell
def _(ax, ay, bx, by, complement, coords, cx, cy, draw_incidence, dx, dy, gm, line_equation, mo, np, point):
    _A = point(ax.value, ay.value).name("A")
    _B = point(bx.value, by.value).name("B")
    _C = point(cx.value, cy.value).name("C")
    _D = point(dx.value, dy.value).name("D")

    _line_ab = (complement(_A) ^ complement(_B)).name(latex=r"\ell_{AB}")
    _line_cd = (complement(_C) ^ complement(_D)).name(latex=r"\ell_{CD}")

    _a1, _b1, _c1 = line_equation(_line_ab)
    _a2, _b2, _c2 = line_equation(_line_cd)
    _M = np.array([[_a1, _b1], [_a2, _b2]])
    _rhs = -np.array([_c1, _c2])
    _meet = np.linalg.solve(_M, _rhs) if abs(np.linalg.det(_M)) > 1e-9 else np.array([np.nan, np.nan])

    _md = t"""
    {_A.display()} <br/>
    {_B.display()} <br/>
    {_C.display()} <br/>
    {_D.display()} <br/>
    {_line_ab.display()} <br/>
    {_line_cd.display()} <br/>
    $\\ell_{{AB}}: {_a1:.3f}x + {_b1:.3f}y + {_c1:.3f} = 0$ <br/>
    $\\ell_{{CD}}: {_a2:.3f}x + {_b2:.3f}y + {_c2:.3f} = 0$ <br/>
    Meet point: $({_meet[0]:.3f}, {_meet[1]:.3f})$
    """

    mo.vstack([
        ax, ay, bx, by, cx, cy, dx, dy,
        gm.md(_md),
        draw_incidence(
            [coords(_A)[:2], coords(_B)[:2], coords(_C)[:2], coords(_D)[:2]],
            [(_a1, _b1, _c1), (_a2, _b2, _c2)],
            _meet,
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why PGA Helps

    The important simplification is that the join construction is uniform: points become lines through the same exterior-product machinery. The plotted meet is then the familiar affine intersection point of those joined lines. PGA keeps the incidence structure primary instead of treating line formulas as the starting point.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
