#!/usr/bin/env bash
# blogger/theme.template.xml の /*@STYLE@*/ に assets/style.css を流し込んで
# ルートに blogger-theme.xml を出力します。
#
#   bash tools/build-blogger-theme.sh
#
# 出力された blogger-theme.xml を Blogger の
# 「テーマ → ⋮ → 復元」からアップロードしてください。
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import pathlib, sys, xml.dom.minidom

css = pathlib.Path("assets/style.css").read_text(encoding="utf-8")
tpl = pathlib.Path("blogger/theme.template.xml").read_text(encoding="utf-8")

if "/*@STYLE@*/" not in tpl:
    sys.exit("theme.template.xml に /*@STYLE@*/ が見つかりません")
if "]]>" in css:
    sys.exit("style.css に ]]> が含まれています（CDATA を壊すため使えません）")

# @charset は <b:skin> の中では無効なので落とす
css = css.replace('@charset "UTF-8";\n', "")

out = tpl.replace("/*@STYLE@*/", css)
pathlib.Path("blogger-theme.xml").write_text(out, encoding="utf-8")

# Blogger は厳密な XML を要求するので、ここで整形式かどうか検査する
xml.dom.minidom.parseString(out.encode("utf-8"))
print("OK: blogger-theme.xml を出力しました（XML 整形式チェック通過）")
PY
