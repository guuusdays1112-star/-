"""v2 のプレビュー・比較・一覧表示（グリッド）縮小・シリーズ展開イメージを作る。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = str(Path.home() / ".fonts/ShipporiMincho-Medium.ttf")
f30, f22 = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 22)
BG, INK = "#F4EFE5", "#38251F"
LABEL = {"A": "A案　大胆なタイポグラフィ", "B": "B案　エディトリアル", "C": "C案　01×03の融合（推奨）"}


def load(prefix, i):
    return Image.open(f"{prefix}-{i}.png").convert("RGB").crop((0, 0, 1080, 1350))


def grid_tile(im, w):
    """プロフィールグリッドの 3:4 中央切り抜きを幅 w で。"""
    cw = 1013
    x0 = (1080 - cw) // 2
    return im.crop((x0, 0, x0 + cw, 1350)).resize((w, round(w * 4 / 3)), Image.LANCZOS)


ims = {k: load("_shiori_v2_ABC", i) for i, k in enumerate("ABC", 1)}
for i, k in enumerate("ABC", 1):
    ims[k].save(f"thumb_{k}.png")
    load("_shiori_v2_template", i).save(f"template_{k}.png")

# 横並び比較（大）
pad, w, h = 40, 540, 675
sheet = Image.new("RGB", (pad + 3 * (w + pad), h + 2 * pad + 50), BG)
d = ImageDraw.Draw(sheet)
for i, k in enumerate("ABC"):
    x = pad + i * (w + pad)
    sheet.paste(ims[k].resize((w, h), Image.LANCZOS), (x, pad))
    d.text((x, pad + h + 14), LABEL[k], font=f30, fill=INK)
sheet.save("compare_ABC.png")

# 一覧表示の縮小プレビュー：スマホ実寸相当（1タイル 124px 幅）と、その 3 倍拡大
tw = 124
th = round(tw * 4 / 3)
row = Image.new("RGB", (3 * tw + 4, th), "white")
for i, k in enumerate("ABC"):
    row.paste(grid_tile(ims[k], tw), (i * (tw + 2), 0))
row.save("grid_actual_size.png")
big = row.resize((row.width * 3, row.height * 3), Image.NEAREST)
canvas = Image.new("RGB", (big.width + 80, big.height + 120), BG)
canvas.paste(big, (40, 40))
d = ImageDraw.Draw(canvas)
d.text((40, big.height + 60), "一覧表示シミュレーション：3:4切り抜き・1タイル124px相当を3倍表示（左からA・B・C）",
       font=f22, fill=INK)
canvas.save("grid_preview_x3.png")

# シリーズ展開イメージ（C型を並べたとき）
mock = [load("__series_mock", i) for i in (1, 2, 3)]
row = Image.new("RGB", (3 * 300 + 4, 400), "white")
for i, im in enumerate(mock):
    row.paste(grid_tile(im, 300), (i * 302, 0))
canvas = Image.new("RGB", (row.width + 80, row.height + 110), BG)
canvas.paste(row, (40, 40))
d = ImageDraw.Draw(canvas)
d.text((40, row.height + 56), "C型を並べたイメージ（同じ写真の別トリミングで仮置き・実投稿ではありません）",
       font=f22, fill=INK)
canvas.save("series_mock_C.png")
