import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import galaga_marimo as gm
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return gm, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2D CGA Circumcircle and Delaunay Triangle

    Three non-collinear points determine one circle. In Delaunay language, that
    circumcircle is the local object that decides whether the triangle is
    well-formed and which side of an edge a fourth point belongs on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For three points $A,B,C$, the circumcenter is the common point of the three
    pairwise Voronoi bisectors. The circumcircle then has radius

    $$
    r = \|A - c_{\mathrm{circ}}\|.
    $$

    In the 2D-CGA picture, this is one circle object passing through the three
    sites.
    """)
    return


@app.cell
def _(mo):
    ax = mo.ui.slider(-1.6, 1.6, step=0.05, value=-1.0, label="A along e1", show_value=True)
    ay = mo.ui.slider(-1.6, 1.6, step=0.05, value=-0.5, label="A along e2", show_value=True)
    bx = mo.ui.slider(-1.6, 1.6, step=0.05, value=1.0, label="B along e1", show_value=True)
    by = mo.ui.slider(-1.6, 1.6, step=0.05, value=-0.25, label="B along e2", show_value=True)
    cx = mo.ui.slider(-1.6, 1.6, step=0.05, value=0.1, label="C along e1", show_value=True)
    cy = mo.ui.slider(-1.6, 1.6, step=0.05, value=1.0, label="C along e2", show_value=True)
    return ax, ay, bx, by, cx, cy


@app.cell
def _(ax, ay, bx, by, circumcircle_plot, cx, cy, gm, mo, np):
    a = np.array([ax.value, ay.value], dtype=float)
    b = np.array([bx.value, by.value], dtype=float)
    c = np.array([cx.value, cy.value], dtype=float)
    mat = 2 * np.array([[b[0] - a[0], b[1] - a[1]], [c[0] - a[0], c[1] - a[1]]], dtype=float)
    rhs = np.array([np.dot(b, b) - np.dot(a, a), np.dot(c, c) - np.dot(a, a)], dtype=float)

    if abs(np.linalg.det(mat)) > 1e-8:
        center = np.linalg.solve(mat, rhs)
        radius = float(np.linalg.norm(a - center))
        center_text = rf"({center[0]:.3f}, {center[1]:.3f})"
        radius_text = f"{radius:.3f}"
    else:
        center_text = r"\text{undefined (collinear)}"
        radius_text = r"\text{undefined}"

    _md = rf"""
    Circumcenter:

    $$
    c_{{\mathrm{{circ}}}} = {center_text}
    $$

    Circumradius:

    $$
    r_{{\mathrm{{circ}}}} = {radius_text}
    $$
    """

    mo.vstack([ax, ay, bx, by, cx, cy, gm.md(_md), circumcircle_plot(a, b, c)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def circumcircle_plot(a, b, c):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.8, 5.2))

        pts = np.stack([a, b, c], axis=0)
        labels = ["A", "B", "C"]
        colors = ["#2563eb", "#d62828", "#2f855a"]

        mat = 2 * np.array([[b[0] - a[0], b[1] - a[1]], [c[0] - a[0], c[1] - a[1]]], dtype=float)
        rhs = np.array([np.dot(b, b) - np.dot(a, a), np.dot(c, c) - np.dot(a, a)], dtype=float)
        center = None
        radius = None
        if abs(np.linalg.det(mat)) > 1e-8:
            center = np.linalg.solve(mat, rhs)
            radius = float(np.linalg.norm(a - center))

        for ax in (ax0, ax1):
            ax.fill(pts[:, 0], pts[:, 1], color="#ede9fe", alpha=0.22)
            ax.plot([a[0], b[0], c[0], a[0]], [a[1], b[1], c[1], a[1]], color="#6b7280", lw=1.6)
            ax.scatter(pts[:, 0], pts[:, 1], color=colors, s=42, zorder=5)
            for p, label, color in zip(pts, labels, colors):
                ax.text(p[0] + 0.05, p[1] + 0.05, label, color=color, fontsize=11, weight="bold")
            ax.set_xlim(-2.0, 2.0)
            ax.set_ylim(-2.0, 2.0)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        if center is not None and radius is not None:
            t = np.linspace(0, 2 * np.pi, 240)
            circle_x = center[0] + radius * np.cos(t)
            circle_y = center[1] + radius * np.sin(t)
            ax0.plot(circle_x, circle_y, color="#7c3aed", lw=2.2)
            ax0.scatter([center[0]], [center[1]], color="#111111", s=42)

            bisector_pairs = [(a, b, "#2563eb"), (b, c, "#d62828"), (c, a, "#2f855a")]
            for p, q, color in bisector_pairs:
                n = 2 * (q - p)
                rhs_line = float(np.dot(q, q) - np.dot(p, p))
                if abs(n[1]) > 1e-9:
                    xs = np.linspace(-2.1, 2.1, 240)
                    ys = (rhs_line - n[0] * xs) / n[1]
                    ax1.plot(xs, ys, color=color, lw=1.8)
                else:
                    ax1.axvline(rhs_line / n[0], color=color, lw=1.8)
            ax1.scatter([center[0]], [center[1]], color="#111111", s=42, zorder=6)

        ax0.set_title("Triangle and its circumcircle")
        ax1.set_title("Voronoi bisectors meeting at the circumcenter")

        plt.close(fig)
        return fig

    return (circumcircle_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
