"""栞 リール表紙 9:16（1080×1920）— 10/13「いちじくが主役のフルーツサンド！」

「強い白文字 × 栞らしい写真」。文字はプロフィールグリッドの 3:4 切り抜き
（中央 1080×1440 = y240〜1680）とリール再生画面の UI を避けた範囲に置く。

使い方:
    python3 build.py ../source_photo.jpg
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build as v1  # noqa: E402
from build import add_line, add_picture, add_text, new_prs, px  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "out"
v1.ASSETS = OUT / "assets"

W, H = 1080, 1920
IVORY, BROWN, AMBER_ON_PHOTO = "F4EFE5", "38251F", "D9A877"
MINCHO = "Shippori Mincho"
TILT = -3

COVERS = {
    "fig_sandwich": dict(lines=[
        ("いちじくが主役の", 104, 72, 372),
        ("フルーツサンド!", 120, 62, 498),
    ], line=(80, 672, 480, 651)),
    "template": dict(lines=[
        ("ひとことの特徴、", 104, 72, 372),
        ("主役の名前!", 120, 62, 498),
    ], line=(80, 672, 480, 651)),
}


def cover(slide, photo, ov, c):
    add_picture(slide, photo, 0, 0, W, H, "01_背景写真")
    add_picture(slide, ov, 0, 0, W, 1100, "02_半透明オーバーレイ（上部）")
    add_text(slide, 80, 300, 700, 36, "栞｜関西の喫茶店記録", font=MINCHO, size=26,
             color=IVORY, spacing=5, name="03_署名（全投稿で固定）")
    for i, (text, size, x, y) in enumerate(c["lines"], 1):
        add_text(slide, x, y, W - x - 20, round(size * 1.3), text, font=MINCHO, size=size,
                 color=IVORY, spacing=-round(size * 0.05), bold=True, rotation=TILT,
                 name=f"0{3 + i}_メインタイトル（{i}行目）")
    x1, y1, x2, y2 = c["line"]
    add_line(slide, x1, y1, x2, y2, AMBER_ON_PHOTO, 6, "06_装飾線（琥珀）")


def main(src):
    v1.ASSETS.mkdir(parents=True, exist_ok=True)
    photo = v1.crop_photo(src, W, H, 0.5, "photo_9x16.jpg")
    ov = v1.gradient_overlay(W, 1100, BROWN, 0.62, 0.0, "overlay_top_reel.png", ease=1.25)
    for name, c in COVERS.items():
        prs = new_prs()
        prs.slide_width, prs.slide_height = px(W), px(H)
        cover(prs.slides.add_slide(prs.slide_layouts[6]), photo, ov, c)
        prs.save(OUT / f"reel_cover_{name}.pptx")


if __name__ == "__main__":
    main(sys.argv[1])
