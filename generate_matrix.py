"""
タスクの優先順位マトリクス（4象限マップ）を生成するスクリプト
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

# ===== カラーパレット =====
BG           = (255, 255, 255)
RED_FILL     = (254, 226, 226)   # 右上：すぐやる（赤系）
RED_ACCENT   = (239,  68,  68)
BLUE_FILL    = (219, 234, 254)   # 左上：計画する（青系）
BLUE_ACCENT  = (59,  130, 246)
YELLOW_FILL  = (254, 249, 195)   # 右下：任せる（黄系）
YELLOW_ACCENT= (202, 138,   4)
GRAY_FILL    = (241, 245, 249)   # 左下：やめる（グレー）
GRAY_ACCENT  = (100, 116, 135)
DARK         = (15,  23,  42)
WHITE        = (255, 255, 255)
AXIS_COLOR   = (51,  65,  85)
GRID_COLOR   = (226, 232, 240)

def fnt(size):
    return ImageFont.truetype(FONT_PATH, size)

def cx_text(draw, text, x, y, f, fill):
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (bb[2] - bb[0]) // 2, y), text, font=f, fill=fill)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ===== タイトル =====
cx_text(draw, "タスクの優先順位マトリクス", W // 2, 28, fnt(58), DARK)
draw.line([(100, 112), (W - 100, 112)], fill=GRID_COLOR, width=2)

# ===== マトリクスレイアウト =====
MX = 140       # マトリクス左端X
MY = 140       # マトリクス上端Y
MW = 1320      # マトリクス幅（右パネルを廃止して拡張）
MH = 700       # マトリクス高さ
CX = MX + MW // 2   # 十字の交点X
CY = MY + MH // 2   # 十字の交点Y
RADIUS = 14          # 角丸

# ===== 4象限の塗りつぶし =====
quads = [
    # (x1, y1, x2, y2, fill, accent, label, sublabel, icon_type)
    (CX, MY,     MX + MW, CY,     RED_FILL,    RED_ACCENT,    "すぐやる",  "重要 × 緊急", "fire"),
    (MX, MY,     CX,      CY,     BLUE_FILL,   BLUE_ACCENT,   "計画する",  "重要 × 余裕", "calendar"),
    (CX, CY,     MX + MW, MY + MH,YELLOW_FILL, YELLOW_ACCENT, "任せる",   "緊急 × 非重要","delegate"),
    (MX, CY,     CX,      MY + MH,GRAY_FILL,   GRAY_ACCENT,   "やめる",   "非重要 × 非緊急","trash"),
]

# ===== アイコン描画 =====
def draw_fire(draw, cx, cy, color):
    """炎アイコン"""
    draw.ellipse([cx-18, cy+10, cx+18, cy+40], fill=color, outline=color)
    pts = [
        (cx, cy-40), (cx+22, cy-10), (cx+16, cy+18),
        (cx, cy+6), (cx-16, cy+18), (cx-22, cy-10),
    ]
    draw.polygon(pts, fill=color)
    # 内側の明るい炎
    bright = tuple(min(255, c + 60) for c in color)
    pts2 = [(cx, cy-20), (cx+10, cy+4), (cx, cy+14), (cx-10, cy+4)]
    draw.polygon(pts2, fill=bright)

def draw_calendar(draw, cx, cy, color):
    """カレンダーアイコン"""
    draw.rounded_rectangle([cx-32, cy-28, cx+32, cy+32], radius=6,
                            outline=color, fill=WHITE, width=3)
    draw.rectangle([cx-32, cy-28, cx+32, cy-8], fill=color)
    # リングバインダー
    for bx in [cx-16, cx+16]:
        draw.rounded_rectangle([bx-5, cy-36, bx+5, cy-18], radius=4, fill=color)
    # 日付グリッド
    for row in range(2):
        for col in range(3):
            gx = cx - 20 + col * 20
            gy = cy + 2 + row * 16
            draw.rounded_rectangle([gx-6, gy-5, gx+6, gy+5], radius=2, fill=color)

def draw_delegate(draw, cx, cy, color):
    """委任（人物2人）アイコン"""
    # 左の人
    draw.ellipse([cx-38, cy-36, cx-18, cy-16], outline=color, fill=WHITE, width=3)
    draw.arc([cx-50, cy-12, cx-6, cy+32], 200, 340, fill=color, width=3)
    # 右の人（小さめ）
    draw.ellipse([cx+14, cy-28, cx+34, cy-8], fill=color)
    draw.arc([cx+2, cy-4, cx+46, cy+30], 200, 340, fill=color, width=3)
    # 矢印（委任の矢）
    draw.line([(cx-6, cy-24), (cx+10, cy-24)], fill=color, width=3)
    draw.polygon([(cx+10, cy-30), (cx+20, cy-24), (cx+10, cy-18)], fill=color)

def draw_trash(draw, cx, cy, color):
    """ゴミ箱アイコン"""
    # 蓋
    draw.rounded_rectangle([cx-28, cy-36, cx+28, cy-22], radius=4, fill=color)
    draw.rounded_rectangle([cx-18, cy-44, cx+18, cy-32], radius=4, fill=color)
    # 本体
    draw.rounded_rectangle([cx-26, cy-20, cx+26, cy+32], radius=6,
                            outline=color, fill=WHITE, width=3)
    # 縦線
    for lx in [cx-10, cx, cx+10]:
        draw.line([(lx, cy-12), (lx, cy+24)], fill=color, width=2)

icon_funcs = {
    "fire": draw_fire,
    "calendar": draw_calendar,
    "delegate": draw_delegate,
    "trash": draw_trash,
}

# 象限ラベル設定（見出し＋サブ＋説明）
quad_details = {
    "すぐやる":  {
        "desc": ["締め切りが近い重要タスク。", "今すぐ取り掛かる。"],
        "example": "例：明日の締め切り資料"
    },
    "計画する": {
        "desc": ["重要だが今でなくていい。", "日時を決めて着手する。"],
        "example": "例：スキルアップの勉強"
    },
    "任せる":  {
        "desc": ["急ぎだが自分でなくていい。", "他者に依頼または簡略化。"],
        "example": "例：日常的な報告・連絡"
    },
    "やめる":  {
        "desc": ["価値が低く急ぎでもない。", "思い切って削除・中断。"],
        "example": "例：惰性での作業・会議"
    },
}

for (x1, y1, x2, y2, fill, accent, label, sublabel, icon_type) in quads:
    qcx = (x1 + x2) // 2
    qcy = (y1 + y2) // 2

    # 塗りつぶし
    draw.rectangle([x1, y1, x2, y2], fill=fill)

    # アイコン（上部中央）
    icon_y = y1 + 72
    icon_funcs[icon_type](draw, qcx, icon_y, accent)

    # メインラベル（大きく）
    cx_text(draw, label, qcx, icon_y + 72, fnt(48), accent)

    # サブラベル（タグ風）
    tag_w = len(sublabel) * 14 + 24
    tag_x = qcx - tag_w // 2
    tag_y = icon_y + 128
    draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + 30], radius=14,
                            fill=accent, outline=accent)
    cx_text(draw, sublabel, qcx, tag_y + 6, fnt(18), WHITE)

    # 説明テキスト
    det = quad_details[label]
    for k, line in enumerate(det["desc"]):
        cx_text(draw, line, qcx, tag_y + 44 + k * 28, fnt(20), DARK)

    # 例テキスト
    ex = det["example"]
    cx_text(draw, ex, qcx, tag_y + 112, fnt(18), GRAY_ACCENT)

# ===== 軸線（十字） =====
# 横軸
draw.line([(MX, CY), (MX + MW, CY)], fill=AXIS_COLOR, width=4)
# 縦軸
draw.line([(CX, MY), (CX, MY + MH)], fill=AXIS_COLOR, width=4)

# 軸矢印（4方向）
arr = 14
draw.polygon([(MX+MW, CY), (MX+MW-arr, CY-arr//2), (MX+MW-arr, CY+arr//2)], fill=AXIS_COLOR)  # →
draw.polygon([(MX, CY), (MX+arr, CY-arr//2), (MX+arr, CY+arr//2)], fill=AXIS_COLOR)            # ←
draw.polygon([(CX, MY), (CX-arr//2, MY+arr), (CX+arr//2, MY+arr)], fill=AXIS_COLOR)            # ↑
draw.polygon([(CX, MY+MH), (CX-arr//2, MY+MH-arr), (CX+arr//2, MY+MH-arr)], fill=AXIS_COLOR)  # ↓

# ===== 軸ラベル =====
# 縦軸：重要度
cx_text(draw, "重要度 高", CX, MY - 36, fnt(24), AXIS_COLOR)
cx_text(draw, "重要度 低", CX, MY + MH + 10, fnt(24), AXIS_COLOR)

# 横軸：緊急度
ax_fnt = fnt(24)
# 右端（緊急度 高）
draw.text((MX + MW + 12, CY - 16), "緊急度 高", font=ax_fnt, fill=AXIS_COLOR)
# 左端（緊急度 低）
bb = draw.textbbox((0,0), "緊急度 低", font=ax_fnt)
draw.text((MX - (bb[2]-bb[0]) - 12, CY - 16), "緊急度 低", font=ax_fnt, fill=AXIS_COLOR)

# ===== フッター =====
cx_text(draw, "アイゼンハワー・マトリクス：重要度と緊急度でタスクを整理し、本質的な仕事に集中する。",
        W // 2, H - 38, fnt(22), GRAY_ACCENT)

# ===== 保存 =====
out = "/Users/yamamichisouta/test/public/matrix_tasks.png"
img.save(out, "PNG", dpi=(144, 144))
print(f"保存完了: {out}")
