"""LibreOffice 描画結果から各案プレビュー・横並び比較・グリッド表示シミュレーションを作る。"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path(".")
font = ImageFont.truetype(str(Path.home() / ".fonts/ShipporiMincho-Medium.ttf"), 30)
labels = {"A": "A案　参考アカウント寄り", "B": "B案　栞の世界観重視", "C": "C案　中間案（推奨）"}
ims = {}
for i, k in enumerate("ABC", 1):
    im = Image.open(f"_abc-{i}.png").convert("RGB").crop((0, 0, 1080, 1350))
    im.save(f"preview_{k}.png")
    ims[k] = im
    Image.open(f"_tpl-{i}.png").convert("RGB").crop((0, 0, 1080, 1350)).save(f"template_preview_{k}.png")

# 横並び比較
pad, w, h = 40, 540, 675
sheet = Image.new("RGB", (pad + 3 * (w + pad), h + 2 * pad + 50), "#EFE7D8")
d = ImageDraw.Draw(sheet)
for i, k in enumerate("ABC"):
    x = pad + i * (w + pad)
    sheet.paste(ims[k].resize((w, h), Image.LANCZOS), (x, pad))
    d.text((x, pad + h + 14), labels[k], font=font, fill="#3A2A20")
sheet.save("compare_ABC.png")

# プロフィールグリッド(3:4 表示)での見え方：スマホ実寸に近い 1 タイル ≒ 130px 幅
tw, th = 130, 173
grid = Image.new("RGB", (3 * tw + 4, th), "#FFFFFF")
for i, k in enumerate("ABC"):
    im = ims[k]
    cw = round(1350 * 3 / 4)
    x0 = (1080 - cw) // 2
    grid.paste(im.crop((x0, 0, x0 + cw, 1350)).resize((tw, th), Image.LANCZOS), (i * (tw + 2), 0))
grid.resize((grid.width * 3, grid.height * 3), Image.NEAREST).save("grid_simulation_x3.png")
