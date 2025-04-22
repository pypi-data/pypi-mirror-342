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
    Draws a triangle with intelligently‑sized angle arcs and neatly placed labels.

    All public parameters are exactly the same as in the original version.
    """

    ###########################################################################
    # Standard imports
    ###########################################################################
    import numpy as np
    import sympy as sp
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc

    # ------------------------------------------------------------------ helpers
    def _to_xy(pt):
        """Return (float(x), float(y)) for any SymPy Point‑like."""
        return (float(pt.x.evalf()), float(pt.y.evalf()))

    def _angle(p, c):
        """atan2 angle of vector p‑>c."""
        return np.degrees(np.arctan2(c[1] - p[1], c[0] - p[0]))

    def _unit(v):
        v = np.asarray(v, dtype=float)
        n = np.linalg.norm(v)
        return v / n if n else v

    def _arc_radius(adj1, adj2, in_r):
        """
        Pick a radius that is
            • 18 % of the shorter adjacent side, *and*
            • no larger than 80 % of the in‑radius.
        """
        r = 0.18 * min(adj1, adj2)
        if in_r is not None:
            r = min(r, 0.8 * in_r)
        return r

    def _draw_angle_arc(ax, v, p1, p2, r, label, label_text):
        """
        Draw an angle arc centred at `v` between the rays v→p1 and v→p2
        with radius `r`; write `label_text` on the bisector when `label`.
        """
        # vectors
        v1 = np.array(p1) - np.array(v)
        v2 = np.array(p2) - np.array(v)

        ang1 = np.degrees(np.arctan2(v1[1], v1[0]))
        ang2 = np.degrees(np.arctan2(v2[1], v2[0]))

        # smallest positive/negative sweep (inside the triangle)
        sweep = (ang2 - ang1) % 360
        if sweep > 180:
            sweep -= 360  # go the other way (negative sweep)

        # Draw the arc
        ax.add_patch(
            Arc(
                v,
                width=2 * r,
                height=2 * r,
                angle=0,
                theta1=ang1,
                theta2=ang1 + sweep,
                lw=1.5,
                fill=False,
            )
        )

        # Label on the angle bisector
        if label:
            bis_vec = _unit(v1 / np.linalg.norm(v1) + v2 / np.linalg.norm(v2))
            txt_pos = np.array(v) + bis_vec * (1.25 * r)
            ax.text(
                txt_pos[0],
                txt_pos[1],
                f"${label_text}$",
                ha="center",
                va="center",
                fontsize=fontsize,
            )

    ###########################################################################
    # Build the SymPy Triangle object
    ###########################################################################
    if sss:
        tri = sp.Triangle(sss=sss)
    elif asa:
        tri = sp.Triangle(asa=asa)
    elif sas:
        tri = sp.Triangle(sas=sas)
    else:
        tri = sp.Triangle(*points)

    # Geometry data -----------------------------------------------------------
    verts_sp = tri.vertices
    verts = [_to_xy(v) for v in verts_sp]  # plain tuples
    side_lengths = [float(s.length.evalf()) for s in tri.sides]
    in_r = float(tri.incircle.radius.evalf()) if tri.is_regular is False else None
    centroid = np.mean(verts, axis=0)

    # A pleasant stable colour choice
    if color is None:
        import plotmath

        color = plotmath.COLORS.get("blue")

    ###########################################################################
    # Plot the polygon shell
    ###########################################################################
    import plotmath

    plotmath.plot_polygon(*verts, show_vertices=show_vertices, alpha=alpha, color=color)
    ax = plotmath.gca()

    ###########################################################################
    # Angle arcs, angle labels and vertex labels
    ###########################################################################
    default_angle_letters = (r"\alpha", r"\beta", r"\gamma")

    for i, (v, show_ang, vlabel) in enumerate(zip(verts, label_angles, vertex_labels)):
        # indices of the two other vertices
        p1, p2 = verts[(i + 1) % 3], verts[(i + 2) % 3]
        # adjacent side lengths
        adj1 = np.linalg.norm(np.array(v) - np.array(p1))
        adj2 = np.linalg.norm(np.array(v) - np.array(p2))

        # Arc radius – automatic if radius=None, otherwise honour user value
        r_i = radius if radius is not None else _arc_radius(adj1, adj2, in_r)

        # Draw arc + label
        _draw_angle_arc(
            ax,
            v,
            p1,
            p2,
            r_i,
            show_ang,
            default_angle_letters[i] if show_ang is True else show_ang,
        )

        # Vertex name – outside the triangle
        vec_out = _unit(np.array(v) - centroid)
        ax.text(
            *(np.array(v) + vec_out * (1.4 * r_i)),
            f"${vlabel}$",
            ha="center",
            va="center",
            fontsize=fontsize,
        )

    ###########################################################################
    # Side‑length labels
    ###########################################################################
    for seg, show_side in zip(tri.sides, label_sides):
        if not show_side:
            continue

        p, q = _to_xy(seg.points[0]), _to_xy(seg.points[1])
        mid = (np.array(p) + np.array(q)) / 2.0
        edge_vec = np.array(q) - np.array(p)

        # interior normal: choose sign so that it points towards the centroid
        normal = np.array([-edge_vec[1], edge_vec[0]])
        if np.dot(normal, centroid - mid) < 0:
            normal *= -1
        n_hat = _unit(normal)

        offset = 0.07 * float(seg.length.evalf())  # 7 % of that side

        # Actual text to write
        if show_side is True:  # auto label = length symbol
            text = f"${sp.latex(seg.length)}$"
        else:
            text = f"${show_side}$"

        if numerical_len:
            # prettify numeric output
            num_val = float(seg.length.evalf())
            text = (
                f"${num_val:.0f}$"
                if abs(num_val - round(num_val)) < 1e-8
                else f"${num_val:.2f}$"
            )

        ax.text(
            *(mid + offset * n_hat),
            text,
            ha="center",
            va="center",
            fontsize=fontsize,
        )

    ###########################################################################
    # Finishing touches
    ###########################################################################
    ax.axis("equal")
    if axis_off:
        ax.axis("off")

    if show:
        plotmath.show()
    else:
        return ax
