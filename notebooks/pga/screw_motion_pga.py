import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra, exp
    import galaga_marimo as gm
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    return Algebra, exp, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Screw Motion in PGA

    A screw motion combines a rotation around an axis with a translation along
    that same axis. In projective geometric algebra, that is the natural rigid
    motion language.

    This notebook keeps the geometry tight: one axis, one angle, one pitch.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We use 3D projective geometric algebra with signature $(1,1,1,0)$.

    The Euclidean directions live in $e_1,e_2,e_3$, while the null basis vector
    $e_0$ carries ideal structure and translations.
    """
    )
    return


@app.cell
def _(Algebra):
    pga = Algebra((1, 1, 1, 0))
    e1, e2, e3, e0 = pga.basis_vectors(lazy=True)
    return e0, e1, e2, e3, pga


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## One Motor-Like Element

    We build a rotation around the $e_3$ axis and pair it with a translation
    along that same axis.

    The purpose here is not a full PGA motor derivation. The point is to make the
    geometry of “rotation plus axis drift” visually and algebraically explicit.
    """
    )
    return


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 360, step=1, value=120, label="Rotation angle", show_value=True)
    pitch = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.0, label="Axis translation", show_value=True)
    radius = mo.ui.slider(0.5, 3.0, step=0.1, value=1.5, label="Radius", show_value=True)
    return angle, pitch, radius


@app.cell
def _(angle, draw_screw_motion, e0, e1, e2, e3, exp, gm, mo, np, pitch, radius):
    _theta = np.radians(angle.value)
    _rotation_generator = (e1 * e2).name(latex=r"B_{\mathrm{rot}}")
    _translation_generator = (e0 * e3).name(latex=r"T_{\mathrm{axis}}")
    _R = exp((-_theta / 2) * _rotation_generator).name("R")
    _T = (1 + 0.5 * pitch.value * _translation_generator).name("T")
    _M = (_T * _R).name("M")

    _md = t"""
    {_rotation_generator.display()} <br/>
    {_translation_generator.display()} <br/>
    {_R.display()} <br/>
    {_T.display()} <br/>
    {_M.display()} <br/>
    This motor-like element combines one planar rotation with one translation along the same axis.
    """

    mo.vstack([angle, pitch, radius, gm.md(_md), draw_screw_motion(angle.value, pitch.value, radius.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Point

    PGA treats rigid motion as one geometric object. A screw motion is not “first
    rotate, then separately translate” as a bookkeeping trick. It is one natural
    motion type in the rigid-motion algebra.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendum: Plotting Code""")
    return


@app.cell(hide_code=True)
def _(np, plt):
    def draw_screw_motion(angle_deg, pitch, radius):
        _t = np.linspace(0, np.radians(angle_deg), 300)
        _x = radius * np.cos(_t)
        _y = radius * np.sin(_t)
        _z = pitch * (_t / max(_t[-1], 1e-9))

        _fig = plt.figure(figsize=(7.4, 5.4))
        _ax = _fig.add_subplot(111, projection="3d")
        _ax.plot(_x, _y, _z, color="#2563eb", linewidth=2.6)
        _ax.plot([0, 0], [0, 0], [min(_z.min(), -1.5), max(_z.max(), 1.5)], color="#222222", alpha=0.5, linewidth=1.6)
        _ax.scatter([_x[-1]], [_y[-1]], [_z[-1]], color="#d62828", s=55)
        _ax.set_xlim(-3.2, 3.2)
        _ax.set_ylim(-3.2, 3.2)
        _ax.set_zlim(-3.2, 3.2)
        _ax.set_box_aspect((1, 1, 1))
        _ax.set_xlabel("e1")
        _ax.set_ylabel("e2")
        _ax.set_zlabel("e3")
        _ax.set_title("Screw-like trajectory around the e3 axis")
        plt.close(_fig)
        return _fig

    return (draw_screw_motion,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
