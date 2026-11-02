#!/bin/bash
# Publish the board to GitHub Pages.
# Usage: ./publish.sh /path/to/standalone.html "commit message"
# The main board is one page with three tabs (Cargo jetties / Tuna / Liquid); tuna.html and liquid.html
# are only redirects to index.html#tuna / #liquid so old links keep working.
set -e
SRC="$1"; MSG="${2:-Update DPA Berth Board}"
cd "$(dirname "$0")"
git fetch -q origin main && git reset -q --hard origin/main
cp "$SRC" index.html
git add index.html tuna.html liquid.html publish.sh 2>/dev/null || true
git -c user.name="Berth Board" -c user.email="mihir@neelkanth.co.in" commit -q -m "$MSG" || { echo "nothing to commit"; exit 0; }
git push -q origin HEAD:main
echo "pushed → https://kangadmt-art.github.io/berth-board/ (tabs: #tuna, #liquid)"
