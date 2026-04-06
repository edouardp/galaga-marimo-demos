import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_pga
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return Algebra, b_pga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Thin Lens Image Construction in PGA

    A thin lens turns one object point into one image point. The usual paraxial
    picture with principal rays is already projective in spirit: points, lines,
    and incidence are the real geometric objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use 3D projective geometric algebra with signature $(1,1,1,0)$.

    The picture stays in one optical plane, but the PGA point representation lets
    us name the object tip, lens center, focal points, and image tip as geometric
    objects rather than only as coordinate pairs.
    """)
    return


@app.cell
def _(Algebra, b_pga):
    pga = Algebra((1, 1, 1, 0), blades=b_pga())
    e0, e1, e2, e3 = pga.basis_vectors(lazy=True)

    e012 = e0 ^ e1 ^ e2
    E1 = (e1 ^ e2 ^ e3).name(latex="E_1")
    E2 = (-(e0 ^ e2 ^ e3)).name(latex="E_2")
    E3 = (e0 ^ e1 ^ e3).name(latex="E_3")

    return E1, E2, E3, e012, pga


@app.cell
def _(E1, E2, E3, e012, np):
    def point(x, y, z=0.0):
        return (e012 + x * E1 + y * E2 + z * E3).name(latex=rf"P({x:.2f},{y:.2f},{z:.2f})")

    def coords(P):
        _P = P.eval()
        _nz = np.flatnonzero(np.abs(_P.data) > 1e-12)
        _w_idx = int(_nz[0])
        _w = _P.data[_w_idx]
        return np.array([
            _P.data[11] / _w,
            _P.data[13] / _w,
            _P.data[14] / _w,
        ])

    return coords, point


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Object Point, One Lens, One Image Point

    The thin-lens equation is

    $$
    \frac{1}{f} = \frac{1}{s} + \frac{1}{s'}.
    $$

    We keep the object on the left of the lens, place the lens at the origin,
    and build the object tip and image tip as PGA points in the optical plane.
    """)
    return


@app.cell
def _(mo):
    object_distance = mo.ui.slider(1.0, 12.0, step=0.1, value=6.0, label="Object distance s", show_value=True)
    focal_length = mo.ui.slider(0.5, 8.0, step=0.1, value=2.0, label="Focal length f", show_value=True)
    object_height = mo.ui.slider(0.2, 3.0, step=0.1, value=1.2, label="Object height h", show_value=True)
    return focal_length, object_distance, object_height


@app.cell
def _(coords, draw_thin_lens, focal_length, gm, mo, np, object_distance, object_height, pga, point):
    s = pga.scalar(object_distance.value).name(latex="s")
    f = pga.scalar(focal_length.value).name(latex="f")
    h = pga.scalar(object_height.value).name(latex="h")

    _s_val = s.scalar_part
    _f_val = f.scalar_part
    _h_val = h.scalar_part

    if abs(_s_val - _f_val) < 1e-9:
        s_prime = None
        magnification = None
    else:
        s_prime = (1.0 / (1.0 / _f_val - 1.0 / _s_val))
        magnification = -s_prime / _s_val

    object_tip = point(-_s_val, _h_val, 0.0).name(latex="O")
    lens_center = point(0.0, 0.0, 0.0).name(latex="L")
    focus_left = point(-_f_val, 0.0, 0.0).name(latex="F")
    focus_right = point(_f_val, 0.0, 0.0).name(latex="F'")

    if s_prime is None:
        image_tip = point(15.0, 0.0, 0.0).name(latex="I")
        _image_tip_md = r"$I$ moves off to infinity when $s=f$."
        _s_prime_md = r"$s' = \infty$"
        _magnification_md = r"$m = \infty$"
    else:
        image_tip = point(s_prime, magnification * _h_val, 0.0).name(latex="I")
        _image_tip_md = image_tip.display()
        _s_prime_md = f"$s' = {s_prime:.3f}$"
        _magnification_md = f"$m = -s'/s = {magnification:.3f}$"

    _md = t"""
    {s.display()} <br/>
    {f.display()} <br/>
    {h.display()} <br/>
    {object_tip.display()} <br/>
    {lens_center.display()} <br/>
    {focus_left.display()} <br/>
    {focus_right.display()} <br/>
    {_image_tip_md} <br/>
    $\\frac{{1}}{{f}} = \\frac{{1}}{{s}} + \\frac{{1}}{{s'}}$ <br/>
    {_s_prime_md} <br/>
    {_magnification_md}
    """

    mo.vstack(
        [
            object_distance,
            focal_length,
            object_height,
            gm.md(_md),
            draw_thin_lens(
                coords(object_tip)[:2],
                coords(lens_center)[:2],
                coords(focus_left)[:2],
                coords(focus_right)[:2],
                coords(image_tip)[:2] if s_prime is not None else None,
                _s_val,
                _f_val,
                _h_val,
                s_prime,
                magnification,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The thin-lens formula gives the image distance, but the geometry is what makes
    it readable. One ray goes straight through the lens center, another arrives
    parallel to the axis and leaves through the focal point. Their intersection
    determines the image point.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_thin_lens(object_tip, lens_center, focus_left, focus_right, image_tip, s, f, h, s_prime, magnification):
        _fig, _ax = plt.subplots(figsize=(9.4, 4.8))

        _ax.axhline(0, color="#333333", lw=1.0, alpha=0.8)
        _ax.axvline(lens_center[0], color="#111111", lw=2.2, alpha=0.5)

        _ax.plot([object_tip[0], object_tip[0]], [0, object_tip[1]], color="#2563eb", linewidth=3.0, label="object")
        _ax.scatter([focus_left[0], focus_right[0]], [focus_left[1], focus_right[1]], color="#111111", s=28, zorder=4)
        _ax.text(focus_left[0], -0.18, "F", ha="center", va="top")
        _ax.text(focus_right[0], -0.18, "F'", ha="center", va="top")
        _ax.text(lens_center[0] + 0.08, 2.35, "lens", color="#111111")

        if image_tip is not None:
            _ax.plot([image_tip[0], image_tip[0]], [0, image_tip[1]], color="#d62828", linewidth=3.0, label="image")
            _ax.scatter([image_tip[0]], [image_tip[1]], color="#d62828", s=42, zorder=5)

            _ax.plot([object_tip[0], lens_center[0]], [object_tip[1], object_tip[1]], color="#f59e0b", linewidth=2.0)
            _ax.plot([lens_center[0], image_tip[0]], [object_tip[1], 0], color="#f59e0b", linewidth=2.0, label="parallel ray")

            _ax.plot([object_tip[0], lens_center[0]], [object_tip[1], 0], color="#10b981", linewidth=2.0)
            _ax.plot([lens_center[0], image_tip[0]], [0, image_tip[1]], color="#10b981", linewidth=2.0, label="central ray")

            _ax.plot([object_tip[0], focus_left[0]], [object_tip[1], 0], color="#7c3aed", linewidth=1.8, alpha=0.9)
            _ax.plot([lens_center[0], image_tip[0]], [object_tip[1], image_tip[1]], color="#7c3aed", linewidth=1.8, alpha=0.9, label="focal ray")
        else:
            _far_x = max(12.0, 1.8 * s)
            _ax.plot([object_tip[0], lens_center[0]], [object_tip[1], object_tip[1]], color="#f59e0b", linewidth=2.0)
            _ax.plot([lens_center[0], _far_x], [object_tip[1], 0], color="#f59e0b", linewidth=2.0, label="parallel ray")

            _ax.plot([object_tip[0], lens_center[0]], [object_tip[1], 0], color="#10b981", linewidth=2.0)
            _ax.plot([lens_center[0], _far_x], [0, 0], color="#10b981", linewidth=2.0, label="central ray")

            _ax.text(5.2, 0.35, "image at infinity", color="#d62828")

        _x_extent = max(4.0, 1.45 * max(abs(object_tip[0]), abs(image_tip[0]) if image_tip is not None else s))
        _y_extent = max(2.6, abs(h) * 1.8, abs(image_tip[1]) * 1.5 if image_tip is not None else 2.0)
        _ax.set_xlim(-_x_extent, _x_extent)
        _ax.set_ylim(-_y_extent, _y_extent)
        _ax.set_xlabel("optical axis")
        _ax.set_ylabel("height")
        _ax.set_title("Thin-lens image construction")
        _ax.grid(True, alpha=0.18)
        _ax.legend(loc="upper right")
        plt.close(_fig)
        return _fig

    return (draw_thin_lens,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
