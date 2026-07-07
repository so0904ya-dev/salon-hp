"""
紙の本 vs 電子書籍 比較図解を生成するスクリプト
"""
from PIL import Image, ImageDraw, ImageFont

# ===== キャンバス設定 =====
W, H = 1600, 900
BG = (255, 255, 255)
BLUE = (37, 99, 235)       # ブルー（紙の本）
ORANGE = (234, 88, 12)     # オレンジ（電子書籍）
BLUE_LIGHT = (219, 234, 254)
ORANGE_LIGHT = (255, 237, 213)
GRAY = (100, 116, 139)
DARK = (15, 23, 42)
LINE_GRAY = (226, 232, 240)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

def font(size, bold=False):
    # Arial Unicode は日本語全漢字対応
    return ImageFont.truetype(FONT_PATH, size)

def center_text(draw, text, x, y, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text((x - tw // 2, y), text, font=fnt, fill=fill)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

# ===== レイアウト定数 =====
MARGIN = 60
CARD_Y = 200
CARD_H = 620
CARD_W = 620
LEFT_X = MARGIN
RIGHT_X = W - MARGIN - CARD_W
CENTER_X = W // 2

# ===== 背景グラデーション風の薄い色帯 =====
# 左側：青みがかった薄い背景
draw_rounded_rect(draw, [LEFT_X, CARD_Y, LEFT_X + CARD_W, CARD_Y + CARD_H], 24,
                  fill=BLUE_LIGHT, outline=BLUE, width=3)
# 右側：オレンジみがかった薄い背景
draw_rounded_rect(draw, [RIGHT_X, CARD_Y, RIGHT_X + CARD_W, CARD_Y + CARD_H], 24,
                  fill=ORANGE_LIGHT, outline=ORANGE, width=3)

# ===== タイトル =====
title_fnt = font(64, bold=True)
center_text(draw, "紙の本  vs  電子書籍", CENTER_X, 48, title_fnt, DARK)

# タイトル下のライン
draw.line([(MARGIN, 148), (W - MARGIN, 148)], fill=LINE_GRAY, width=2)

# ===== 左カード：紙の本 =====
header_fnt = font(44, bold=True)
body_fnt = font(32)
sub_fnt = font(26)

# ヘッダーバー（左）
draw_rounded_rect(draw, [LEFT_X + 20, CARD_Y + 20, LEFT_X + CARD_W - 20, CARD_Y + 90], 14,
                  fill=BLUE)
center_text(draw, "紙の本", LEFT_X + CARD_W // 2, CARD_Y + 30, header_fnt, (255, 255, 255))

# 本のアイコン（ライン画）
bx, by = LEFT_X + CARD_W // 2, CARD_Y + 170
# 本の外枠
draw.rounded_rectangle([bx - 70, by - 60, bx + 70, by + 60], radius=6,
                        fill=(255, 255, 255), outline=BLUE, width=4)
# 背表紙ライン
draw.rectangle([bx - 70, by - 60, bx - 50, by + 60], fill=BLUE)
# ページライン
for i, ly in enumerate(range(by - 36, by + 40, 16)):
    draw.line([(bx - 42, ly), (bx + 62, ly)], fill=BLUE, width=2)

# 特徴テキスト
left_features = [
    ("●  物理的な質感・所有感がある", CARD_Y + 280),
    ("●  電源不要でどこでも読める", CARD_Y + 360),
    ("●  目に優しく読書が快適", CARD_Y + 440),
]
for text, ty in left_features:
    draw.text((LEFT_X + 48, ty), text, font=body_fnt, fill=DARK)

# サブ説明
sub_texts_left = [
    ("書き込みや付箋が自由にでき、", CARD_Y + 520),
    ("本棚に飾るコレクションとしても楽しめる。", CARD_Y + 558),
]
for text, ty in sub_texts_left:
    draw.text((LEFT_X + 48, ty), text, font=sub_fnt, fill=GRAY)

# ===== 右カード：電子書籍 =====
# ヘッダーバー（右）
draw_rounded_rect(draw, [RIGHT_X + 20, CARD_Y + 20, RIGHT_X + CARD_W - 20, CARD_Y + 90], 14,
                  fill=ORANGE)
center_text(draw, "電子書籍", RIGHT_X + CARD_W // 2, CARD_Y + 30, header_fnt, (255, 255, 255))

# ===== ビジネスパーソン＋PCのアイコン（ライン画） =====
ix, iy = RIGHT_X + CARD_W // 2, CARD_Y + 170   # アイコン中心
C = ORANGE   # アクセントカラー
W2 = (255, 255, 255)

# --- デスク ---
desk_y = iy + 62
draw.rounded_rectangle([ix - 90, desk_y, ix + 90, desk_y + 12], radius=4, fill=C)
# 脚（左右）
for lx in [ix - 70, ix + 70]:
    draw.line([(lx, desk_y + 12), (lx, desk_y + 36)], fill=C, width=5)

# --- ノートPC本体（下半分：キーボード部） ---
kb_x1, kb_y1 = ix - 72, desk_y - 18
kb_x2, kb_y2 = ix + 72, desk_y
draw.rounded_rectangle([kb_x1, kb_y1, kb_x2, kb_y2], radius=3,
                        fill=(255, 237, 213), outline=C, width=3)
# タッチパッド
draw.rounded_rectangle([ix - 16, kb_y1 + 3, ix + 16, kb_y2 - 3], radius=3,
                        outline=C, width=2)

# --- ノートPC蓋（ディスプレイ部） ---
sc_x1, sc_y1 = ix - 68, iy - 62
sc_x2, sc_y2 = ix + 68, desk_y - 16
draw.rounded_rectangle([sc_x1, sc_y1, sc_x2, sc_y2], radius=6,
                        fill=(255, 237, 213), outline=C, width=3)
# 画面内のコンテンツ（グラフ風）
draw.rounded_rectangle([sc_x1 + 8, sc_y1 + 8, sc_x2 - 8, sc_y2 - 8], radius=3,
                        fill=W2)
# 棒グラフ
bar_data = [28, 44, 36, 52]
bw = 12
for j, bh in enumerate(bar_data):
    bx = sc_x1 + 16 + j * 20
    draw.rectangle([bx, sc_y2 - 16 - bh // 2, bx + bw, sc_y2 - 16],
                   fill=C)
# 折れ線グラフ風
pts = []
for j, bh in enumerate(bar_data):
    pts.append((sc_x1 + 16 + j * 20 + bw // 2, sc_y2 - 16 - bh // 2 - 4))
for k in range(len(pts) - 1):
    draw.line([pts[k], pts[k+1]], fill=(255, 150, 50), width=2)
for pt in pts:
    draw.ellipse([pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3], fill=(255, 150, 50))

# --- 人物（スティックマン・着席） ---
# 頭
head_r = 18
hx, hy = ix + 26, iy - 74
draw.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r],
             fill=W2, outline=C, width=3)
# 表情（笑顔）
draw.arc([hx - 8, hy - 4, hx + 8, hy + 8], 10, 170, fill=C, width=2)
draw.ellipse([hx - 6, hy - 6, hx - 2, hy - 2], fill=C)
draw.ellipse([hx + 2, hy - 6, hx + 6, hy - 2], fill=C)

# 胴体
body_top = hy + head_r
body_bot = desk_y - 4
draw.line([(hx, body_top), (hx, body_bot)], fill=C, width=4)

# 腕（左：画面に向かって伸ばす）
elbow_x, elbow_y = hx - 20, body_top + 30
hand_x, hand_y   = ix - 10, kb_y1 + 4
draw.line([(hx, body_top + 14), (elbow_x, elbow_y)], fill=C, width=4)
draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=C, width=4)

# 腕（右：キーボードへ）
draw.line([(hx, body_top + 14), (hx + 22, elbow_y)], fill=C, width=4)
draw.line([(hx + 22, elbow_y), (ix + 30, kb_y1 + 4)], fill=C, width=4)

# 脚（座った状態）
draw.line([(hx, body_bot), (hx - 22, body_bot + 26)], fill=C, width=4)
draw.line([(hx, body_bot), (hx + 22, body_bot + 26)], fill=C, width=4)

# 特徴テキスト
right_features = [
    ("●  携帯性・軽量で持ち運び楽々", CARD_Y + 280),
    ("●  検索・マーカーで効率的に復習", CARD_Y + 360),
    ("●  省スペースで大量保管できる", CARD_Y + 440),
]
for text, ty in right_features:
    draw.text((RIGHT_X + 48, ty), text, font=body_fnt, fill=DARK)

# サブ説明
sub_texts_right = [
    ("価格割引・セールが多く、", CARD_Y + 520),
    ("即時購入してすぐに読み始められる。", CARD_Y + 558),
]
for text, ty in sub_texts_right:
    draw.text((RIGHT_X + 48, ty), text, font=sub_fnt, fill=GRAY)

# ===== 中央 VS バッジ =====
cx, cy_badge = CENTER_X, CARD_Y + CARD_H // 2
# 白い円背景
draw.ellipse([cx - 64, cy_badge - 64, cx + 64, cy_badge + 64], fill=(255, 255, 255))
# 青のリング
draw.ellipse([cx - 64, cy_badge - 64, cx + 64, cy_badge + 64], outline=BLUE, width=4)
# VS テキスト
vs_fnt = font(56, bold=True)
center_text(draw, "VS", cx, cy_badge - 36, vs_fnt, DARK)

# 矢印ライン（左→中）
draw.line([(LEFT_X + CARD_W + 10, cy_badge), (cx - 72, cy_badge)], fill=LINE_GRAY, width=3)
# 矢印ライン（中→右）
draw.line([(cx + 72, cy_badge), (RIGHT_X - 10, cy_badge)], fill=LINE_GRAY, width=3)

# ===== 左右のアクセントドット装飾 =====
for i in range(3):
    x_dot = MARGIN // 2
    draw.ellipse([x_dot - 5, CARD_Y + 20 + i * 30, x_dot + 5, CARD_Y + 30 + i * 30], fill=BLUE)
    x_dot2 = W - MARGIN // 2
    draw.ellipse([x_dot2 - 5, CARD_Y + 20 + i * 30, x_dot2 + 5, CARD_Y + 30 + i * 30], fill=ORANGE)

# ===== フッター =====
foot_fnt = font(22)
center_text(draw, "© 2026  比較図解ジェネレーター", CENTER_X, H - 40, foot_fnt, GRAY)

# ===== 保存 =====
out_path = "/Users/yamamichisouta/test/public/comparison_books.png"
img.save(out_path, "PNG", dpi=(144, 144))
print(f"保存完了: {out_path}")
