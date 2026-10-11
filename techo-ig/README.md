# techo-ig（てもと手帳室）

指示書は [CLAUDE.md](CLAUDE.md)。ここは使い方のメモ。

## 毎日の流れ

1. 前日の夜：`illust/<投稿日>/NN.png` にイラストを置く（NN はページ番号 01〜09）。
2. Claude Code に「<投稿日> を書き出して」と頼む（中身は下のコマンド）。
3. `posts/<投稿日>/out/01.png〜09.png` と `caption.txt` をスマホに送って投稿。

```
pip install playwright
python3 scripts/render.py 2026-10-13            # 書き出し
python3 scripts/render.py --check 2026-10-13    # チェックだけ
```

## フォルダ

| 場所 | 中身 |
|---|---|
| `posts/<日付>/slides.json` | 各ページの文言。`status` が `ready` なら確定、`要確認` は本人の確認待ち |
| `posts/<日付>/caption.txt` | キャプション（そのまま貼る） |
| `posts/<日付>/products.md` | 紹介商品の現行品・価格メモ |
| `posts/<日付>/out/` | 書き出したPNG（1080×1350） |
| `illust/<日付>/` | イラスト。`NN.png` / `NN.jpg` を置くとそれが使われる。なければ `NN.svg`（Claude Codeの仮イラスト）、それもなければ点線枠 |
| `templates/` | 表紙・中ページ・最終ページのHTML/CSSとフォント |
| `config.json` | アカウント名・ID。確定したら書き換えて再書き出し |

## slides.json の書き方

```json
{ "type": "cover", "copy": "来年の手帳、\n3問で決まる", "sub": "小さい一文", "pr": true, "illust": "描いてほしい絵のメモ" }
{ "type": "page", "label": "Q1", "heading": "15字以内の見出し", "body": ["1行目", "2行目", "3行目まで"], "illust": "..." }
{ "type": "last", "heading": "まとめの一言", "body": ["保存の呼びかけ"], "cta": "紹介品はプロフィールのリンクから" }
```

- `copy` の `\n` が表紙の改行位置。`body` の「→」は朱色になる。
- 紹介商品のない回は `"affiliate": false` にすると、PRタグと広告表記なしで書き出せる（それ以外で表紙に PR がないとエラー）。
- 見出しは1行に収まらないと自動で縮小し、警告を出す。

## フォント

`templates/fonts/` に Zen Old Mincho Bold／Zen Kaku Gothic New（Medium・Bold）を同梱（Google Fonts の配布元 google/fonts から取得、SIL Open Font License）。読めない場合は Noto Serif JP／Noto Sans JP に切り替わり、render.py が警告を出す。
