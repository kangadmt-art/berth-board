#!/usr/bin/env python3
"""Stevedore of every vessel, as the DPR prints it (column "Stevd."), from every xlsx DPR archived in data/.
   python3 tools/stevedores.py <board.html>   -> prints the JS line  const STV={...};  (keys matched to the names the board uses; the matches made by likeness go to stderr — read them)
   python3 tools/stevedores.py --list         -> every vessel and her runs, as read
   key = vessel name in capitals, letters and digits only; value = runs [first DPR day 'MM-DD', last DPR day 'MM-DD', stevedore].
   PDF DPRs (13, 14, 15, 21, 24 Nov) are not read — their columns do not split cleanly."""
import json, subprocess, glob, re, os, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD = {'J M BAXI': 'JM Baxi', 'JM BAXI': 'JM Baxi', 'JMB': 'JM Baxi', 'JMB PORT': 'JMB Port', 'TRUE BLUE': 'True Blue', 'TRUEBLUE': 'True Blue', "T'BLUE": 'True Blue', 'TBLUE': 'True Blue', 'TB': 'True Blue', 'TRUEB': 'True Blue',
        'MIHIR': 'Mihir & Co', 'RISPL': 'RSIPL', 'OTA KANDLA': 'OTA Kandla', 'GAUTAM': 'Gautam', 'SYNERGY': 'Synergy', 'SEABRIDGE': 'Seabridge', 'SAMUDRA': 'Samudra', 'RUSHRAJ': 'Rushraj', 'INAYAT': 'Inayat', 'MYSTIC': 'Mystic',
        'RISHI': 'Rishi', 'RISHI GLOBAL': 'Rishi Global', "A'WAD": "A'wad"}
SKIP = {'KICT', 'TT', 'M/S', ''}
def key(n):
    n = n.upper(); n = re.sub(r'\(.*?\)', '', n); n = re.sub(r'^\s*(M\.?\s?V\.?|M\.?\s?T\.?|LPG/C\.?|TUG)\s*[-.]*\s*', lambda m: 'TUG' if m.group(1) == 'TUG' else '', n)
    n = re.sub(r'\bWITH\b', '', n); return re.sub(r'[^A-Z0-9]', '', n)
def toks(v):
    v = re.sub(r'\s+', ' ', v.replace('\\', '/')).strip().upper(); out = []
    for t in [x.strip() for x in v.split('/')]:
        if t in SKIP: continue
        t = WORD.get(t, t)
        if t not in out: out.append(t)
    return out
def day(f):
    m = re.search(r'(\d\d)[._-](\d\d)', os.path.basename(f)); return '%s-%s' % (m.group(2), m.group(1))
days = collections.defaultdict(dict)      # key -> {day: [tokens]}
names = {}
for f in sorted(glob.glob(ROOT + '/data/*/[Dd][Pp][Rr]*.xlsx'), key=day):
    out = '/tmp/_dpr_' + os.path.basename(f) + '.json'
    subprocess.run([sys.executable, '-I', ROOT + '/tools/parse_xlsx.py', f, out], capture_output=True)
    for rows in json.load(open(out)).values():
        sc = None
        for r in rows:
            r = [('' if x is None else str(x).strip()) for x in r]
            if sc is None:
                if any(re.match(r'Stevd', x, re.I) for x in r):
                    sc = [i for i, x in enumerate(r) if re.match(r'Stevd', x, re.I)][0]; nc = [i for i, x in enumerate(r) if re.match(r'Name of Vessel', x, re.I)][0]
                continue
            if len(r) <= sc or not r[nc] or not re.match(r'^(CJ|OJ|MS|M/S|OTB|BA|IFFCO|BUNDER|MID)', r[0], re.I) and not re.match(r'^(M\.?V|M\.?T|TUG|LPG)', r[nc], re.I): continue
            t = toks(r[sc])
            if not t or re.fullmatch(r'[\d ()CJ]+', r[sc]): continue
            k = key(r[nc]); names[k] = r[nc]
            cur = days[k].setdefault(day(f), [])
            for x in t:
                if x not in cur: cur.append(x)
STV = {}
for k, dd in days.items():
    runs = []
    for d in sorted(dd):
        v = ' / '.join(dd[d])
        if runs and runs[-1][2] == v: runs[-1][1] = d
        else: runs.append([d, d, v])
    STV[k] = runs
def bkey(n):
    n = re.sub(r'\s*\(.*?\)', '', n).upper(); n = re.sub(r'\bWITH\b', '', n); return re.sub(r'[^A-Z0-9]', '', n)   # the same as stvKey() on the board
board = [a for a in sys.argv[1:] if a.endswith('.html')]
if board:
    import difflib
    t = open(board[0], encoding='utf-8').read()
    bn = set(m.group(1).replace("\\'", "'") for m in re.finditer(r"[{,]n:'((?:[^'\\]|\\.){2,60})'", t)) | set(m.group(1) for m in re.finditer(r"^ \['((?:[^'\\]|\\.)+)',", t, re.M))
    bk = {bkey(n): n for n in bn}
    out = {}
    for k, runs in STV.items():
        if k in bk: out[k] = runs; continue
        c = difflib.get_close_matches(k, list(bk), 1, 0.84)
        if c and c[0] not in STV:
            sys.stderr.write('alias  %-28s -> %s\n' % (names[k], bk[c[0]])); out[c[0]] = runs
        else: out[k] = runs
    STV = out
if '--list' in sys.argv:
    for k in sorted(STV): print(k, names[k], STV[k])
else:
    print('const STV=' + json.dumps(STV, separators=(',', ':'), ensure_ascii=False).replace("'", "\\'").replace('"', "'") + ';')
