#!/usr/bin/env python3
"""Helpers for patching the board HTML with asserted anchors. Every helper stops the script (before anything is written)
if its anchor is missing or not unique, so a half-applied patch never reaches the file.

    import sys; sys.path.insert(0, '<repo>/tools'); from boardpatch import Board
    B = Board('/home/claude/work/dpa-berth-board.html')        # reads the file, keeps the text in B.s
    B.rep("const NOW=h('11-14 18:00');", "const NOW=h('11-15 10:30');")
    B.sub_entry("{b:'1',n:'Drake Well'", "t:'11-16 22:20'", "t:'11-17 02:00'")     # edit inside one V / PREDLOG / TIMBER entry
    B.note_prefix("{b:'1',n:'Drake Well'", "LIST 15.11: ... ")                      # prepend to that entry's note:'...'
    B.add_after("{b:'1',n:'Drake Well'", " {b:'1',n:'Next Vessel',...},\n")        # new entry after it
    B.wrow('Rahma', "STL 1 · GEN 9", rk="STL:1,GEN:9", rdy="11-06 11:00")          # waiting-row fields + 'LIST dd.mm: ...' note prefix
    B.wdel('Truong Minh Dream')                                                    # vessel programmed / berthed -> out of WRAW
    B.save()

Text that goes inside a JS '...' string must have apostrophes written as \\' (use B.q(text)).
"""
import re, sys

class Board:
    def __init__(self, path, list_tag='LIST'):
        self.path = path; self.s = open(path, encoding='utf-8').read(); self.n0 = len(self.s); self.list_tag = list_tag
    def die(self, m): print(m); sys.exit(1)
    @staticmethod
    def q(t): return t.replace("\\", "\\\\").replace("'", "\\'")
    def rep(self, old, new, cnt=1):
        k = self.s.count(old)
        if k != cnt: self.die('ANCHOR FAIL (%d found, want %d): %r' % (k, cnt, old[:150]))
        self.s = self.s.replace(old, new)
    def entry_span(self, marker):
        if self.s.count(marker) != 1: self.die('MARKER not unique (%d): %s' % (self.s.count(marker), marker))
        a = self.s.index(marker); b = self.s.index("},\n", a) + 1; return a, b
    def sub_entry(self, marker, old, new):
        a, b = self.entry_span(marker); ent = self.s[a:b]
        if ent.count(old) != 1: self.die('ENTRY FAIL %s: %d x %r' % (marker, ent.count(old), old))
        self.s = self.s[:a] + ent.replace(old, new) + self.s[b:]
    def note_prefix(self, marker, text):
        a, b = self.entry_span(marker); ent = self.s[a:b]; i = ent.index("note:'") + 6
        self.s = self.s[:a] + ent[:i] + text + ent[i:] + self.s[b:]
    def add_after(self, marker, text):
        a, b = self.entry_span(marker); self.s = self.s[:b + 2] + text + self.s[b + 2:]
    def line_of(self, prefix):
        if self.s.count(prefix) != 1: self.die('LINE prefix not unique (%d): %s' % (self.s.count(prefix), prefix))
        a = self.s.index(prefix); b = self.s.index("\n", a); return a, b
    def set_line(self, prefix, new):
        a, b = self.line_of(prefix); self.s = self.s[:a] + new + self.s[b:]
    # ---- waiting rows: [' name','cargo',qty,'unit',loa,draught,readiness|null,{ranks},'note'],
    def _row(self, name):
        return re.compile(r" \['" + re.escape(name) + r"','((?:[^'\\]|\\.)*)',([^,]*),'([^']*)',([^,]*),([^,]*),(null|'[^']*'),\{([^}]*)\},'")
    def wrow(self, name, add, rk=None, rdy=None, cargo=None, qty=None, dr=None, loa=None):
        """rk: text of the rank object, e.g. "SAAGAR:1,'8K':3,GEN:13" (98 = 'Y' flag). rdy: 'MM-DD HH:MM', '' for null, None to keep."""
        rx = self._row(name); m = rx.search(self.s)
        if not m or len(rx.findall(self.s)) != 1: self.die('WRAW row not found / not unique: ' + name)
        c, qq, u, lo, d, r, k = m.groups()
        new = " ['%s','%s',%s,'%s',%s,%s,%s,{%s},'%s" % (name, cargo if cargo is not None else c, qty if qty is not None else qq, u,
              loa if loa is not None else lo, dr if dr is not None else d,
              ("'%s'" % rdy if rdy else 'null') if rdy is not None else r, rk if rk is not None else k, self.list_tag + ": " + add + " · ")
        self.s = self.s[:m.start()] + new + self.s[m.end():]
    def wdel(self, name):
        m = self._row(name).search(self.s)
        if not m: self.die('WRAW del: ' + name)
        b = self.s.index("],\n", m.start()) + 3; self.s = self.s[:m.start()] + self.s[b:]
    def save(self):
        open(self.path, 'w', encoding='utf-8').write(self.s); print('saved', self.n0, '->', len(self.s))
