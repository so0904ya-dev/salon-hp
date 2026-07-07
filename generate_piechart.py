"""
SNS利用時間の内訳 円グラフを生成するスクリプト
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

BG    = (255, 255, 255)
DARK  = (15,  23,  42)
GRAY  = (100, 116, 135)
WHITE = (255, 255, 255)

def fnt(size):
    return ImageFont.truetype(FONT_PATH, size)

def cx_text(draw, text, x, y, f, fill):
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (bb[2] - bb[0]) // 2, y), text, font=f, fill=fill)

# ===== データ =====
data = [
    {"label": "YouTube",       "pct": 35, "color": (239,  68,  68)},   # 赤
    {"label": "Instagram",     "pct": 25, "color": (168,  85, 247)},   # 紫
    {"label": "X（Twitter）",  "pct": 20, "color": (15,  23,  42)},    # ほぼ黒
    {"label": "TikTok",        "pct": 15, "color": (20, 184, 166)},    # ティール
    {"label": "その他",         "pct":  5, "color": (148, 163, 184)},   # グレー
]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ===== 背景の薄い円装飾 =====
for r, alpha in [(420, (245,248,252)), (340, (240,244,250))]:
    draw.ellipse([W//2 - 200 - r, H//2 - r, W//2 - 200 + r, H//2 + r], fill=alpha)

# ===== タイトル =====
cx_text(draw, "SNS 利用時間の内訳", W // 2, 28, fnt(58), DARK)
draw.line([(100, 112), (W - 100, 112)], fill=(226, 232, 240), width=2)

# ===== 円グラフ描画 =====
CX, CY = 510, 490       # グラフ中心
R_OUTER = 265           # 外径
R_INNER = 108           # 内径（ドーナツ）
GAP     = 5             # セクション間の隙間（度）

# 各セクションの開始角度を計算（-90度から開始 = 12時方向）
start_angle = -90.0
sections = []
for d in data:
    sweep = d["pct"] / 100 * 360
    sections.append({**d, "start": start_angle, "sweep": sweep})
    start_angle += sweep

# ===== セクション描画（外側から内側を白で抜く） =====
for sec in sections:
    s = sec["start"] - GAP / 2
    e = sec["start"] + sec["sweep"] + GAP / 2

    # 外側の扇形
    draw.pieslice(
        [CX - R_OUTER, CY - R_OUTER, CX + R_OUTER, CY + R_OUTER],
        start=s, end=e, fill=sec["color"]
    )

# 内側を白で抜いてドーナツに
draw.ellipse([CX - R_INNER, CY - R_INNER, CX + R_INNER, CY + R_INNER], fill=BG)

# セクション境界線（白）
for sec in sections:
    for angle_deg in [sec["start"], sec["start"] + sec["sweep"]]:
        rad = math.radians(angle_deg)
        x1 = CX + R_INNER * math.cos(rad)
        y1 = CY + R_INNER * math.sin(rad)
        x2 = CX + R_OUTER * math.cos(rad)
        y2 = CY + R_OUTER * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=BG, width=4)

# ===== ドーナツ中央テキスト =====
cx_text(draw, "SNS", CX, CY - 38, fnt(32), GRAY)
cx_text(draw, "利用時間", CX, CY, fnt(28), GRAY)

# ===== セクションラベル（外側に引き出し線付き） =====
for sec in sections:
    mid_angle = math.radians(sec["start"] + sec["sweep"] / 2)
    pct = sec["pct"]

    # 引き出し線の始点（外縁）・中継点・終点
    r1 = R_OUTER + 18
    r2 = R_OUTER + 52
    x1 = CX + r1 * math.cos(mid_angle)
    y1 = CY + r1 * math.sin(mid_angle)
    x2 = CX + r2 * math.cos(mid_angle)
    y2 = CY + r2 * math.sin(mid_angle)

    # 水平方向の端点（左側は短めに）
    is_right = math.cos(mid_angle) >= 0
    hline_len = 50 if is_right else 30
    x3 = x2 + (hline_len if is_right else -hline_len)
    # 左端からはみ出さないようにクランプ
    if not is_right:
        x3 = max(x3, 80)
    y3 = y2

    # 引き出し線
    draw.line([(x1, y1), (x2, y2)], fill=sec["color"], width=2)
    draw.line([(x2, y2), (x3, y3)], fill=sec["color"], width=2)

    # テキスト配置
    text_x = x3 + (8 if is_right else -8)
    pct_text = f"{pct}%"
    label_text = sec["label"]

    if is_right:
        # 右側：左揃え
        draw.text((text_x, y3 - 32), pct_text, font=fnt(30), fill=sec["color"])
        draw.text((text_x, y3 + 2), label_text, font=fnt(24), fill=DARK)
    else:
        # 左側：右揃え
        bb_p = draw.textbbox((0,0), pct_text, font=fnt(30))
        bb_l = draw.textbbox((0,0), label_text, font=fnt(24))
        draw.text((text_x - (bb_p[2]-bb_p[0]), y3 - 32), pct_text, font=fnt(30), fill=sec["color"])
        draw.text((text_x - (bb_l[2]-bb_l[0]), y3 + 2), label_text, font=fnt(24), fill=DARK)

# ===== 右側：凡例パネル =====
LX = 900
LY = 200
for i, d in enumerate(data):
    ly = LY + i * 100

    # カラースウォッチ（丸）
    sw = 26
    draw.ellipse([LX, ly, LX + sw*2, ly + sw*2], fill=d["color"])

    # ラベル
    draw.text((LX + sw*2 + 20, ly), d["label"], font=fnt(32), fill=DARK)

    # パーセントバー
    BAR_X = LX + sw*2 + 20
    BAR_Y = ly + 44
    BAR_W = 380
    BAR_H = 18
    BAR_R = 9
    # 背景バー
    draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H],
                            radius=BAR_R, fill=(241, 245, 249))
    # 塗りバー
    fill_w = int(BAR_W * d["pct"] / 100)
    if fill_w > BAR_R * 2:
        draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H],
                                radius=BAR_R, fill=d["color"])
    # パーセントテキスト
    pct_str = f"{d['pct']}%"
    draw.text((BAR_X + BAR_W + 14, BAR_Y - 2), pct_str, font=fnt(26), fill=d["color"])

# ===== 合計表示 =====
total_y = LY + len(data) * 100 + 20
draw.line([(LX, total_y), (LX + 480, total_y)], fill=(226, 232, 240), width=2)
draw.text((LX, total_y + 14), "合計", font=fnt(26), fill=GRAY)
bb = draw.textbbox((0,0), "100%", font=fnt(26))
draw.text((LX + 480 - (bb[2]-bb[0]), total_y + 14), "100%", font=fnt(26), fill=DARK)

# ===== フッター =====
cx_text(draw, "※ データは架空のサンプルです", W // 2, H - 38, fnt(22), (203, 213, 225))

# ===== 保存 =====
out = "/Users/yamamichisouta/test/public/piechart_sns.png"
img.save(out, "PNG", dpi=(144, 144))
print(f"保存完了: {out}")
