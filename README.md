# 「AI臭さ」を取り除く Web UI/UX ガイドライン

テンプレートの見た目を変えるだけでなく、**利用者・目的・実際の情報に根ざしたサービス**にするための、日本語の実践ガイドです。

- [ガイドライン本文](GUIDELINES.md)：設計原則、画面・文章・インタラクション、Before / After、検証
- [レビュー用チェックリスト](REVIEW-CHECKLIST.md)：設計レビュー・PR・公開前確認にコピーして使用

## まず何をするか

1. 主な利用者と「この画面で終えたい仕事」を一文にする。
2. 空のカードやキャッチコピーより先に、実際に扱う情報と操作を並べる。
3. 正常系だけでなく、空・読み込み中・失敗・中断・復帰を作る。
4. 見た目の好みではなく、迷い・誤解・操作失敗を観察して直す。

## この文書の立場

「AI臭さ」は主観的な印象を表す便宜的な言葉です。AI生成を判定する基準ではありません。紫のグラデーション、角丸、カード、絵文字、イラストを禁止するものでもありません。

目標は **AIの利用を隠すことではなく、画一的で文脈の薄い体験を減らすこと**。人間が作ったUIにも同じ問題は起きます。必要なAI利用の説明や出典を消してはいけません。

本文中の推奨は設計上の仮説です。アクセシビリティの規格要件とは区別し、利用者調査で更新してください。全文がWCAG適合を保証するものではありません。

最終更新：2026-11-12

## GitHub Pages

このリポジトリには、Markdown 3文書から読みやすい静的ページを生成するワークフローがあります。Markdownを編集すると、mainへの反映後に再生成します。公開対象は `_site` のHTML・CSSだけです。JavaScript、解析タグ、Cookie、ブラウザ保存は使いません。

### 初回公開（管理者が実施）

1. このワークフローをmainへマージする。
2. Settings → Pages → Build and deployment → Source を **GitHub Actions** にする（別途設定が必要な場合）。
3. Actions の **Build and deploy Pages** をmainで実行する。初回失敗時はPages設定を確認して再実行する。
4. deployの結果と公開ページの表示を確認する。

想定URL：`https://d-muramatsu.github.io/human-centered-web-uiux-guidelines/`。設定とデプロイが成功するまでは公開済みではありません。PRではbuild/testだけが実行され、Pagesの書き込み権限はmainのdeployジョブだけに付与します。リポジトリのPages設定・ブランチ保護はこのコードから変更しません。

### ローカル確認

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_site.py
python -m unittest discover -s tests -v
python -m http.server 8000 --directory _site
```

`http://localhost:8000` を開きます。生成物はコミット不要です。Windowsでは仮想環境の有効化に `.venv\Scripts\Activate.ps1` を使用してください。
