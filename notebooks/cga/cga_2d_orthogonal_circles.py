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
    # 2D CGA Orthogonal Circles

    Two circles are orthogonal when they meet at right angles. In Euclidean
    geometry that is a local angle condition at the intersection points. In CGA
    it becomes a simple relation between the two circle objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For circles with centres $c_1,c_2$ and radii $r_1,r_2$, orthogonality means

    $$
    \|c_2-c_1\|^2 = r_1^2 + r_2^2.
    $$

    When this holds, the radius directions to either shared point are
    perpendicular, so the circles cross at $90^\circ$.
    """)
    return


@app.cell
def _(mo):
    r1 = mo.ui.slider(0.3, 1.5, step=0.05, value=0.9, label="circle 1 radius", show_value=True)
    r2 = mo.ui.slider(0.3, 1.5, step=0.05, value=0.7, label="circle 2 radius", show_value=True)
    angle_deg = mo.ui.slider(-180, 180, step=1, value=25, label="centre direction", show_value=True)
    offset = mo.ui.slider(-0.8, 0.8, step=0.01, value=0.0, label="distance offset from orthogonal", show_value=True)
    return angle_deg, offset, r1, r2


@app.cell
def _(angle_deg, gm, mo, offset, orthogonal_circles_plot, r1, r2):
    base_d = (r1.value**2 + r2.value**2) ** 0.5
    d = max(0.05, base_d + offset.value)
    lhs = d**2
    rhs = r1.value**2 + r2.value**2
    diff = lhs - rhs

    if abs(diff) < 1e-6:
        status = "orthogonal"
    elif diff < 0:
        status = "acute intersection"
    else:
        status = "obtuse / separated trend"

    _md = rf"""
    Orthogonality test:

    $$
    \|c_2-c_1\|^2 = {lhs:.4f}
    $$

    $$
    r_1^2 + r_2^2 = {rhs:.4f}
    $$

    Difference:

    $$
    \|c_2-c_1\|^2 - (r_1^2+r_2^2) = {diff:.4f}
    $$

    Status: **{status}**
    """

    mo.vstack([r1, r2, angle_deg, offset, gm.md(_md), orthogonal_circles_plot(r1.value, r2.value, d, angle_deg.value)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    def orthogonal_circles_plot(r1, r2, d, angle_deg):
        angle = np.radians(angle_deg)
        c1 = np.array([0.0, 0.0], dtype=float)
        c2 = np.array([d * np.cos(angle), d * np.sin(angle)], dtype=float)
        t = np.linspace(0, 2 * np.pi, 260)

        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.6, 5.2))

        x1 = r1 * np.cos(t)
        y1 = r1 * np.sin(t)
        x2 = c2[0] + r2 * np.cos(t)
        y2 = c2[1] + r2 * np.sin(t)

        for ax in (ax0, ax1):
            ax.plot(x1, y1, color="#2563eb", lw=2.2)
            ax.plot(x2, y2, color="#d62828", lw=2.2)
            ax.scatter([c1[0], c2[0]], [c1[1], c2[1]], color=["#2563eb", "#d62828"], s=38)
            ax.set_xlim(-2.1, 2.1)
            ax.set_ylim(-2.1, 2.1)
            ax.set_aspect("equal")
            ax.grid(True, alpha=0.18)
            ax.set_xlabel(r"$\mathbf{e_1}$")
            ax.set_ylabel(r"$\mathbf{e_2}$")

        dist = float(np.linalg.norm(c2))
        if dist > 1e-8:
            ex = c2 / dist
            ey = np.array([-ex[1], ex[0]])
            x = (dist**2 + r1**2 - r2**2) / (2 * dist)
            y_sq = r1**2 - x**2
            if y_sq >= -1e-8:
                y = np.sqrt(max(y_sq, 0.0))
                pts = [x * ex + y * ey] if y < 1e-6 else [x * ex + y * ey, x * ex - y * ey]
                for p in pts:
                    ax0.scatter([p[0]], [p[1]], color="#111111", s=42, zorder=5)
                    v1 = p - c1
                    v2 = p - c2
                    ax0.plot([c1[0], p[0]], [c1[1], p[1]], color="#2563eb", alpha=0.35, lw=1.4)
                    ax0.plot([c2[0], p[0]], [c2[1], p[1]], color="#d62828", alpha=0.35, lw=1.4)
                    ax1.scatter([p[0]], [p[1]], color="#111111", s=42, zorder=5)
                    ax1.quiver(
                        [p[0], p[0]],
                        [p[1], p[1]],
                        [v1[0], v2[0]],
                        [v1[1], v2[1]],
                        angles="xy",
                        scale_units="xy",
                        scale=1,
                        color=["#2563eb", "#d62828"],
                        alpha=0.65,
                        width=0.006,
                    )

        ax0.set_title("Two circles meeting")
        ax1.set_title("Radius directions at the intersections")

        plt.close(fig)
        return fig

    return (orthogonal_circles_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
