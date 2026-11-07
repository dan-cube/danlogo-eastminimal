"""Lockups: symbol + EonPoint + 亿触点, built on one grid per proposal."""
from ep import move, bbox, render, svg_doc
import hanzi


def wordmark(face, text, kern=None):
    sh, w = face.set(text, kern)
    return sh, w


def horizontal(sym, face, text, cn, kern=None, sym_h=None, gap_sym=None, cn_gap=None,
               cn_em=None, cn_track=None, cn_w=None, sym_valign="block"):
    """symbol | EN over CN.  Units: EN cap (or x-height for lower case) = face metric.
    returns shapes and tight box."""
    en, en_w = wordmark(face, text, kern)
    top_metric = face.H if face.case != "lower" else face.X
    # EN ink top (cap top / x-height); i-dot and ascenders may rise above — fine.
    cn_em = cn_em or 0.46 * top_metric
    cn_gap = cn_gap if cn_gap is not None else 0.34 * top_metric
    cn_sh, cn_wd = hanzi.name_cn(W=cn_w or 9, size=cn_em, track=cn_track if cn_track is not None else 30)
    desc = face.desc if (face.case == "lower" and "p" in text) else 0
    cn_y = max(desc, 0) + cn_gap if face.case == "lower" else cn_gap
    cn_sh = move(cn_sh, 0, cn_y)
    block_top = -top_metric
    block_bot = cn_y + cn_em * 0.97
    s_sh, (sw, sh_h) = sym
    H = sym_h or (block_bot - block_top)
    sc = H / sh_h
    gap_sym = gap_sym if gap_sym is not None else 0.42 * top_metric
    sym_y = block_top + ((block_bot - block_top) - H) / 2 if sym_valign == "block" else -top_metric
    s2 = move(s_sh, 0, sym_y, sc)
    x_text = sw * sc + gap_sym
    shapes = s2 + move(en, x_text, 0) + move(cn_sh, x_text, 0)
    return shapes


def single_line(sym, face, text, cn, kern=None, sym_h=None, gap_sym=None, cn_em=None,
                cn_track=None, cn_w=None, rule=True, rule_w=None, gap_rule=None):
    """symbol | EN | 亿触点 on one line (CN vertically centred on the EN body)."""
    from ep import S, n
    en, en_w = wordmark(face, text, kern)
    top_metric = face.H if face.case != "lower" else face.X
    cn_em = cn_em or 0.78 * top_metric
    cn_sh, cn_wd = hanzi.name_cn(W=cn_w or 9, size=cn_em, track=cn_track if cn_track is not None else 12)
    s_sh, (sw, sh_h) = sym
    H = sym_h or top_metric * 1.25
    sc = H / sh_h
    gap_sym = gap_sym if gap_sym is not None else 0.4 * top_metric
    sym_y = -top_metric / 2 - H / 2
    out = move(s_sh, 0, sym_y, sc)
    x = sw * sc + gap_sym
    out += move(en, x, 0)
    x += en_w
    gap_rule = gap_rule if gap_rule is not None else 0.42 * top_metric
    if rule:
        rw = rule_w or face.W * 0.42
        x += gap_rule
        out.append(S(f"M{n(x)} {n(-top_metric * 1.0)}V{n(top_metric * 0.0)}", rw, "rule"))
        x += gap_rule
    else:
        x += gap_rule * 1.4
    out += move(cn_sh, x, -top_metric / 2 - cn_em * 0.5)
    return out


def stacked(sym, face, text, cn, kern=None, sym_h=None, gap1=None, gap2=None, cn_em=None,
            cn_track=None, cn_w=None):
    """symbol centred above EN, CN centred below."""
    en, en_w = wordmark(face, text, kern)
    top_metric = face.H if face.case != "lower" else face.X
    s_sh, (sw, sh_h) = sym
    H = sym_h or top_metric * 2.4
    sc = H / sh_h
    gap1 = gap1 if gap1 is not None else 0.75 * top_metric
    cn_em = cn_em or 0.5 * top_metric
    cn_sh, cn_wd = hanzi.name_cn(W=cn_w or 9, size=cn_em, track=cn_track if cn_track is not None else 40)
    desc = face.desc if (face.case == "lower" and "p" in text) else 0
    gap2 = gap2 if gap2 is not None else 0.36 * top_metric + desc
    out = move(s_sh, en_w / 2 - sw * sc / 2, -top_metric - gap1 - H, sc)
    out += en
    out += move(cn_sh, en_w / 2 - cn_wd / 2, gap2)
    return out


def doc(shapes, colors, pad=40, bg=None, cap="butt", width=None, square=False):
    x0, y0, x1, y1 = bbox(shapes)
    if square:
        cx, cy, m = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / 2
        x0, y0, x1, y1 = cx - m, cy - m, cx + m, cy + m
    return svg_doc(render(shapes, colors, cap=cap), (x0, y0, x1, y1), bg=bg, pad=pad, width=width)
