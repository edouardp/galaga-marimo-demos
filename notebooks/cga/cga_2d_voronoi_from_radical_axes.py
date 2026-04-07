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
    # 2D Voronoi from CGA Radical Axes

    A Voronoi edge is the Euclidean locus of points that are equally distant from
    two sites. In CGA language, each site can be treated as a zero-radius circle,
    so a Voronoi bisector is just the radical axis of two point-circles.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For two sites $a$ and $b$, define the two point-circles by radius $0$. Their
    powers at a probe point $x$ are

    $$
    P_a(x) = (x-a)^2,
    \qquad
    P_b(x) = (x-b)^2.
    $$

    The Voronoi bisector is where these powers are equal:

    $$
    P_a(x) - P_b(x) = 0.
    $$

    That is exactly the radical-axis condition. With three sites, the Voronoi
    vertex is where the three radical axes meet.
    """)
    return


@app.cell
def _(Algebra, b_cga):
    alg = Algebra(3, 1, blades=b_cga(euclidean=2, null_basis="plus_minus"))
    e1, e2, ep, em = alg.basis_vectors(lazy=True)
    return alg, e1, e2, em, ep


@app.cell
def _(mo):
    ax = mo.ui.slider(-1.8, 1.8, step=0.05, value=-1.0, label="A along e1", show_value=True)
    ay = mo.ui.slider(-1.8, 1.8, step=0.05, value=-0.2, label="A along e2", show_value=True)
    bx = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.9, label="B along e1", show_value=True)
    by = mo.ui.slider(-1.8, 1.8, step=0.05, value=-0.1, label="B along e2", show_value=True)
    cx = mo.ui.slider(-1.8, 1.8, step=0.05, value=0.0, label="C along e1", show_value=True)
    cy = mo.ui.slider(-1.8, 1.8, step=0.05, value=1.0, label="C along e2", show_value=True)
    show_regions = mo.ui.checkbox(value=True, label="Show Voronoi regions")
    return ax, ay, bx, by, cx, cy, show_regions


@app.cell
def _(
    alg,
    ax,
    ay,
    bx,
    by,
    cx,
    cy,
    e1,
    e2,
    em,
    ep,
    gm,
    mo,
    np,
    show_regions,
    voronoi_radical_axes_plot,
):
    a = np.array([ax.value, ay.value], dtype=float)
    b = np.array([bx.value, by.value], dtype=float)
    c = np.array([cx.value, cy.value], dtype=float)

    half = alg.frac(1, 2)
    eo = half * (em - ep)
    einf = ep + em
    a_mv = (ax.value * e1 + ay.value * e2).name(latex="a")
    b_mv = (bx.value * e1 + by.value * e2).name(latex="b")
    c_mv = (cx.value * e1 + cy.value * e2).name(latex="c")
    A = (eo + a_mv + half * (a_mv | a_mv) * einf).name(latex="A")
    B = (eo + b_mv + half * (b_mv | b_mv) * einf).name(latex="B")
    C = (eo + c_mv + half * (c_mv | c_mv) * einf).name(latex="C")

    def _bisector_equation(p, q):
        n = 2 * (q - p)
        rhs = float(np.dot(q, q) - np.dot(p, p))
        return n, rhs

    nab, rhsab = _bisector_equation(a, b)
    nbc, rhsbc = _bisector_equation(b, c)
    nca, rhsca = _bisector_equation(c, a)

    mat = np.stack([nab, nbc], axis=0)
    vec = np.array([rhsab, rhsbc], dtype=float)
    if abs(np.linalg.det(mat)) > 1e-8:
        vertex = np.linalg.solve(mat, vec)
        vertex_text = rf"({vertex[0]:.3f}, {vertex[1]:.3f})"
    else:
        vertex_text = r"\text{undefined (sites nearly collinear)}"

    _md = t"""
    {A.display()} <br/>
    {B.display()} <br/>
    {C.display()} <br/>
    For a probe point $X = \\operatorname{{up}}(x)$, the pairwise Voronoi bisectors are the CGA equal-distance conditions
    $$
    X \\cdot A = X \\cdot B,\\qquad
    X \\cdot B = X \\cdot C,\\qquad
    X \\cdot C = X \\cdot A.
    $$
    In coordinates these become:
    $$
    {nab[0]:.2f}x + {nab[1]:.2f}y = {rhsab:.3f}
    $$
    $$
    {nbc[0]:.2f}x + {nbc[1]:.2f}y = {rhsbc:.3f}
    $$
    $$
    {nca[0]:.2f}x + {nca[1]:.2f}y = {rhsca:.3f}
    $$
    Voronoi vertex / circumcenter:
    $$
    x_{{\\mathrm{{vor}}}} = {vertex_text}
    $$
    """

    mo.vstack(
        [
            ax,
            ay,
            bx,
            by,
            cx,
            cy,
            show_regions,
            gm.md(_md),
            voronoi_radical_axes_plot(a, b, c, show_regions.value),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _plot_line(ax, p, q, color):
        n = 2 * (q - p)
        rhs = float(np.dot(q, q) - np.dot(p, p))
        if np.linalg.norm(n) < 1e-9:
            return
        if abs(n[1]) > 1e-9:
            xs = np.linspace(-2.3, 2.3, 240)
            ys = (rhs - n[0] * xs) / n[1]
            ax.plot(xs, ys, color=color, lw=2.0)
        else:
            x0 = rhs / n[0]
            ax.axvline(x0, color=color, lw=2.0)

    def voronoi_radical_axes_plot(a, b, c, show_regions):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.4))

        xs = np.linspace(-2.2, 2.2, 220)
        ys = np.linspace(-2.2, 2.2, 220)
        gx, gy = np.meshgrid(xs, ys)
        da = (gx - a[0]) ** 2 + (gy - a[1]) ** 2
        db = (gx - b[0]) ** 2 + (gy - b[1]) ** 2
        dc = (gx - c[0]) ** 2 + (gy - c[1]) ** 2

        if show_regions:
            nearest = np.argmin(np.stack([da, db, dc], axis=0), axis=0)
            cmap = plt.matplotlib.colors.ListedColormap(["#bfdbfe", "#fecaca", "#dcfce7"])
            ax0.contourf(gx, gy, nearest, levels=[-0.5, 0.5, 1.5, 2.5], cmap=cmap, alpha=0.33)

        ax1.contour(gx, gy, da - db, levels=[0], colors=["#2563eb"], linewidths=2.0)
        ax1.contour(gx, gy, db - dc, levels=[0], colors=["#d62828"], linewidths=2.0)
        ax1.contour(gx, gy, dc - da, levels=[0], colors=["#2f855a"], linewidths=2.0)

        _plot_line(ax0, a, b, "#2563eb")
        _plot_line(ax0, b, c, "#d62828")
        _plot_line(ax0, c, a, "#2f855a")

        sites = np.stack([a, b, c], axis=0)
        site_colors = ["#2563eb", "#d62828", "#2f855a"]
        labels = ["A", "B", "C"]
        for ax in (ax0, ax1):
            ax.scatter(sites[:, 0], sites[:, 1], color=site_colors, s=42, zorder=5)
            for pt, label, color in zip(sites, labels, site_colors):
                ax.text(pt[0] + 0.05, pt[1] + 0.05, label, color=color, fontsize=11, weight="bold")
            ax.set_xlim(-2.2, 2.2)
            ax.set_ylim(-2.2, 2.2)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        mat = np.stack([2 * (b - a), 2 * (c - b)], axis=0)
        rhs = np.array(
            [float(np.dot(b, b) - np.dot(a, a)), float(np.dot(c, c) - np.dot(b, b))], dtype=float
        )
        if abs(np.linalg.det(mat)) > 1e-8:
            vertex = np.linalg.solve(mat, rhs)
            ax0.scatter([vertex[0]], [vertex[1]], color="#111111", s=45, zorder=6)
            ax1.scatter([vertex[0]], [vertex[1]], color="#111111", s=45, zorder=6)

        ax0.set_title("Voronoi bisectors as radical axes")
        ax1.set_title("Zero contours of pairwise power differences")

        plt.close(fig)
        return fig

    return (voronoi_radical_axes_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
