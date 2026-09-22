# ガラス工房 nazuna薺 ウェブサイト

京都・西陣のガラス工房「ガラス工房 nazuna薺」のウェブサイトです。
ビルド不要の静的サイト（HTML / CSS / JavaScript）で、依存ライブラリはありません。

## ページ構成

| ファイル | 内容 |
|---|---|
| `index.html` | トップページ（はじめての方へ・体験の抜粋・作品・工房・アクセス） |
| `experience.html` | 体験メニュー一覧、当日の流れ、注意事項、よくあるご質問 |
| `works.html` | 作品ギャラリー、作品の購入先 |
| `about.html` | 工房の紹介、制作のテーマ、これまでの歩み、工房概要 |
| `access.html` | 地図・アクセス・お問い合わせ |

共通パーツ（ヘッダー／フッター）は各 HTML に直接書かれています。
リンクやメニューを増やすときは、5ファイルすべてを同じように直してください。

## ディレクトリ

```
.
├── index.html / experience.html / works.html / about.html / access.html
├── assets/
│   ├── css/style.css   … 全ページ共通のスタイル
│   ├── js/main.js      … メニュー開閉とスクロール表示のみ
│   └── img/            … 画像（現在はすべてプレースホルダーの SVG）
├── robots.txt
└── sitemap.xml
```

## 公開前にかならず差し替えるもの

1. **ドメイン**
   `https://example.com` を実際の公開先 URL に置き換えてください。
   対象：各 HTML の `<link rel="canonical">`・`og:url`・`og:image`・JSON-LD の `url`、
   `robots.txt`、`sitemap.xml`。

   ```sh
   # 例：https://nazuna-glass.example.jp に置き換える場合
   grep -rl 'https://example.com' . --include='*.html' --include='*.txt' --include='*.xml' \
     | xargs sed -i 's#https://example\.com#https://nazuna-glass.example.jp#g'
   ```

2. **写真**
   `assets/img/` の SVG は、色と文字だけの仮画像です。
   同じファイル名で `.jpg` / `.webp` を置き、HTML 側の `src` の拡張子を直してください。
   推奨サイズの目安：

   | 用途 | ファイル | 目安 |
   |---|---|---|
   | トップの大きな写真 | `hero.svg` | 横長 4:3・1280px 以上 |
   | 工房の外観 | `studio.svg` | 縦長 |
   | 作業風景 | `studio-wide.svg` | 横長 16:9 |
   | 体験メニュー | `menu-*.svg` | 4:3 |
   | 作品 | `work-*.svg` | 正方形 |
   | SNS シェア画像 | `ogp.svg` | 1200×630 |

   画像を差し替えたら、`alt` 属性の説明文も実際の写真に合わせて書き直してください。

3. **掲載内容の確認**
   住所・電話番号・営業時間・定休日・体験メニューの料金と所要時間は、
   公開されている予約サイトや情報サイトの掲載内容をもとに作成しています。
   公開前に、工房の最新の情報と照らし合わせてご確認ください。
   紹介文（工房の説明文、作品の説明、これまでの歩み）は、
   実際に書きたい文章に差し替えていただく前提の下書きです。

## 掲載情報

- 住所：〒602-8164 京都府京都市上京区十四軒町413-45
- 電話：090-8368-3756
- 営業時間：10:00–17:00
- 定休日：水曜・木曜・金曜
- 予約：select-type の予約ページへ外部リンク
- SNS・販売：Instagram / minne / Creema

体験メニューと料金は `experience.html` の一覧、
およびトップページの抜粋（3件）の2か所に書かれています。
料金を変えるときは、両方を直してください。

## ローカルでの確認

ビルドは不要です。ファイルを直接ブラウザで開いても表示できますが、
簡易サーバーを立てたほうが実際の公開環境に近い状態を確認できます。

```sh
python3 -m http.server 8000
# → http://localhost:8000
```

## 公開について

静的ファイルのみなので、GitHub Pages、Netlify、Cloudflare Pages、
レンタルサーバーへの FTP アップロードなど、どの方法でも公開できます。
GitHub Pages を使う場合は、リポジトリの Settings → Pages で
公開するブランチとルートディレクトリ（`/`）を指定してください。

## 技術的なメモ

- フォントは Google Fonts（Shippori Mincho / Zen Kaku Gothic New）を読み込んでいます。
  外部読み込みを避けたい場合は、各 HTML の `fonts.googleapis.com` の `<link>` を外し、
  `assets/css/style.css` の `--f-serif` / `--f-sans` を端末標準のフォントだけにしてください。
- 地図は Google マップの埋め込み（API キー不要）です。
- JavaScript は、スマートフォンのメニュー開閉とスクロール時の表示だけに使っています。
  JavaScript が無効でも、内容はすべて読めます。
- `prefers-reduced-motion` を設定している端末では、アニメーションを止めています。
