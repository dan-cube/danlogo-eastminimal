"""亿触点 — monoline construction on a 100 × 100 body (y down).

Every 点-stroke (the dot in 虫, the four dots of 灬) is a true circle: the brand point,
so the Chinese name carries the symbol's idea instead of sitting under it as a caption.
"""
import math
from ep import S, C, n, move


def _fillet(a, c, b, d):
    """polyline a → c → b with corner c rounded over distance d (quadratic)."""
    def towards(p, q, dist):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        return (p[0] + (q[0] - p[0]) * dist / L, p[1] + (q[1] - p[1]) * dist / L)
    p1, p2 = towards(c, a, d), towards(c, b, d)
    return f"L{n(p1[0])} {n(p1[1])}Q{n(c[0])} {n(c[1])} {n(p2[0])} {n(p2[1])}"


def yi(W, dot=1.0):
    sh = []
    # 亻
    sh.append(S("M30 3L6.5 45", W))
    t = (30 - 19) / 23.5
    sh.append(S(f"M19 {n(3 + 42 * t)}V97", W))
    # 乙 — 横 · 折 · 弯 · 钩
    d = "M39 14H86" + _fillet((86, 14), (40, 89), (93, 89), 15) + "H93V75"
    sh.append(S(d, W))
    return sh


def chu(W, dot=1.0):
    sh = []
    # 角 — ⺈
    sh.append(S("M23 2.5L10 21", W))
    sh.append(S("M16.5 11.5H36L29.5 22.5", W))
    # 角 — body
    sh.append(S("M8.5 28V73Q8.5 89 2.5 97", W))
    sh.append(S("M8.5 28H40.5V97", W))
    sh.append(S("M8.5 47.5H40.5M8.5 67H40.5", W))
    sh.append(S("M24.5 28V67", W))
    # 虫
    sh.append(S("M54 29H92V61H54Z", W))
    sh.append(S("M73 11V86", W))
    sh.append(S("M51 89.5H95", W))
    sh.append(C(89.5, 75.5, W * 0.72 * dot, "accent"))
    return sh


def dian(W, dot=1.0):
    sh = []
    sh.append(S("M47 2V35", W))
    sh.append(S("M47 18H80", W))
    sh.append(S("M21 35H80V63H21Z", W))
    r = W * 0.82 * dot
    for x in (14, 38, 62, 86):
        sh.append(C(x, 86, r, "accent"))
    return sh


GLYPHS = [yi, chu, dian]


def name_cn(W=7.5, size=100, track=12, dot=1.0, accent_dots=True):
    """亿触点 set left to right; returns shapes (top-left origin) and width."""
    out, x = [], 0
    for i, g in enumerate(GLYPHS):
        sh = g(W, dot)
        if not accent_dots:
            for s_ in sh:
                s_["role"] = None
        out += move(sh, x, 0)
        x += 100 + (track if i < 2 else 0)
    return move(out, 0, 0, size / 100), x * size / 100
