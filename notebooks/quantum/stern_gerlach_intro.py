import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # One Stern-Gerlach Machine

    This notebook is a simpler companion to the larger three-machine Stern-Gerlach notebook.

    We start with a single input spin state, send it through one Stern-Gerlach machine, and read off:

    - the machine measurement axis
    - the two output spin states
    - the probabilities for the `N` and `S` outcomes

    If the input beam is an unpolarized ensemble average, we represent it by the effective Bloch vector

    $$
    \langle s_{\mathrm{in}} \rangle = 0.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D slice of the Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    The machine axis is a unit vector $a$. If the incoming spin state is the Bloch vector $s_{\mathrm{in}}$, then the Stern-Gerlach probabilities are

    $$
    P(N) = \frac{1 + s_{\mathrm{in}} \cdot a}{2},
    \qquad
    P(S) = \frac{1 - s_{\mathrm{in}} \cdot a}{2}.
    $$

    After the measurement, the outgoing pure spin states are simply aligned with the machine axis:

    $$
    s_N = a,
    \qquad
    s_S = -a.
    $$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    use_random_ensemble = mo.ui.checkbox(value=False, label="Use random ensemble input ⟨s_in⟩ = 0")
    input_angle = mo.ui.slider(0, 360, step=1, value=30, label="Input spin angle", show_value=True)
    machine_angle = mo.ui.slider(0, 180, step=1, value=90, label="Machine angle", show_value=True)
    return input_angle, machine_angle, use_random_ensemble


@app.cell
def _(
    draw_single_sg,
    e1,
    e2,
    gm,
    input_angle,
    machine_angle,
    mo,
    np,
    use_random_ensemble,
):
    _input_theta = np.radians(input_angle.value)
    _machine_theta = np.radians(machine_angle.value)

    axis = (np.cos(_machine_theta) * e1 + np.sin(_machine_theta) * e2).eval().name(latex=r"a")
    pure_input_state = (np.cos(_input_theta) * e1 + np.sin(_input_theta) * e2).eval().name(latex=r"s_{\mathrm{in}}")
    input_state = (
        pure_input_state
        if not use_random_ensemble.value
        else (0 * e1).eval().name(latex=r"\langle s_{\mathrm{in}} \rangle")
    )

    north_state = axis.copy_as(latex=r"s_N")
    south_state = (-axis).eval().name(latex=r"s_S")

    north_prob = (0.5 * (1 + (input_state | axis))).eval().name(latex=r"P(N)")
    south_prob = (0.5 * (1 - (input_state | axis))).eval().name(latex=r"P(S)")

    _state_kind = "unpolarized ensemble average" if use_random_ensemble.value else "pure input spin state"
    _md = t"""
    Input type: {_state_kind}. <br/>
    {input_state.display()} <br/>
    {axis.display()} <br/>
    {north_state.display()} <br/>
    {south_state.display()} <br/>
    {north_prob.display()} = {north_prob.scalar_part:.3f} <br/>
    {south_prob.display()} = {south_prob.scalar_part:.3f}
    """

    mo.vstack(
        [
            use_random_ensemble,
            input_angle,
            machine_angle,
            gm.md(_md),
            draw_single_sg(input_state, axis, north_state, south_state, north_prob, south_prob, use_random_ensemble.value),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    A Stern-Gerlach machine does two different things at once: it defines the two outgoing spin states by its own axis, and it assigns probabilities according to how well the input state aligns with it's axis.
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
    def draw_single_sg(input_state, machine_axis, north_state, south_state, north_prob, south_prob, use_random_ensemble):
        _input = np.array(input_state.eval().vector_part[:2], dtype=float)
        _axis = np.array(machine_axis.eval().vector_part[:2], dtype=float)
        _north_state = np.array(north_state.eval().vector_part[:2], dtype=float)
        _south_state = np.array(south_state.eval().vector_part[:2], dtype=float)
        _north_prob = north_prob.scalar_part if hasattr(north_prob, "scalar_part") else float(north_prob)
        _south_prob = south_prob.scalar_part if hasattr(south_prob, "scalar_part") else float(south_prob)

        _fig = plt.figure(figsize=(10.5, 9.0))
        _gs = _fig.add_gridspec(2, 2)
        _input_ax = _fig.add_subplot(_gs[0, 0])
        _machine_ax = _fig.add_subplot(_gs[0, 1])
        _output_ax = _fig.add_subplot(_gs[1, 0])
        _prob_ax = _fig.add_subplot(_gs[1, 1])

        def _setup_panel(_ax):
            _circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", alpha=0.25, linewidth=1.2)
            _ax.add_patch(_circle)
            _ax.axhline(0, color="gray", alpha=0.15, linewidth=0.8)
            _ax.axvline(0, color="gray", alpha=0.15, linewidth=0.8)
            _ax.set_xlim(-1.25, 1.25)
            _ax.set_ylim(-1.25, 1.25)
            _ax.set_aspect("equal")
            _ax.set_xticks([])
            _ax.set_yticks([])

        def _draw_magnets(_ax, _axis_xy):
            _axis_xy = _axis_xy / np.linalg.norm(_axis_xy)
            _perp = np.array([-_axis_xy[1], _axis_xy[0]])
            _north_center = 0.72 * _axis_xy
            _south_center = -0.72 * _axis_xy
            _height = 0.40
            _half_width = 0.22

            _north_top_center = _north_center + 0.32 * _height * _axis_xy
            _north_shoulder_center = _north_center - 0.06 * _height * _axis_xy
            _north_tip = _north_center - 0.5 * _height * _axis_xy
            _north_shape = np.vstack(
                [
                    _north_top_center + _half_width * _perp,
                    _north_top_center - _half_width * _perp,
                    _north_shoulder_center - _half_width * _perp,
                    _north_tip,
                    _north_shoulder_center + _half_width * _perp,
                ]
            )

            _south_top_center = _south_center - 0.5 * _height * _axis_xy
            _south_bottom_left = _south_center + 0.5 * _height * _axis_xy + _half_width * _perp
            _south_bottom_right = _south_center + 0.5 * _height * _axis_xy - _half_width * _perp
            _south_notch = _south_center + 0.12 * _height * _axis_xy
            _south_shape = np.vstack(
                [
                    _south_top_center + _half_width * _perp,
                    _south_top_center - _half_width * _perp,
                    _south_bottom_right,
                    _south_notch,
                    _south_bottom_left,
                ]
            )

            _ax.add_patch(plt.Polygon(_north_shape, closed=True, facecolor="#d62828", edgecolor="none", alpha=0.96))
            _ax.add_patch(plt.Polygon(_south_shape, closed=True, facecolor="#2563eb", edgecolor="none", alpha=0.96))
            _ax.text(*(_north_center + 0.40 * _axis_xy), "N", color="#d62828", ha="center", va="center", fontsize=12, fontweight="bold")
            _ax.text(*(_south_center - 0.40 * _axis_xy), "S", color="#2563eb", ha="center", va="center", fontsize=12, fontweight="bold")

        def _draw_arrow(_ax, _vec, _color, _label, _alpha=0.95):
            _ax.annotate(
                "",
                xy=_vec,
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=_color, lw=2.4, mutation_scale=18, alpha=_alpha),
            )
            _ax.text(1.10 * _vec[0], 1.10 * _vec[1], _label, color=_color, ha="center", va="center")

        _setup_panel(_input_ax)
        if use_random_ensemble:
            _input_ax.scatter([0], [0], color="#222222", s=42, zorder=5)
            _input_ax.text(0, -0.16, "ensemble avg", color="#222222", ha="center", va="center")
        else:
            _draw_arrow(_input_ax, _input, "#222222", r"$s_{in}$")
        _input_ax.set_title("Input Spin State", fontsize=11)

        _setup_panel(_machine_ax)
        _draw_magnets(_machine_ax, _axis)
        _machine_ax.set_title("Machine Orientation", fontsize=11)

        _setup_panel(_output_ax)
        _draw_arrow(_output_ax, _north_state, "#d62828", "N", 0.90)
        _draw_arrow(_output_ax, _south_state, "#2563eb", "S", 0.90)
        _output_ax.set_title("Output Spin States", fontsize=11)

        _x = np.arange(2)
        _bars = _prob_ax.bar(
            _x,
            [_north_prob, _south_prob],
            width=0.55,
            color=["#d62828", "#2563eb"],
            alpha=0.88,
        )
        _prob_ax.set_xticks(_x, ["N", "S"])
        _prob_ax.set_ylim(0, 1.1)
        _prob_ax.set_ylabel("probability")
        _prob_ax.set_title("Output Probabilities", fontsize=11)
        _prob_ax.grid(axis="y", alpha=0.18)
        _prob_ax.set_box_aspect(1)
        for _bar, _value in zip(_bars, [_north_prob, _south_prob]):
            _prob_ax.text(
                _bar.get_x() + _bar.get_width() / 2,
                _value + 0.03,
                f"{_value:.3f}",
                ha="center",
                va="bottom",
                color="#222222",
            )

        _fig.tight_layout()
        plt.close(_fig)
        return _fig

    return (draw_single_sg,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
