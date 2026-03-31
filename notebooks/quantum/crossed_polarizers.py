import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_crossed_polarizers(theta_deg, show_middle, mid_axis_xy, fields_xy, intensities, labels):
        _mid_axis = np.array(mid_axis_xy, dtype=float)
        _fields = [np.array(_f, dtype=float) for _f in fields_xy]
        _intensities = np.array(intensities, dtype=float)

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11.4, 4.8))

        def _draw_axis(_ax, _direction, _color, _label, _ls="-", _alpha=1.0):
            _d = np.array(_direction, dtype=float)
            _ax.plot(
                [-1.25 * _d[0], 1.25 * _d[0]],
                [-1.25 * _d[1], 1.25 * _d[1]],
                color=_color,
                linestyle=_ls,
                linewidth=2.4,
                alpha=_alpha,
            )
            _ax.text(1.34 * _d[0], 1.34 * _d[1], _label, color=_color, fontsize=12, ha="center", va="center")

        _draw_axis(_ax1, (1.0, 0.0), "#d62828", "start")
        _draw_axis(_ax1, (0.0, 1.0), "#2563eb", "end")
        if show_middle:
            _draw_axis(_ax1, _mid_axis, "#7c3aed", "middle")
        else:
            _draw_axis(_ax1, _mid_axis, "#7c3aed", "middle", _ls="--", _alpha=0.25)

        _field_colors = ["#d62828", "#f97316", "#7c3aed", "#2563eb"]
        for _i, (_field, _label) in enumerate(zip(_fields, labels)):
            if np.linalg.norm(_field) < 1e-8:
                continue
            _ax1.annotate(
                "",
                xy=_field,
                xytext=(0, 0),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=_field_colors[min(_i, len(_field_colors) - 1)],
                    lw=2.8,
                    mutation_scale=20,
                    alpha=0.95,
                ),
            )
            _offset = 0.08 * (_i + 1)
            _ax1.text(
                _field[0] + _offset,
                _field[1] + 0.03,
                _label,
                color=_field_colors[min(_i, len(_field_colors) - 1)],
                fontsize=12,
            )

        _ax1.set_xlim(-1.45, 1.45)
        _ax1.set_ylim(-1.45, 1.45)
        _ax1.set_aspect("equal")
        _ax1.grid(True, alpha=0.22)
        _ax1.set_xlabel("e1")
        _ax1.set_ylabel("e2")
        _ax1.set_title("Polarizer axes and transmitted field")

        _x = np.arange(len(_intensities))
        _bar_colors = ["#222222", "#d62828", "#7c3aed", "#2563eb"][: len(_intensities)]
        _ax2.bar(_x, _intensities, color=_bar_colors, alpha=0.85)
        _ax2.set_xticks(_x, labels)
        _ax2.set_ylim(0.0, 1.05)
        _ax2.grid(True, axis="y", alpha=0.22)
        _ax2.set_ylabel("relative intensity")
        _ax2.set_title("Intensity through the stack")

        plt.close(_fig)
        return _fig

    return (draw_crossed_polarizers,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Crossed Polarizers and an Intermediate Basis

    Two ideal linear polarizers at $90^\circ$ block all transmission. But if you insert a third one in between, some light gets through.

    The geometric-algebra story is simple: each polarizer projects the field onto its transmission axis. The intermediate polarizer changes the basis in which the field is being resolved.

    This is a clean superposition example. Horizontal polarization is not an eigenstate of a rotated middle polarizer, so it has a component along that new axis, and that component can then have a nonzero overlap with the final vertical polarizer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 2D Euclidean geometric algebra $\mathrm{Cl}(2,0)$.

    A linear polarizer with unit axis $n$ acts by projection:

    $$
    E_{\mathrm{out}} = (E \cdot n)\,n.
    $$

    If intensity is proportional to squared field magnitude, then this recovers Malus's law. For crossed start and end polarizers:

    - without the middle polarizer, the final transmission is zero
    - with a middle axis at angle $\theta$, the final intensity becomes
      $I_{\mathrm{end}} = \cos^2\theta\,\sin^2\theta = \tfrac{1}{4}\sin^2(2\theta)$
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1))
    e1, e2 = alg.basis_vectors(lazy=True)
    return e1, e2


@app.cell
def _(mo):
    use_middle = mo.ui.checkbox(value=True, label="Enable intermediate polarizer")
    theta = mo.ui.slider(0, 90, step=1, value=45, label="Intermediate angle θ", show_value=True)
    return theta, use_middle


@app.cell
def _(draw_crossed_polarizers, e1, e2, gm, mo, np, theta, use_middle):
    _Ein = e1.name(latex=r"E_{\mathrm{in}}")
    _start_axis = e1.name(latex=r"n_{\mathrm{start}}")
    _end_axis = e2.name(latex=r"n_{\mathrm{end}}")

    _theta = np.radians(theta.value)
    _middle_axis = (np.cos(_theta) * e1 + np.sin(_theta) * e2).name(latex=r"n_{\mathrm{mid}}")

    _after_start = ((_Ein | _start_axis) * _start_axis).name(latex=r"E_1")
    if use_middle.value:
        _after_middle = (((_after_start | _middle_axis) * _middle_axis)).name(latex=r"E_2")
        _after_end = (((_after_middle | _end_axis) * _end_axis)).name(latex=r"E_3")
        _field_chain = [_Ein, _after_start, _after_middle, _after_end]
        _labels = ["in", "after start", "after middle", "after end"]
    else:
        _after_middle = (0 * e1).name(latex=r"E_2")
        _after_end = (((_after_start | _end_axis) * _end_axis)).name(latex=r"E_3")
        _field_chain = [_Ein, _after_start, _after_end]
        _labels = ["in", "after start", "after end"]

    def _intensity(_field):
        return (_field | _field).scalar_part

    _intensities = [_intensity(_field) for _field in _field_chain]
    _transmission = _intensities[-1]

    if use_middle.value:
        _formula = rf"$I_{{\mathrm{{end}}}} = \cos^2({theta.value}^\circ)\sin^2({theta.value}^\circ) = {_transmission:.3f}$"
    else:
        _formula = r"$I_{\mathrm{end}} = 0$ because the start and end polarizers are crossed."

    _md = t"""
    {_Ein.display()} <br/>
    {_start_axis.display()} <br/>
    {_middle_axis.display()} <br/>
    {_end_axis.display()} <br/>
    {_after_start.display()} <br/>
    {_after_middle.display()} <br/>
    {_after_end.display()} <br/>
    Relative intensities: $1.000 \\rightarrow {" \\rightarrow ".join(f"{_i:.3f}" for _i in _intensities[1:])}$ <br/>
    {_formula}
    """

    _field_xy = [_field.vector_part[:2] if hasattr(_field, "vector_part") else np.zeros(2) for _field in _field_chain]
    _middle_xy = _middle_axis.vector_part[:2]

    mo.vstack(
        [
            use_middle,
            theta,
            gm.md(_md),
            draw_crossed_polarizers(theta.value, use_middle.value, _middle_xy, _field_xy, _intensities, _labels),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The intermediate polarizer does not "create extra light." It changes the basis of the transmitted field, so the component passed by the middle axis acquires a nonzero projection onto the final vertical axis.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
