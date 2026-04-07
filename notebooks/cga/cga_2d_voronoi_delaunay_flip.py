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
    # 2D Voronoi / Delaunay Flip

    With four nearby sites, the Delaunay triangulation can flip from one diagonal
    to the other. In the dual Voronoi picture, that is the moment when a Voronoi
    vertex changes which three sites define it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The local decision is an in-circle test. If the fourth point moves across the
    circumcircle of a triangle, the chosen Delaunay diagonal flips. This notebook
    keeps the picture local and visual rather than trying to build a full global
    triangulation.
    """)
    return


@app.cell
def _(mo):
    dy = mo.ui.slider(-1.2, 1.2, step=0.02, value=0.15, label="D along e2", show_value=True)
    return (dy,)


@app.cell
def _(dy, flip_plot, gm, mo, np):
    a = np.array([-1.0, -0.8], dtype=float)
    b = np.array([1.0, -0.75], dtype=float)
    c = np.array([0.85, 0.95], dtype=float)
    d = np.array([-0.95, dy.value], dtype=float)

    def _incircle_det(p, q, r, s):
        rows = []
        for pt in (p, q, r, s):
            rows.append([pt[0], pt[1], pt[0] ** 2 + pt[1] ** 2, 1.0])
        return float(np.linalg.det(np.array(rows, dtype=float)))

    det_val = _incircle_det(a, b, c, d)
    if abs(det_val) < 1e-6:
        decision = "on the circumcircle"
    elif det_val > 0:
        decision = "inside the circumcircle"
    else:
        decision = "outside the circumcircle"

    diagonal = "AC" if det_val > 0 else "BD"

    _md = rf"""
    In-circle test for $D$ against the circumcircle of $\triangle ABC$:

    $$
    \det = {det_val:.4f}
    $$

    Point $D$ is **{decision}**.

    Preferred local Delaunay diagonal: **{diagonal}**
    """

    mo.vstack([dy, gm.md(_md), flip_plot(a, b, c, d, det_val)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def _circumcircle(p, q, r):
        mat = 2 * np.array([[q[0] - p[0], q[1] - p[1]], [r[0] - p[0], r[1] - p[1]]], dtype=float)
        rhs = np.array([np.dot(q, q) - np.dot(p, p), np.dot(r, r) - np.dot(p, p)], dtype=float)
        if abs(np.linalg.det(mat)) <= 1e-8:
            return None, None
        center = np.linalg.solve(mat, rhs)
        radius = float(np.linalg.norm(center - p))
        return center, radius

    def _bisector(ax, p, q, color):
        n = 2 * (q - p)
        rhs = float(np.dot(q, q) - np.dot(p, p))
        if abs(n[1]) > 1e-9:
            xs = np.linspace(-2.0, 2.0, 240)
            ys = (rhs - n[0] * xs) / n[1]
            ax.plot(xs, ys, color=color, lw=1.6, alpha=0.9)
        else:
            ax.axvline(rhs / n[0], color=color, lw=1.6, alpha=0.9)

    def flip_plot(a, b, c, d, det_val):
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.8, 5.2))

        pts = np.stack([a, b, c, d], axis=0)
        labels = ["A", "B", "C", "D"]
        colors = ["#2563eb", "#d62828", "#2f855a", "#7c3aed"]

        center, radius = _circumcircle(a, b, c)
        if center is not None and radius is not None:
            t = np.linspace(0, 2 * np.pi, 240)
            ax0.plot(center[0] + radius * np.cos(t), center[1] + radius * np.sin(t), color="#9ca3af", lw=1.8)

        if det_val > 0:
            diag = (a, c)
        else:
            diag = (b, d)

        ax0.plot([a[0], b[0], c[0], d[0], a[0]], [a[1], b[1], c[1], d[1], a[1]], alpha=0.0)
        ax0.plot([diag[0][0], diag[1][0]], [diag[0][1], diag[1][1]], color="#111111", lw=2.2)
        ax0.plot([a[0], b[0]], [a[1], b[1]], color="#9ca3af", alpha=0.45)
        ax0.plot([b[0], c[0]], [b[1], c[1]], color="#9ca3af", alpha=0.45)
        ax0.plot([c[0], d[0]], [c[1], d[1]], color="#9ca3af", alpha=0.45)
        ax0.plot([d[0], a[0]], [d[1], a[1]], color="#9ca3af", alpha=0.45)

        if det_val > 0:
            _bisector(ax1, a, b, "#2563eb")
            _bisector(ax1, b, d, "#d62828")
            _bisector(ax1, d, a, "#7c3aed")
        else:
            _bisector(ax1, b, c, "#d62828")
            _bisector(ax1, c, d, "#2f855a")
            _bisector(ax1, d, b, "#7c3aed")

        for ax in (ax0, ax1):
            ax.scatter(pts[:, 0], pts[:, 1], color=colors, s=42, zorder=5)
            for p, label, color in zip(pts, labels, colors):
                ax.text(p[0] + 0.05, p[1] + 0.05, label, color=color, fontsize=11, weight="bold")
            ax.set_xlim(-1.8, 1.8)
            ax.set_ylim(-1.6, 1.6)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        ax0.set_title("Local Delaunay diagonal and circumcircle")
        ax1.set_title("Dual Voronoi vertex changing ownership")

        plt.close(fig)
        return fig

    return (flip_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
