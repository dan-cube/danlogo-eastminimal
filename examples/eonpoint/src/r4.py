"""Round 4 — the two keepers, H1 相切 and H3 句点, as one system: 一实一空.

Two kinds of point, one line weight:
  实 • the solid point  — the English full stop, the point that is touched (触点)
  空 ○ the hollow circle — the Chinese 句号, the vessel that holds 亿 points
H1 puts the solid point inside the hollow circle (合);  H3 lets each close its own language (分).
Letters, Chinese strokes and marks are all built from the same three things: a line, a circle, a point.
"""
import math, os
from ep import *
from latin import Face
import hanzi, lockup as lk

ENJI = "#8E1B2A"     # 胭脂
SHU = "#C9413A"      # 朱 — the point on dark grounds
SUMI = "#231F1C"     # 墨
WASHI = "#F5F2EC"    # 和纸
STONE = "#8C857C"
EMB = "#E9E4DB"      # blind-emboss tone

LW = 6.2             # THE line weight (absolute, at cap height 100) shared by every element


# ───────── type ─────────
def face_upper():
    return Face(H=100, X=72, W=LW, case="upper", sb_straight=24, sb_round=18, track=34)


def face_title():
    return Face(H=100, X=72, W=LW, case="title", sb_straight=15, sb_round=9.5, track=6, idot=1.4,
                accent_dot=False, n_w=0.9 * 72)


def cn(size=52, track=30, W_abs=LW * 0.68):
    """亿触点 with the same line (≈ 0.68 of the Latin stroke — Chinese is denser)."""
    sh, w = hanzi.name_cn(W=W_abs / size * 100, size=size, track=track, accent_dots=False)
    return sh, w


def set_with(face, text, extra):
    """Face.set, but extra(i, x) may return shapes to add at glyph i (origin = glyph left)."""
    shapes, x, prev = [], 0, None
    for i, ch in enumerate(text):
        sh, w, L, R = face.glyph(ch)
        if prev is not None:
            x += face.side(prev) + face.side(L) + face.track
        shapes += move(sh, x, 0)
        add = extra(i, ch, x, w)
        if add:
            shapes += add
        x += w
        prev = R
    return shapes, x


# ───────── H1 相切 ─────────
K_POINT = 0.24       # point ⌀ / circle ⌀


def mark_H1(D=100, lw=None):
    lw = lw if lw is not None else D * 0.031
    R = D / 2
    r = D * K_POINT / 2
    inner = R - lw
    sh = [S(ring(R, R, R - lw / 2), lw, "line"), C(R, R + inner - r, r, "point")]
    return sh, (D, D)


def logotype_H1(point=True):
    """EONPOINT — the O of POINT is the mark at letter size (same circle, same line, same point)."""
    f = face_upper()

    def extra(i, ch, x, w):
        if point and i == 4:
            D = f.H + 2 * f.os
            inner = D / 2 - f.W
            r = D * K_POINT / 2
            return [C(x + D / 2, -f.H / 2 + inner - r, r, "point")]
    return set_with(f, "EONPOINT", extra)


def H1_stacked(mark_h=200):
    en, w = logotype_H1(point=False)
    m, _ = mark_H1(D=mark_h, lw=LW)
    c, cw = cn(52, track=46)
    return move(m, w / 2 - mark_h / 2, -100 - 96 - mark_h) + en + move(c, w / 2 - cw / 2, 60)


def H1_horizontal():
    en, w = logotype_H1(point=False)
    c, cw = cn(46, track=40)
    block = 100 + 52 + 46 * 0.97
    m, _ = mark_H1(D=block, lw=LW)
    return move(m, 0, -100) + move(en + move(c, 0, 52), block + 72, 0)


def H1_single():
    en, w = logotype_H1(point=False)
    m, _ = mark_H1(D=130, lw=LW)
    c, cw = cn(78, track=16)
    return move(m, 0, -115) + move(en, 130 + 64, 0) + [S(f"M{n(130 + 64 + w + 56)} -100V0", LW * 0.6, "line")] + \
        move(c, 130 + 64 + w + 112, -78 * 0.95)


def H1_logotype_cn():
    en, w = logotype_H1(point=True)
    c, cw = cn(46, track=40)
    return en + move(c, 0, 52)


# ───────── H3 句点 ─────────
P_D = 20             # solid point ⌀ = hollow 。 ⌀  (absolute, cap 100)


def logotype_H3():
    f = face_title()
    sh, w = f.set("EonPoint")
    gap = f.sb_s * 0.9 + f.track
    sh.append(C(w + gap + P_D / 2, -P_D / 2, P_D / 2, "point"))
    return sh, w + gap + P_D, (w + gap + P_D / 2)


def cn_H3(size=52, track=30):
    c, cw = cn(size, track=track)
    lw = LW * 0.68
    cx = cw + size * 0.12 + P_D / 2
    cy = size * 0.93 - P_D / 2
    c.append(S(ring(cx, cy, P_D / 2 - lw / 2), lw, "point"))
    return c, cx + P_D / 2, cx


def H3_horizontal(align="left"):
    en, w, ex = logotype_H3()
    c, cw, cx = cn_H3()
    dx = 0 if align == "left" else ex - cx          # right: 。 sits exactly under .
    return en + move(c, dx, 58)


def H3_stacked():
    en, w, ex = logotype_H3()
    c, cw, cx = cn_H3(track=40)
    return en + move(c, w / 2 - cw / 2, 64)


def H3_single():
    en, w, ex = logotype_H3()
    c, cw, cx = cn_H3(80, track=14)
    return en + move(c, w + 96, -80 * 0.93)


def symbol_H3(d=100, gap=0.62, lw_k=0.2):
    """• ○ — the two points of the two languages, same size, one solid, one hollow."""
    lw = d * lw_k
    return [C(d / 2, d / 2, d / 2, "point"), S(ring(d * 1.5 + gap * d, d / 2, d / 2 - lw / 2), lw, "point")], \
        (2 * d + gap * d, d)


# ───────── colourways ─────────
CW = {
    "color":   ({None: SUMI, "line": SUMI, "point": ENJI}, None),
    "reverse": ({None: WASHI, "line": WASHI, "point": SHU}, SUMI),
    "enji":    ({None: WASHI, "line": WASHI, "point": WASHI}, ENJI),
    "black":   ({None: SUMI, "line": SUMI, "point": SUMI}, None),
    "white":   ({None: WASHI, "line": WASHI, "point": WASHI}, SUMI),
    "emboss":  ({None: EMB, "line": EMB, "point": ENJI}, None),
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg_r4")


def _save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)


def save_cw(name, shapes, pad=30, ways=CW):
    for k, (cols, bg) in ways.items():
        _save(f"{name}-{k}", lk.doc(shapes, cols, pad=pad))      # grounds are painted by the page


def icon(shapes, bg, cols, scale=0.56, size=1024, dy=0.0, round_=True):
    x0, y0, x1, y1 = bbox(shapes)
    w, h = x1 - x0, y1 - y0
    s = size * scale / max(w, h)
    sh = move(shapes, -x0 * s + size / 2 - w * s / 2, -y0 * s + size / 2 - h * s / 2 + dy * size, s)
    shape = (f'<rect width="{size}" height="{size}" rx="{n(size * 0.225)}" fill="{bg}"/>' if round_
             else f'<circle cx="{size / 2}" cy="{size / 2}" r="{size / 2}" fill="{bg}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{shape}{render(sh, cols)}</svg>')


def H3_standard():
    """EonPoint. over 亿触点。 — right-aligned on one vertical axis: the hollow 。 sits exactly under the solid full stop."""
    en, w, ex = logotype_H3()
    c, cw, cx = cn_H3(56, track=16)
    return en + move(c, ex - cx, 60)


# ───────── construction & motion ─────────
G = "#B3AA9F"


def _g(d, dash=False, w=0.7, col=G):
    da = ' stroke-dasharray="3 3"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{n(w)}"{da}/>'


def cons_H1():
    D = 300
    sh, _ = mark_H1(D=D, lw=D * 0.031)
    R, r = D / 2, D * K_POINT / 2
    lw = D * 0.031
    g = [_g(ring(R, R, R), dash=True), _g(ring(R, R, R - lw), dash=True),
         _g(f"M-40 {R}H{D + 40}M{R} -40V{D + 40}", dash=True)]
    cy = R + (R - lw) - r
    g.append(_g(ring(R, cy, r + 8), col="#C9413A", w=1))           # the point's own orbit
    g.append(_g(f"M{R - 26} {D - lw}H{R + 26}", col="#C9413A", w=1.4))  # the single tangent point
    g.append(_g(f"M{D + 30} 0V{D}M{D + 22} 0H{D + 38}M{D + 22} {D}H{D + 38}"))   # D
    g.append(_g(f"M{-30} {cy - r}V{cy + r}M{-38} {cy - r}H{-22}M{-38} {cy + r}H{-22}"))  # d
    return svg_doc("".join(g) + render(sh, CW["color"][0]), (-60, -60, D + 60, D + 60))


def cons_H3():
    f = face_title()
    sh = H3_standard()
    x0, y0, x1, y1 = bbox(sh)
    en, w, ex = logotype_H3()
    g = [_g(f"M{x0 - 30} 0H{x1 + 30}"), _g(f"M{x0 - 30} -100H{x1 + 30}", dash=True),
         _g(f"M{x0 - 30} -72H{x1 + 30}", dash=True),
         _g(f"M{ex} -60V{y1 + 20}", col="#C9413A", w=1)]
    return svg_doc("".join(g) + render(sh, CW["color"][0]), (x0 - 40, -130, x1 + 40, y1 + 30))


def motion_H1(phase):
    """the point travels inside the circle while the agent 'thinks', then comes to rest at the bottom."""
    D = 300
    R, r, lw = D / 2, D * K_POINT / 2, D * 0.031
    path_r = R - lw - r
    end = {0: -90, 1: 20, 2: 90}[phase]
    sh = [S(ring(R, R, R - lw / 2), lw, "line")]
    ghosts = []
    if phase < 2:
        for k in range(1, 5):
            a = math.radians(end - k * 19)
            ghosts.append(C(R + path_r * math.cos(a), R + path_r * math.sin(a), r * (0.8 - k * 0.14), "ghost"))
    a = math.radians(end)
    sh += ghosts[::-1] + [C(R + path_r * math.cos(a), R + path_r * math.sin(a), r, "point")]
    return svg_doc(render(sh, {**CW["color"][0], "ghost": "#E9DCD9"}), (-20, -20, D + 20, D + 20))


def motion_H3(phase):
    """a cursor types 'EonPoint', then folds into the full stop."""
    f = face_title()
    sh, w = f.set("EonPoint")
    gap = f.sb_s * 0.9 + f.track
    cx = w + gap + P_D / 2
    if phase == 0:
        sh.append(S(f"M{cx} {-100}V{8}", 4.5, "point"))
    elif phase == 1:
        sh.append(S(f"M{cx} {-46}V{0}", 9, "point"))
    else:
        sh.append(C(cx, -P_D / 2, P_D / 2, "point"))
    return svg_doc(render(sh, CW["color"][0]), (-20, -130, w + gap + P_D + 30, 30))


def build():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    # H1
    save_cw("H1-mark", mark_H1(D=100, lw=3.1)[0], pad=3)
    save_cw("H1-stacked", H1_stacked())
    save_cw("H1-horizontal", H1_horizontal())
    save_cw("H1-single", H1_single())
    save_cw("H1-logotype", logotype_H1()[0])
    save_cw("H1-logotype-cn", H1_logotype_cn())
    m, _ = mark_H1(D=100, lw=4.2)
    _save("H1-icon", icon(m, WASHI, CW["color"][0], scale=0.58))
    _save("H1-icon-dark", icon(m, SUMI, CW["reverse"][0], scale=0.58))
    _save("H1-avatar", icon(m, WASHI, CW["color"][0], scale=0.56, round_=False))
    _save("H1-construction", cons_H1())
    for p in range(3):
        _save(f"H1-motion-{p}", motion_H1(p))
    # H3
    save_cw("H3-standard", H3_standard())
    save_cw("H3-stacked", H3_stacked())
    save_cw("H3-single", H3_single())
    save_cw("H3-logotype", logotype_H3()[0])
    save_cw("H3-symbol", symbol_H3(lw_k=0.14, gap=0.5)[0], pad=4)
    f = face_title(); f.W = 9
    e, w, _, _ = f.g_E()
    e = e + [C(w + 16 + 11, -11, 11, "point")]
    _save("H3-icon", icon(e, WASHI, CW["color"][0], scale=0.46))
    _save("H3-icon-dark", icon(e, SUMI, CW["reverse"][0], scale=0.46))
    _save("H3-avatar", icon(e, WASHI, CW["color"][0], scale=0.44, round_=False))
    _save("H3-construction", cons_H3())
    for p in range(3):
        _save(f"H3-motion-{p}", motion_H3(p))
    print("ok")


if __name__ == "__main__":
    build()


def build_emboss_layers():
    hi = {k: "#FFFFFF" for k in (None, "line", "point")}
    lo = {k: "#CEC6BA" for k in (None, "line", "point")}
    m = mark_H1(D=100, lw=3.1)[0]
    _save("H1-mark-hi", lk.doc(m, hi, pad=3)); _save("H1-mark-lo", lk.doc(m, lo, pad=3))
    s = H3_standard()
    _save("H3-standard-hi", lk.doc(s, hi, pad=30)); _save("H3-standard-lo", lk.doc(s, lo, pad=30))


if __name__ == "__main__":
    build_emboss_layers()
