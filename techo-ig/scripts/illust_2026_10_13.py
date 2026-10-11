#!/usr/bin/env python3
"""10/13「来年の手帳、3問で決まる」の仮イラスト。

    python3 scripts/illust_2026_10_13.py

本人のイラスト（illust/2026-10-13/NN.png）を置けば、そちらが優先される。
"""
from pathlib import Path

from illust_kit import PAPER, SHADE, SHU, SUMI, USU, Svg

OUT = Path(__file__).resolve().parent.parent / "illust" / "2026-10-13"


def p01():
    """表紙：厚さの違う3冊を前に迷う。"""
    s = Svg()
    specs = [(110, 140, 220, 360, 54, "1日1ページ"), (385, 170, 200, 330, 26, "週間"), (640, 190, 190, 310, 10, "日付なし")]
    for x, y, w, h, t, label in specs:
        s.book(x, y, w, h, thick=t)
        s.text(x + w / 2, 560 + 30, label, size=30, fill=USU)
    s.pill(475, 80, "どれにする？", size=34)
    s.path("M455 112 L475 136 L495 112", stroke=SHU, sw=0, fill=SHU)
    return s


def p02():
    """意志じゃなく相性：1〜2月は書いて、3月で白紙。"""
    s = Svg()
    x, y, w, h = 95, 60, 760, 500
    s.rect(x + 10, y + 12, w, h, fill=SHADE, r=14)
    s.rect(x, y, w, h, r=14)
    s.line(x + w / 2, y + 10, x + w / 2, y + h - 10, stroke=SUMI, sw=3)
    # 左ページ：書いてある
    lx = x + 50
    for i, d in enumerate(["1月", "2月"]):
        yy = y + 70 + i * 210
        s.text(lx, yy, d, size=32, anchor="start", font="heading")
        for k, ww in enumerate([280, 230, 260, 180]):
            s.line(lx, yy + 40 + k * 34, lx + ww, yy + 40 + k * 34, stroke=SUMI, sw=4)
    # 右ページ：白紙
    rx = x + w / 2 + 50
    s.text(rx, y + 70, "3月", size=32, anchor="start", fill=SHU, font="heading")
    s.page_lines(rx, y + 120, 280, 10, gap=34, stroke=SHADE, sw=2.5)
    s.circle(rx + 150, y + 300, 74, fill=PAPER, stroke=SHU, sw=5)
    s.text(rx + 150, y + 328, "？", size=80, fill=SHU)
    return s


def p03():
    """Q1：書く量で、厚さが決まる。"""
    s = Svg()
    s.book(120, 170, 250, 330, thick=70)
    s.page_lines(160, 230, 160, 7, gap=36, stroke=USU)
    s.pill(270, 80, "たくさん", size=32)
    s.text(270, 620, "1日1ページ", size=34)

    s.book(600, 210, 250, 300, thick=10)
    for r in range(4):
        for c in range(5):
            s.rect(628 + c * 40, 250 + r * 50, 34, 42, fill=PAPER, stroke=USU, sw=2, r=3)
    s.pill(725, 80, "少し", size=32)
    s.text(725, 620, "月1枚（マンスリー）", size=34)
    return s


def p04():
    """Q2：持ち歩くかで、重さが決まる。"""
    s = Svg()
    # バッグと薄い手帳
    s.path("M150 270 C150 170 310 170 310 270", sw=6)
    s.book(170, 160, 140, 200, thick=8)
    s.path("M90 270 L370 270 L340 520 L120 520 Z", fill=PAPER, sw=5)
    s.pill(230, 70, "毎日持つ", size=32)
    s.text(230, 600, "薄くて軽い", size=34)
    # 机と厚い手帳
    s.line(560, 470, 880, 470, stroke=SUMI, sw=6)
    s.line(600, 470, 600, 560, stroke=SUMI, sw=6)
    s.line(840, 470, 840, 560, stroke=SUMI, sw=6)
    s.rect(610, 390, 230, 80, fill=SHADE, r=10)
    s.rect(610, 380, 230, 30, fill=PAPER, r=8)
    s.line(800, 376, 800, 470, stroke=SHU, sw=7)
    s.pill(720, 70, "家だけ", size=32)
    s.text(720, 620, "厚くてもOK", size=34)
    return s


def p05():
    """Q3：書き方で、中身が決まる。"""
    s = Svg()
    s.rect(80, 120, 360, 430, r=12)
    s.dots(116, 156, 290, 360, step=29)
    s.path("M140 300 C190 250 250 340 320 280", stroke=SHU, sw=5)
    s.pill(260, 60, "自由に書く", size=32)
    s.text(260, 610, "無地・方眼", size=34)

    s.rect(510, 120, 360, 430, r=12)
    s.rect(540, 150, 300, 44, fill=SHADE, stroke=SHADE, sw=0, r=6)
    s.text(556, 182, "TODO", size=24, fill=SUMI, anchor="start")
    for i in range(4):
        s.check(548, 222 + i * 52, done=i < 2)
        s.line(592, 236 + i * 52, 820, 236 + i * 52, stroke=USU, sw=2.5)
    s.rect(540, 440, 300, 44, fill=SHADE, stroke=SHADE, sw=0, r=6)
    s.text(556, 472, "きょうの記録", size=24, fill=SUMI, anchor="start")
    s.pill(690, 60, "型があると安心", size=32)
    s.text(690, 610, "項目入り", size=34)
    return s


def p06():
    """ほぼ日手帳型：1日1ページに日記も予定も。"""
    s = Svg()
    x, y, w, h = 95, 50, 760, 540
    s.rect(x + 10, y + 12, w, h, fill=SHADE, r=14)
    s.rect(x, y, w, h, r=14)
    s.line(x + w / 2, y + 10, x + w / 2, y + h - 10, stroke=SUMI, sw=3)
    for side, day in ((0, "13 火"), (1, "14 水")):
        px = x + 40 + side * (w / 2)
        s.text(px, y + 64, day, size=34, anchor="start", font="heading")
        s.dots(px, y + 100, w / 2 - 80, h - 140, step=26)
    # 左：予定と日記
    s.check(x + 40, y + 120, done=True)
    s.line(x + 80, y + 133, x + 300, y + 133, stroke=SUMI, sw=4)
    s.check(x + 40, y + 166)
    s.line(x + 80, y + 179, x + 260, y + 179, stroke=SUMI, sw=4)
    for k, ww in enumerate([300, 280, 310, 200]):
        s.line(x + 40, y + 260 + k * 40, x + 40 + ww, y + 260 + k * 40, stroke=SUMI, sw=4)
    # 右：まだ余白
    s.line(x + w / 2 + 40, y + 133, x + w / 2 + 240, y + 133, stroke=SUMI, sw=4)
    return s


def p07():
    """ジブン手帳型：時間軸で生活ごと管理。"""
    s = Svg()
    x, y, w, h = 80, 40, 790, 560
    s.rect(x, y, w, h, r=14)
    days = ["月", "火", "水", "木", "金", "土", "日"]
    cw = (w - 90) / 7
    for i, d in enumerate(days):
        cx = x + 80 + i * cw
        s.text(cx + cw / 2, y + 50, d, size=28, fill=SHU if i >= 5 else SUMI)
        s.line(cx, y + 70, cx, y + h - 20, stroke=SHADE, sw=2)
    for k, hour in enumerate(range(8, 22, 2)):
        yy = y + 90 + k * 64
        s.text(x + 50, yy + 9, str(hour), size=22, fill=USU, weight=500)
        s.line(x + 80, yy, x + w - 10, yy, stroke=SHADE, sw=2)
    blocks = [(0, 1.0, 3.5), (1, 1.0, 3.5), (2, 1.0, 3.5), (3, 1.0, 3.5), (4, 1.0, 3.0),
              (0, 5.0, 0.7), (2, 5.5, 1.0), (4, 4.6, 1.4), (5, 2.0, 1.5), (6, 3.0, 2.0)]
    for col, start, length in blocks:
        bx = x + 80 + col * cw + 8
        by = y + 90 + start * 64
        work = start == 1.0
        s.rect(bx, by, cw - 16, length * 64, fill=SHADE if work else SHU, stroke="none", sw=0, r=6)
    return s


def p08():
    """MDノート型：日付なしだから、いつからでも。"""
    s = Svg()
    x, y, w, h = 150, 50, 560, 540
    s.rect(x + 12, y + 14, w, h, fill=SHADE, r=14)
    s.rect(x, y, w, h, r=14)
    s.text(x + 50, y + 90, "3/1", size=64, anchor="start", fill=SHU, font="heading")
    s.page_lines(x + 50, y + 150, w - 100, 10, gap=36, stroke=SHADE)
    s.line(x + 50, y + 186, x + 300, y + 186, stroke=SUMI, sw=4)
    s.line(x + 50, y + 222, x + 240, y + 222, stroke=SUMI, sw=4)
    # ペン
    s.path("M640 600 L860 260 L895 282 L675 622 Z", fill=PAPER, sw=5)
    s.path("M640 600 L675 622 L630 650 Z", fill=SUMI, sw=3)
    s.line(842 , 288, 877, 310, stroke=SHU, sw=6)
    return s


def main():
    for n, fn in enumerate([p01, p02, p03, p04, p05, p06, p07, p08], 1):
        fn().save(OUT / f"{n:02d}.svg")
    print(f"saved → {OUT}")


if __name__ == "__main__":
    main()
