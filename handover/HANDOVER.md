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
| `TIMBER={…}`, `DEM={rate:4000,usd:20000}` | timber desk table and the demurrage section (§7) |
| `MYLOG`, `LEARN`, `PRED`, `PREDLOG` | the logs (§8) |
| `OPTS` | own vessels' "when she berths by each priority" options, with provisional ranks per route |
| `CATS`, `allowedBerths()`, `okBerth()`, `simulate()` | the policy and the projection. `window.__S` = projection, `__OPT` = options, `__DEM` = demurrage rows, `__fmt`, `__dbg` for checks |

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
- **Timber demurrage:** every timber vessel gets laytime from her NOR at Kandla at 4,000 CBM a day; after that demurrage runs at USD 20,000 a day. The board shows it per vessel, so far and at completion. (He may give vessel-wise charter-party terms later.)

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

**As of v161 · 15 Nov 2026 11:00 IST** (version id: see `list_files` on the artifact).

- **Applied:** berthing list 14.11 (0700) · DPR 15.11 (0700 15 Nov) · programme for 15.11 (TF/SH/2102, dated 14 Nov) · HM signals up to the night sheet of 13 Nov, 2nd amendment. `NOW` = 15 Nov 10:30, `PROG_END` = 15 Nov 18:00.
- **Awaited:** 14 / 15 Nov signal sheets, list 15.11, programme 16.11 (meeting 15 Nov 11:00), DPR 16.11.
- **Estimates waiting for actual times** (`est:1`): Princess Joanna CJ-6 → CJ-5 and Truong Minh Dream into CJ-6 — both programmed for the night of 14–15 Nov, NOT done by 0700 (placeholders ~13:00 / ~15:00 on the 15th) · Cape Diversity completes ~13:00 on the 15th, no outward row yet · CD Cherry out 17:00 · Enishi CJ-4 → CJ-15 ~19:00 · African Hornbill in CJ-4 ~20:00 · oil jetties: Searay OJ-7 → OJ-1 and CS Rotterdam into OJ-7 (placeholders), Bochem Ghent out 12:30, SC Larimar out 17:30 → Lujain, Lavraki and Bow Platinum sailing (estimates). TPT Heart was shifted to OTB on 15 Nov 05:24 with 4,016 MT still to load.
- **Own vessels (agent Mihir & Company):**
  - *Drake Well* — pine logs 26,111 CBM, CJ-1 under 6.5K/8K, made fast 13 Nov 14:00, list ETC 16 Nov 22:20; DPR 15.11: 7,882 CBM in 24 h, 13,871 left → ~17 Nov 01:15. NOR 5 Nov 15:00, laytime ended 12 Nov 03:39 — on demurrage (~USD 98,000 at completion on the 4,000 CBM/day basis).
  - *Rome Trader (salt, next call)* — salt 55,275 MT export, ready 14 Nov 17:00. Mihir (15 Nov): she is declared under SAAGAR, HP, 30K/25K and 8K — the list's single `SGR Y` is the port's mistake. Board ranks until the list prints them: SGR 5 (she takes the SAAGAR *bulk* place), HP 4, 8K 8. Board: CJ-14 ~18 Nov 06:00 under HP / 30K-25K; SAAGAR place ~18 Nov 22:00. A clean berth is what holds her, not the priority.
  - *CD Glory* — timber logs 29,158 CBM, 179.9 m, 10.5 m, ETA 15 Nov 12:00. Mihir (15 Nov): not ready for the 15 Nov meeting; ready at the 16 Nov meeting under SAAGAR and 6.5K (board ranks SGR 6 / 8K 9). Board: ~21 Nov at CJ-4. She fits only CJ-1, CJ-4, CJ-5.
- **Open with Mihir:** nothing — the four points of 14 Nov were answered on 15 Nov 10:49 (LEARN entry of that time: Rome Trader's routes; CD Glory's readiness; Xin Hai Tong 71 is only under SAAGAR project; Karpathos Dawn's 31 h was an extension given to that vessel — the 24-hour cap stays). Older, unanswered: what a vessel loses by declining a programmed movement; charter-party exceptions for timber laytime. To look at: on the Mihir & Co card Rome Trader's 6.5K/8K and General option lines show no date since v161.
- **Known gaps:** cape lighterage is not modelled (Cape Venture lightered 50,844 of 165,051 MT before berthing) — code it with the next cape · the timber desk table is from the team sheet of 7–8 Nov plus list-only rows (AG Varvara appears twice) · the old "berth history" chart shows a fixed 31 Oct – 9 Nov window · several PREDLOG rows still wait for actual berthing times · Sea Gautham is held out of the projection while the list carries "DISPUTE".
- **History:** `git log` in the repo (one commit per version, message says what changed); the artifact keeps every version.
