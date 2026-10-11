#!/usr/bin/env python3
"""slides.json から 1080×1350 の PNG を書き出す。

使い方:
    python3 scripts/render.py 2026-10-13            # 1本
    python3 scripts/render.py 2026-10-13 2026-10-14 # 複数
    python3 scripts/render.py --check 2026-10-13    # 書き出さずにチェックだけ

エラー（書き出し中止）:
    - 1枚目が表紙でない／表紙に PR タグがない（affiliate: false の投稿を除く）
警告（書き出しは続行）:
    - 表紙コピー・見出しが15字超／本文が3行超／枚数が8〜10枚の範囲外
    - 文字のはみ出し・見出しの自動縮小・フォントの代替
    - キャプション冒頭の「#PR」、末尾の広告表記がない
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
BUILD = TEMPLATES / ".build"
POSTS = ROOT / "posts"
ILLUST = ROOT / "illust"

W, H = 1080, 1350
MAX_CHARS = 15
MAX_BODY_LINES = 3
AD_NOTICE = "※本投稿にはアフィリエイト広告を含みます"

SAVE_ICON = (
    '<svg class="save-icon" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linejoin="round">'
    '<path d="M6 3h12v18l-6-4.5L6 21z"/></svg>'
)


class RenderError(Exception):
    pass


def char_count(text: str) -> int:
    """見出しの字数。改行・空白は数えない。"""
    return len(re.sub(r"\s", "", text))


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def fill(template: str, values: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        return values.get(m.group(1), "")
    return re.sub(r"\{\{(\w+)\}\}", repl, template)


def body_html(lines: list[str]) -> str:
    out = []
    for line in lines:
        t = esc(line).replace("→", '<span class="arrow">→</span>')
        out.append(f"<p>{t}</p>")
    return "".join(out)


def find_illust(date: str, n: int) -> Path | None:
    d = ILLUST / date
    for name in (f"{n:02d}", str(n)):
        for ext in ("png", "jpg", "jpeg", "webp", "svg"):
            p = d / f"{name}.{ext}"
            if p.exists():
                return p
    return None


def illust_html(date: str, n: int, note: str | None, optional: bool = False) -> str:
    p = find_illust(date, n)
    if p and p.suffix == ".svg":
        # SVGは埋め込む（ページのZenフォントを文字に使うため）
        return f'<div class="illust">{p.read_text(encoding="utf-8")}</div>'
    if p:
        return f'<div class="illust"><img src="{p.as_uri()}" alt=""></div>'
    if optional and not note:
        return ""
    note_html = f'<p class="ph-note">{esc(note)}</p>' if note else ""
    return (
        '<div class="illust placeholder">'
        '<p class="ph-title">ILLUST</p>'
        f"{note_html}"
        f'<p class="ph-path">illust/{date}/{n:02d}.png</p>'
        "</div>"
    )


def validate(date: str, data: dict) -> tuple[list[str], list[str]]:
    errors, warns = [], []
    slides = data.get("slides", [])
    affiliate = data.get("affiliate", True)

    if not slides:
        errors.append("slides が空です")
        return errors, warns
    cover = slides[0]
    if cover.get("type") != "cover":
        errors.append("1枚目が表紙（type: cover）ではありません")
    elif affiliate and not cover.get("pr"):
        errors.append("表紙に PR タグがありません（\"pr\": true が必要）")
    if not affiliate:
        warns.append("affiliate: false の投稿です（PRタグ・広告表記なしで書き出し）")

    if not 8 <= len(slides) <= 10:
        warns.append(f"枚数が {len(slides)} 枚です（基準は8〜10枚）")
    if slides[-1].get("type") != "last":
        warns.append("最後のページが type: last ではありません")

    for i, s in enumerate(slides, 1):
        if s.get("type") == "cover":
            text = s.get("copy", "")
            if char_count(text) > MAX_CHARS:
                warns.append(f"{i:02d} 表紙コピーが {char_count(text)} 字です（15字以内）: {text!r}")
        else:
            text = s.get("heading", "")
            if not text:
                warns.append(f"{i:02d} 見出しが空です")
            if char_count(text) > MAX_CHARS:
                warns.append(f"{i:02d} 見出しが {char_count(text)} 字です（15字以内）: {text!r}")
            body = s.get("body", [])
            if len(body) > MAX_BODY_LINES:
                warns.append(f"{i:02d} 本文が {len(body)} 行です（3行以内）")

    cap_path = POSTS / date / "caption.txt"
    if not cap_path.exists():
        warns.append("caption.txt がありません")
    elif affiliate:
        cap = cap_path.read_text(encoding="utf-8").strip()
        if not cap.startswith("#PR"):
            warns.append("キャプション冒頭に「#PR」がありません")
        tail = "\n".join(cap.splitlines()[-3:])
        if AD_NOTICE not in tail:
            warns.append(f"キャプション末尾に「{AD_NOTICE}」がありません")
    return errors, warns


def build_html(date: str, data: dict, config: dict) -> list[str]:
    tpl = {k: (TEMPLATES / f"{k}.html").read_text(encoding="utf-8") for k in ("cover", "page", "last")}
    total = len(data["slides"])
    handle = esc(config.get("handle", ""))
    pages = []
    for i, s in enumerate(data["slides"], 1):
        kind = s.get("type", "page")
        page_no = f"<b>{i}</b>/{total}"
        illust = illust_html(date, i, s.get("illust", ""), optional=kind == "last")
        if kind == "cover":
            copy = "".join(f"<span>{esc(line)}</span>" for line in s.get("copy", "").split("\n"))
            values = {
                "pr_tag": "PR" if s.get("pr") else "",
                "copy": copy,
                "sub": esc(s.get("sub", "")),
                "illust": illust,
                "save_icon": SAVE_ICON.format(s=34),
                "footer": esc(s.get("footer", "保存して売り場へ")),
                "handle": handle,
            }
            out = fill(tpl["cover"], values)
            if not s.get("pr"):
                out = out.replace('<div class="pr-tag" data-check="pr"></div>', "")
        elif kind == "last":
            values = {
                "page_no": page_no,
                "save_icon_large": SAVE_ICON.format(s=120),
                "heading": esc(s.get("heading", "")),
                "body": body_html(s.get("body", [])),
                "illust": illust,
                "cta": esc(s.get("cta", "紹介品はプロフィールのリンクから")),
                "handle": handle,
            }
            out = fill(tpl["last"], values)
            if not illust:
                out = out.replace('class="slide last"', 'class="slide last no-illust"')
        else:
            label = s.get("label")
            values = {
                "page_no": page_no,
                "label": f'<p class="label">{esc(label)}</p>' if label else "",
                "heading": esc(s.get("heading", "")),
                "body": body_html(s.get("body", [])),
                "illust": illust,
            }
            out = fill(tpl["page"], values)
        pages.append(out)
    return pages


# ページ内で実行するレイアウト調整とチェック
FIT_JS = r"""
async () => {
  await document.fonts.ready;
  const warns = [];
  const fonts = {};
  for (const f of document.fonts) {
    if (f.family.replace(/"/g, '') === 'Heading' || f.family.replace(/"/g, '') === 'Body') {
      fonts[f.family.replace(/"/g, '') + ' ' + f.weight] = f.status;
    }
  }
  const slide = document.querySelector('.slide');
  const innerW = slide.clientWidth - 2 * 64;

  // 見出し：1行に収まるまで縮小（下限56px）
  const shrink = (el, min, name) => {
    let size = parseFloat(getComputedStyle(el).fontSize);
    const start = size;
    while (el.scrollWidth > innerW && size > min) {
      size -= 2;
      el.style.fontSize = size + 'px';
    }
    if (el.scrollWidth > innerW) warns.push(name + 'が横にはみ出しています');
    else if (size < start) warns.push(name + 'を ' + start + 'px → ' + size + 'px に縮小しました');
  };
  const copy = document.querySelector('[data-fit=copy]');
  if (copy) {
    let size = 96;
    const tooWide = () => [...copy.children].some(s => s.scrollWidth > innerW);
    while (tooWide() && size > 56) { size -= 2; copy.style.fontSize = size + 'px'; }
    if (tooWide()) warns.push('表紙コピーが横にはみ出しています');
    else if (size < 96) warns.push('表紙コピーを 96px → ' + size + 'px に縮小しました（改行位置の見直し推奨）');
    const area = document.querySelector('.copy-area');
    if (area.scrollHeight > area.clientHeight + 1) warns.push('表紙コピーが上1/3に収まっていません');
  }
  const heading = document.querySelector('[data-fit=heading]');
  if (heading) shrink(heading, 56, '見出し');

  const body = document.querySelector('[data-fit=body]');
  if (body) {
    for (const p of body.querySelectorAll('p')) {
      if (p.scrollWidth > innerW) warns.push('本文の行がはみ出しています: ' + p.textContent);
    }
  }

  // キャンバス外へのはみ出し
  for (const el of slide.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (r.right > 1080.5 || r.bottom > 1350.5 || r.left < -0.5 || r.top < -0.5) {
      const cls = typeof el.className === 'string' ? el.className : '';
      warns.push('画面外にはみ出し: ' + el.tagName.toLowerCase() + (cls ? '.' + cls : ''));
      break;
    }
  }
  const ill = document.querySelector('.illust');
  if (ill && ill.clientHeight < 280) warns.push('イラスト枠が小さすぎます（高さ ' + ill.clientHeight + 'px）');

  return { warns, fonts };
}
"""


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:
        candidates = [os.environ.get("CHROMIUM_PATH", "")]
        candidates += sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True)
        for c in candidates:
            if c and Path(c).exists():
                return p.chromium.launch(executable_path=c)
        raise


def render(date: str, check_only: bool = False) -> bool:
    post_dir = POSTS / date
    slides_path = post_dir / "slides.json"
    if not slides_path.exists():
        print(f"[{date}] ERROR: {slides_path.relative_to(ROOT)} がありません")
        return False
    data = json.loads(slides_path.read_text(encoding="utf-8"))
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

    errors, warns = validate(date, data)
    print(f"[{date}] {data.get('title', '')}  status={data.get('status', '-')}")
    for w in warns:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print("  → 書き出しを中止しました")
        return False
    if check_only:
        return True

    from playwright.sync_api import sync_playwright

    out_dir = post_dir / "out"
    if out_dir.exists():
        for old in out_dir.glob("*.png"):
            old.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(exist_ok=True)

    pages = build_html(date, data, config)
    font_report: dict[str, str] = {}
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, doc in enumerate(pages, 1):
            tmp = BUILD / f"{date}-{i:02d}.html"
            base = f'<head>\n<base href="{TEMPLATES.as_uri()}/">'
            tmp.write_text(doc.replace("<head>", base, 1), encoding="utf-8")
            page.goto(tmp.as_uri())
            res = page.evaluate(FIT_JS)
            font_report.update(res["fonts"])
            for w in res["warns"]:
                print(f"  WARN  {i:02d} {w}")
            page.screenshot(path=str(out_dir / f"{i:02d}.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
        browser.close()
    shutil.rmtree(BUILD, ignore_errors=True)

    bad = {k: v for k, v in font_report.items() if v != "loaded"}
    if not font_report or bad:
        print(f"  WARN  Zenフォントが読めず代替書体（Noto/システム）で書き出しました: {bad or 'フォント未検出'}")
    print(f"  OK    {len(pages)} 枚 → {out_dir.relative_to(ROOT)}/")
    return True


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    dates = [a for a in argv if not a.startswith("--")]
    if not dates:
        print(__doc__)
        return 2
    ok = all([render(d, check_only) for d in dates])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
