#!/bin/bash
# ダブルクリックで「GTO Trainer.app」を(再)作成し、デスクトップにも置くスクリプト。
# index.html の絶対パスはこのファイルの場所から自動で決まるので、フォルダを移動しても動く。
cd "$(dirname "$0")" || exit 1
DIR="$(pwd)"
rm -rf "GTO Trainer.app"
osacompile -o "GTO Trainer.app" -e "do shell script \"open '$DIR/index.html'\"" || { echo "osacompile に失敗しました"; exit 1; }
cp -R "GTO Trainer.app" "$HOME/Desktop/" 2>/dev/null && DESK="（デスクトップにもコピー）" || DESK=""
echo "✅ 'GTO Trainer.app' を作成しました $DESK"
echo "   → ダブルクリックでトレーナーが開きます。Dock にドラッグすると常駐できます。"
