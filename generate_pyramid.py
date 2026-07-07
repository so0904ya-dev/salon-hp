"""
学習の3段階ピラミッド 図解を生成するスクリプト
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

# ===== カラーパレット =====
BG          = (255, 255, 255)
BLUE_LIGHT  = (219, 234, 254)   # 下段：薄い青
BLUE_MID    = (59,  130, 246)   # 中段：青
BLUE_DARK   = (30,  64,  175)   # 上段：濃い青
BLUE_BORDER = (37,  99,  235)
GRAY        = (100, 116, 135)
DARK        = (15,  23,  42)
WHITE       = (255, 255, 255)
BLUE_PALE   = (239, 246, 255)   # 背景の微妙な色帯

def fnt(size):
    return ImageFont.truetype(FONT_PATH, size)

def cx_text(draw, text, x, y, f, fill):
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (bb[2] - bb[0]) // 2, y), text, font=f, fill=fill)

def text_w(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ===== 背景の薄い斜めストライプ装飾 =====
for i in range(0, W + H, 80):
    draw.line([(i, 0), (i - H, H)], fill=(245, 248, 255), width=40)

# ===== タイトル =====
title_fnt = fnt(62)
cx_text(draw, "学習の 3段階ピラミッド", W // 2, 44, title_fnt, DARK)
draw.line([(160, 132), (W - 160, 132)], fill=(226, 232, 240), width=2)

# ===== ピラミッドパラメータ =====
# ピラミッド全体の底辺中心X、底辺Y、頂点Y
CX      = W // 2 - 80    # 少し左寄り（右に説明テキスト）
PY_BOT  = 840            # 底辺Y
PY_TOP  = 180            # 頂点Y
PY_H    = PY_BOT - PY_TOP

# 3段の高さ比率（下：中：上 = 5:4:3）
ratios  = [5, 4, 3]
total_r = sum(ratios)
seg_h   = [PY_H * r // total_r for r in ratios]
# 誤差補正
seg_h[0] += PY_H - sum(seg_h)

# 各段の上下Y座標
ys = [PY_BOT]
for h in reversed(seg_h):
    ys.insert(0, ys[0] - h)
# ys[0]=top, ys[1]=mid1, ys[2]=mid2, ys[3]=bottom

# ピラミッドの幅：高さに比例（底辺最大、頂点0）
BASE_HALF = 420   # 底辺の半幅

def x_at_y(y):
    """Y座標に対応するピラミッドの半幅"""
    t = (PY_BOT - y) / PY_H   # 0=底辺, 1=頂点
    return int(BASE_HALF * (1 - t))

# ===== 段の設定 =====
levels = [
    {
        "num": "3",
        "text": "人に教える",
        "sub": "Teaching",
        "fill": BLUE_DARK,
        "text_color": WHITE,
        "y_top": ys[0],
        "y_bot": ys[1],
    },
    {
        "num": "2",
        "text": "実際にやってみる",
        "sub": "Practice",
        "fill": BLUE_MID,
        "text_color": WHITE,
        "y_top": ys[1],
        "y_bot": ys[2],
    },
    {
        "num": "1",
        "text": "基礎知識をインプットする",
        "sub": "Knowledge",
        "fill": BLUE_LIGHT,
        "text_color": DARK,
        "y_top": ys[2],
        "y_bot": ys[3],
    },
]

# ===== 影（少し右下にずらした同形ポリゴン） =====
SHADOW_OFFSET = 8
shadow_poly = [
    (CX + SHADOW_OFFSET,           PY_TOP + SHADOW_OFFSET),
    (CX + x_at_y(PY_BOT) + SHADOW_OFFSET, PY_BOT + SHADOW_OFFSET),
    (CX - x_at_y(PY_BOT) + SHADOW_OFFSET, PY_BOT + SHADOW_OFFSET),
]
draw.polygon(shadow_poly, fill=(210, 220, 235))

# ===== 各段を描画 =====
for lv in levels:
    yt, yb = lv["y_top"], lv["y_bot"]
    xl_top = CX - x_at_y(yt)
    xr_top = CX + x_at_y(yt)
    xl_bot = CX - x_at_y(yb)
    xr_bot = CX + x_at_y(yb)

    # 台形を塗りつぶし
    poly = [(xl_top, yt), (xr_top, yt), (xr_bot, yb), (xl_bot, yb)]
    draw.polygon(poly, fill=lv["fill"])

    # 枠線
    draw.polygon(poly, outline=WHITE, width=3)

    # 段の中間高さでの幅（台形の中間）を使って中央を計算
    mid_y = (yt + yb) // 2
    xl_mid = CX - x_at_y(mid_y)
    xr_mid = CX + x_at_y(mid_y)
    mid_x  = (xl_mid + xr_mid) // 2

    # メインテキスト（段の中央）
    cx_text(draw, lv["text"], mid_x, mid_y - 22, fnt(32), lv["text_color"])
    # サブテキスト（英語・小さめ）
    sub_color = GRAY if lv["fill"] == BLUE_LIGHT else lv["text_color"]
    cx_text(draw, lv["sub"], mid_x, mid_y + 16, fnt(20), sub_color)

# ===== 右側：説明テキストパネル =====
PANEL_X = CX + BASE_HALF + 60
PANEL_Y = PY_TOP
PANEL_W = W - PANEL_X - 40

desc = [
    {
        "num": "①",
        "title": "基礎知識をインプットする",
        "body": "本・動画・講座などで知識を\nまず頭に入れる段階。",
        "color": BLUE_MID,
    },
    {
        "num": "②",
        "title": "実際にやってみる",
        "body": "手を動かして練習・演習を\n繰り返し、体で覚える段階。",
        "color": BLUE_MID,
    },
    {
        "num": "③",
        "title": "人に教える",
        "body": "他者へ説明することで\n理解が深まり定着する段階。",
        "color": BLUE_DARK,
    },
]

desc_y = PANEL_Y + 20
for d in desc:
    # 左のアクセントライン
    draw.rectangle([PANEL_X, desc_y, PANEL_X + 5, desc_y + 108], fill=d["color"])

    # 番号＋タイトル
    draw.text((PANEL_X + 20, desc_y + 4), d["num"] + "  " + d["title"],
              font=fnt(26), fill=d["color"])
    # 本文
    for k, line in enumerate(d["body"].split("\n")):
        draw.text((PANEL_X + 20, desc_y + 44 + k * 32), line, font=fnt(22), fill=GRAY)

    desc_y += 192

# 矢印（右パネル下部：「上にいくほど高度」）
arr_x = PANEL_X + PANEL_W // 2 - 20
arr_y_bot = desc_y + 20
arr_y_top = desc_y + 80
draw.line([(arr_x, arr_y_bot), (arr_x, arr_y_top)], fill=BLUE_BORDER, width=3)
draw.polygon([(arr_x, arr_y_top - 16), (arr_x - 10, arr_y_top), (arr_x + 10, arr_y_top)],
             fill=BLUE_BORDER)
draw.text((arr_x + 18, arr_y_top - 8), "より高度な学習段階", font=fnt(20), fill=GRAY)

# ===== フッター =====
cx_text(draw, "知識は「インプット → 実践 → アウトプット」の順で本物になる。",
        W // 2, H - 44, fnt(26), GRAY)

# ===== 保存 =====
out = "/Users/yamamichisouta/test/public/pyramid_learning.png"
img.save(out, "PNG", dpi=(144, 144))
print(f"保存完了: {out}")
