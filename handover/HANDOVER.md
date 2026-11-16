# DPA Berth Board — handover note

Read this whole note before touching the board. It is the working memory of the board: any chat can pick the work up from here.
Keep the **Current state** section (the last one) up to date with every version you publish.

## 1. What this is

A live berthing board for Deendayal Port (Kandla): cargo jetties CJ-1 to CJ-16, the oil jetties (OJ-1 to OJ-7) and Tuna Tekra (TT).
It is one self-contained HTML file. Mihir (Mihir & Company, stevedores and agents at Kandla; Neelkanth Group) sends the port's documents
as they come out — berthing list, movement programme, DPR, harbour-master signal sheets, gang sheets — and the board is updated from each one.

The board does two jobs:

1. **Shows the port as it stands** — who is at which berth, on what panels, till when; who is waiting, with what rank; what is expected.
2. **Projects who berths next, where and when** from the port's berthing policy, and keeps score of how right it was
   (expected vs actual), so the rules get better. His own vessels (agent "Mihir & Company") get a dedicated card with options by priority and demurrage.

## 2. Where everything lives

| Thing | Where |
|---|---|
| The board (private, the master copy he opens) | Claude artifact "DPA Berth Board" — slug `4d00546f-fb6c-494f-b720-904988576a0c`, https://claude.ai/artifact/AWVRBbjBx4EJGBctgGPRS3 |
| Staff mirror (public page) | https://kangadmt-art.github.io/berth-board/ — GitHub repo `kangadmt-art/berth-board`, file `index.html` (byte-identical to the artifact's `index.html`) |
| Tabs on the one page | The tab a viewer used last is remembered in his browser (`localStorage` `bb.view`) and opened when the link has no `#tab`. Cargo jetties (`#cargo`) · **Timber** (`#timber`, since 16 Nov — log vessels: active list, laytime / demurrage, completed record) · Tuna (`#tuna`) · Liquid (`#liquid`). `timber.html`, `tuna.html`, `liquid.html` in the repo are only redirects. |
| Source documents archive | `data/YYYY-MM-DD/` in the repo |
| Tools | `tools/` in the repo (see §4) |
| This note | `handover/HANDOVER.md` in the repo |

The artifact also holds DPA circulars (`circ/*.pdf`) and tanker line-ups (`liq/*.pdf`) that the board links to. Publish only `index.html`; never remove the others.

## 3. Setting up in a new chat

1. Attach the repo with **push** access (`kangadmt-art/berth-board`) and clone it. Work on a copy of `index.html`, e.g. `/home/claude/work/dpa-berth-board.html`.
2. Check the artifact's live version (`list_files` on the slug gives `version` and the sha256 of `index.html`) and confirm the repo's `index.html` has the same sha256.
   If they differ, the artifact is the master — stop and tell Mihir before changing anything.
3. Check the tools run: `node tools/check.js <file> --all` must end with `OK` (playwright + chromium are preinstalled in this environment; `pip install openpyxl --break-system-packages` if the xlsx parser needs it; `pdftotext -layout` for DPR PDFs).
4. Only **one chat at a time** should update the board. The artifact refuses a publish on a stale `base_version`; `publish.sh` rebases on the remote.

Do not load the whole HTML into context (≈ 660 KB, ≈ 2,700 lines). Use `grep -n` / `sed -n` on the block you need (§6 has the anchors) and patch with a script.

## 4. How an update is made

1. `cp` the working file to `bak_vNNN.html`.
2. Parse the document: `python3 -I tools/parse_xlsx.py <file.xlsx> <out.json>` (list / programme), `python3 -I tools/list_summary.py <list.json>` for the waiting and ETA sheets with ranks;
   `pdftotext -layout` for the DPR; signal sheets and gang sheets come as photos — read them directly, including hand corrections.
3. Write a patch script with `tools/boardpatch.py` (`Board.rep / sub_entry / note_prefix / add_after / set_line / wrow / wdel`). Every helper asserts its anchor and stops before writing if it fails.
   Worked examples from 14 Nov are in `tools/examples/` (list + programme in two parts; a rule confirmation with a correction).
4. Validate: `node tools/check.js <file> --all` → syntax, no `},,`, no page errors, no `undefined`/`NaN` on any tab, then **read the projection**: does a junior jump a senior of the same group? is anyone on a berth her cargo, length or draught cannot use? does a slot hold more vessels than it has places? Read the Mihir & Co card.
5. After the data is in, export the projection (`node tools/dump_projection.js <file> S.json`) and rebuild the prediction snapshot and logs (§8) from it.
6. Publish the artifact: `list_files` (for the live `version`) → `publish_files` with `slug`, `base_version`, `files=[{as:"index.html", path:<file>}]`, a label like `v160 · list 15.11`. The version number is the `seq` in the publish result (last was 159).
7. Push the mirror: copy source documents to `data/YYYY-MM-DD/`, update §10 of this note, then `./publish.sh <file> "v160: what changed"` — it commits `index.html`, `data/`, `handover/` and `tools/` together. End the commit message with the attribution lines your own session gives you.
8. Reply to Mihir (§9).

**Timber tab — with every DPR:** (a) a log vessel that has *commenced* gets `comm:'MM-DD HH:MM'` on her row in `TIMBER.rows` (the average discharge is counted from it); (b) a log vessel that has *completed* is taken out of `TIMBER.rows` and added to `TIMBER.done` with `nor`, `mf`, `comm`, `done` (the DPR's "completed" hour — not the let-go), `out`, `berth`, `pri`, `ag`, `pcs` — the record is never trimmed; (c) a new desk sheet ("Kandla Timber Vessel's Position") updates `cbm`, `eta`, `etb` and `TIMBER.d / upto`. A log vessel that is on the DPA list but not in `TIMBER.rows` still shows (from the list), and one that has sailed but is not yet in `TIMBER.done` still shows in the record with a "not yet written into the record" mark — so nothing drops out, but write it in. Check with `node tools/check.js <file> --timber`.

Things to change at every update: `NOW`, `UPDATED`, `PROG_END` (end of the current programme window), the header line (`List <b>…</b> · DPR <b>…</b> · Programme <b>…</b> · Signals to …`), the "Sources, rules & tide" line, `BOARD_SRC`, `LIQ.src` / `LIQ.asOf`, `TUNA.src`.

## 5. Reading the port's documents

- **Whose word counts:** harbour-master signal sheet (what actually moved, with times and pilots) > movement programme (what the 11:00 meeting decided) > berthing list (0700 position). The DPR gives actual made-fast / commencement / completion times and the 24-hour output.
- **The port is taken as right.** Where the board expected something else, write a LEARN entry (expected / actual / why / fix), leave it `open` until Mihir confirms, and explain every open point to him in simple words in the same reply.
- **List ETC = permissible time** (dry cargo: commencement + quantity ÷ daily norm; tankers: made fast + quantity ÷ hourly norm + 4 h). Show ETCs and norms exactly as printed. The DPR pace is used only to project the real completion.
- **The 0700 list pre-prints the day:** `B'TODAY` vessels and shifted panels are printed before they happen; a berth in brackets (`[7]`) means sailed / sailing today. Times for those are estimates (`est:1`) until a signal sheet or the next DPR gives the actual.
- **Waiting sheet columns** (list 14.11 layout): reporting, commercial readiness, then ranks GP · CSTL · HP · SGR · 24H · 8K/6.5K · STL/PRJ · GEN, agent, remarks. A number is a queue place; **`Y` is only a flag, not a place** (board value 98); `X` = berthing today; `N/A` readiness = not in the queue yet. A vessel that is N/A in the morning can declare readiness before the 11:00 meeting and take her group's slot the same day.
- **Programme rows:** BERTH · OUTWARD · READINESS · OUTWARD DRAFT · INWARD / SHIFTING · PANELS · CATEGORY · ETA · SAILING DRAFT · REMARKS. Outward `READINESS` is taken as the sailing time; the inward vessel is put ~2 h after it unless a time is given. Remarks carry the shifts ("PORT C." = port convenience, "AGENT'S A/C").
- **The port's sheets have slips:** a wrong vessel name (programme 14.11 printed CD GLORY for CD CHERRY), a rank in the next column, a copied quantity, a wrong date. If a line does not fit the vessel's known cargo / length, say so and ask — do not build on it. Fertiliser vessels are sometimes missing their Govt rank in the morning list.
- The meeting is at 11:00 every day and programmes the window 18:00 → 18:00 next day.

## 6. Inside the HTML — data blocks (find with `grep -n "^const NAME"`)

| Block | What it holds |
|---|---|
| `NOW`, `UPDATED`, `PROG_END`, `BOARD_SRC` | clock and sources. Times are written `h('MM-DD HH:MM')`; hour 0 = 25 Oct 2026 00:00 IST |
| `V=[…]` | every berth occupation, past, present and programmed: `{b,n,nm,p:[from,to],c,q,u,cat,slot?,via?,f,t,est?,note}` — `b` berth, `nm` norm, `p` panels, `cat` priority group (GOV, COASTAL, HP, SAAGAR, 24H, 8K, STL, BIT, GEN), `f`/`t` from/to, `est:1` while a time is an estimate. One vessel can have several entries (shift = new entry). |
| `WRAW=[…]` → `W` | waiting and expected vessels: `[name,cargo,qty,unit,loa,draught,readiness|null,{ranks},note]`. Ranks e.g. `{SAAGAR:1,'8K':3,GEN:13}`; 98 = `Y`. A vessel put on the programme moves to `V` (with `est:1`) and is deleted here. |
| `REP`, `ETA`, `AG`, `IE`, `LOA` (+ `Object.assign(...)` blocks after them) | reporting time (= seniority; for an expected vessel her ETA — `rep <= NOW` makes her "waiting"), ETA, agent, IMP/EXP, length. Own vessels = agent contains "Mihir". |
| `DPR={…}` | the latest DPR: rows `{loc,n,ie,c,l24,upto,bal,g,hk,partial?,comm?,note}` |
| `LIQ={…}`, `TUNA={…}` | oil jetties and Tuna: `berths:[{b,prev,now,out,outBy,next}]`, `wait`, `eta`, `moves` |
| `MV=[…]` | cargo-jetty movement groups: `['title',[[time,type,vessel,route,pilot,'MM-DD HH:MM',note],…]]` — newest group first |
| `TIMBER={src,d,upto,rows:[…],done:[…]}`, `DEM={rate:4000,usd:20000,free:12,desp:10000}` | the Timber tab. `rows` = active vessels (desk CBM, ETA, team ETB, `comm`); `done` = the completed record, self-contained rows kept for good. `tmbRows()` builds one record per vessel (laytime, average discharge, status). `timber()` draws the summary pills (`#tmbstats`) and THE SHEET (`#timber`: one row a vessel — arrival, berth, average discharge / work, completes, laytime bar, demurrage so far, at completion); `demur()` draws the completed record (`#tdone`) and the notes (`#tnote`). `window.__TMB` = `{active, done, recAvg}`. `DEM.desp` = despatch USD a day = half the demurrage rate (Mihir, 16 Nov). LAYOUT RULE (Mihir, 16 Nov 01:26 — "top par hona chahiye"): the list comes first; no tiles, chips or paragraphs above it — explanations live in "How this sheet counts" at the bottom. Both tables carry class `tc`: on phones (≤ 640 px) a row shows only its `td.sm` summary (name + status chip, one line of facts, work bar, laytime bar + money) and a tap toggles `tr.open`, which shows the other cells as a labelled two-column grid (`data-l` = label, `full` = full-width cell, `mt` = hide when empty, `no` = hide on phones, `o6…o9` = order on phones). Keep `td.sm` and `data-l` on anything you add. On phones the Timber tab also hides the list / programme line of the page header (`body[data-view="timber"]`). |
| `MYLOG`, `LEARN`, `PRED`, `PREDLOG` | the logs (§8) |
| `OPTS` | own vessels' "when she berths by each priority" options, with provisional ranks per route |
| `CATS`, `allowedBerths()`, `okBerth()`, `simulate()` | the policy and the projection. `window.__S` = projection, `__OPT` = options, `__DEM` = laytime rows of the active timber vessels, `__TMB` = the whole timber sheet, `__fmt`, `__dbg` for checks |

Conventions and traps:

- Notes are newest-first and start with their source: `LIST 15.11: …`, `PROGRAMME 16.11 (TF/SH/2102): …`, `DPR 15.11: …`.
- Board names: **`Enshi`** is the board's name for MV Enishi (DPR rows must use it too); a second call is named `Name (salt, next call)`; `Alberta (re-berthing)`.
- **Waiting-row notes are parsed.** If a note contains `REQ` or `CJ`, any digit range in it (`13 TO 16`, `2-3`, `14–15`) is read as a berth requirement — never write a digit range there unless it is one. `30K/25K` in a note puts the vessel in the Sr No 7 quote pool. `2 SHORE CRANE` triggers the crane rule.
- The 24-hr group is capped in code at 24 h from berthing. Vessels in `PROG_SAIL` keep their programmed sailing (the DPR pace does not override it).
- Apostrophes inside a JS string must be `\'`.
- The "Mihir & Co" card: a berthed own vessel is one line; a sailed own vessel is dropped.

## 7. Rules in the projection (as confirmed by Mihir unless marked)

- **Slots, in order:** Govt 2 · Coastal 1 · Higher productivity 2 · SAAGAR 1 bulk + 1 break bulk · 24 hrs 1 · 6.5K/8K 1 · Steel/Project 1 · Bitumen 1 · General 3 (bagged max 3).
  Fallbacks: Govt and Coastal → SAAGAR project cargo, else a 30k/25k quote (Sr No 7); 24 hrs → 30k/25k quote; Bitumen → senior General; HP has no fallback — the berth goes down the order and lastly to General as a cross-fill.
- **A slot counts as free for the whole programme window if its vessel sails inside that window.** A berth is offered to the groups in the order above, each to its senior ready vessel *that the berth suits*; a vessel is alongside ~2 h after the berth frees.
- **SAAGAR bulk and SAAGAR break bulk are separate priorities** (1 Nov; confirmed 14 Nov). With no bulk vessel waiting, a break-bulk vessel takes the berth and the priority is occupied; when a berth frees again, a waiting SAAGAR bulk vessel gets it even if a break-bulk vessel is senior. SAAGAR project cargo does not use these two places.
- **Fertiliser:** every *bulk* fertiliser cargo is Govt priority even when the list prints no rank (bags are not).
- **24 hrs:** a vessel that can finish in 24 h is allotted by seniority *and* availability of the particular berth she needs; if there is none, a vessel ready for 30k/25k. The port will shift a working vessel to make that berth (15 Nov: Enishi moved for African Hornbill at the incoming agent's cost).
- **"2 SHORE CRANE REQ":** bags → CJ-2/3; bulk → CJ-6/7/8 or CJ-13 to 16.
- **Clean berths CJ-13 to 16 (incl. 15A):** salt, windmill and project cargo work only there; fertiliser does not go there; timber cannot work CJ-2, 3, 6. The port now lets pellets and other dirty bulk onto CJ-13–16 / CJ-16 (seen since 11 Nov; no circular).
- **Port-convenience shift:** the port moves a logs / bags vessel off a clean berth to seat a priority vessel that needs one — the group's *senior* vessel needing it, by cargo or by her berth requirement.
- **A General vessel cross-filled against a vacant HP slot does not block a real HP vessel** (board's reading of 12–14 Nov, adopted 14 Nov).
- **Loaded draught (exports):** no berth she would have to shift out of after loading. Board's steps: ≥ 40,000 MT → 12.5 m, ≥ 30,000 MT → 11.2 m, else arrival draught (25,000 MT loads to 10.0 m at CJ-4 — programme 15.11).
- One panel of clear quay is kept between two vessels.
- **Timber laytime / demurrage (Mihir; the 12 free hours added 16 Nov):** after a timber vessel arrives (NOR at Kandla = the DPA reporting time) the first 12 hours are free. Laytime starts when they end — or at berthing, if she is berthed inside those 12 hours. Allowed time = quantity ÷ 4,000 CBM a day; after it demurrage runs at USD 20,000 a day until she COMPLETES (the DPR's completion hour, not the let-go). Completed before laytime ends = despatch at HALF the demurrage rate, USD 10,000 a day on the time saved (Mihir, 16 Nov 00:24; `DEM.desp`). Demurrage and despatch are totalled separately, never netted — each vessel is its own account. Time runs without a break — no exception (Sunday, holiday, rain, shifting) is applied because none has been given. Quantity = the desk's CBM where there is one, else the DPA list figure. Shown per vessel on the Timber tab, so far and at completion; for a vessel still waiting the completion is the projection at the port norm, and the sheet also shows the figure at the record average of the completed vessels. (He may give vessel-wise charter-party terms later.)
- **Average discharge ("avg dispatch", Mihir 16 Nov — read as average DISCHARGE per day, to be confirmed):** completed vessel = quantity ÷ (commencement → completion), from made fast where the commencement is not on record; vessel at berth = DPR up-to-date ÷ (commencement → DPR 0700).

- **Bag vessels under General — 2 days' extension (Mihir, 15 Nov):** every bag-cargo vessel berthed under General may stay 2 days beyond the list ETC. Code: in the `V` DPR post-processing, `bagGen` → berth free at the earlier of the DPR pace and list ETC + 48 h (`v.extTo`). Projected stays of bag vessels not yet berthed stay at the norm.
- **Who pays for a shift (Mihir, 15 Nov):** a shift that opens a clean berth for a vessel whose cargo must work at CJ-13–16 and lies on that side (salt) is on PORT account — the projection's port-convenience shift. A shift made because an agent wants a particular berth is at that agent's cost ("A/C <agent>" on the programme: Rahma / Parekh Marine, African Hornbill / Delta).

## 8. The logs — keep them honest

- **`LEARN`** (newest first): `{d,v,exp,act,why,fix,st}` — `st` is `open` (needs his confirmation), `adopted` (rule coded), `ok` (matched), `closed`. Number the open questions inside `fix` as `OPEN (1) …`; when he answers, write `ANSWERED (Mihir, date): …` in place.
- **`MYLOG`**: for each own vessel, one entry per reading `{d,exp,b,slot,why}` — the card shows the history and why the date moved. Add an entry whenever her date or route changes.
- **`PRED`**: the snapshot `['vessel','berth' or 'sails','date','note']` rebuilt at every update — programmed / estimated moves first, then the projection — to compare with the next documents.
- **`PREDLOG`**: `{v,predAt,pb,pt,ab,at,src?,note}`. The daily prediction is taken when the DPR arrives (DPR + policy). A re-run on new information adds rows for the picks that changed and marks the old ones superseded in their note — never delete a published prediction.
  When the programme arrives: add `src:'prog'` rows (readings, not scored) and `pb:null` rows for berthings the board had not projected. Fill `ab` (berth actually given) when known and `at` (actual made-fast time from DPR / signal) — a row is scored only when `at` is filled: hit ≤ 6 h, near ≤ 12 h, else miss. Small sailing slips are not counted.

## 9. How Mihir wants it

- He usually sends the files with no text — that means "update the board". Do it end to end and publish; do not ask what he wants.
- Reply in casual Hinglish, short, bottom line first: what the programme / document says, his own vessels (date, berth, route, demurrage), where the board was wrong, and the open points he must confirm — each in one simple line. Documents and the board itself are in English.
- Be direct, including when the board (or his reading) looks wrong. Give ranges and conditions instead of a false single date.
- Do not email him while he is in the chat. Do not put his personal e-mail address anywhere. The scheduled tasks for this board are paused — leave them paused.
- When he states a rule, record it in `LEARN` as he said it, code it, re-run, and show what it changes for his vessels.

## 10. Current state — update this section with every version

**As of v169 · 16 Nov 2026 10:25 IST** (version id: see `list_files` on the artifact).

- **Applied:** berthing list 14.11 (0700) · DPR 15.11 (0700 15 Nov) · programme for 16.11 (TF/SH/2102, dated 15 Nov, received 16:41) on top of programme 15.11 · HM night signal of 15 Nov, AMENDED sheet (disp 1805 / 1850 / 2048) — before it only the sheets up to the night sheet of 13 Nov, 2nd amendment (the 14 Nov sheets and the 15 Nov day sheet were never received). `NOW` = 15 Nov 20:54, `PROG_END` = 16 Nov 18:00. Mihir's answers of 15 Nov 17:48 applied (v163).
- **Awaited:** amendments to the 15 Nov night sheet, 16 Nov day sheet, list 16.11, DPR 16.11, programme 17.11 (meeting 16 Nov 11:00).
- **Night signal 15 Nov in one paragraph:** Lavraki OUT 20:00 → MAPLE CASTOR IN o/c → OJ-3 (not on any list / programme; the programme's Lujain move OJ-4 → OJ-3 and Avyaan into OJ-4 are not on the sheet) · Princess Joanna SHIFT 00:01 CJ-6 → CJ-5 (PORT-C) · Bow Platinum RT OUT 21:00 → Haein Hope o/c → OJ-2 · Shanaya OUT 02:00 → Truong Minh Dream IN o/c → CJ-6 (~04:30 est) · Ishaan IN 00:30 flood → OJ-6 · Velika 03:30 (KICT) → tug Chandra Sun + barge Victoria 251 o/c → 166½–171¾ (on the chart as `cat:'SPACE'`) · Cape Diversity RT OUT 03:00 → Evangelia D o/c → 173½–188 (~06:00 est) · Coastal Amigo SHIFT 06:00 boat basin → OTB · TCI Anand OUT 05:25. Rule of thumb used: inward "o/c" behind a round-trip sailing = outward time + ~3 h. AMENDED (disp 2048): Princess Joanna SHIFT 23:15 (00:01 struck) · Bow Platinum RT OUT 22:00 (21:00 struck) · Evangelia D now o/c with Capt Bali after TCI Anand's 05:25 (→ ~08:30 est, sailing ~17 Nov 15:00 est) · new row Vira 1 → 87–95 (KICT, not tracked).
- **Programme 16.11 in one paragraph:** Cape Diversity out 16 Nov 03:00 (night) → Evangelia D CJ-16 173½–188 HP(50K) · Merchia out 13:00 → North Gate shifted CJ-15A → CJ-3 (18½–26¼) "A/C PAREKH MARINE" → Rahma CJ-15A 156–164½ STEEL/PROJ · Leya "shifting CJ-09 to OTB, agent's req." 17:30 → Honor Star CJ-9 (GFPL) · tug Chandra Sun + barge Victoria 251 CJ-15A (CSTL, night) · oil: Lavraki out 15 Nov 20:00 → Haein Hope OJ-2; Bow Platinum out 21:00 → Lujain moved OJ-4 → OJ-3 (agent's a/c) → Avyaan OJ-4; Shanaya out 16 Nov 02:00 → Ishaan OJ-6 · Tuna: Mykonos Wave out 12:30 → Beagle TT-3. No outward row for Theometor, Bomustafao O, Drake Well; no rows for CJ-5 / CJ-6.
- **Estimates waiting for actual times** (`est:1`): everything on the night sheet and on programme 16.11 above · from programme 15.11, no sheet seen: CD Cherry out 17:00, Enishi CJ-4 → CJ-15 ~19:00, African Hornbill into CJ-4 ~20:00, Lujain into OJ-4, Searay OJ-7 → OJ-1, CS Rotterdam into OJ-7, SC Larimar out 17:30 · Princess Joanna's completion (~16 Nov 13:00), Truong Minh Dream's (~19 Nov 10:30), Evangelia D's sailing (17 Nov 15:00), Rahma's (18 Nov 16:00) and the barge's (17 Nov 15:00) are board estimates until a list / DPR gives them.
- **New in the code (v162–v163):** (1) bag vessels under General: 2 days' extension (see §7) — Theometor → ~17 Nov 14:13 (allowed till 18 Nov 02:06), North Gate → ~18 Nov 11:05, Bomustafao O → ~16 Nov 11:00; for other vessels, a permissible time that falls inside a programme with no outward row for her is carried to the DPR completion; (2) options run: `onlyOK()` keeps a route-limited vessel out of the pools of other routes (she was ranked through the 30K/25K pool first and then dropped, so her own-group lines came back empty).
- **Own vessels (agent Mihir & Company):**
  - *Drake Well* — pine logs 26,111 CBM, CJ-1 under 6.5K/8K, made fast 13 Nov 14:00, list ETC 16 Nov 22:20; DPR 15.11: 7,882 CBM in 24 h, 13,871 left → ~17 Nov 01:15. Not on programme 16.11. NOR 5 Nov 15:00 → laytime from 6 Nov 03:00 (12 free hours), ended 12 Nov 15:40 — on demurrage (~USD 88,000 at completion on the DPR pace; ~USD 67,000 by midnight 15/16 Nov). Average discharge since she commenced (13 Nov 15:35): ~7,450 CBM/day.
  - *Rome Trader (salt, next call)* — salt 55,275 MT export, ready 14 Nov 17:00, declared under SAAGAR, HP, 30K/25K and 8K (Mihir, 15 Nov; board ranks SGR 5 bulk place, HP 4, 8K 8). Not on programme 16.11. Board: CJ-14 ~17 Nov 14:50 under HP (v165: the HP place now comes from Cape Venture ~12:50; Evangelia D sails ~15:00). The projection shifts Theometor CJ-14 → CJ-2 and African Peacock CJ-13 → CJ-5 under port convenience — Mihir (15 Nov): that shift is on port account for her. If the port does not make it in that window: CJ-15A after Rahma ~18 Nov 18:00. Ahead of her for clean berths on the 17th: Xin Hai Tong 71 (Coastal slot as SAAGAR project) and HN Doris (HP 3). Other routes: 30K/25K ~18 Nov 18:00, SAAGAR bulk ~19 Nov 00:30, 8K ~21 Nov, General ~23 Nov.
  - *CD Glory* — timber logs 29,158 CBM, 179.9 m, 10.5 m. Ready at the 16 Nov meeting under SAAGAR and 6.5K (board ranks SGR 6 / 8K 9). Board (v164): CJ-5 ~19 Nov 22:45 under General against the vacant Bitumen slot — a fragile gain (it appears only because Uni Blossom / AG Varvara now go to CJ-14 / CJ-15 in the re-run); the 6.5K/8K fallback is ~21 Nov at CJ-4 if ML Egret (8K 2, deep berths only) finds no berth when Pioneer Fortune finishes, ~27 Nov at CJ-1 if she does (v165 run). Her date cannot be narrowed before the 16 Nov meeting. She fits only CJ-1, CJ-4, CJ-5.
- **v166 (16 Nov 00:01, no new port document — `NOW` stays 15 Nov 20:54):** timber moved out of the Cargo jetties page into its own tab, laytime rule with the 12 free hours, average discharge per vessel, completed record (AC Kathryn, Centurion Buyo, African Quail, Lanna Naree). Completed-vessel results on the new rule: African Quail USD 72,700 (3.6 d), Lanna Naree USD 98,800 (4.9 d); AC Kathryn and Centurion Buyo are not counted (arrival not on record). Record average discharge 7,430 CBM/day (three vessels with full times).
- **v169 (16 Nov 10:04):** new timber desk sheet (dated 14 Nov 1200, updated 15 Nov 1800 after the meeting; text in `data/2026-11-16/`). Team ETBs now: ML Egret 18 Nov · Uni Blossom 19 Nov · AG Varvara 25 Nov · CD Glory 25 Nov · Darya Priya 29 Nov (desk ETA 16 Nov 19:30) · Paiwan Ace 4 Dec · Erna Oldendorff 7 Dec · African Pheasant 8 Dec · Paiwan Wisdom 17 Dec; desk counts 44 vessels waiting. Board vs desk: Uni Blossom same day (19 Nov); ML Egret board ~21 Nov (desk 18); AG Varvara board 19 Nov (desk 25); CD Glory board 19 Nov night (desk 25). The projection was NOT changed — a desk estimate is not a port document. `TIMBER.etaFromDesk:true` makes the Timber tab use the desk's ETA for a vessel that has not arrived yet — set it `false` when a DPA list newer than 15 Nov 18:00 goes on the board. `NOW` unchanged (15 Nov 20:54).
- **v168 (16 Nov 01:26):** Mihir — "layout timber wale ka barobar nahi hai … top par hona chahiye" (read as: the vessel list must be at the top, the layout tidy). Timber tab reshaped: six big tiles → one row of pills; the separate position and laytime tables merged into ONE sheet, so a vessel appears once; source chips and the explanatory paragraphs moved to the bottom; phone rows collapsed to 3–4 lines that open on a tap (first vessel now ~460 px down a phone screen, was ~1,700; whole tab ~4,000 px, was ~14,000); the last-used tab is remembered. If he still says it is not right, ask for one screenshot — the reading of "tip.per" was a guess.
- **v167 (16 Nov 00:24):** despatch = half of demurrage (Mihir) → `DEM.desp=10000`; no figure on the sheet changes today because no vessel is in despatch.
- **Open with Mihir:** (1) LEARN "16 Nov 10:04": is ML Egret the first vessel in the SAAGAR line? She was SGR 1 on list 13.11 and shows only "Y" on list 14.11; the desk seats her on 18 Nov, the board gives that SAAGAR place to AG Varvara. If she is first, AG Varvara and CD Glory move towards the desk's 25 Nov. (2) LEARN "16 Nov 00:01": "avg dispatch" was read as average discharge per day — he answered only the despatch rate, so this stays unconfirmed (do not press).
- **Known gaps:** when two berths free inside ONE programme window, the projection still deals the vacant slots in the order the berths free (v164 → v165: a 2½-hour change in Evangelia D's time swapped the Coastal / 24-hr fallback picks between Xin Hai Tong 71, Gokova-M and Propel Confidence) — the port allots the whole window at one meeting, so those picks are loose · the projection makes a port-convenience shift at the first moment a CJ-1–10 berth is free, even when the priority slot it is made for frees only later in the window (v162: shifts at 16 Nov 20:00 for HP places that free 17 Nov ~11:30 — the clean berths stand empty on the chart for those hours; the beneficiary's time is right, the shift's own time is the port's) · the pipe barge at CJ-15A is not modelled as quay occupancy · cape lighterage is not modelled (Cape Venture lightered 50,844 of 165,051 MT before berthing) — code it with the next cape · the desk sheet has no CBM for CD Glory and Darya Priya (the DPA list figures are used — ask for the B/L CBM, laytime is counted on it) · on the Timber tab a waiting vessel's "at completion" figure rests on the board's projected berth, so it moves with every re-run · the old "berth history" chart shows a fixed 31 Oct – 9 Nov window · several PREDLOG rows still wait for actual berthing times · Sea Gautham is held out of the projection while the list carries "DISPUTE".
- **History:** `git log` in the repo (one commit per version, message says what changed); the artifact keeps every version.
