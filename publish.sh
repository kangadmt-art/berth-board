#!/bin/bash
# Publish the board to GitHub Pages.
# Usage: ./publish.sh /path/to/standalone.html "commit message"
# The main board is one page with four tabs (Cargo jetties / Timber / Tuna / Liquid); timber.html, tuna.html and liquid.html
# are only redirects to index.html#timber / #tuna / #liquid so short links keep working.
# Commits index.html together with anything changed under data/, handover/ and tools/, so the source documents
# and the handover note travel with the version they belong to. Rebases on the remote first (another chat may have pushed).
set -e
SRC="$(readlink -f "$1")"; MSG="${2:-Update DPA Berth Board}"
cd "$(dirname "$0")"
ID=(-c user.name="Berth Board" -c user.email="mihir@neelkanth.co.in")
git "${ID[@]}" pull -q --rebase --autostash origin main
[ "$SRC" = "$(readlink -f index.html)" ] || cp "$SRC" index.html
git add index.html timber.html tuna.html liquid.html publish.sh README.md data handover tools 2>/dev/null || true
git "${ID[@]}" commit -q -m "$MSG" || { echo "nothing to commit"; exit 0; }
git push -q origin HEAD:main
echo "pushed → https://kangadmt-art.github.io/berth-board/ (tabs: #timber, #tuna, #liquid)"
