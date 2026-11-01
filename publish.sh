#!/bin/bash
# Publish the board to GitHub Pages.
# Usage: ./publish.sh /path/to/standalone.html "commit message"
# Copies the main board to index.html and regenerates tuna.html + liquid.html from it (build_pages.py),
# then commits and pushes everything to main.
set -e
SRC="$1"; MSG="${2:-Update DPA Berth Board}"
cd "$(dirname "$0")"
git fetch -q origin main && git reset -q --hard origin/main
cp "$SRC" index.html
if [ -f build_pages.py ]; then python3 build_pages.py index.html . >/dev/null; fi
git add index.html tuna.html liquid.html build_pages.py publish.sh 2>/dev/null || true
git -c user.name="Berth Board" -c user.email="mihir@neelkanth.co.in" commit -q -m "$MSG" || { echo "nothing to commit"; exit 0; }
git push -q origin HEAD:main
echo "pushed → https://kangadmt-art.github.io/berth-board/ (+ tuna.html, liquid.html)"
