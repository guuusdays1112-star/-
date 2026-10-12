#!/bin/sh
# リール表紙：build → PPTX を LibreOffice で描画 → 表紙PNG・グリッド切り抜き・再生画面の確認画像
set -e
cd "$(dirname "$0")"
python3 build.py ../source_photo.jpg
cd out
for f in reel_cover_fig_sandwich reel_cover_template; do
  soffice --headless --convert-to pdf "$f.pptx" >/dev/null 2>&1
  pdftoppm -r 96 -singlefile -png "$f.pdf" "_$f"
done
python3 - <<'P'
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
F = str(Path.home() / ".fonts/ShipporiMincho-Medium.ttf")
f = ImageFont.truetype(F, 22)
for n in ("fig_sandwich", "template"):
    im = Image.open(f"_reel_cover_{n}.png").convert("RGB").crop((0, 0, 1080, 1920))
    im.save(f"reel_cover_{n}.png")
im = Image.open("reel_cover_fig_sandwich.png")
# 1) プロフィールグリッドの 3:4 切り抜き（中央 1080×1440）
grid = im.crop((0, 240, 1080, 1680))
small = grid.resize((124, 165), Image.LANCZOS)
# 2) 再生画面の確認：右のアイコン列と下部キャプション帯（目安）を半透明で重ねる
ui = im.copy().convert("RGBA")
ov = Image.new("RGBA", ui.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.rectangle((940, 1080, 1080, 1700), fill=(255, 60, 60, 90))
d.rectangle((0, 1560, 1080, 1920), fill=(255, 60, 60, 90))
d.rectangle((0, 240, 1079, 1680), outline=(80, 200, 255, 255), width=6)
ui = Image.alpha_composite(ui, ov).convert("RGB")
# 並べる
W = 40 + 540 + 40 + 540 + 40 + 372 + 40
S = Image.new("RGB", (W, 960 + 120), "#F4EFE5")
S.paste(im.resize((540, 960), Image.LANCZOS), (40, 40))
S.paste(ui.resize((540, 960), Image.LANCZOS), (620, 40))
S.paste(small.resize((372, 495), Image.NEAREST), (1200, 40))
d = ImageDraw.Draw(S)
d.text((40, 1012), "表紙（1080×1920）", font=f, fill="#38251F")
d.text((620, 1012), "青枠＝グリッドの3:4範囲／赤＝再生画面のUI（目安）", font=f, fill="#38251F")
d.text((1200, 552), "一覧表示（124px相当を3倍）", font=f, fill="#38251F")
S.save("reel_cover_check.png")
P
rm -f _reel_cover_*.png *.pdf
