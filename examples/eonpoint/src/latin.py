"""Monoline geometric letters for EonPoint — only the glyphs the name needs.

Each glyph returns (shapes, ink_width, left_side, right_side) with the ink starting at x = 0,
baseline y = 0 (y grows downward, so the x-height sits at y = -X).
"""
import math
from ep import S, C, F, n, ring


class Face:
    def __init__(self, H=100, X=72, W=15, os=None, desc=None, tasc=None,
                 sb_straight=None, sb_round=None, track=0, n_w=None, e_open=38,
                 e_bar=0.5, idot=1.22, idot_gap=0.8, t_bar=(0.32, 0.42), o_wide=1.0,
                 cap_e=0.56, cap_p=0.58, case="lower", round_caps=False, accent_dot=True):
        self.H, self.X, self.W = H, X, W
        self.os = os if os is not None else 0.012 * H
        self.desc = desc if desc is not None else 0.30 * H
        self.tasc = tasc if tasc is not None else 0.30 * X
        self.sb_s = sb_straight if sb_straight is not None else 0.9 * W
        self.sb_r = sb_round if sb_round is not None else 0.55 * W
        self.track = track
        self.n_w = n_w if n_w is not None else 0.94 * X
        self.e_open, self.e_bar = e_open, e_bar
        self.idot, self.idot_gap = idot, idot_gap
        self.t_bar = t_bar
        self.o_wide = o_wide
        self.cap_e, self.cap_p = cap_e, cap_p
        self.case = case
        self.round_caps = round_caps
        self.accent_dot = accent_dot
        self.rc = W / 2 if round_caps else 0

    # ── lowercase ──
    def g_o(self):
        X, W, os = self.X, self.W, self.os
        D = X + 2 * os
        rx = D / 2 * self.o_wide - W / 2
        ry = D / 2 - W / 2
        cx, cy = D * self.o_wide / 2, -X / 2
        d = (f"M{n(cx - rx)} {n(cy)}A{n(rx)} {n(ry)} 0 1 1 {n(cx + rx)} {n(cy)}"
             f"A{n(rx)} {n(ry)} 0 1 1 {n(cx - rx)} {n(cy)}")
        return [S(d, W)], D * self.o_wide, "r", "r"

    def g_e(self):
        X, W, os = self.X, self.W, self.os
        D = X + 2 * os
        r = D / 2 - W / 2
        cx, cy = D / 2, -X * self.e_bar
        oy = -X / 2
        ep = getattr(self, "e_point", None)       # (clearance × W, ball ⌀ × W)
        if ep:
            # the Point sits in the aperture with the SAME clearance to the bar and to the stroke end
            gap, Rb = ep[0] * W, ep[1] * W / 2
            tb = math.asin((gap + Rb + W / 2 + cy - oy) / r)
            te = tb + math.asin((gap + Rb) / r) + (self.rc / r)
            ep = (math.degrees(te), math.degrees(tb), ep[1])
        a = math.radians(ep[0] if ep else self.e_open)
        ex, ey = cx + r * math.cos(a), oy + r * math.sin(a)
        # ring from the bar's right end, counter-clockwise (up first) to the aperture
        d = f"M{n(cx + r)} {n(oy)}A{n(r)} {n(r)} 0 1 0 {n(ex)} {n(ey)}"
        if ep:
            # bar end follows the outer contour, so no square nub pokes out of the bowl
            Ro = r + W / 2
            xt = cx + math.sqrt(Ro * Ro - (cy - W / 2 - oy) ** 2)
            xb = cx + math.sqrt(Ro * Ro - (cy + W / 2 - oy) ** 2)
            bar_sh = F(f"M{n(cx - r)} {n(cy - W / 2)}H{n(xt)}A{n(Ro)} {n(Ro)} 0 0 1 {n(xb)} {n(cy + W / 2)}"
                       f"H{n(cx - r)}Z")
        else:
            bar_sh = S(f"M{n(cx - r)} {n(cy)}H{n(cx + r + W / 2)}", W)
        sh = [S(d, W), bar_sh]
        if ep:
            b = math.radians(ep[1])
            sh.append(C(cx + r * math.cos(b), oy + r * math.sin(b), W * ep[2] / 2, "point"))
        if self.round_caps:
            sh[0]["cap"] = "round"
            sh[1]["cap"] = "butt"
        return sh, D, "r", "r"

    def g_n(self):
        X, W, os = self.X, self.W, self.os
        xs = W / 2
        ra = (self.n_w - W) / 2
        xr = xs + 2 * ra
        yc = -X - os + W / 2 + ra
        rc = self.rc
        stem = f"M{n(xs)} {n(-X + rc)}V{n(-rc)}"
        arch = f"M{n(xs)} {n(yc)}A{n(ra)} {n(ra)} 0 0 1 {n(xr)} {n(yc)}V{n(-rc)}"
        return [S(stem, W), S(arch, W)], self.n_w, "s", "s"

    def g_p(self):
        X, W, os = self.X, self.W, self.os
        D = X + 2 * os
        r = D / 2 - W / 2
        xs = W / 2
        stem = f"M{n(xs)} {n(-X + self.rc)}V{n(self.desc - self.rc)}"
        bowl = ring(xs + r, -X / 2, r)
        return [S(stem, W), S(bowl, W)], W + 2 * r, "s", "r"

    def g_i(self):
        X, W = self.X, self.W
        xs = W / 2
        rd = W * self.idot / 2
        yd = -X - self.idot_gap * W - rd
        sh = [S(f"M{n(xs)} {n(-X + self.rc)}V{n(-self.rc)}", W), C(xs, yd, rd, "accent" if self.accent_dot else None)]
        return sh, W, "s", "s"

    def g_t(self):
        X, W = self.X, self.W
        l, r = self.t_bar
        xs = l * X
        top = -X - self.tasc
        rc = self.rc
        stem = f"M{n(xs)} {n(top + rc)}V{n(-rc)}"
        bar = f"M{n(rc)} {n(-X + W / 2)}H{n(xs + r * X - rc)}"
        return [S(stem, W), S(bar, W)], xs + r * X, "t", "t"

    # ── capitals ──
    def g_E(self):
        H, W = self.H, self.W
        w = self.cap_e * H
        xs = W / 2
        d = (f"M{n(w)} {n(-H + W / 2)}H{n(xs)}V{n(-W / 2)}H{n(w)}"
             f"M{n(xs)} {n(-H / 2)}H{n(w * 0.92)}")
        return [S(d, W)], w, "s", "o"

    def g_P(self):
        H, W = self.H, self.W
        xs = W / 2
        bh = self.cap_p * H          # outer bowl height
        rb = (bh - W) / 2
        bw = self.cap_p * H * 1.0    # outer bowl width
        xb = bw - W / 2 - rb
        yt = -H + W / 2
        d = (f"M{n(xs)} {n(0)}V{n(yt)}H{n(xb)}A{n(rb)} {n(rb)} 0 0 1 {n(xb)} {n(yt + 2 * rb)}H{n(xs)}")
        return [S(d, W)], bw, "s", "r"

    def g_O(self):
        H, W, os = self.H, self.W, self.os
        D = H + 2 * os
        r = D / 2 - W / 2
        return [S(ring(D / 2, -H / 2, r), W)], D, "r", "r"

    def g_I(self):
        W = self.W
        return [S(f"M{n(W / 2)} {n(-self.H)}V0", W)], W, "s", "s"

    def g_N(self):
        H, W = self.H, self.W
        w = 0.78 * H
        # diagonal as a parallelogram with perpendicular thickness ≈ W
        wd = W
        for _ in range(20):
            run = w - wd
            t = wd * H / math.hypot(H, run)
            wd *= W * 1.02 / t
        dg = (f"M0 {n(-H)}H{n(wd)}L{n(w)} 0H{n(w - wd)}Z")
        stems = f"M{n(W / 2)} 0V{n(-H)}M{n(w - W / 2)} 0V{n(-H)}"
        return [S(stems, W), F(dg)], w, "s", "s"

    def g_T(self):
        H, W = self.H, self.W
        w = 0.66 * H
        d = f"M0 {n(-H + W / 2)}H{n(w)}M{n(w / 2)} {n(-H)}V0"
        return [S(d, W)], w, "o", "o"

    # ── setting ──
    def glyph(self, ch):
        return getattr(self, "g_" + ch)()

    def side(self, kind):
        return {"s": self.sb_s, "r": self.sb_r, "o": self.sb_r * 0.35, "t": self.sb_r * 0.55}[kind]

    def set(self, text, kern=None):
        """returns shapes (ink from x = 0) and total ink width."""
        kern = kern or {}
        shapes, x, prev = [], 0, None
        from ep import move
        for i, ch in enumerate(text):
            sh, w, L, R = self.glyph(ch)
            if prev is not None:
                pR, pch = prev
                x += self.side(pR) + self.side(L) + self.track + kern.get(pch + ch, 0)
            shapes += move(sh, x, 0)
            x += w
            prev = (R, ch)
        if self.round_caps:
            for s_ in shapes:
                if s_["k"] == "s" and "cap" not in s_:
                    s_["cap"] = "round"
        return shapes, x
