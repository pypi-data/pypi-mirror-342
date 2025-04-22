def _draw_angle_arc(
    vertex,
    *other_points,
    radius=0.4,
    show_angle=False,
    vertex_label=None,
    fontsize=20,
):
    """
    Draw an arc to show the angle between two points relative to a vertex.
    For right angles (90 degrees), draws a small square instead.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to draw on
    vertex : tuple
        The vertex point (x, y)
    p1, p2 : tuple
        The two points forming the angle with the vertex
    radius : float
        Radius of the arc or size of the square for right angles
    """
    import numpy as np
    import plotmath

    ax = plotmath.gca()

    # Convert points to numpy arrays with float values
    vertex = np.array(vertex, dtype=float)
    p1, p2 = other_points
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)

    # Calculate vectors from vertex to points
    v1 = p1 - vertex
    v2 = p2 - vertex

    # Calculate angles
    angle1 = np.arctan2(v1[1], v1[0])
    angle2 = np.arctan2(v2[1], v2[0])

    # Calculate the angle between vectors
    dot_product = np.dot(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)
    angle = np.arccos(np.clip(dot_product / norms, -1.0, 1.0))

    # Check if it's approximately a right angle (90 degrees = π/2 radians)
    if np.abs(angle - np.pi / 2) < 1e-10:
        # Draw a square for right angle
        # Get unit vectors

        katet_len = radius / np.sqrt(2)

        u1 = v1 / np.linalg.norm(v1)
        u2 = v2 / np.linalg.norm(v2)

        u1 = u1 * katet_len
        u2 = u2 * katet_len

        # Calculate square corners
        square_points = [
            vertex + u1,
            vertex + (u1 + u2),
            vertex + u2,
            vertex,
        ]

        # Convert to separate x and y arrays
        x = [p[0] for p in square_points]
        y = [p[1] for p in square_points]

        # Plot the square
        ax.plot(x, y, "k-", linewidth=1)

        unit_vector = np.array(
            [
                2 * radius * 0.5 * (np.cos(angle1) + np.cos(angle2)),
                2 * radius * 0.5 * (np.sin(angle1) + np.sin(angle2)),
            ]
        )

        if vertex_label:
            ax.text(
                x=vertex[0] - 0.5 * unit_vector[0],
                y=vertex[1] - 0.5 * unit_vector[1],
                s=f"${vertex_label}$",
                fontsize=fontsize,
                ha="center",
                va="center",
            )

    else:
        # Ensure proper angle range for drawing the smaller angle
        if abs(angle2 - angle1) > np.pi:
            if angle2 > angle1:
                angle2 -= 2 * np.pi
            else:
                angle1 -= 2 * np.pi

        # Create arc points
        if np.degrees(angle) > 90:
            theta = np.linspace(angle1, angle2, 100)
            x = vertex[0] + 0.5 * radius * np.cos(theta)
            y = vertex[1] + 0.5 * radius * np.sin(theta)
        else:
            theta = np.linspace(angle1, angle2, 100)
            x = vertex[0] + radius * np.cos(theta)
            y = vertex[1] + radius * np.sin(theta)

        # Draw the arc
        if show_angle:
            ax.plot(x, y, "k-", linewidth=1)

        # Calculate text position
        unit_vector = np.array(
            [
                1.5 * radius * 0.5 * (np.cos(angle1) + np.cos(angle2)),
                1.5 * radius * 0.5 * (np.sin(angle1) + np.sin(angle2)),
            ]
        )
        x = vertex[0] + unit_vector[0]
        y = vertex[1] + unit_vector[1]

        angle_deg = np.degrees(angle)
        if np.abs(angle_deg - round(angle_deg)) < 1e-8:
            angle_str = f"${int(round(angle_deg))}^\\circ$"
        else:
            angle_str = f"${angle_deg:.2f}^\\circ$"

        # Plot the angle value
        # Determine text alignment based on position relative to vertex
        dx = x - vertex[0]
        dy = y - vertex[1]

        # Set horizontal alignment
        if abs(dx) < 0.1:  # Near vertical
            ha = "center"
        elif dx > 0:
            ha = "left"
        else:
            ha = "right"

        # Set vertical alignment
        if abs(dy) < 0.1:  # Near horizontal
            va = "center"
        elif dy > 0:
            va = "bottom"
        else:
            va = "top"

        if show_angle:
            if show_angle is True:
                ax.text(x, y, angle_str, fontsize=fontsize, ha="center", va="center")
            else:
                ax.text(
                    x=x,
                    y=y,
                    s=f"${show_angle}$",
                    fontsize=fontsize,
                    ha="center",
                    va="center",
                )

        if vertex_label:
            ax.text(
                x=vertex[0] - 0.5 * unit_vector[0],
                y=vertex[1] - 0.5 * unit_vector[1],
                s=f"${vertex_label}$",
                fontsize=fontsize,
                ha=ha,
                va=va,
            )


def draw_triangle(
    *points,
    sss=None,
    asa=None,
    sas=None,
    show_vertices=True,
    radius=None,  # None → automatic per‑vertex
    alpha=0.15,
    show=True,
    fontsize=20,
    label_angles=(True, True, True),
    vertex_labels=("A", "B", "C"),
    label_sides=(True, True, True),
    numerical_len=False,
    axis_off=True,
    color=None,
):
    """
    Draw a triangle with sensible angle‑arc radii and well‑placed labels.

    • `label_angles`:  True  → write the numeric angle value
                       str   → write that string
                       False → nothing
    • Side labels are always placed **outside** the triangle.
    """

    # ---------------------------------------------------------------- imports
    import numpy as np
    import sympy as sp
    from matplotlib.patches import Arc
    import plotmath  # <- your helper library

    # ----------------------------------------------------- tiny helpers
    def _to_xy(pt):
        return float(pt.x.evalf()), float(pt.y.evalf())

    def _unit(v):
        v = np.asarray(v, float)
        n = np.linalg.norm(v)
        return v / n if n else v

    def _arc_radius(adj1, adj2, in_r):
        r = 0.18 * min(adj1, adj2)
        if in_r is not None:
            r = min(r, 0.8 * in_r)
        return r

    # --------------------- angle‑arc / angle‑label drawing ------------------
    def _draw_angle_arc(ax, v, p1, p2, r, label):
        """
        Draw the interior angle at `v` with radius `r`.
        `label` controls the text:
            • False → no text
            • True  → numeric angle value
            • str   → that string
        """
        v, p1, p2 = map(np.asarray, (v, p1, p2))
        v1, v2 = p1 - v, p2 - v

        # raw angles for the arc endpoints
        a1 = np.degrees(np.arctan2(v1[1], v1[0]))
        a2 = np.degrees(np.arctan2(v2[1], v2[0]))
        sweep = (a2 - a1) % 360
        if sweep > 180:
            sweep -= 360  # interior sweep
        ang_rad = np.radians(abs(sweep))

        # right‑angle test
        right_angle = abs(ang_rad - np.pi / 2) < 1e-10

        if right_angle:  # draw the little square
            kat = r / np.sqrt(2)
            u1 = _unit(v1) * kat
            u2 = _unit(v2) * kat
            square = np.array([v, v + u1, v + u1 + u2, v + u2, v])
            ax.plot(square[:, 0], square[:, 1], "k-", lw=1.5)
        else:  # ordinary arc
            ax.add_patch(
                Arc(
                    v,
                    2 * r,
                    2 * r,
                    angle=0,
                    theta1=a1,
                    theta2=a1 + sweep,
                    lw=1.5,
                    fill=False,
                )
            )

        # ------------------------------------------------ text on bisector
        if label:
            # choose the string to display
            if label is True:
                angle_deg = np.degrees(ang_rad)
                angle_txt = (
                    f"{int(round(angle_deg))}"
                    if abs(angle_deg - round(angle_deg)) < 1e-8
                    else f"{angle_deg:.2f}"
                )
                text = rf"${angle_txt}^\circ$"
            else:  # a custom string
                text = rf"${label}$"

            # position: 1.25 r along the angle‑bisector
            bis = _unit(v1 / np.linalg.norm(v1) + v2 / np.linalg.norm(v2))
            pos = v + bis * (1.25 * r)
            ax.text(
                pos[0],
                pos[1],
                text,
                ha="center",
                va="center",
                fontsize=fontsize,
            )

    # --------------------------------------------------- build Triangle obj
    if sss:
        tri = sp.Triangle(sss=sss)
    elif asa:
        tri = sp.Triangle(asa=asa)
    elif sas:
        tri = sp.Triangle(sas=sas)
    else:
        tri = sp.Triangle(*points)

    verts_sp = tri.vertices
    verts = [_to_xy(v) for v in verts_sp]
    side_lengths = [float(s.length.evalf()) for s in tri.sides]

    # robust in‑radius
    try:
        in_r = float(tri.incircle.radius.evalf())
    except Exception:
        area = float(tri.area.evalf())
        per = sum(side_lengths)
        in_r = 2 * area / per if per else None

    centroid = np.mean(verts, axis=0)

    # -------------------------------------------- draw the polygon shell
    if color is None:
        color = plotmath.COLORS.get("blue")

    plotmath.plot_polygon(*verts, show_vertices=show_vertices, alpha=alpha, color=color)
    ax = plotmath.gca()

    # ------------------------------------------------- angles & vertices
    for i, (v, show_ang, vlab) in enumerate(zip(verts, label_angles, vertex_labels)):
        p1, p2 = verts[(i + 1) % 3], verts[(i + 2) % 3]
        adj1 = np.linalg.norm(np.array(v) - np.array(p1))
        adj2 = np.linalg.norm(np.array(v) - np.array(p2))
        r_i = radius if radius is not None else _arc_radius(adj1, adj2, in_r)

        _draw_angle_arc(ax, v, p1, p2, r_i, show_ang)

        # vertex name, pushed outwards
        ax.text(
            *(np.array(v) + _unit(np.array(v) - centroid) * (1.4 * r_i)),
            rf"${vlab}$",
            ha="center",
            va="center",
            fontsize=fontsize,
        )

    # ------------------------------------------------------- side labels
    for seg, lab in zip(tri.sides, label_sides):
        if not lab:
            continue

        p, q = map(np.asarray, (_to_xy(seg.points[0]), _to_xy(seg.points[1])))
        mid = (p + q) / 2
        edge = q - p

        # exterior normal: point *away* from the centroid
        normal = np.array([-edge[1], edge[0]])
        if np.dot(normal, centroid - mid) > 0:  # pointing inward
            normal *= -1
        n_hat = _unit(normal)

        offset = 0.07 * float(seg.length.evalf())  # 7 % of side length

        # decide the text to show
        if lab is True:  # use SymPy symbolic length
            txt = rf"${sp.latex(seg.length)}$"
        else:
            txt = rf"${lab}$"

        if numerical_len:
            num = float(seg.length.evalf())
            txt = rf"${num:.0f}$" if abs(num - round(num)) < 1e-8 else rf"${num:.2f}$"

        ax.text(
            *(mid + offset * n_hat),
            txt,
            ha="center",
            va="center",
            fontsize=fontsize,
        )

    # ------------------------------------------------------- finish up
    ax.axis("equal")
    if axis_off:
        ax.axis("off")
    if show:
        plotmath.show()
    else:
        return ax
