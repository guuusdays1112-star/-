"""栞 サムネイル v2 —「強い入口 × 静かな余韻」A/B/C 案 + テンプレート

v1 (../build.py) の PPTX ヘルパーを流用し、写真・タイトル・サブ・装飾線・
オーバーレイ・ラベルをすべて独立オブジェクトとして 1080×1350px 相当に配置する。

使い方:
    python3 build.py ../source_photo.jpg
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build as v1  # noqa: E402
from build import add_line, add_picture, add_rect, add_text, new_prs  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "out"
v1.ASSETS = OUT / "assets"  # 素材の書き出し先を v2 に向ける

W, H = 1080, 1350

# ── カラー（指定パレット） ───────────────────────
IVORY = "F4EFE5"
BROWN = "38251F"
AMBER = "B77B43"
BORDEAUX = "75464D"
AMBER_ON_PHOTO = "D9A877"  # 写真の暗部に乗せる琥珀（#B77B43 を明度だけ上げたもの）

# ── フォント（Canva で同名認識を確認済み：ファミリー名 + 太字フラグ） ──
MINCHO = "Shippori Mincho"
LATIN = "Cormorant Garamond"


def design_a(slide, photo, ov, c):
    """A案｜大胆なタイポグラフィ。3行の大小で「絵を→描きたくなる→喫茶店！」と
    視線を加速させ、最後の一語を最大にする。"""
    add_picture(slide, photo, 0, 0, W, H, "01_背景写真")
    add_picture(slide, ov, 0, 0, W, 720, "02_半透明オーバーレイ（上部）")
    add_rect(slide, 80, 72, 214, 46, BORDEAUX, name="03_ラベル地（ボルドー）")
    add_text(slide, 80, 72, 214, 46, c["label"], font=MINCHO, size=24, color=IVORY,
             spacing=6, align="c", anchor="m", name="04_ラベル文字")
    add_text(slide, 76, 140, 600, 120, c["title"][0], font=MINCHO, size=100, color=IVORY,
             spacing=-2, bold=True, name="05_メインタイトル（1行目）")
    add_text(slide, 70, 252, 960, 170, c["title"][1], font=MINCHO, size=148, color=IVORY,
             spacing=-8, bold=True, name="06_メインタイトル（2行目）")
    add_text(slide, 200, 404, 860, 210, c["title"][2], font=MINCHO, size=188, color=IVORY,
             spacing=-10, bold=True, name="07_メインタイトル（3行目）")
    add_line(slide, 212, 628, 600, 628, AMBER_ON_PHOTO, 6, "08_装飾線（琥珀）")
    add_text(slide, 316, 79, 720, 36, c["sub"], font=MINCHO, size=26, color=IVORY,
             spacing=4, name="09_サブタイトル")


def design_b(slide, photo, ov, c):
    """B案｜エディトリアル。雑誌の表紙のように誌名（栞）・号・写真・特集見出しを組む。"""
    add_rect(slide, 0, 0, W, H, IVORY, name="01_背景（アイボリー）")
    add_text(slide, 56, 44, 200, 150, c["masthead"], font=MINCHO, size=128, color=BROWN,
             bold=True, name="02_誌名（栞）")
    add_text(slide, 236, 74, 500, 40, c["kicker"], font=MINCHO, size=26, color=BROWN,
             spacing=6, name="03_誌名サブ")
    add_text(slide, 236, 118, 500, 34, c["eyebrow"], font=LATIN, size=22, color=AMBER,
             spacing=6, name="04_欧文（号表記）")
    add_text(slide, 700, 118, 324, 34, c["issue"], font=LATIN, size=22, color=AMBER,
             spacing=6, align="r", name="05_号数")
    add_line(slide, 56, 196, 1024, 196, BROWN, 2, "06_装飾線（誌名下）")
    add_picture(slide, photo, 56, 222, 968, 820, "07_写真")
    add_rect(slide, 56, 222, 968, 820, BROWN, alpha=0.05, name="08_半透明オーバーレイ（写真の締め）")
    add_text(slide, 56, 1074, 700, 110, c["title"][0], font=MINCHO, size=84, color=BROWN,
             spacing=2, bold=True, name="09_メインタイトル（1行目）")
    add_text(slide, 152, 1178, 760, 110, c["title"][1], font=MINCHO, size=84, color=BROWN,
             spacing=2, bold=True, name="10_メインタイトル（2行目）")
    add_line(slide, 820, 1112, 1024, 1112, AMBER, 2, "11_装飾線（特集）")
    add_text(slide, 760, 1126, 264, 80, c["sub"], font=MINCHO, size=22, color=BROWN,
             spacing=3, line_height=1.5, align="r", name="12_サブタイトル")


def design_c(slide, photo, ov, c):
    """C案｜01×03 の融合。写真の上に大きな見出し（入口）、アイボリーの額縁と
    署名帯で余韻をつくる。"""
    add_rect(slide, 0, 0, W, H, IVORY, name="01_背景（アイボリーの額縁）")
    add_picture(slide, photo, 36, 36, 1008, 1196, "02_背景写真")
    add_picture(slide, ov, 36, 36, 1008, 640, "03_半透明オーバーレイ（上部）")
    add_text(slide, 84, 92, 700, 120, c["title"][0], font=MINCHO, size=92, color=IVORY,
             spacing=0, bold=True, name="04_メインタイトル（1行目）")
    add_text(slide, 74, 198, 960, 160, c["title"][1], font=MINCHO, size=132, color=IVORY,
             spacing=-6, bold=True, name="05_メインタイトル（2行目）")
    add_line(slide, 88, 395, 148, 395, AMBER_ON_PHOTO, 3, "06_装飾線（琥珀）")
    add_text(slide, 166, 374, 800, 46, c["sub"], font=MINCHO, size=34, color=IVORY,
             spacing=5, name="07_サブタイトル")
    add_text(slide, 56, 1252, 560, 70, c["sign"], font=MINCHO, size=26, color=BROWN,
             spacing=5, anchor="m", name="08_署名（栞）")
    add_text(slide, 524, 1252, 380, 70, c["eyebrow"], font=LATIN, size=22, color=AMBER,
             spacing=6, align="r", anchor="m", name="09_欧文")
    add_rect(slide, 918, 1265, 106, 44, BORDEAUX, name="10_号数の地（ボルドー）")
    add_text(slide, 918, 1265, 106, 44, c["issue"], font=LATIN, size=24, color=IVORY,
             spacing=2, align="c", anchor="m", bold=True, name="11_号数（投稿番号）")


COPY = {
    "A": dict(label="関西の純喫茶", title=["絵を", "描きたくなる", "喫茶店!"],
              sub="いちじくのフルーツサンドと、スケッチ帳"),
    "B": dict(masthead="栞", kicker="関西の喫茶店記録", eyebrow="KISSATEN NOTES",
              issue="2026 AUTUMN", title=["喫茶店で、", "絵を描く午後。"],
              sub="いちじくのフルーツサンド\n珈琲と、スケッチ帳"),
    "C": dict(title=["いちじくの", "フルーツサンド"], sub="珈琲と、スケッチの午後。",
              sign="栞｜関西の喫茶店記録", eyebrow="KISSATEN NOTES", issue="No.91"),
}
TEMPLATE_COPY = {
    "A": dict(label="関西の純喫茶", title=["短い", "テーマの言葉", "喫茶店!"],
              sub="サブ：主役のメニュー"),
    "B": dict(masthead="栞", kicker="関西の喫茶店記録", eyebrow="KISSATEN NOTES",
              issue="SEASON / YEAR", title=["一行目の言葉、", "二行目の余韻。"],
              sub="サブ：メニュー名\n店名・街"),
    "C": dict(title=["主役の", "メニュー名"], sub="過ごし方の、ひとこと。",
              sign="栞｜関西の喫茶店記録", eyebrow="KISSATEN NOTES", issue="No.00"),
}
SERIES_MOCK = [  # シリーズ展開イメージ：同じ写真の別トリミングで仮置き（実投稿ではない）
    (1.00, 1.0, dict(title=["いちじくの", "フルーツサンド"], sub="珈琲と、スケッチの午後。")),
    (0.55, 0.0, dict(title=["一杯の", "ブレンド珈琲"], sub="まっすぐ帰れない日に。")),
    (0.60, 0.3, dict(title=["琥珀色の", "灯りの下で"], sub="ひとり時間の、栞。")),
]
LAYOUT = {"A": design_a, "B": design_b, "C": design_c}


def main(src):
    v1.ASSETS.mkdir(parents=True, exist_ok=True)
    full = v1.crop_photo(src, W, H, 0.82, "photo_4x5.jpg")
    mag = v1.crop_photo(src, 968, 820, 1.0, "photo_magazine.jpg")
    framed = v1.crop_photo(src, 1008, 1196, 1.0, "photo_framed.jpg")
    ov_a = v1.gradient_overlay(W, 720, BROWN, 0.70, 0.0, "overlay_top_A.png", ease=1.3)
    ov_c = v1.gradient_overlay(1008, 640, BROWN, 0.66, 0.0, "overlay_top_C.png", ease=1.4)
    photos = {"A": (full, ov_a), "B": (mag, None), "C": (framed, ov_c)}

    for fname, copy in (("shiori_v2_ABC.pptx", COPY), ("shiori_v2_template.pptx", TEMPLATE_COPY)):
        prs = new_prs()
        for key in "ABC":
            LAYOUT[key](prs.slides.add_slide(prs.slide_layouts[6]), *photos[key], copy[key])
        prs.save(OUT / fname)
    for key in "ABC":
        prs = new_prs()
        LAYOUT[key](prs.slides.add_slide(prs.slide_layouts[6]), *photos[key], COPY[key])
        prs.save(OUT / f"shiori_v2_{key}.pptx")

    # シリーズ展開イメージ（グリッドの統一感確認用。納品物ではない）
    prs = new_prs()
    for i, (scale, y_anchor, copy) in enumerate(SERIES_MOCK):
        p = mock_crop(src, scale, y_anchor, f"mock_{i}.jpg")
        LAYOUT["C"](prs.slides.add_slide(prs.slide_layouts[6]), p, ov_c,
                    dict(COPY["C"], issue=f"No.{91 - i}", **copy))
    prs.save(OUT / "_series_mock.pptx")


def mock_crop(src, scale, y_anchor, name):
    """モック用：写真の一部を拡大トリミング（scale=元幅に対する切り出し幅）。"""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    cw = round(sw * scale)
    ch = round(cw * 1196 / 1008)
    x0 = (sw - cw) // 2 if y_anchor == 1.0 else round((sw - cw) * 0.15)
    y0 = round((sh - ch) * (y_anchor if y_anchor != 0.0 else 0.55))
    y0 = max(0, min(y0, sh - ch))
    path = v1.ASSETS / name
    im.crop((x0, y0, x0 + cw, y0 + ch)).save(path, quality=92)
    return path


if __name__ == "__main__":
    main(sys.argv[1])
