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
    from sankeyflow import Sankey

    return Algebra, Sankey, gm, mo, np, plt


@app.cell
def _(Sankey, np, plt):
    def draw_sg_sequence(axis_1, axis_2, axis_3, spin_in, spin_1, spin_2, spin_3, north_probs, south_probs, total_pass):
        import colorsys
        import matplotlib.colors as mcolors

        def _hue_shift(_rgb, _shift):
            _h, _l, _s = colorsys.rgb_to_hls(*_rgb)
            _r, _g, _b = colorsys.hls_to_rgb((_h + _shift) % 1.0, _l, _s)
            return (_r, _g, _b)

        def _rgba(_color, _alpha):
            _r, _g, _b, _ = mcolors.to_rgba(_color)
            return (_r, _g, _b, _alpha)

        _axes = [axis_1.eval().vector_part[:2], axis_2.eval().vector_part[:2], axis_3.eval().vector_part[:2]]
        _states = [spin_in.eval().vector_part[:2], spin_1.eval().vector_part[:2], spin_2.eval().vector_part[:2], spin_3.eval().vector_part[:2]]
        _north = np.array([_p.scalar_part if hasattr(_p, "scalar_part") else _p for _p in north_probs], dtype=float)
        _south = np.array([_p.scalar_part if hasattr(_p, "scalar_part") else _p for _p in south_probs], dtype=float)
        _total_pass = total_pass.scalar_part if hasattr(total_pass, "scalar_part") else total_pass
        _north_cumulative = np.array(
            [
                _north[0],
                _north[0] * _north[1],
                _north[0] * _north[1] * _north[2],
            ],
            dtype=float,
        )
        _south_cumulative = np.array(
            [
                _south[0],
                _north[0] * _south[1],
                _north[0] * _north[1] * _south[2],
            ],
            dtype=float,
        )

        _fig = plt.figure(figsize=(18.0, 15.0))
        _gs = _fig.add_gridspec(3, 7, height_ratios=[1.0, 2.0, 2.2])
        _top_axes = [_fig.add_subplot(_gs[0, i]) for i in range(7)]
        _bar_ax = _fig.add_subplot(_gs[1, :])
        _sankey_ax = _fig.add_subplot(_gs[2, :])

        _titles = [
            "Input Spin State",
            "Machine 1 Orientation",
            "Spin State After Machine 1",
            "Machine 2 Orientation",
            "Spin State After Machine 2",
            "Machine 3 Orientation",
            "Final Spin States",
        ]

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

        def _draw_state(_ax, _state, _label):
            _setup_panel(_ax)
            if np.linalg.norm(_state) < 1e-8:
                _ax.scatter([0], [0], color="#222222", s=36, zorder=5)
                _ax.text(0.0, -0.14, _label, color="#222222", ha="center", va="center")
            else:
                _ax.annotate(
                    "",
                    xy=_state,
                    xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="#222222", lw=2.2, mutation_scale=18, alpha=0.95),
                )
                _ax.text(1.10 * _state[0], 1.10 * _state[1] - 0.08, _label, color="#222222", ha="center", va="center")

        def _draw_split_state(_ax, _axis, _south_alpha):
            _setup_panel(_ax)
            _north = np.array(_axis, dtype=float)
            _south = -_north
            _ax.annotate(
                "",
                xy=_north,
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#d62828", lw=2.4, mutation_scale=18, alpha=0.95),
            )
            _ax.annotate(
                "",
                xy=_south,
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.4, mutation_scale=18, alpha=_south_alpha),
            )
            _ax.text(1.08 * _north[0], 1.08 * _north[1] - 0.08, "N", color="#d62828", ha="center", va="center")
            _ax.text(1.08 * _south[0], 1.08 * _south[1] + 0.08, "S", color="#2563eb", ha="center", va="center")

        def _draw_machine(_ax, _axis):
            _setup_panel(_ax)
            _draw_magnets(_ax, _axis)

        def _draw_path_sankey(_ax):
            _highlight_alpha = 0.66
            _other_alpha = 0.20

            _NN = _north[0] * _north[1]
            _NS = _north[0] * _south[1]
            _SN = _south[0] * _south[1]
            _SS = _south[0] * _north[1]

            _NNN = _NN * _north[2]
            _NNS = _NN * _south[2]
            _NSN = _NS * _south[2]
            _NSS = _NS * _north[2]
            _SNN = _SN * _north[2]
            _SNS = _SN * _south[2]
            _SSN = _SS * _south[2]
            _SSS = _SS * _north[2]

            _red_base = (214 / 255, 40 / 255, 40 / 255)
            _blue_base = (37 / 255, 99 / 255, 235 / 255)
            _reds = [_hue_shift(_red_base, _shift) for _shift in (-0.01, 0.0, 0.01)]
            _blues = [_hue_shift(_blue_base, _shift) for _shift in (-0.01, 0.0, 0.01)]

            _nodes = [
                [("Input beam", 1.0, {"color": "#6b7280"})],
                [("M1 N", _north[0], {"color": _reds[0]}), ("M1 S", _south[0], {"color": _blues[0]})],
                [
                    ("NN", _NN, {"color": _reds[1]}),
                    ("NS", _NS, {"color": _blues[1]}),
                    ("SN", _SN, {"color": _reds[1]}),
                    ("SS", _SS, {"color": _blues[1]}),
                ],
                [
                    ("NNN", _NNN, {"color": _reds[2]}), ("NNS", _NNS, {"color": _blues[2]}),
                    ("NSN", _NSN, {"color": _reds[2]}), ("NSS", _NSS, {"color": _blues[2]}),
                    ("SNN", _SNN, {"color": _reds[2]}), ("SNS", _SNS, {"color": _blues[2]}),
                    ("SSN", _SSN, {"color": _reds[2]}), ("SSS", _SSS, {"color": _blues[2]}),
                ],
            ]
            _flows = [
                ("Input beam", "M1 N", _north[0], {"color": _rgba(_reds[0], _highlight_alpha)}),
                ("Input beam", "M1 S", _south[0], {"color": _rgba(_blues[0], _other_alpha)}),

                ("M1 N", "NN", _NN, {"color": _rgba(_reds[1], _highlight_alpha)}),
                ("M1 N", "NS", _NS, {"color": _rgba(_blues[1], _other_alpha)}),
                ("M1 S", "SN", _SN, {"color": _rgba(_reds[1], _other_alpha)}),
                ("M1 S", "SS", _SS, {"color": _rgba(_blues[1], _other_alpha)}),

                ("NN", "NNN", _NNN, {"color": _rgba(_reds[2], _highlight_alpha)}),
                ("NN", "NNS", _NNS, {"color": _rgba(_blues[2], _highlight_alpha)}),
                ("NS", "NSN", _NSN, {"color": _rgba(_reds[2], _other_alpha)}),
                ("NS", "NSS", _NSS, {"color": _rgba(_blues[2], _other_alpha)}),
                ("SN", "SNN", _SNN, {"color": _rgba(_reds[2], _other_alpha)}),
                ("SN", "SNS", _SNS, {"color": _rgba(_blues[2], _other_alpha)}),
                ("SS", "SSN", _SSN, {"color": _rgba(_reds[2], _other_alpha)}),
                ("SS", "SSS", _SSS, {"color": _rgba(_blues[2], _other_alpha)}),
            ]

            _sankey = Sankey(
                flows=_flows,
                nodes=_nodes,
                node_pad_y_min=0.03,
                node_pad_y_max=0.08,
                node_height_pad_min=0.02,
                node_opts={
                    "label_format": "{label}: {value:.3f}",
                    "label_opts": {"fontsize": 12},
                },
            )
            _sankey.draw(ax=_ax)
            _ax.set_title("All measurement paths through the three-machine sequence")

        _machine_panels = [1, 3, 5]

        _draw_state(_top_axes[0], _states[0], "0 Spin State")
        _draw_split_state(_top_axes[2], _axes[0], 0.15)
        _draw_split_state(_top_axes[4], _axes[1], 0.15)
        _draw_split_state(_top_axes[6], _axes[2], 0.95)

        for _panel, _axis in zip(_machine_panels, _axes):
            _draw_machine(_top_axes[_panel], _axis)

        for _i, _ax in enumerate(_top_axes):
            _ax.set_title(_titles[_i], fontsize=11)

        for _left_idx, _right_idx in zip(range(6), range(1, 7)):
            _top_axes[_left_idx].annotate(
                "",
                xy=(1.12, 0.5),
                xytext=(1.00, 0.5),
                xycoords="axes fraction",
                textcoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="gray", lw=1.2, alpha=0.55),
            )

        _x = np.arange(3)
        _w = 0.34
        _north_bars = _bar_ax.bar(_x - _w / 2, _north_cumulative, width=_w, color="#d62828", alpha=0.88, label="N-path fraction")
        _south_alphas = [0.15, 0.15, 0.88]
        _south_bars = []
        for _i, (_x_i, _y_i, _alpha_i) in enumerate(zip(_x + _w / 2, _south_cumulative, _south_alphas)):
            _container = _bar_ax.bar(_x_i, _y_i, width=_w, color="#2563eb", alpha=_alpha_i, label="S-path fraction" if _i == 0 else None)
            _south_bars.append(_container[0])
        _bar_ax.set_xticks(_x, ["machine 1", "machine 2 (N spin input)", "machine 3 (N spin input)"])
        _bar_ax.set_ylim(0.0, 1.05)
        _bar_ax.grid(True, axis="y", alpha=0.22)
        _bar_ax.set_ylabel("fraction of original beam")
        _bar_ax.set_title(f"Cumulative path fractions through the sequence; retained NNN fraction = {_total_pass:.3f}")
        _bar_ax.legend(loc="upper right")
        _south_labels = [
            f"S {_south_cumulative[0]:.3f} (discarded)",
            f"S {_south_cumulative[1]:.3f} (discarded)",
            f"S {_south_cumulative[2]:.3f}",
        ]
        for _bar, _value in zip(_north_bars, _north_cumulative):
            _bar_ax.text(
                _bar.get_x() + _bar.get_width() / 2,
                _value + 0.02,
                f"N {_value:.3f}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="#7f1d1d",
            )
        for _bar, _label, _value in zip(_south_bars, _south_labels, _south_cumulative):
            _bar_ax.text(
                _bar.get_x() + _bar.get_width() / 2,
                _value + 0.02,
                _label,
                ha="center",
                va="bottom",
                fontsize=10,
                color="#1d4ed8",
                rotation=0,
            )
        _draw_path_sankey(_sankey_ax)

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
    alpha = mo.ui.slider(0, 180, step=1, value=60, label="Machine 2 angle α from Machine 1 orientation", show_value=True)
    beta = mo.ui.slider(0, 180, step=1, value=90, label="Machine 3 angle β from Machine 1 orientation", show_value=True)
    return alpha, beta


@app.cell
def _(alg, alpha, beta, draw_sg_sequence, e1, e2, gm, mo, np):
    _alpha = np.radians(alpha.value)
    _beta = np.radians(beta.value)

    _angle_m1 = e2.copy_as(latex=r"\angle_{m1}")
    _angle_m2 = (np.sin(_alpha) * e1 + np.cos(_alpha) * e2).eval().name(latex=r"\angle_{m2}")
    _angle_m3 = (np.sin(_beta) * e1 + np.cos(_beta) * e2).eval().name(latex=r"\angle_{m3}")


    _s_in = alg.scalar(0).name(latex=r"s_{\mathrm{in}}")
    _s1 = _angle_m1.copy_as(latex=r"s_1")

    p1_up = (0.5 * (1 + (_s_in | _angle_m1))).name(latex=r"P_{s_{in}}(N)")
    p1_down = (1 - p1_up).name(latex=r"P_{s_{in}}(S)")

    p2_up = (0.5 * (1 + (_s1 | _angle_m2))).name(latex=r"P_{s_1}(N)")
    p2_down = (1 - p2_up).name(latex=r"P_{s_1}(S)")

    _s2 = _angle_m2.copy_as(latex=r"s_2")

    p3_up = (0.5 * (1 + (_s2 | _angle_m3))).name(latex=r"P_{s_2}(N)")
    p3_down = (1 - p3_up).name(latex=r"P_{s_2}(S)")

    _s3 = _angle_m3.copy_as(latex=r"s_3")
    _total_pass = p1_up * p2_up * p3_up

    _md = t"""
    Machine 1 input spin state:$\\quad$ {_s_in.display()} <br/>
    Machine 1 measurement angle / Machine 2 input spin state:$\\quad$ {_s1.display()} <br/>
    Machine 2 measurement angle / Machine 3 input spin state:$\\quad$ {_s2.display()} <br/>
    Machine 3 measurement angle / Final N spin state:$\\quad$ {_s3.display()} <br/>
    {p1_up.display()} $\\qquad and \\quad$ {p1_down.display()} <br/>
    {p2_up.display()} $\\qquad and \\quad$ {p2_down.display()} <br/>
    {p3_up.display()} $\\qquad and \\quad$ {p3_down.display()} <br/>
    Total surviving fraction along the N-only path:$\\quad$ {_total_pass.display()}
    """

    mo.vstack(
        [
            alpha,
            beta,
            gm.md(_md),
            draw_sg_sequence(_angle_m1, _angle_m2, _angle_m3, _s_in, _s1, _s2, _s3, [p1_up, p2_up, p3_up], [p1_down, p2_down, p3_down], _total_pass),
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
