#!/bin/bash
# ダブルクリックで変更をGitHubに公開（push）するスクリプト。
# 初回公開後、index.html を作り直したら（make_launcher.command や build_site.py の後）これを実行。
cd "$(dirname "$0")" || exit 1
git add -A
if git diff --cached --quiet; then
  echo "変更はありません。"
else
  git commit -m "${1:-update}"
fi
git push && echo "" && echo "✅ 公開ページ: https://shell0423.github.io/poker-gto-trainer/"
echo "（反映まで数十秒〜1分かかることがあります）"
