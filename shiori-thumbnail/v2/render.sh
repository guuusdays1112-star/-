#!/bin/sh
# v2: build → LibreOffice で PPTX を描画 → プレビュー・比較・グリッド縮小・シリーズ確認
set -e
cd "$(dirname "$0")"
python3 build.py ../source_photo.jpg
cd out
for f in shiori_v2_ABC shiori_v2_template _series_mock; do
  soffice --headless --convert-to pdf "$f.pptx" >/dev/null 2>&1
  pdftoppm -r 96 -png "$f.pdf" "_$f"
done
python3 ../compose.py
rm -f _shiori_v2_*.png __series_mock-*.png *.pdf _series_mock.pptx
