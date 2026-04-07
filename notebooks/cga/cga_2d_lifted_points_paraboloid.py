import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    from galaga.blade_convention import b_cga
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return Algebra, b_cga, gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA Lifted Points Form a Paraboloid

    A Euclidean point does not just get "renamed" in CGA. Under `up(x)`, it is
    lifted into a higher-dimensional null vector whose extra coordinate grows
    quadratically with distance from the origin.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In 2D conformal GA,

    $$
    X = \operatorname{up}(x) = e_o + x + \frac{1}{2}x^2 e_\infty.
    $$

    So if we keep the Euclidean part $(x,y)$ and plot the extra
    $e_\infty$ coefficient as height, the lifted points lie on the paraboloid

    $$
    z = \frac{1}{2}(x^2 + y^2).
    $$
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    px = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.9, label="e1", show_value=True)
    py = mo.ui.slider(-1.8, 1.8, step=0.05, value=-0.4, label="e2", show_value=True)
    show_pm = mo.ui.checkbox(value=False, label="Show e+, e- coefficient plot")
    view_yaw = mo.ui.slider(-30, 30, step=1, value=0, label="View yaw", show_value=True)
    return px, py, show_pm, view_yaw


@app.cell
def _(
    alg,
    e1,
    e2,
    em,
    ep,
    gm,
    lifted_point_plot,
    mo,
    px,
    py,
    show_pm,
    view_yaw,
):
    half = alg.frac(1, 2)
    eo = (half * (em - ep)).name(latex=r"e_o")
    einf = (ep + em).name(latex=r"e_\infty")

    x = (px.value * e1 + py.value * e2).name(latex="x")
    X = (eo + x + half * (x | x) * einf).name(latex=r"X = \operatorname{up}(x)")

    einf_coeff = (half * (x | x)).name(latex=r"\tfrac{1}{2}x^2")
    ep_coeff = (X | em).name(latex=r"X \cdot e_-")
    em_coeff = (X | ep).name(latex=r"X \cdot e_+")

    _md = t"""
    {eo.display()} <br/>
    {einf.display()} <br/>
    {x.display()} <br/>
    {X.display()} <br/>
    {einf_coeff.display()} <br/>
    {ep_coeff.display()} <br/>
    {em_coeff.display()} <br/>
    As the Euclidean point moves in the plane, the lifted point moves on a paraboloid in the extra conformal direction.
    """

    mo.vstack([px, py, show_pm, gm.md(_md), lifted_point_plot(x, X, eo, einf, ep, em, show_pm.value, view_yaw.value), view_yaw])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    The conformal lift is easiest to see geometrically if you treat the
    $e_\infty$ coefficient as height. Then Euclidean points in the plane become
    points on a paraboloid. The null-basis coefficients are still useful, but
    the paraboloid is the pattern the eye can actually track.
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
    def lifted_point_plot(x, X, eo, einf, ep, em, show_pm, view_yaw_deg):
        _xy = np.array(x.vector_part[:2], dtype=float)
        _height = 0.5 * float(np.dot(_xy, _xy))

        _X_eval = X.eval()
        _eo_coeff = float((_X_eval | eo.eval()).scalar_part)
        _ep_coeff = float((_X_eval | ep.eval()).scalar_part)
        _em_coeff = float((_X_eval | em.eval()).scalar_part)

        _grid = np.linspace(-1.8, 1.8, 80)
        _gx, _gy = np.meshgrid(_grid, _grid)
        _gz = 0.5 * (_gx**2 + _gy**2)

        if show_pm:
            _fig = plt.figure(figsize=(13.0, 5.2))
            _ax0 = _fig.add_subplot(121)
            _ax1 = _fig.add_subplot(122, projection="3d")
        else:
            _fig = plt.figure(figsize=(7.2, 5.2))
            _ax0 = _fig.add_subplot(111, projection="3d")
            _ax1 = None

        _target_ax = _ax1 if show_pm else _ax0
        _target_ax.plot_surface(_gx, _gy, _gz, color="#ddd6fe", alpha=0.28, linewidth=0, shade=False)
        _target_ax.scatter([_xy[0]], [_xy[1]], [0], color="#2563eb", s=38, alpha=0.75)
        _target_ax.scatter([_xy[0]], [_xy[1]], [_height], color="#7c3aed", s=58)
        _target_ax.plot([_xy[0], _xy[0]], [_xy[1], _xy[1]], [0, _height], color="#7c3aed", alpha=0.35, linewidth=1.8)
        _target_ax.set_xlim(-1.9, 1.9)
        _target_ax.set_ylim(-1.9, 1.9)
        _target_ax.set_zlim(0, 3.4)
        _target_ax.set_box_aspect((1, 1, 0.85))
        _target_ax.view_init(elev=22, azim=-58 + view_yaw_deg)
        _target_ax.set_xlabel(r"$\mathbf{e_1}$")
        _target_ax.set_ylabel(r"$\mathbf{e_2}$")
        _target_ax.set_zlabel(r"$e_\infty\ \mathrm{coeff}$")
        _target_ax.set_title("Lifted point on the paraboloid")

        if show_pm:
            _ax0.axline((-1.2, -0.2), slope=1.0, color="#999999", alpha=0.35, linewidth=1.0)
            _ax0.scatter([_ep_coeff], [_em_coeff], color="#7c3aed", s=65)
            _ax0.set_xlim(-2.2, 2.2)
            _ax0.set_ylim(-1.2, 3.2)
            _ax0.grid(True, alpha=0.18)
            _ax0.set_aspect("equal")
            _ax0.set_xlabel(r"$e_+\ \mathrm{coeff}$")
            _ax0.set_ylabel(r"$e_-\ \mathrm{coeff}$")
            _ax0.set_title(r"$e_+,e_-$ coefficients of $X$")

        plt.close(_fig)
        return _fig

    return (lifted_point_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
