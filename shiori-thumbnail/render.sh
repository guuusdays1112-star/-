#!/bin/sh
# PPTX を LibreOffice で描画し、プレビュー PNG と比較画像を作る
set -e
cd "$(dirname "$0")"
python3 build.py source_photo.jpg
cd out
soffice --headless --convert-to pdf shiori_thumbnails_ABC.pptx >/dev/null 2>&1
soffice --headless --convert-to pdf shiori_template.pptx >/dev/null 2>&1
pdftoppm -r 96 -png shiori_thumbnails_ABC.pdf _abc
pdftoppm -r 96 -png shiori_template.pdf _tpl
python3 ../compose.py
rm -f _abc-*.png _tpl-*.png *.pdf
