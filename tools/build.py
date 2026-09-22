#!/usr/bin/env python3
"""src/sections.html（本文の唯一の出典）から
   - index.html        … 静的HTML版
   - blogger-theme.xml … Bloggerテーマ
の両方を生成する。

  python3 tools/build.py

本文を直すときは src/sections.html を、
見た目を直すときは assets/style.css を編集してこれを実行する。
"""
import pathlib, re, sys, xml.dom.minidom

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def strip_markers(s, *names):
    """<!--NAME:START--> … <!--NAME:END--> の囲みだけ外して中身は残す"""
    for n in names:
        s = s.replace(f"<!--{n}:START-->", "").replace(f"<!--{n}:END-->", "")
    return s


def drop_blocks(s, *names):
    """<!--NAME:START--> … <!--NAME:END--> を中身ごと削除"""
    for n in names:
        s = re.sub(rf"<!--{n}:START-->.*?<!--{n}:END-->", "", s, flags=re.S)
    return s


def to_xml(s):
    """Blogger は厳密な XML を要求するので、HTML の書き方を寄せる"""
    s = re.sub(r"<!--(?!\[).*?-->", "", s, flags=re.S)          # コメントは全部落とす
    s = re.sub(r"<(br|hr|img|input|meta|link)(\s[^<>]*?)?>", r"<\1\2/>", s)  # 空要素を閉じる
    s = s.replace("&nbsp;", "&#160;")                            # XML に nbsp 実体は無い
    s = re.sub(r"&(?!(?:[a-zA-Z][a-zA-Z0-9]*|#\d+|#x[0-9a-fA-F]+);)", "&amp;", s)
    return s


def main():
    sections = read("src/sections.html")
    css = read("assets/style.css")

    # ---- 静的HTML版 ----
    static = strip_markers(sections, "HOMEONLY", "STATIC")
    static = drop_blocks(static, "BLOGGER")
    static = static.replace("{{HOME}}", "")
    page = read("src/page.template.html").replace("<!--@BODY@-->", static.strip())
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    # ---- Bloggerテーマ ----
    blog = drop_blocks(sections, "STATIC")
    blog = re.sub(
        r"<!--HOMEONLY:START-->(.*?)<!--HOMEONLY:END-->",
        lambda m: "<b:if cond='data:blog.url == data:blog.homepageUrl'>"
                  + m.group(1) + "</b:if>",
        blog, flags=re.S,
    )
    blog = to_xml(blog).replace("{{HOME}}", "/")

    if "]]>" in css:
        sys.exit("style.css に ]]> が含まれています（CDATA を壊します）")
    skin = css.replace('@charset "UTF-8";\n', "")   # @charset は b:skin 内では無効

    theme = (read("blogger/theme.template.xml")
             .replace("/*@STYLE@*/", skin)
             .replace("<!--@BODY@-->", blog.strip()))
    (ROOT / "blogger-theme.xml").write_text(theme, encoding="utf-8")
    xml.dom.minidom.parseString(theme.encode("utf-8"))   # 整形式チェック

    print("OK: index.html と blogger-theme.xml を生成しました（XML 整形式チェック通過）")


if __name__ == "__main__":
    main()
