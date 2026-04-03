import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp, grade, project, reject, unit
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, grade, mo, np, plt, project, reject, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # One-Sided Rotor Action

    The full rotor action

    $$
    v' = R v \widetilde{R}
    $$

    is easy to treat as a black box. This notebook pulls it apart by looking at just the **left half**:

    $$
    R v.
    $$

    The point is that one-sided multiplication is not “half of a vector rotation” in any naive sense. It depends on where the vector sits relative to the rotor plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean algebra $\mathrm{Cl}(3,0)$.

    If the rotor plane is the unit bivector $\widehat B$, then we first split the vector into:

    $$
    v = v_{\parallel} + v_{\perp},
    \qquad
    v_{\parallel} = \operatorname{proj}_{\widehat B}(v),
    \qquad
    v_{\perp} = \operatorname{rej}_{\widehat B}(v).
    $$

    Then the one-sided action behaves differently on the two pieces:

    - $R v_{\parallel}$ stays in grade 1 and looks like an ordinary in-plane rotation
    - $R v_{\perp}$ mixes into grades 1 and 3

    That is one reason the sandwich product is needed: the final multiplication by $\widetilde R$ removes the unwanted grade mixing.

    Geometrically, the perpendicular piece must stay fixed under the full rotation. So the left and right one-sided actions cannot reinforce each other on $v_{\perp}$ the way they do on $v_{\parallel}$. Instead, their mixed grade effects have to oppose each other so that the sandwich product gives

    $$
    R v_{\perp} \widetilde R = v_{\perp}.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    I = e1 * e2 * e3
    return I, alg, e1, e2, e3


@app.cell
def _(mo):
    plane = mo.ui.dropdown(
        options=["e12 plane", "e23 plane", "e13 plane"],
        value="e12 plane",
        label="Rotor plane",
    )
    angle = mo.ui.slider(0, 360, step=1, value=60, label="Rotor angle θ", show_value=True)
    vx = mo.ui.slider(-1.5, 1.5, step=0.1, value=0.8, label="v_x", show_value=True)
    vy = mo.ui.slider(-1.5, 1.5, step=0.1, value=0.5, label="v_y", show_value=True)
    vz = mo.ui.slider(-1.5, 1.5, step=0.1, value=0.9, label="v_z", show_value=True)
    return angle, plane, vx, vy, vz


@app.cell
def _(
    I,
    alg,
    angle,
    draw_one_sided_action,
    e1,
    e2,
    e3,
    exp,
    gm,
    grade,
    mo,
    np,
    plane,
    project,
    reject,
    unit,
    vx,
    vy,
    vz,
):
    _plane_data = {
        "e12 plane": {
            "blade": (e1 ^ e2).name(latex=r"B"),
            "basis_1": e1,
            "basis_2": e2,
            "basis_labels": (r"e_1", r"e_2"),
            "perp_basis": e3,
        },
        "e23 plane": {
            "blade": (e2 ^ e3).name(latex=r"B"),
            "basis_1": e2,
            "basis_2": e3,
            "basis_labels": (r"e_2", r"e_3"),
            "perp_basis": e1,
        },
        "e13 plane": {
            "blade": (e1 ^ e3).name(latex=r"B"),
            "basis_1": e1,
            "basis_2": e3,
            "basis_labels": (r"e_1", r"e_3"),
            "perp_basis": e2,
        },
    }[plane.value]

    B_hat = unit(_plane_data["blade"]).name(latex=r"\hat{B}")
    theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
    R = exp((-theta / 2) * B_hat).name(latex=r"R")

    v = (vx.value * e1 + vy.value * e2 + vz.value * e3).name(latex=r"v")
    v_parallel = project(v, B_hat).name(latex=r"v_{\parallel}")
    v_perp = reject(v, B_hat).name(latex=r"v_{\perp}")

    Rv_parallel = (R * v_parallel).name(latex=r"R v_{\parallel}")
    Rv_perp = (R * v_perp).name(latex=r"R v_{\perp}")
    v_parallel_tilde_R = (v_parallel * ~R).name(latex=r"v_{\parallel} \widetilde{R}")
    v_perp_tilde_R = (v_perp * ~R).name(latex=r"v_{\perp} \widetilde{R}")

    Rv_parallel_g1 = grade(Rv_parallel, 1).name(latex=r"\langle R v_{\parallel} \rangle_1")
    Rv_parallel_g3 = grade(Rv_parallel, 3).name(latex=r"\langle R v_{\parallel} \rangle_3")
    v_parallel_tilde_R_g1 = grade(v_parallel_tilde_R, 1).name(latex=r"\langle v_{\parallel} \widetilde{R} \rangle_1")
    v_parallel_tilde_R_g3 = grade(v_parallel_tilde_R, 3).name(latex=r"\langle v_{\parallel} \widetilde{R} \rangle_3")
    Rv_perp_g1 = grade(Rv_perp, 1).name(latex=r"\langle R v_{\perp} \rangle_1")
    Rv_perp_g3 = grade(Rv_perp, 3).name(latex=r"\langle R v_{\perp} \rangle_3")
    v_perp_tilde_R_g1 = grade(v_perp_tilde_R, 1).name(latex=r"\langle v_{\perp} \widetilde{R} \rangle_1")
    v_perp_tilde_R_g3 = grade(v_perp_tilde_R, 3).name(latex=r"\langle v_{\perp} \widetilde{R} \rangle_3")

    _md = t"""
    {B_hat.display()} <br/>
    {R.display()} <br/>
    {v.display()} <br/>
    {v_parallel.display()} <br/>
    {v_perp.display()} <br/>
    {Rv_parallel.display()} <br/>
    {Rv_parallel_g1.display()} <br/>
    {Rv_parallel_g3.display()} <br/>
    {v_parallel_tilde_R.display()} <br/>
    {v_parallel_tilde_R_g1.display()} <br/>
    {v_parallel_tilde_R_g3.display()} <br/>
    {Rv_perp.display()} <br/>
    {Rv_perp_g1.display()} <br/>
    {Rv_perp_g3.display()} <br/>
    {v_perp_tilde_R.display()} <br/>
    {v_perp_tilde_R_g1.display()} <br/>
    {v_perp_tilde_R_g3.display()} <br/>
    One-sided action on the plane part stays in grade 1, while one-sided action on the perpendicular part mixes a vector piece and a trivector piece.
    """

    mo.vstack(
        [
            plane,
            angle,
            vx,
            vy,
            vz,
            gm.md(_md),
            draw_one_sided_action(
                v_parallel,
                Rv_parallel_g1,
                v_parallel_tilde_R_g1,
                Rv_perp_g1,
                Rv_perp_g3,
                v_perp_tilde_R_g1,
                v_perp_tilde_R_g3,
                _plane_data["basis_1"],
                _plane_data["basis_2"],
                _plane_data["basis_labels"],
                I,
                _plane_data["perp_basis"],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The sandwich product looks cleaner than one-sided multiplication because it is doing cleanup. Left multiplication by a rotor already rotates the in-plane piece correctly, but it also mixes the perpendicular piece across grades. Right multiplication by $\widetilde R$ cancels that unwanted perpendicular mixing while preserving the in-plane rotation.

    So the two sides play different roles:

    - **parallel parts**: the left and right actions cooperate, so the vector rotates in the rotor plane. $R$ rotates in half the way, and $\hat{R}$ rotates it the rest of the way
    - **perpendicular parts**: the left and right actions oppose each other, so the vector-trivector mixing cancels and the perpendicular component remains unchanged
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
    def draw_one_sided_action(v_parallel, Rv_parallel_g1, v_parallel_tilde_R_g1, Rv_perp_g1, Rv_perp_g3, v_perp_tilde_R_g1, v_perp_tilde_R_g3, basis_1, basis_2, basis_labels, I, perp_basis):
        def _plane_coords(_mv):
            _v = _mv.eval()
            _x = (_v | basis_1).scalar_part / ((basis_1 | basis_1).scalar_part)
            _y = (_v | basis_2).scalar_part / ((basis_2 | basis_2).scalar_part)
            return np.array([_x, _y], dtype=float)

        def _g1_coeff(_mv):
            _g1 = _mv.eval()
            return (_g1 | perp_basis).scalar_part / ((perp_basis | perp_basis).scalar_part)

        def _g3_coeff(_mv):
            _g3 = _mv.eval()
            if not np.any(np.abs(_g3.data) > 1e-12):
                return 0.0
            return ((_g3 | I).scalar_part) / ((I | I).scalar_part)

        _v_parallel_xy = _plane_coords(v_parallel)
        _Rv_parallel_xy = _plane_coords(Rv_parallel_g1)
        _v_parallel_tilde_R_xy = _plane_coords(v_parallel_tilde_R_g1)

        _left_g1 = _g1_coeff(Rv_perp_g1)
        _left_g3 = _g3_coeff(Rv_perp_g3)
        _right_g1 = _g1_coeff(v_perp_tilde_R_g1)
        _right_g3 = _g3_coeff(v_perp_tilde_R_g3)
        _left_sq_g1 = np.sign(_left_g1) * (_left_g1 ** 2)
        _left_sq_g3 = np.sign(_left_g3) * (_left_g3 ** 2)
        _right_sq_g1 = np.sign(_right_g1) * (_right_g1 ** 2)
        _right_sq_g3 = np.sign(_right_g3) * (_right_g3 ** 2)

        _fig = plt.figure(figsize=(11.6, 8.8))
        _gs = _fig.add_gridspec(2, 2)
        _ax_plane = _fig.add_subplot(_gs[0, 0])
        _ax_square = _fig.add_subplot(_gs[0, 1])
        _ax_left = _fig.add_subplot(_gs[1, 0])
        _ax_right = _fig.add_subplot(_gs[1, 1])

        _ax_plane.annotate(
            "",
            xy=_v_parallel_xy,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=2.3, mutation_scale=18),
        )
        _ax_plane.annotate(
            "",
            xy=_Rv_parallel_xy,
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.5, mutation_scale=18),
        )
        _ax_plane.text(1.08 * _v_parallel_xy[0], 1.08 * _v_parallel_xy[1], r"$v_{\parallel}$", color="black", ha="center", va="center")
        _ax_plane.text(1.08 * _Rv_parallel_xy[0], 1.08 * _Rv_parallel_xy[1], "$R v_{\\parallel}$\n$v_{\\parallel}\\hat{R}$", color="#d62828", ha="center", va="center")
        _ax_plane.axhline(0, color="gray", alpha=0.18, linewidth=0.8)
        _ax_plane.axvline(0, color="gray", alpha=0.18, linewidth=0.8)
        _ax_plane.set_xlim(-1.7, 1.7)
        _ax_plane.set_ylim(-1.7, 1.7)
        _ax_plane.set_aspect("equal")
        _ax_plane.grid(True, alpha=0.22)
        _ax_plane.set_xlabel(basis_labels[0])
        _ax_plane.set_ylabel(basis_labels[1])
        _ax_plane.set_title("Parallel Subspace: one-sided action stays vector-like")

        _coeff_bound = max(1.2, np.max(np.abs([_left_g1, _left_g3])) * 1.25)
        _ax_square.annotate(
            "",
            xy=(_left_g1, _left_g3),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2.5, mutation_scale=18, alpha=0.95),
        )
        _ax_square.annotate(
            "",
            xy=(_right_g1, _right_g3),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.5, mutation_scale=18, alpha=0.95),
        )
        _ax_square.scatter([_left_g1], [_left_g3], color="#7c3aed", s=34, zorder=3)
        _ax_square.scatter([_right_g1], [_right_g3], color="#2563eb", s=34, zorder=3)
        _ax_square.text(
            1.04 * _left_g1 if abs(_left_g1) > 1e-9 else 0.08,
            1.04 * _left_g3 if abs(_left_g3) > 1e-9 else 0.08,
            r"$R v_{\perp}$",
            color="#7c3aed",
            ha="left",
            va="bottom",
        )
        _ax_square.text(
            1.04 * _right_g1 if abs(_right_g1) > 1e-9 else 0.08,
            1.04 * _right_g3 if abs(_right_g3) > 1e-9 else -0.08,
            r"$v_{\perp}\widetilde{R}$",
            color="#2563eb",
            ha="left",
            va="top" if _right_g3 < 0 else "bottom",
        )
        _ax_square.axhline(0, color="gray", alpha=0.18, linewidth=0.8)
        _ax_square.axvline(0, color="gray", alpha=0.18, linewidth=0.8)
        _ax_square.set_xlim(-_coeff_bound, _coeff_bound)
        _ax_square.set_ylim(-_coeff_bound, _coeff_bound)
        _ax_square.set_aspect("equal")
        _ax_square.grid(True, alpha=0.22)
        _ax_square.set_xlabel(r"$\langle R v_{\perp} \rangle_1$")
        _ax_square.set_ylabel(r"$\langle R v_{\perp} \rangle_3$")
        _ax_square.set_title(r"Coefficient space for $R v_{\perp}$ and $v_{\perp}\widetilde{R}$")

        def _draw_parallel_compare(_ax, _left_xy, _right_xy):
            _labels = [basis_labels[0], basis_labels[1]]
            _x = np.arange(len(_labels))
            _w = 0.35
            _ax.bar(_x - _w / 2, _left_xy, width=_w, color="#d62828", alpha=0.88, label=r"$R v_{\parallel}$")
            _ax.bar(_x + _w / 2, _right_xy, width=_w, color="#111111", alpha=0.70, label=r"$v_{\parallel}\widetilde{R}$")
            _ax.set_xticks(_x, _labels)
            _bound = max(1.2, np.max(np.abs(np.concatenate([_left_xy, _right_xy]))) * 1.25)
            _ax.set_ylim(-_bound, _bound)
            _ax.axhline(0, color="gray", alpha=0.18, linewidth=0.8)
            _ax.grid(True, axis="y", alpha=0.22)
            _ax.set_ylabel("plane coefficient")
            _ax.set_title(r"Compare $R v_{\parallel}$ and $v_{\parallel}\widetilde{R}$")
            _ax.legend(loc="upper right")

            for _i, _value in enumerate(_left_xy):
                _offset = 0.04 * _bound if _value >= 0 else -0.04 * _bound
                _ax.text(_x[_i] - _w / 2, _value + _offset, f"{_value:.3f}", ha="center", va="bottom" if _value >= 0 else "top")
            for _i, _value in enumerate(_right_xy):
                _offset = 0.04 * _bound if _value >= 0 else -0.04 * _bound
                _ax.text(_x[_i] + _w / 2, _value + _offset, f"{_value:.3f}", ha="center", va="bottom" if _value >= 0 else "top")

        def _draw_compare_bars(_ax, _left_g1, _left_g3, _right_g1, _right_g3):
            _labels = [r"$\langle \cdot \rangle_1$", r"$\langle \cdot \rangle_3$"]
            _left_values = [_left_g1, _left_g3]
            _right_values = [_right_g1, _right_g3]
            _x = np.arange(len(_labels))
            _w = 0.35
            _ax.bar(_x - _w / 2, _left_values, width=_w, color="#7c3aed", alpha=0.88, label=r"$R v_{\perp}$")
            _ax.bar(_x + _w / 2, _right_values, width=_w, color="#2563eb", alpha=0.88, label=r"$v_{\perp}\widetilde{R}$")
            _ax.set_xticks(_x, _labels)
            _bound = max(1.2, np.max(np.abs(_left_values + _right_values)) * 1.25)
            _ax.set_ylim(-_bound, _bound)
            _ax.axhline(0, color="gray", alpha=0.18, linewidth=0.8)
            _ax.grid(True, axis="y", alpha=0.22)
            _ax.set_ylabel("signed coefficient")
            _ax.set_title(r"Compare $R v_{\perp}$ and $v_{\perp}\widetilde{R}$")
            _ax.legend(loc="upper right")

            for _i, _value in enumerate(_left_values):
                _offset = 0.04 * _bound if _value >= 0 else -0.04 * _bound
                _ax.text(_x[_i] - _w / 2, _value + _offset, f"{_value:.3f}", ha="center", va="bottom" if _value >= 0 else "top")
            for _i, _value in enumerate(_right_values):
                _offset = 0.04 * _bound if _value >= 0 else -0.04 * _bound
                _ax.text(_x[_i] + _w / 2, _value + _offset, f"{_value:.3f}", ha="center", va="bottom" if _value >= 0 else "top")

        _draw_parallel_compare(_ax_left, _Rv_parallel_xy, _v_parallel_tilde_R_xy)
        _draw_compare_bars(_ax_right, _left_g1, _left_g3, _right_g1, _right_g3)

        plt.tight_layout()
        plt.close(_fig)
        return _fig

    return (draw_one_sided_action,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
