"""仮イラスト（線画SVG）を作るための部品。

本人のイラストが届くまでの「つなぎ」。商品のロゴや公式画像は描かない。
描いたSVGは illust/<投稿日>/NN.svg に保存し、render.py がページに埋め込む
（同じ番号の .png / .jpg を置けば、そちらが優先される）。
"""
from __future__ import annotations

from html import escape
from pathlib import Path

SUMI = "#2B2B2B"
SHU = "#C8553D"
USU = "#8A8478"
PAPER = "#FBF8F2"
SHADE = "#E8E0D2"

VW, VH = 950, 640


class Svg:
    def __init__(self, w: int = VW, h: int = VH):
        self.w, self.h = w, h
        self.parts: list[str] = []

    def add(self, s: str) -> "Svg":
        self.parts.append(s)
        return self

    def rect(self, x, y, w, h, fill=PAPER, stroke=SUMI, sw=4, r=10, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=USU, sw=3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>')

    def path(self, d, stroke=SUMI, sw=4, fill="none"):
        return self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"/>')

    def circle(self, cx, cy, r, fill="none", stroke=SUMI, sw=4):
        return self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=30, fill=SUMI, anchor="middle", weight=700, font="body"):
        fam = '"Heading", serif' if font == "heading" else '"Body", sans-serif'
        return self.add(
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f"font-weight=\"{weight}\" font-family='{fam}'>{escape(s)}</text>"
        )

    # ---- 部品 ----

    def book(self, x, y, w, h, thick=16, band=True, title=None):
        """閉じた手帳（右下に厚み）。"""
        self.rect(x + thick, y + thick, w, h, fill=SHADE, r=12)
        self.rect(x, y, w, h, fill=PAPER, r=12)
        if band:
            self.line(x + w - 34, y - 2, x + w - 34, y + h + 2, stroke=SHU, sw=7)
        if title:
            self.text(x + w / 2 - 14, y + h / 2 + 10, title, size=28, fill=USU)
        return self

    def page_lines(self, x, y, w, n, gap=34, stroke=USU, sw=2.5):
        for i in range(n):
            self.line(x, y + i * gap, x + w, y + i * gap, stroke=stroke, sw=sw)
        return self

    def dots(self, x, y, w, h, step=28):
        cx = x
        while cx <= x + w:
            cy = y
            while cy <= y + h:
                self.add(f'<circle cx="{cx}" cy="{cy}" r="2.4" fill="{USU}"/>')
                cy += step
            cx += step
        return self

    def check(self, x, y, s=26, done=False):
        self.rect(x, y, s, s, fill=PAPER, sw=3, r=4)
        if done:
            self.path(f"M{x+5} {y+s/2} L{x+s/2-2} {y+s-6} L{x+s+6} {y-6}", stroke=SHU, sw=4)
        return self

    def arrow(self, x1, y1, x2, y2, stroke=SHU, sw=5):
        import math
        self.line(x1, y1, x2, y2, stroke=stroke, sw=sw)
        a = math.atan2(y2 - y1, x2 - x1)
        L = 20
        p1 = (x2 - L * math.cos(a - 0.5), y2 - L * math.sin(a - 0.5))
        p2 = (x2 - L * math.cos(a + 0.5), y2 - L * math.sin(a + 0.5))
        return self.path(f"M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}", stroke=stroke, sw=sw)

    def pill(self, cx, cy, s, size=30, fill=SHU, color="#FFFFFF", pad=26):
        w = len(s) * size + pad * 2
        h = size + 28
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=fill, sw=0, r=h / 2)
        return self.text(cx, cy + size * 0.36, s, size=size, fill=color)

    def render(self) -> str:
        body = "\n  ".join(self.parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img">\n  {body}\n</svg>\n'
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(), encoding="utf-8")
