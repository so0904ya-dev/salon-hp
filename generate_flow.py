"""
朝のルーティン 3ステップ フロー図を生成するスクリプト
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

# ===== カラーパレット（淡いグリーン系） =====
BG          = (236, 248, 240)   # 淡いグリーン背景
GREEN       = (34, 139, 87)     # メイングリーン
GREEN_DARK  = (21, 100, 62)     # 濃いグリーン
GREEN_LIGHT = (187, 230, 207)   # 薄いグリーン（カード背景）
WHITE       = (255, 255, 255)
DARK        = (20,  40,  30)    # ほぼ黒
GRAY        = (100, 130, 110)   # グレーグリーン
LINE_COLOR  = (140, 200, 165)   # 矢印・ライン色

def fnt(size):
    return ImageFont.truetype(FONT_PATH, size)

def cx_text(draw, text, x, y, f, fill):
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (bb[2] - bb[0]) // 2, y), text, font=f, fill=fill)

# ===== キャンバス =====
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ===== 装飾：背景の小丸 =====
import random
random.seed(42)
for _ in range(30):
    rx, ry = random.randint(0, W), random.randint(0, H)
    r = random.randint(4, 14)
    draw.ellipse([rx-r, ry-r, rx+r, ry+r], fill=(200, 235, 215))

# ===== タイトル =====
title_fnt = fnt(66)
cx_text(draw, "業務効率化の 3ステップ", W//2, 48, title_fnt, GREEN_DARK)

# タイトル下ライン
draw.line([(120, 140), (W-120, 140)], fill=GREEN_LIGHT, width=3)

# ===== カード設定 =====
CARD_W  = 380
CARD_H  = 520
CARD_Y  = 180
CARD_R  = 28          # 角丸半径

# 3枚のカード X 座標（均等配置）
gap = (W - 3 * CARD_W) // 4
card_xs = [gap, gap*2 + CARD_W, gap*3 + CARD_W*2]

steps = [
    {
        "num": "1",
        "title": "起きたらコップ1杯の水を飲む",
        "lines": ["起床直後に", "コップ1杯の水"],
    },
    {
        "num": "2",
        "title": "10分ストレッチ",
        "lines": ["全身を10分", "ゆっくり伸ばす"],
    },
    {
        "num": "3",
        "title": "今日のタスクを3つ書き出す",
        "lines": ["今日やること3つを", "紙に書き出す"],
    },
]

# ===== アイコン描画関数 =====
def draw_water_icon(draw, cx, cy, color, size=90):
    """コップのアイコン"""
    hw = size // 2
    hh = int(size * 0.65)
    # コップ本体（台形）
    draw.polygon([
        (cx - hw + 10, cy - hh),
        (cx + hw - 10, cy - hh),
        (cx + hw,      cy + hh),
        (cx - hw,      cy + hh),
    ], outline=color, width=4)
    # 水面ライン
    draw.line([(cx - hw + 14, cy + 4), (cx + hw - 4, cy + 4)], fill=color, width=3)
    # 水の波線（2本）
    for yi in [cy + 20, cy + 38]:
        draw.arc([cx - hw + 18, yi - 6, cx - 6, yi + 6], 180, 0, fill=color, width=2)
        draw.arc([cx - 6, yi - 6, cx + hw - 18, yi + 6], 180, 0, fill=color, width=2)

def draw_stretch_icon(draw, cx, cy, color, size=90):
    """ストレッチする人物アイコン"""
    head_r = 14
    # 頭
    draw.ellipse([cx - head_r, cy - size//2 - head_r,
                  cx + head_r, cy - size//2 + head_r], outline=color, width=4)
    # 胴体
    body_top = cy - size//2 + head_r
    body_bot = cy + size//5
    draw.line([(cx, body_top), (cx, body_bot)], fill=color, width=4)
    # 左腕（斜め上）
    draw.line([(cx, body_top + 20), (cx - size//2, cy - size//5)], fill=color, width=4)
    # 右腕（斜め上・高く上げる）
    draw.line([(cx, body_top + 20), (cx + size//2 + 10, cy - size//2 + 10)], fill=color, width=4)
    # 左脚
    draw.line([(cx, body_bot), (cx - size//3, cy + size//2)], fill=color, width=4)
    # 右脚
    draw.line([(cx, body_bot), (cx + size//3, cy + size//2)], fill=color, width=4)

def draw_task_icon(draw, cx, cy, color, size=90):
    """メモ帳＋チェックアイコン"""
    hw = size // 2
    hh = int(size * 0.6)
    # メモ帳外枠
    draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                            radius=8, outline=color, width=4)
    # クリップ部分（上部）
    draw.rounded_rectangle([cx - 20, cy - hh - 14, cx + 20, cy - hh + 10],
                            radius=6, fill=BG, outline=color, width=3)
    # 行ライン × 3
    for i, lx in enumerate(range(cy - hh + 28, cy + hh - 20, 28)):
        # チェックマーク（最初の2行）
        if i < 2:
            draw.line([(cx - hw + 14, lx + 6), (cx - hw + 22, lx + 14)], fill=color, width=3)
            draw.line([(cx - hw + 22, lx + 14), (cx - hw + 34, lx - 2)], fill=color, width=3)
            draw.line([(cx - hw + 40, lx + 4), (cx + hw - 14, lx + 4)], fill=color, width=3)
        else:
            draw.line([(cx - hw + 14, lx + 4), (cx + hw - 14, lx + 4)], fill=color, width=2)

# ===== カードを描く =====
icon_drawers = [draw_water_icon, draw_stretch_icon, draw_task_icon]

for i, (step, cx_card) in enumerate(zip(steps, card_xs)):
    cx = cx_card + CARD_W // 2
    # カード影（微妙にずらす）
    draw.rounded_rectangle(
        [cx_card + 6, CARD_Y + 6, cx_card + CARD_W + 6, CARD_Y + CARD_H + 6],
        radius=CARD_R, fill=(180, 220, 195))
    # カード本体
    draw.rounded_rectangle(
        [cx_card, CARD_Y, cx_card + CARD_W, CARD_Y + CARD_H],
        radius=CARD_R, fill=WHITE, outline=GREEN, width=3)

    # ステップ番号バッジ（カード内に収まるよう位置調整）
    badge_r = 32
    bx, by = cx, CARD_Y + 52
    draw.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r], fill=GREEN)
    cx_text(draw, f"Step {step['num']}", bx, by - 18, fnt(26), WHITE)

    # セパレーターライン
    draw.line([(cx_card + 24, CARD_Y + 98), (cx_card + CARD_W - 24, CARD_Y + 98)],
              fill=GREEN_LIGHT, width=2)

    # アイコン描画
    icon_drawers[i](draw, cx, CARD_Y + 220, GREEN, size=88)

    # テキスト（2行）
    body_fnt = fnt(28)
    for j, line in enumerate(step["lines"]):
        cx_text(draw, line, cx, CARD_Y + 336 + j * 40, body_fnt, DARK)

    # カード下部：タイトル帯
    draw.rounded_rectangle(
        [cx_card + 16, CARD_Y + CARD_H - 100, cx_card + CARD_W - 16, CARD_Y + CARD_H - 16],
        radius=14, fill=GREEN_LIGHT)
    title_text = step["title"]
    # 長いタイトルは2行に分割
    if len(title_text) > 12:
        mid = len(title_text) // 2
        # 句読点・助詞で折る（簡易）
        split_pos = mid
        for k in range(mid, len(title_text)):
            if title_text[k] in "のをにはがでも、。":
                split_pos = k + 1
                break
        line1 = title_text[:split_pos]
        line2 = title_text[split_pos:]
        cx_text(draw, line1, cx, CARD_Y + CARD_H - 94, fnt(24), GREEN_DARK)
        cx_text(draw, line2, cx, CARD_Y + CARD_H - 62, fnt(24), GREEN_DARK)
    else:
        cx_text(draw, title_text, cx, CARD_Y + CARD_H - 76, fnt(26), GREEN_DARK)

# ===== 矢印を描く =====
ARROW_Y = CARD_Y + CARD_H // 2
for i in range(2):
    ax1 = card_xs[i] + CARD_W + 12
    ax2 = card_xs[i + 1] - 12
    amid = (ax1 + ax2) // 2
    # 矢印本体
    draw.line([(ax1, ARROW_Y), (ax2 - 18, ARROW_Y)], fill=GREEN, width=6)
    # 矢印頭（三角）
    draw.polygon([
        (ax2,      ARROW_Y),
        (ax2 - 22, ARROW_Y - 14),
        (ax2 - 22, ARROW_Y + 14),
    ], fill=GREEN)

# ===== 番号ドット（タイムライン風） =====
tl_y = CARD_Y - 30
draw.line([(card_xs[0] + CARD_W//2, tl_y), (card_xs[2] + CARD_W//2, tl_y)],
          fill=GREEN_LIGHT, width=2)
for i, cx_card in enumerate(card_xs):
    cx = cx_card + CARD_W // 2
    draw.ellipse([cx - 10, tl_y - 10, cx + 10, tl_y + 10], fill=GREEN)

# ===== フッター =====
cx_text(draw, "毎朝3つの習慣で、1日のパフォーマンスが上がる。", W//2, H - 52, fnt(28), GRAY)

# ===== 保存 =====
out = "/Users/yamamichisouta/test/public/flow_morning.png"
img.save(out, "PNG", dpi=(144, 144))
print(f"保存完了: {out}")
