"""EonPoint 亿触点 — parametric logo construction.

Everything is drawn from geometry (no fonts), so every file is self-contained:
  * symbols  : A 裂变 Fission (1·2·4) / B 星芒 Spark (1+8) / C 点动成线 Trace (dissolving e)
  * wordmark : monoline geometric letters  E o n P i t  (lower / title / upper case)
  * 中文      : monoline 亿触点 on a 100-unit body, the 点 strokes drawn as true dots
Coordinates: x → right, y ↓ down, baseline at y = 0 for type.
"""
import math

# ───────────────────────────── palette ─────────────────────────────
RED = "#9B1C2E"       # Eon Red — the original wine red, cleaned up
RED_DEEP = "#6E1022"
RED_MID = "#C8323C"
CORAL = "#F07158"
INK = "#15131A"
PAPER = "#F4F1EC"
WHITE = "#FFFFFF"


def n(v):
    s = f"{v:.2f}"
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ───────────────────────────── primitives ─────────────────────────────
# a shape list is a list of dicts:
#   {"k": "s", "d": path, "w": stroke}        stroked path
#   {"k": "c", "x":, "y":, "r":}              filled circle
#   {"k": "f", "d": path}                     filled path
#   optional "role": "accent" / "a1" / "a2" … used for colouring


def S(d, w, role=None):
    return {"k": "s", "d": d, "w": w, "role": role}


def C(x, y, r, role=None):
    return {"k": "c", "x": x, "y": y, "r": r, "role": role}


def F(d, role=None):
    return {"k": "f", "d": d, "role": role}


def ring(cx, cy, r):
    return (f"M{n(cx - r)} {n(cy)}A{n(r)} {n(r)} 0 1 1 {n(cx + r)} {n(cy)}"
            f"A{n(r)} {n(r)} 0 1 1 {n(cx - r)} {n(cy)}")


def move(shapes, dx=0, dy=0, s=1.0):
    """translate + uniform scale a shape list (returns new list)."""
    out = []
    for sh in shapes:
        sh = dict(sh)
        if sh["k"] == "c":
            sh["x"], sh["y"], sh["r"] = sh["x"] * s + dx, sh["y"] * s + dy, sh["r"] * s
        else:
            sh["d"] = _xform_path(sh["d"], dx, dy, s)
            if sh["k"] == "s":
                sh["w"] = sh["w"] * s
        out.append(sh)
    return out


def _xform_path(d, dx, dy, s):
    """transform an absolute-command path (M L H V A Q C Z only)."""
    import re
    toks = re.findall(r"[MLHVAQCZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            out.append(t)
            i += 1
            if cmd == "Z":
                continue
        if cmd in ("M", "L"):
            x, y = float(toks[i]), float(toks[i + 1]); i += 2
            out.append(f"{n(x * s + dx)} {n(y * s + dy)}")
        elif cmd == "H":
            out.append(n(float(toks[i]) * s + dx)); i += 1
        elif cmd == "V":
            out.append(n(float(toks[i]) * s + dy)); i += 1
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]; i += 7
            out.append(f"{n(float(rx) * s)} {n(float(ry) * s)} {rot} {la} {sw} "
                       f"{n(float(x) * s + dx)} {n(float(y) * s + dy)}")
        elif cmd == "Q":
            v = [float(t) for t in toks[i:i + 4]]; i += 4
            out.append(" ".join(n(v[j] * s + (dx if j % 2 == 0 else dy)) for j in range(4)))
        elif cmd == "C":
            v = [float(t) for t in toks[i:i + 6]]; i += 6
            out.append(" ".join(n(v[j] * s + (dx if j % 2 == 0 else dy)) for j in range(6)))
        elif cmd == "Z":
            pass
    return "".join(out).replace("M", "M").strip()


def bbox(shapes):
    """approximate bbox (stroke aware; arcs sampled crudely via endpoints + radii)."""
    xs, ys = [], []
    import re
    for sh in shapes:
        if sh["k"] == "c":
            xs += [sh["x"] - sh["r"], sh["x"] + sh["r"]]
            ys += [sh["y"] - sh["r"], sh["y"] + sh["r"]]
            continue
        hw = sh.get("w", 0) / 2 if sh["k"] == "s" else 0
        pts = _sample(sh["d"])
        for x, y in pts:
            xs += [x - hw, x + hw]
            ys += [y - hw, y + hw]
    return min(xs), min(ys), max(xs), max(ys)


def _sample(d):
    """sample points along an absolute path (good enough for bboxes)."""
    import re
    toks = re.findall(r"[MLHVAQCZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    pts, i, cmd, cx, cy, sx, sy = [], 0, None, 0, 0, 0, 0
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd == "Z":
                cx, cy = sx, sy
                continue
        if cmd == "M":
            cx, cy = float(toks[i]), float(toks[i + 1]); i += 2; sx, sy = cx, cy; pts.append((cx, cy))
        elif cmd == "L":
            cx, cy = float(toks[i]), float(toks[i + 1]); i += 2; pts.append((cx, cy))
        elif cmd == "H":
            cx = float(toks[i]); i += 1; pts.append((cx, cy))
        elif cmd == "V":
            cy = float(toks[i]); i += 1; pts.append((cx, cy))
        elif cmd == "Q":
            x1, y1, x, y = map(float, toks[i:i + 4]); i += 4
            for k in range(1, 11):
                u = k / 10
                pts.append(((1 - u) ** 2 * cx + 2 * (1 - u) * u * x1 + u * u * x,
                            (1 - u) ** 2 * cy + 2 * (1 - u) * u * y1 + u * u * y))
            cx, cy = x, y
        elif cmd == "C":
            x1, y1, x2, y2, x, y = map(float, toks[i:i + 6]); i += 6
            for k in range(1, 11):
                u = k / 10
                a, b, c_, d_ = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3
                pts.append((a * cx + b * x1 + c_ * x2 + d_ * x, a * cy + b * y1 + c_ * y2 + d_ * y))
            cx, cy = x, y
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]; i += 7
            pts += _arc_pts(cx, cy, float(rx), int(la), int(sw), float(x), float(y))
            cx, cy = float(x), float(y)
    return pts


def _arc_pts(x1, y1, r, la, sw, x2, y2):
    # circle arc endpoint → centre parameterisation
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    d2 = dx * dx + dy * dy
    if d2 == 0:
        return []
    r = max(r, math.sqrt(d2))
    f = math.sqrt(max(r * r - d2, 0) / d2)
    if la == sw:
        f = -f
    cxp, cyp = f * dy, -f * dx
    cx, cy = cxp + (x1 + x2) / 2, cyp + (y1 + y2) / 2
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    da = a2 - a1
    if sw and da < 0:
        da += 2 * math.pi
    if not sw and da > 0:
        da -= 2 * math.pi
    return [(cx + r * math.cos(a1 + da * k / 24), cy + r * math.sin(a1 + da * k / 24)) for k in range(25)]


# ───────────────────────────── rendering ─────────────────────────────

def render(shapes, colors, cap="butt", join="miter"):
    """colors: dict role → colour (key None = default)."""
    out = []
    for sh in shapes:
        col = colors.get(sh.get("role"), colors[None])
        if sh["k"] == "c":
            out.append(f'<circle cx="{n(sh["x"])}" cy="{n(sh["y"])}" r="{n(sh["r"])}" fill="{col}"/>')
        elif sh["k"] == "f":
            out.append(f'<path d="{sh["d"]}" fill="{col}"/>')
        else:
            out.append(f'<path d="{sh["d"]}" fill="none" stroke="{col}" stroke-width="{n(sh["w"])}" '
                       f'stroke-linecap="{sh.get("cap", cap)}" stroke-linejoin="{join}" stroke-miterlimit="10"/>')
    return "".join(out)


def svg_doc(inner, box, bg=None, pad=0, width=None):
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    w, h = x1 - x0, y1 - y0
    wa = f' width="{n(width)}" height="{n(width * h / w)}"' if width else ""
    bgr = f'<rect x="{n(x0)}" y="{n(y0)}" width="{n(w)}" height="{n(h)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(x0)} {n(y0)} {n(w)} {n(h)}"{wa}>'
            f'{bgr}{inner}</svg>')
