import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, grade
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, gm, mo, np, plt


@app.cell
def _(np, plt):
    def draw_sg_sequence(axes, incoming_states, outgoing_states, north_probs, south_probs, total_pass):
        _axes = [np.array(_a, dtype=float) for _a in axes]
        _incoming = [np.array(_s, dtype=float) for _s in incoming_states]
        _outgoing = [np.array(_s, dtype=float) if _s is not None else None for _s in outgoing_states]
        _north = np.array(north_probs, dtype=float)
        _south = np.array(south_probs, dtype=float)

        _fig = plt.figure(figsize=(12.0, 8.0))
        _gs = _fig.add_gridspec(2, 3, height_ratios=[1.0, 0.95])
        _panel_axes = [_fig.add_subplot(_gs[0, i]) for i in range(3)]
        _bar_ax = _fig.add_subplot(_gs[1, :])

        _titles = ["Machine 1: prepare +e2", "Machine 2: rotate and split", "Machine 3: test final axis"]

        def _draw_magnets(_ax, _axis):
            _axis = np.array(_axis, dtype=float)
            _axis = _axis / np.linalg.norm(_axis)
            _perp = np.array([-_axis[1], _axis[0]])
            _north_center = 0.72 * _axis
            _south_center = -0.72 * _axis
            _height = 0.40
            _half_width = 0.22

            _north_top_center = _north_center + 0.32 * _height * _axis
            _north_shoulder_center = _north_center - 0.06 * _height * _axis
            _north_tip = _north_center - 0.5 * _height * _axis
            _north_shape = np.vstack(
                [
                    _north_top_center + _half_width * _perp,
                    _north_top_center - _half_width * _perp,
                    _north_shoulder_center - _half_width * _perp,
                    _north_tip,
                    _north_shoulder_center + _half_width * _perp,
                ]
            )

            _south_top_center = _south_center - 0.5 * _height * _axis
            _south_bottom_left = _south_center + 0.5 * _height * _axis + _half_width * _perp
            _south_bottom_right = _south_center + 0.5 * _height * _axis - _half_width * _perp
            _south_notch = _south_center + 0.12 * _height * _axis
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
            _ax.text(
                *(_north_center + 0.40 * _axis),
                "N",
                color="#d62828",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )
            _ax.text(
                *(_south_center - 0.40 * _axis),
                "S",
                color="#2563eb",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

        for _i, _ax in enumerate(_panel_axes):
            _n = _axes[_i]
            _s_in = _incoming[_i]
            _s_out = _outgoing[_i]

            _circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", alpha=0.25, linewidth=1.2)
            _ax.add_patch(_circle)
            _ax.axhline(0, color="gray", alpha=0.15, linewidth=0.8)
            _ax.axvline(0, color="gray", alpha=0.15, linewidth=0.8)
            _draw_magnets(_ax, _n)
            _ax.annotate(
                "",
                xy=_s_in,
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#222222", lw=2.0, mutation_scale=18, alpha=0.9),
            )
            if np.linalg.norm(_s_in) < 1e-8:
                _ax.scatter([0], [0], color="#222222", s=36, zorder=5)

            if np.linalg.norm(_s_in) < 1e-8:
                _ax.text(0.0, -0.14, "ensemble avg", color="#222222", ha="center", va="center")
            else:
                _ax.text(1.12 * _s_in[0], 1.12 * _s_in[1] - 0.08, "in", color="#222222", ha="center", va="center")

            _ax.set_xlim(-1.25, 1.25)
            _ax.set_ylim(-1.25, 1.25)
            _ax.set_aspect("equal")
            _ax.set_xticks([])
            _ax.set_yticks([])
            _ax.set_title(_titles[_i])

        _x = np.arange(3)
        _w = 0.34
        _bar_ax.bar(_x - _w / 2, _north, width=_w, color="#d62828", alpha=0.88, label="N output")
        _bar_ax.bar(_x + _w / 2, _south, width=_w, color="#2563eb", alpha=0.88, label="S output")
        _bar_ax.set_xticks(_x, ["machine 1", "machine 2", "machine 3"])
        _bar_ax.set_ylim(0.0, 1.05)
        _bar_ax.grid(True, axis="y", alpha=0.22)
        _bar_ax.set_ylabel("conditional probability")
        _bar_ax.set_title(f"N/S output probabilities at each machine; total surviving fraction = {total_pass:.3f}")
        _bar_ax.legend(loc="upper right")

        plt.close(_fig)
        return _fig

    return (draw_sg_sequence,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sequential Stern-Gerlach Measurement

    A Stern-Gerlach device measures spin along an axis and splits the beam into "up" and "down" outputs. The classic surprise is that if you insert a middle device at a different angle, the third device can recover outcomes that a direct two-device setup would have blocked.

    This notebook starts with an **unpolarized ensemble**, so the incoming ensemble-average Bloch vector is $\langle s_{\mathrm{in}} \rangle = 0$. The first device is fixed along $e_2$, then you choose the axes of the second and third devices. To keep the story focused, we always follow the **up** output from the first two devices.

    It builds on [qubit_superposition.py](./qubit_superposition.py): there the main idea was that a pure spin state is a Bloch-sphere direction, and here that same direction determines the measurement probabilities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the 3D Euclidean geometric algebra $\mathrm{Cl}(3,0)$, but restrict the measurement axes to the $e_1$-$e_2$ plane for clarity.

    For a spin state with Bloch vector $s$ and a measurement axis $n$, the probabilities are

    $$
    P(\uparrow_n) = \frac{1 + s \cdot n}{2},
    \qquad
    P(\downarrow_n) = \frac{1 - s \cdot n}{2}.
    $$

    For an unpolarized ensemble, $\langle s_{\mathrm{in}} \rangle = 0$, so every first measurement gives a 50/50 split. After selecting the "up" branch, the new spin state is simply aligned with that axis.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True) 
    return alg, e1, e2


@app.cell
def _(mo):
    alpha = mo.ui.slider(0, 180, step=1, value=60, label="Machine 2 angle α from e2", show_value=True)
    beta = mo.ui.slider(0, 180, step=1, value=90, label="Machine 3 angle β from e2", show_value=True)
    return alpha, beta


@app.cell
def _(alg, alpha, beta, draw_sg_sequence, e1, e2, gm, mo, np):
    _s_in = alg.scalar(0).name(latex=r"s_{\mathrm{in}}")
    _s1 = e2.copy_as(latex=r"s_1")

    _alpha = np.radians(alpha.value)
    _beta = np.radians(beta.value)

    _n1 = e2.copy_as(latex=r"\angle_1")
    _n2 = (np.sin(_alpha) * e1 + np.cos(_alpha) * e2).eval().name(latex=r"\angle_2")
    _n3 = (np.sin(_beta) * e1 + np.cos(_beta) * e2).eval().name(latex=r"\angle_3")

    _p1_up = (0.5 * (1 + (_s_in | _n1))).name(latex=r"P_1(N)")
    _p1_down = (1 - _p1_up).name(latex=r"P_1(S)")

    _p2_up = (0.5 * (1 + (_s1 | _n2))).name(latex=r"P_2(N)")
    _p2_down = (1 - _p2_up).name(latex=r"P_2(S)")
    _s2 = _n2.copy_as(latex=r"s_2")

    _p3_up = (0.5 * (1 + (_s2 | _n3))).name(latex=r"P_3(N \mid N_2)")
    _p3_down = (1 - _p3_up).name(latex=r"P_3(S \mid N_2)")
    _total_pass = _p1_up * _p2_up * _p3_up

    _md = t"""
    Machine 1 measurement angle:$\\quad$ {_n1.display()} <br/>
    Machine 2 measurement angle:$\\quad$ {_n2.display()} <br/>
    Machine 3 measurement angle:$\\quad$ {_n3.display()} <br/>
    Machine 1 input spin state:$\\quad$ {_s_in.display()} <br/>
    Machine 2 input spin state:$\\quad$ {_s1.display()} <br/>
    Machine 3 input spin state:$\\quad$ {_s2.display()} <br/>
    {_p1_up.display()} $\\qquad and \\quad$ {_p1_down.display()} <br/>
    {_p2_up.display()} $\\qquad and \\quad$ {_p2_down.display()} <br/>
    {_p3_up.display()} $\\qquad and \\quad$ {_p3_down.display()} <br/>
    Total surviving fraction along the chosen path:$\\quad$ {_total_pass.display()}
    """

    _axes = [_n1.vector_part[:2], _n2.vector_part[:2], _n3.vector_part[:2]]
    _incoming = [_s_in.vector_part[:2], _s1.vector_part[:2], _s2.vector_part[:2]]
    _outgoing = [_s1.vector_part[:2], _s2.vector_part[:2], None]
    _up = [_p1_up.scalar_part, _p2_up.scalar_part, _p3_up.scalar_part]
    _down = [_p1_down.scalar_part, _p2_down.scalar_part, _p3_down.scalar_part]

    mo.vstack(
        [
            alpha,
            beta,
            gm.md(_md),
            draw_sg_sequence(_axes, _incoming, _outgoing, _up, _down, _total_pass),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The middle device does not preserve the old "up along $e_2$" state. It prepares a new state aligned with its own axis. Once that happens, the third machine is measuring a different input state, so the final probabilities change.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
