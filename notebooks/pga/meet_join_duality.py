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
    def draw_meet_join(points, line_1, line_2, meet_point):
        _fig, _ax = plt.subplots(figsize=(6.4, 6.4))
        _xs = np.linspace(-3.0, 3.0, 200)

        for (_a, _b, _c), _color in zip([line_1, line_2], ["steelblue", "crimson"]):
            if abs(_b) > 1e-12:
                _ys = (-_a * _xs - _c) / _b
                _ax.plot(_xs, _ys, color=_color, linewidth=2.5)
            else:
                _x = -_c / _a if abs(_a) > 1e-12 else 0.0
                _ax.plot([_x, _x], [-3.0, 3.0], color=_color, linewidth=2.5)

        _pts = np.array(points)
        _ax.scatter(_pts[:, 0], _pts[:, 1], color="black", zorder=3)
        for _label, (_x, _y) in zip(["A", "B", "C", "D"], points):
            _ax.text(_x + 0.08, _y + 0.08, _label)

        _mx, _my = meet_point
        if np.isfinite(_mx) and np.isfinite(_my):
            _ax.scatter([_mx], [_my], color="darkgreen", s=60, zorder=4)
            _ax.text(_mx + 0.08, _my + 0.08, "meet", color="darkgreen")

        _ax.set_aspect("equal")
        _ax.set_xlim(-3, 3)
        _ax.set_ylim(-3, 3)
        _ax.set_xlabel("x")
        _ax.set_ylabel("y")
        _ax.set_title("Join in one picture, meet in the dual picture")
        _ax.grid(True, alpha=0.25)
        plt.close(_fig)
        return _fig

    return (draw_meet_join,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Meet and Join as Dual Operations

    In projective geometric algebra, join and meet are the same structural idea seen from opposite sides. You join in one representation, then use complement to read the dual intersection story.

    This notebook is intentionally paired with [meets_joins_pga.py](./meets_joins_pga.py): that one is a concrete construction notebook, while this one is about the symmetry behind the construction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We build 2D projective geometric algebra with signature $(1,1,1,0)$.

    Points are easier to join after converting them into the complementary line-style representation. Likewise, lines can be understood as meeting at a point through the same incidence structure viewed dually.
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
    return E1, E2, E3, e0, e1, e2, e123, pga


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

    return coords, line_equation, point


@app.cell
def _(mo):
    ax = mo.ui.slider(-2.5, 2.5, step=0.1, value=-1.5, label="A_x", show_value=True)
    ay = mo.ui.slider(-2.5, 2.5, step=0.1, value=-0.5, label="A_y", show_value=True)
    bx = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.7, label="B_x", show_value=True)
    by = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.0, label="B_y", show_value=True)
    cx = mo.ui.slider(-2.5, 2.5, step=0.1, value=-1.2, label="C_x", show_value=True)
    cy = mo.ui.slider(-2.5, 2.5, step=0.1, value=1.7, label="C_y", show_value=True)
    dx = mo.ui.slider(-2.5, 2.5, step=0.1, value=2.1, label="D_x", show_value=True)
    dy = mo.ui.slider(-2.5, 2.5, step=0.1, value=-1.0, label="D_y", show_value=True)
    return ax, ay, bx, by, cx, cy, dx, dy


@app.cell
def _(ax, ay, bx, by, complement, coords, cx, cy, draw_meet_join, dx, dy, gm, line_equation, mo, np, point):
    _A = point(ax.value, ay.value).name("A")
    _B = point(bx.value, by.value).name("B")
    _C = point(cx.value, cy.value).name("C")
    _D = point(dx.value, dy.value).name("D")

    _line_ab = (complement(_A) ^ complement(_B)).name(latex=r"\ell_{AB}")
    _line_cd = (complement(_C) ^ complement(_D)).name(latex=r"\ell_{CD}")
    _dual_meet_pattern = (complement(_line_ab) ^ complement(_line_cd)).name(latex=r"\ell_{AB}^\complement \wedge \ell_{CD}^\complement")

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
    {_dual_meet_pattern.display()} <br/>
    Join builds the lines; the dual viewpoint packages their meet into the same outer-product pattern.
    """

    mo.vstack(
        [
            ax, ay, bx, by, cx, cy, dx, dy,
            gm.md(_md),
            draw_meet_join(
                [coords(_A)[:2], coords(_B)[:2], coords(_C)[:2], coords(_D)[:2]],
                (_a1, _b1, _c1),
                (_a2, _b2, _c2),
                _meet,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Join and meet are not unrelated formulas. They are the same incidence machinery viewed in complementary representations. PGA makes that symmetry explicit.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
