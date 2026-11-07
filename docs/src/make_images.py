"""make_images.py — 生成 README 用的说明图（docs/images/*.png）

用法：在仓库根目录运行  python3 docs/src/make_images.py
只依赖 Python 标准库；PNG 由 scripts/render.sh 渲染，审看板由 scripts/review.py 生成。
案例图全部来自 EonPoint 亿触点「一实一空」的真实过程与成稿（docs/src/eonpoint/，只用品牌名）。
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "images")
SRC = os.path.join(ROOT, "docs", "src")
SCRIPTS = os.path.join(ROOT, "scripts")

PAPER = "#F5F2EC"
SUMI = "#231F1C"
GREY = "#6B6560"
MUTE = "#9A938B"
RULE = "#D9D3CA"
SHU = "#C9413A"
CARD = "#FBF9F5"
FONT = "PingFang SC, Helvetica Neue, Helvetica, Arial, sans-serif"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, color=SUMI, weight=400, anchor="start", spacing=0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{ls}>{esc(s)}</text>')


def doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>{"".join(body)}</svg>')


def save(name, w, h, body):
    svg = os.path.join(OUT, name + ".svg")
    open(svg, "w", encoding="utf-8").write(doc(w, h, body))
    subprocess.run([os.path.join(SCRIPTS, "render.sh"), svg, str(w), os.path.join(OUT, name + ".png")],
                   check=True, stdout=subprocess.DEVNULL)
    os.remove(svg)


STAGES = [
    ("1", "简报", "Brief", "一页简报卡 · brief card"),
    ("2", "概念", "Concepts", "每轮 5 个 + 黑白速写 · 5 per round, with sketches"),
    ("3", "原型", "Prototypes", "≥3 个 + 审看板 · ≥3 each + review board"),
    ("4", "精修", "Refine", "构造 + 小尺寸版 · construction, small size"),
    ("5", "定稿", "Finalize", "定制字 + 配色 · custom lettering + colour"),
    ("6", "体系", "System", "组合、变色、规范 · lockups, colourways, rules"),
    ("7", "场景", "Scenes", "6–10 个场景示意 · 6–10 mock-ups"),
    ("8", "提案", "Proposal", "提报文档 + 讲稿 · deck + speaker notes"),
    ("9", "总结", "Retrospective", "沉淀进 skill · feed the skill"),
]


def hero():
    W, H = 1600, 600
    b = [text(120, 168, "DANLOGO", 22, MUTE, 500, spacing=6),
         f'<circle cx="284" cy="161" r="4" fill="{SHU}"/>',
         text(304, 168, "EAST MINIMAL", 22, MUTE, 500, spacing=6),
         text(114, 318, "东方极简", 128, SUMI, 300, spacing=8),
         text(120, 392, "Complete logo identity systems, the East-Asian minimalist way", 30, SUMI, 300),
         text(120, 452, "用最少的形，承载最深的意思；留出空间，让人自己完成理解。", 24, GREY, 300),
         text(120, 496, "The fewest forms, the deepest meaning — leaving room for the viewer to complete it.", 20, MUTE, 300),
         f'<rect x="1104" y="132" width="1.5" height="372" fill="{RULE}"/>',
         text(1150, 150, "NINE STAGES", 15, MUTE, 500, spacing=4)]
    for i, (n, zh, en, _) in enumerate(STAGES):
        y = 192 + i * 36
        b += [text(1150, y, n, 17, SHU if n == "1" else MUTE, 500),
              text(1180, y, zh, 19, SUMI, 400),
              text(1236, y, en, 17, GREY, 300)]
    b.append(text(1150, 532, "For AI tools · Claude, Codex and more", 15, MUTE, 400))
    save("hero", W, H, b)


def workflow():
    W, H = 1600, 800
    groups = [("想 · Think", STAGES[0:3]), ("做 · Make", STAGES[3:5]), ("交付 · Deliver", STAGES[5:9])]
    b = [text(80, 92, "九个阶段", 40, SUMI, 400), text(268, 92, "Nine stages", 30, GREY, 300),
         text(80, 134, "每个阶段都以你的确认结束；decisions.md 记下每一轮的方案、你的原话和决定。", 20, GREY, 300),
         text(80, 162, "Every stage ends with your sign-off; decisions.md records each round, your words and what was locked.", 17, MUTE, 300)]
    x0, colw, gap = 80, 452, 40
    for gi, (title, items) in enumerate(groups):
        x = x0 + gi * (colw + gap)
        b += [text(x, 226, title, 18, MUTE, 500, spacing=2),
              f'<rect x="{x}" y="240" width="{colw}" height="1.5" fill="{RULE}"/>']
        for i, (n, zh, en, out) in enumerate(items):
            y = 262 + i * 118
            b += [f'<rect x="{x}" y="{y}" width="{colw}" height="100" rx="6" fill="{CARD}" stroke="{RULE}"/>',
                  text(x + 24, y + 58, n, 40, SHU if n in ("2", "3") else SUMI, 300),
                  text(x + 78, y + 44, zh, 26, SUMI, 500), text(x + 78 + 60, y + 44, en, 20, GREY, 300),
                  text(x + 78, y + 76, out, 15, GREY, 300)]
        if gi < 2:
            ax = x + colw + 8
            b.append(f'<path d="M{ax} 300 L{ax + 22} 300 M{ax + 14} 292 L{ax + 22} 300 L{ax + 14} 308" '
                     f'stroke="{MUTE}" stroke-width="2" fill="none"/>')
    b += [text(80, 762, "红色的两步是本 skill 花力气最多的地方：发散母题，再把图解走成只属于这个品牌的图形。", 17, GREY, 300),
          text(1520, 762, "Most of the craft lives in stages 2–3.", 17, MUTE, 300, anchor="end")]
    save("workflow", W, H, b)


GENES = [
    ("少", "Less", "再删一个就不成立", "Remove one more and it fails"),
    ("空", "Void ↔ Solid", "实与空成对：白也是一个形", "Solid and void as a pair — the white is a shape too"),
    ("轻", "Light", "放下，而不是压下", "Set down, not pressed down"),
    ("准", "Precise", "每个比例都说得出来源", "Every proportion has a reason"),
    ("落定", "Settled", "刚刚停住的那一刻", "The moment just after motion"),
    ("字为题款", "Type as inscription", "字退一步，托住图形", "Lettering steps back and supports"),
    ("同源", "One hand", "图与字出自同一只手", "Mark and type share one hand"),
    ("色少有因", "Colour with reason", "颜色少，每一种都有理由", "Few colours, each explained"),
    ("可感", "Tangible", "压印、刻、织，在实物上更好", "Better embossed, cut, woven"),
]


def genes():
    W, H = 1600, 930
    b = [text(80, 92, "九条风格基因", 40, SUMI, 400), text(340, 92, "Nine style genes", 30, GREY, 300),
         text(80, 134, "规定气质与质量，不规定形状、颜色或工艺——每个品牌都长出自己的形。", 20, GREY, 300),
         text(80, 162, "They govern temperament and quality, never a shape, colour or technique.", 17, MUTE, 300)]
    cw, ch, gx, gy = 464, 222, 24, 24
    for i, (zh, en, dzh, den) in enumerate(GENES):
        r, c = divmod(i, 3)
        x, y = 80 + c * (cw + gx), 200 + r * (ch + gy)
        core = i == 1
        b += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="{CARD}" '
              f'stroke="{SHU if core else RULE}" stroke-width="{2 if core else 1}"/>',
              text(x + 28, y + 52, f"0{i + 1}", 16, SHU if core else MUTE, 500),
              text(x + 28, y + 118, zh, 52 if len(zh) <= 2 else 40, SUMI, 300),
              text(x + 28, y + 160, en, 20, GREY, 400),
              text(x + 28, y + 186, dzh, 16, SUMI, 300),
              text(x + 28, y + 208, den, 14, MUTE, 300)]
        if core:
            b.append(text(x + cw - 28, y + 52, "核心构成 · core relation", 14, SHU, 500, anchor="end"))
    save("genes", W, H, b)


GATES = [
    ("①", "首先是图形", "Graphic first", ["第一眼读成一个东西或画面，", "不是字、字母、标点或图标", "Reads as a thing, not a letter or icon",
                                       "有完整的外形和面", "A whole outline, real planes"]),
    ("②", "辨识度", "Distinctive", ["剪影与反白不撞常见图标", "Silhouette & reverse avoid common icons",
                                   "十字描述后重画一次，还是它", "Redraw from a 10-word description",
                                   "签名在 32 px 还看得见", "Signature survives 32 px"]),
    ("③", "风格", "Style", ["实与空成对；轻；落定", "Solid & void pair; light; settled",
                           "东方在哪里：只看形回答四问", "Where is the East? four questions",
                           "不靠加粗加满，也不拆成几根线", "Neither heavier nor thinner to cheat"]),
]


def gates():
    W, H = 1600, 640
    b = [text(80, 92, "三道关卡", 40, SUMI, 400), text(260, 92, "Three gates for every prototype", 30, GREY, 300),
         text(80, 134, "三关都过才算过；一个都不过时，AI 把最好的一个和失败原因一起交给你选。", 20, GREY, 300),
         text(80, 162, "A prototype passes only when all three hold — otherwise you get the best one and an honest trade-off.", 17, MUTE, 300)]
    cw = 456
    for i, (num, zh, en, lines) in enumerate(GATES):
        x, y = 80 + i * (cw + 36), 210
        b += [f'<rect x="{x}" y="{y}" width="{cw}" height="360" rx="6" fill="{CARD}" stroke="{RULE}"/>',
              text(x + 28, y + 62, num, 34, SHU, 300),
              text(x + 80, y + 60, zh, 30, SUMI, 500), text(x + 80, y + 92, en, 20, GREY, 300),
              f'<rect x="{x + 28}" y="{y + 118}" width="{cw - 56}" height="1" fill="{RULE}"/>']
        yy = y + 158
        if i == 0:
            b += [text(x + 28, yy, lines[0], 18, SUMI, 300), text(x + 28, yy + 28, lines[1], 18, SUMI, 300),
                  text(x + 28, yy + 54, lines[2], 15, MUTE, 300),
                  text(x + 28, yy + 104, lines[3], 18, SUMI, 300), text(x + 28, yy + 130, lines[4], 15, MUTE, 300)]
        else:
            for k in range(0, 6, 2):
                b += [text(x + 28, yy, lines[k], 18, SUMI, 300), text(x + 28, yy + 26, lines[k + 1], 15, MUTE, 300)]
                yy += 66
        if i < 2:
            ax = x + cw + 7
            b.append(f'<path d="M{ax} 390 L{ax + 22} 390 M{ax + 14} 382 L{ax + 22} 390 L{ax + 14} 398" '
                     f'stroke="{MUTE}" stroke-width="2" fill="none"/>')
    save("gates", W, H, b)


def social():
    """GitHub 仓库的社交预览图（1280×640），在仓库 Settings → Social preview 手动上传。"""
    W, H = 1280, 640
    b = [text(96, 168, "DANLOGO", 20, MUTE, 500, spacing=6),
         f'<circle cx="252" cy="161" r="4" fill="{SHU}"/>',
         text(270, 168, "EAST MINIMAL", 20, MUTE, 500, spacing=6),
         text(90, 330, "东方极简", 136, SUMI, 300, spacing=8),
         text(96, 410, "Complete logo identity systems, the East-Asian way", 32, SUMI, 300),
         text(96, 452, "for AI tools such as Claude & Codex · brief to delivery", 26, GREY, 300),
         f'<rect x="96" y="500" width="64" height="1.5" fill="{RULE}"/>',
         text(96, 548, "用最少的形，承载最深的意思", 24, GREY, 300)]
    save("social-preview", W, H, b)


def case():
    """真实案例：EonPoint 亿触点「一实一空」的最终方案与构造图（只用品牌名，不含企业全称）。"""
    import base64
    import tempfile
    img = os.path.join(ROOT, "cases", "eonpoint-yishiyikong", "images")
    tmp = tempfile.mkdtemp()

    def png(name, width):
        out = os.path.join(tmp, name + ".png")
        subprocess.run([os.path.join(SCRIPTS, "render.sh"), os.path.join(img, name + ".svg"), str(width), out],
                       check=True, stdout=subprocess.DEVNULL)
        return "data:image/png;base64," + base64.b64encode(open(out, "rb").read()).decode()

    W, H = 1600, 1180
    b = [text(80, 92, "真实案例", 40, SUMI, 400), text(250, 92, "A real case · EonPoint 亿触点「一实一空」", 30, GREY, 300),
         text(80, 134, "英文的句点是实——被触及的那一个点；中文的句号是空——能容纳亿万个点的圈。", 20, GREY, 300),
         text(80, 162, "The full stop is solid — the one point that is touched; the Chinese full stop is void — a ring that holds a hundred million.", 17, MUTE, 300)]
    cards = [("方案一 · 相切", "Tangent — a point inside the ring, touching it at one spot", "H1-stacked-color", 80, 200, 708, 470),
             ("方案二 · 句点", "Full stop — EonPoint. solid, 亿触点。void, on one vertical", "H3-standard-color", 812, 200, 708, 470),
             ("构造 · 相切", "Construction: one line width for mark and type", "H1-construction", 80, 694, 708, 400),
             ("构造 · 句点", "Construction: the dot and the ring share one axis", "H3-construction", 812, 694, 708, 400)]
    for zh, en, name, x, y, w, h in cards:
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{RULE}"/>')
        iw, ih = w - 120, h - 130
        b.append(f'<image x="{x + 60}" y="{y + 30}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid meet" '
                 f'href="{png(name, 1400)}"/>')
        b += [text(x + 28, y + h - 52, zh, 20, SUMI, 500), text(x + 28, y + h - 24, en, 15, MUTE, 300)]
    b.append(text(80, 1150, "这是本 skill 反向拆解的来源方案：只借方法，不借形式——新项目不复用它的点、圆、句号与关系。", 17, GREY, 300))
    save("case-eonpoint", W, H, b)


def embed(svg_path, width, bg=None):
    """把一个 SVG 渲染成 PNG，返回 data URI，用于拼进说明图。bg：先铺一层底色（反白、色底版本需要）。"""
    import base64
    import re
    import tempfile
    d = tempfile.mkdtemp()
    if bg:
        src = open(svg_path, encoding="utf-8").read()
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
        rect = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{bg}"/>'
        src = re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + rect, src, count=1)
        svg_path = os.path.join(d, "bg.svg")
        open(svg_path, "w", encoding="utf-8").write(src)
    out = os.path.join(d, "x.png")
    subprocess.run([os.path.join(SCRIPTS, "render.sh"), svg_path, str(width), out], check=True, stdout=subprocess.DEVNULL)
    return "data:image/png;base64," + base64.b64encode(open(out, "rb").read()).decode()


EP = os.path.join(SRC, "eonpoint")


def image(name, x, y, w, h, width=900, bg=None):
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" '
            f'href="{embed(os.path.join(EP, name + ".svg"), width, bg)}"/>')


ROUNDS = [
    ("第 1 轮", "Round 1", "三个方向 · three directions",
     [("A-app-icon", "A 裂变", False), ("B-app-icon", "B 星芒", False), ("C-app-icon", "C 点动成线", True)],
     "“深化反而更啰嗦繁琐……不要越变越复杂，反而越变越丑。”", "加层级、加点数，只会更像 AI 拼搭。",
     "More layers only looked more generated."),
    ("第 2 轮", "Round 2", "回到简单 · back to simple",
     [("r2-O4-app-icon", "一到四", False), ("r2-O6-app-icon", "一到六", False), ("r2-O8-app-icon", "一到八", False)],
     "“好像都不满意……”", "排整齐不等于高级：方向本身要换。",
     "Tidier is not better — the direction had to change."),
    ("第 3 轮", "Round 3", "重新认识点 · re-seeing the point",
     [("r3-H1-app-icon", "H1 相切", True), ("r3-H2-app-icon", "H2 盲点", False), ("r3-H3-app-icon", "H3 句点", True)],
     "“保留 H1 和 H3……图文要有同一套设计理念。”", "从“画一个点”转到“重新认识点”。",
     "From drawing a point to seeing it anew."),
]


def process():
    W, H = 1600, 1000
    b = [text(80, 92, "一个真实项目", 40, SUMI, 400), text(330, 92, "A real project · EonPoint 亿触点", 30, GREY, 300),
         text(80, 134, "第 2–4 阶段：概念、原型、精修。每一轮你说一句话，方向就跟着变——四轮之后收拢成「一实一空」。", 20, GREY, 300),
         text(80, 162, "Stages 2–4. Each round, one sentence of feedback changed the direction; after four rounds it became one idea.", 17, MUTE, 300)]
    colw, gap, top = 452, 40, 214
    for ci, (zh, en, sub, icons, quote, lesson, lesson_en) in enumerate(ROUNDS):
        x = 80 + ci * (colw + gap)
        b += [text(x, top, zh, 22, SUMI, 500), text(x + 82, top, en, 18, GREY, 300),
              text(x, top + 30, sub, 15, MUTE, 400),
              f'<rect x="{x}" y="{top + 46}" width="{colw}" height="1.5" fill="{RULE}"/>']
        s, g = 132, 28
        for k, (name, label, kept) in enumerate(icons):
            ix, iy = x + k * (s + g), top + 72
            if kept:
                b.append(f'<rect x="{ix - 6}" y="{iy - 6}" width="{s + 12}" height="{s + 12}" rx="30" fill="none" '
                         f'stroke="{SHU}" stroke-width="2.5"/>')
            b.append(image(name, ix, iy, s, s, 400, PAPER))
            b.append(text(ix + s / 2, iy + s + 34, label, 16, SUMI if kept else GREY, 500 if kept else 400, anchor="middle"))
            if kept:
                b.append(text(ix + s / 2, iy + s + 58, "保留 · kept", 13, SHU, 500, anchor="middle"))
        qy = top + 330
        b += [f'<rect x="{x}" y="{qy - 30}" width="3" height="64" fill="{SHU}"/>']
        lines = [quote[i:i + 21] for i in range(0, len(quote), 21)]
        for li, ln in enumerate(lines):
            b.append(text(x + 18, qy + li * 28, ln, 18, SUMI, 300))
        b += [text(x, qy + 96, lesson, 16, GREY, 400), text(x, qy + 122, lesson_en, 14, MUTE, 300)]
    # round 4: the final idea, full width
    y4 = 720
    b += [f'<rect x="80" y="{y4}" width="1440" height="230" rx="8" fill="#FFFFFF" stroke="{SHU}" stroke-width="2"/>',
          text(112, y4 + 48, "第 4 轮", 22, SUMI, 500), text(196, y4 + 48, "Round 4 · 一实一空 one solid, one void", 18, GREY, 300),
          text(112, y4 + 92, "“我很喜欢这套设计思路。”", 20, SUMI, 300),
          text(112, y4 + 128, "英文句点是实，中文句号是空；一根线宽贯穿图形与中英文。", 16, GREY, 400),
          text(112, y4 + 154, "The full stop is solid, the Chinese full stop is void; one line width runs", 14, MUTE, 300),
          text(112, y4 + 176, "through the mark and both scripts.", 14, MUTE, 300),
          image("H1-icon", 820, y4 + 30, 170, 170, 500, "#FFFFFF"),
          image("H3-standard-color", 1030, y4 + 40, 460, 150, 1200)]
    save("process-eonpoint", W, H, b)


def system():
    W, H = 1600, 1000
    b = [text(80, 92, "成稿与体系", 40, SUMI, 400), text(300, 92, "Final system · EonPoint 亿触点", 30, GREY, 300),
         text(80, 134, "第 5–7 阶段：定制中英文字、配色、组合、反白、盲压、图标与动态。全部由代码生成，改一个基准数就能重出。", 20, GREY, 300),
         text(80, 162, "Stages 5–7: custom bilingual lettering, colour, lockups, reverse, blind emboss, icons and motion — all generated from code.", 17, MUTE, 300)]
    tiles = [("H1-horizontal-color", "横式 · horizontal", "#FFFFFF", 2),
             ("H3-standard-enji", "句点 · 胭脂底 · full stop on enji", "#8E1B2A", 2),
             ("H1-stacked-reverse", "反白 · reverse", "#231F1C", 1),
             ("H1-stacked-emboss", "盲压 · blind emboss", "#F5F2EC", 1),
             ("H1-icon", "App 图标 · app icon", "#FFFFFF", 1),
             ("H1-icon-dark", "深色图标 · dark icon", "#FFFFFF", 1)]
    x0, y0, cw, ch, g = 80, 200, 345, 300, 20
    col, row = 0, 0
    for name, label, bg, span in tiles:
        if col + span > 4:
            col, row = 0, row + 1
        x, y = x0 + col * (cw + g), y0 + row * (ch + 64)
        w = cw * span + g * (span - 1)
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ch}" rx="6" fill="{bg}" stroke="{RULE}"/>')
        pad = 40 if span == 2 else 34
        b.append(image(name, x + pad, y + pad, w - 2 * pad, ch - 2 * pad, 1200, bg))
        b.append(text(x, y + ch + 30, label, 15, GREY, 400))
        col += span
    save("system-eonpoint", W, H, b)


def motion():
    W, H = 1600, 430
    b = [text(80, 80, "动态", 32, SUMI, 400), text(160, 80, "Motion · 思考中 → 完成  thinking → done", 24, GREY, 300),
         text(80, 116, "点沿圆周运行表示“思考中”，停在最低处表示“完成”：标志本身是动后之静的那一帧。", 18, GREY, 300)]
    for i in range(3):
        x = 80 + i * 490
        b += [f'<rect x="{x}" y="150" width="460" height="230" rx="6" fill="#FFFFFF" stroke="{RULE}"/>',
              image(f"H1-motion-{i}", x + 150, 165, 160, 160, 500, "#FFFFFF"),
              text(x + 230, 360, ["运行 · moving", "将停 · settling", "落定 · settled"][i], 15, GREY, 400, anchor="middle")]
    save("motion-eonpoint", W, H, b)


def scenes():
    """场景示意（第 7 阶段）：用 scripts/mockup.py 把 EonPoint 的成稿放进六个扁平场景。"""
    import sys
    sys.path.insert(0, SCRIPTS)
    import mockup
    import tempfile
    e = lambda n: os.path.join(EP, n + ".svg")
    items = [("名片 · 正面盲压、背面横式", "Business card — blind emboss front, horizontal back",
              mockup.card(e("H1-stacked-emboss"), e("H1-horizontal-color"), stock="#F5F2EC")),
             ("App 图标 · 桌面与三个尺寸", "App icon — home screen and three sizes", mockup.phone(e("H1-icon"), "EonPoint")),
             ("官网首屏 · 横式与主视觉", "Website hero — horizontal lockup", mockup.browser(e("H1-horizontal-color"), e("H1-mark-color"))),
             ("前台形象墙", "Reception wall", mockup.wall(e("H1-stacked-color"))),
             ("提案封面 · 胭脂底", "Proposal cover on enji", mockup.slide(e("H3-standard-enji"), bg="#8E1B2A", bars="#B04A55")),
             ("手提袋 · 纸色与墨色", "Paper bags — washi and sumi", mockup.bag(e("H1-stacked-color"), e("H1-stacked-reverse")))]
    tmp = tempfile.mkdtemp()
    W, H = 1600, 1810
    b = [text(80, 92, "场景示意", 40, SUMI, 400), text(260, 92, "Scenes · EonPoint 亿触点", 30, GREY, 300),
         text(80, 134, "第 7 阶段：每个场景证明一件事——小尺寸与工艺、图标、版面、远看、提案、材料。由 scripts/mockup.py 生成的扁平示意，不是实拍。", 20, GREY, 300),
         text(80, 162, "Stage 7: each scene proves one thing. Flat mock-ups generated by scripts/mockup.py — illustrations, not photographs.", 17, MUTE, 300)]
    cw, ch = 704, 458
    for i, (zh, en, (svg, w, h)) in enumerate(items):
        r, c = divmod(i, 2)
        x, y = 80 + c * (cw + 32), 200 + r * (ch + 72)
        f = os.path.join(tmp, f"s{i}.svg")
        open(f, "w", encoding="utf-8").write(svg)
        b.append(f'<image x="{x}" y="{y}" width="{cw}" height="{ch}" href="{embed(f, 1400)}"/>')
        b += [text(x, y + ch + 30, zh, 17, SUMI, 500), text(x + cw, y + ch + 30, en, 14, MUTE, 300, anchor="end")]
    save("scenes-eonpoint", W, H, b)


def review_eonpoint():
    subprocess.run(["python3", os.path.join(SCRIPTS, "review.py"), os.path.join(OUT, "review-eonpoint.png"),
                    os.path.join(EP, "H1-mark-black.svg"),
                    "--labels", "H1 相切 · Tangent（主标志 main mark）"],
                   check=True, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero(); social(); workflow(); genes(); gates(); case(); process(); system(); motion(); scenes(); review_eonpoint()
    print("\n".join(sorted(os.listdir(OUT))))
