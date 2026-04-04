import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, anticommutator, commutator, jordan_product, lie_bracket, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return (
        Algebra,
        anticommutator,
        commutator,
        gm,
        jordan_product,
        lie_bracket,
        mo,
        np,
        plt,
        unit,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Commutator, Lie Bracket, and Jordan Product

    The geometric product of two bivectors splits into two different stories:

    - the antisymmetric side, captured by the commutator / Lie bracket
    - the symmetric side, captured by the anticommutator / Jordan product

    This notebook lets you vary two bivector planes continuously so you can see what happens both for aligned basis bivectors and for intermediate, non-basis planes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean algebra $\mathrm{Cl}(3,0)$.

    In 3D, bivectors can be treated as oriented planes. Here each bivector is chosen from a 2-plane family in bivector space:

    $$
    B(\alpha) = \cos(\alpha) B_1 + \sin(\alpha) B_2.
    $$

    That means the sliders can move smoothly between familiar basis planes like $e_{12}$ and $e_{13}$, instead of forcing only orthogonal cases.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    e12 = e1 ^ e2
    e13 = e1 ^ e3
    e23 = e2 ^ e3
    return e12, e13, e23


@app.cell
def _(mo):
    family_A = mo.ui.dropdown(
        options=["e12 ↔ e13", "e12 ↔ e23", "e13 ↔ e23"],
        value="e12 ↔ e13",
        label="Family for A",
    )
    angle_A = mo.ui.slider(-90, 90, step=1, value=0, label="A family angle", show_value=True)
    family_B = mo.ui.dropdown(
        options=["e12 ↔ e13", "e12 ↔ e23", "e13 ↔ e23"],
        value="e12 ↔ e23",
        label="Family for B",
    )
    angle_B = mo.ui.slider(-90, 90, step=1, value=90, label="B family angle", show_value=True)
    scale_A = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Scale of A", show_value=True)
    scale_B = mo.ui.slider(-2.0, 2.0, step=0.1, value=1.0, label="Scale of B", show_value=True)
    return angle_A, angle_B, family_A, family_B, scale_A, scale_B


@app.cell
def _(
    angle_A,
    angle_B,
    anticommutator,
    commutator,
    draw_lie_jordan,
    e12,
    e13,
    e23,
    family_A,
    family_B,
    gm,
    jordan_product,
    lie_bracket,
    mo,
    np,
    scale_A,
    scale_B,
    unit,
):
    _families = {
        "e12 ↔ e13": (e12, e13),
        "e12 ↔ e23": (e12, e23),
        "e13 ↔ e23": (e13, e23),
    }

    def _family_bivector(_family_name, _angle_deg, _scale, _label):
        _B1, _B2 = _families[_family_name]
        _alpha = np.radians(_angle_deg)
        _blend = (np.cos(_alpha) * unit(_B1) + np.sin(_alpha) * unit(_B2)).name(latex=_label)
        return (_scale * _blend).name(latex=_label)

    A = _family_bivector(family_A.value, angle_A.value, scale_A.value, r"A")
    B = _family_bivector(family_B.value, angle_B.value, scale_B.value, r"B")

    comm = commutator(A, B).name(latex=r"[A,B]")
    anticomm = anticommutator(A, B).name(latex=r"\{A,B\}")
    lie = lie_bracket(A, B).name(latex=r"[A,B]_{\mathrm{Lie}}")
    jordan = jordan_product(A, B).name(latex=r"A \circ B")

    _md = t"""
    {A.display()} <br/>
    {B.display()} <br/>
    {comm.display()} <br/>
    {anticomm.display()} <br/>
    {lie.display()} <br/>
    {jordan.display()} <br/>
    The antisymmetric side returns a bivector, while the symmetric Jordan side returns the scalar overlap information.
    """

    mo.vstack(
        [
            family_A,
            angle_A,
            family_B,
            angle_B,
            scale_A,
            scale_B,
            gm.md(_md),
            draw_lie_jordan(A, B, lie, jordan, e12, e13, e23),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The Lie bracket and Jordan product are not competing definitions. They are the two complementary halves of the same geometric product:

    - Lie bracket: the order-sensitive bivector structure
    - Jordan product: the order-insensitive scalar overlap
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_lie_jordan(A, B, lie, jordan, e12, e13, e23):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        def _bivector_coeffs(_mv):
            _eval = _mv.eval()
            return np.array(
                [
                    (_eval | e12).scalar_part / ((e12 | e12).scalar_part),
                    (_eval | e13).scalar_part / ((e13 | e13).scalar_part),
                    (_eval | e23).scalar_part / ((e23 | e23).scalar_part),
                ],
                dtype=float,
            )

        def _dual_normal(_mv):
            _c12, _c13, _c23 = _bivector_coeffs(_mv)
            return np.array([_c23, -_c13, _c12], dtype=float)

        def _plane_patch(_normal):
            _normal = np.array(_normal, dtype=float)
            _norm = np.linalg.norm(_normal)
            if _norm < 1e-9:
                return None
            _normal = _normal / _norm

            if abs(_normal[0]) < 0.9:
                _trial = np.array([1.0, 0.0, 0.0])
            else:
                _trial = np.array([0.0, 1.0, 0.0])

            _u = np.cross(_normal, _trial)
            _u = _u / np.linalg.norm(_u)
            _v = np.cross(_normal, _u)

            _half = 0.85
            _corners = np.array(
                [
                    -_half * _u - _half * _v,
                    _half * _u - _half * _v,
                    _half * _u + _half * _v,
                    -_half * _u + _half * _v,
                ]
            )
            return _corners

        _A_n = _dual_normal(A)
        _B_n = _dual_normal(B)
        _lie_n = _dual_normal(lie)
        _jordan_value = jordan.eval().scalar_part

        _fig = plt.figure(figsize=(11.2, 5.2))
        _ax_left = _fig.add_subplot(121, projection="3d")
        _ax_right = _fig.add_subplot(122)

        for _vec, _color, _label, _alpha in [
            (_A_n, "#2563eb", "A", 0.18),
            (_B_n, "#d97706", "B", 0.18),
            (_lie_n, "#d62828", "Lie", 0.14),
        ]:
            _patch = _plane_patch(_vec)
            if _patch is not None:
                _ax_left.add_collection3d(
                    Poly3DCollection(
                        [_patch],
                        facecolors=_color,
                        edgecolors="none",
                        alpha=_alpha,
                    )
                )
            _ax_left.quiver(0, 0, 0, _vec[0], _vec[1], _vec[2], color=_color, linewidth=2.5, arrow_length_ratio=0.10)
            _ax_left.text(1.08 * _vec[0], 1.08 * _vec[1], 1.08 * _vec[2], _label, color=_color)

        _u = np.linspace(0, 2 * np.pi, 40)
        _v = np.linspace(0, np.pi, 24)
        _x = np.outer(np.cos(_u), np.sin(_v))
        _y = np.outer(np.sin(_u), np.sin(_v))
        _z = np.outer(np.ones_like(_u), np.cos(_v))
        _ax_left.plot_wireframe(_x, _y, _z, color="gray", alpha=0.08, linewidth=0.5)
        _ax_left.set_xlim(-1.4, 1.4)
        _ax_left.set_ylim(-1.4, 1.4)
        _ax_left.set_zlim(-1.4, 1.4)
        _ax_left.set_box_aspect((1, 1, 1))
        _ax_left.set_xlabel("e1")
        _ax_left.set_ylabel("e2")
        _ax_left.set_zlabel("e3")
        _ax_left.set_title("Plane normals for A, B, and the Lie bracket")

        _labels = ["e12", "e13", "e23", "scalar"]
        _A_vals = np.append(_bivector_coeffs(A), 0.0)
        _B_vals = np.append(_bivector_coeffs(B), 0.0)
        _lie_vals = np.append(_bivector_coeffs(lie), 0.0)
        _jordan_vals = np.array([0.0, 0.0, 0.0, _jordan_value], dtype=float)
        _x = np.arange(len(_labels))
        _w = 0.2
        _ax_right.bar(_x - 1.5 * _w, _A_vals, width=_w, color="#2563eb", alpha=0.82, label="A")
        _ax_right.bar(_x - 0.5 * _w, _B_vals, width=_w, color="#d97706", alpha=0.82, label="B")
        _ax_right.bar(_x + 0.5 * _w, _lie_vals, width=_w, color="#d62828", alpha=0.82, label="Lie")
        _ax_right.bar(_x + 1.5 * _w, _jordan_vals, width=_w, color="#7c3aed", alpha=0.82, label="Jordan")
        _ax_right.axhline(0, color="gray", alpha=0.18, linewidth=0.8)
        _ax_right.set_xticks(_x, _labels)
        _ax_right.set_ylim(-1.1, 1.1)
        _ax_right.grid(True, axis="y", alpha=0.22)
        _ax_right.set_ylabel("coefficient")
        _ax_right.set_title("Bivector coefficients and Jordan scalar")
        _ax_right.legend(loc="upper right")

        plt.tight_layout()
        plt.close(_fig)
        return _fig

    return (draw_lie_jordan,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
