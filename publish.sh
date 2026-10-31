#!/bin/bash
# Publish the board to GitHub Pages. Usage: ./publish.sh /path/to/standalone.html "commit message"
set -e
SRC="$1"; MSG="${2:-Update DPA Berth Board}"
cd "$(dirname "$0")"
git fetch -q origin main && git reset -q --hard origin/main
cp "$SRC" index.html
git add index.html
git -c user.name="Berth Board" -c user.email="mihir@neelkanth.co.in" commit -q -m "$MSG" || { echo "nothing to commit"; exit 0; }
git push -q origin HEAD:main
echo "pushed → https://kangadmt-art.github.io/berth-board/"
