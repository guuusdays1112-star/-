"""栞 サムネイル v3 — コピー比較用（写真・レイアウト固定、言葉だけを変える）

方針：写真は栞らしく、文字の強さは AYU さんの原則（全面写真・大きな太字・
わずかな傾き・特徴をひとつだけ）から学ぶ。装飾は署名と琥珀の線だけ。

使い方:
    python3 build.py ../source_photo.jpg
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build as v1  # noqa: E402
from build import add_line, add_picture, add_text, new_prs  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "out"
v1.ASSETS = OUT / "assets"

W, H = 1080, 1350
IVORY, BROWN, AMBER_ON_PHOTO = "F4EFE5", "38251F", "D9A877"
MINCHO = "Shippori Mincho"
TILT = -3  # 全案共通の傾き（栞の「動き」は控えめに）

# 入口の種類ごとのコピー。行ごとに (文字, サイズpx, x, y)
COPIES = {
    "1_発見": dict(entry="発見を入口に", lines=[
        ("いちじくが主役の", 100, 76, 168),
        ("フルーツサンド!", 116, 70, 290),
    ], line=(84, 458, 470, 438)),
    "2_気持ち": dict(entry="気持ちを入口に", lines=[
        ("絵を描きたくなる", 108, 76, 168),
        ("喫茶店。", 172, 286, 282),
    ], line=(296, 500, 760, 476)),
    "3_時間": dict(entry="時間を入口に", lines=[
        ("喫茶店で過ごす、", 100, 76, 168),
        ("ひとりの午後", 140, 156, 286),
    ], line=(166, 476, 600, 453)),
}


def design(slide, photo, ov, c):
    add_picture(slide, photo, 0, 0, W, H, "01_背景写真")
    add_picture(slide, ov, 0, 0, W, 760, "02_半透明オーバーレイ（上部）")
    add_text(slide, 80, 76, 700, 36, "栞｜関西の喫茶店記録", font=MINCHO, size=24,
             color=IVORY, spacing=5, name="03_署名（全投稿で固定）")
    for i, (text, size, x, y) in enumerate(c["lines"], 1):
        add_text(slide, x, y, W - x - 20, round(size * 1.3), text, font=MINCHO, size=size,
                 color=IVORY, spacing=-round(size * 0.05), bold=True, rotation=TILT,
                 name=f"0{3 + i}_メインタイトル（{i}行目）")
    x1, y1, x2, y2 = c["line"]
    add_line(slide, x1, y1, x2, y2, AMBER_ON_PHOTO, 5, "06_装飾線（琥珀）")


def main(src):
    v1.ASSETS.mkdir(parents=True, exist_ok=True)
    photo = v1.crop_photo(src, W, H, 0.82, "photo_4x5.jpg")
    ov = v1.gradient_overlay(W, 760, BROWN, 0.66, 0.0, "overlay_top.png", ease=1.3)
    prs = new_prs()
    for c in COPIES.values():
        design(prs.slides.add_slide(prs.slide_layouts[6]), photo, ov, c)
    prs.save(OUT / "shiori_v3_copy_test.pptx")


if __name__ == "__main__":
    main(sys.argv[1])
