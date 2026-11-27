# Process book

What is done with each paper, step by step. The aim: papers go into the data book, the rule book is applied, and the display board shows the result.

## 1. What Mihir does

- Send the papers in the chat as they come: berthing list, DPR, programme, signal sheets, timber desk sheet, circulars. No text is needed.
- Say in one line when a rule changes or the port does something different.
- Ask any question. The answer is taken from the data book.

## 2. Daily berthing list (Excel, position 0700)

- At-berth sheet: who is alongside, panels, made fast, commenced, norm, list ETC.
- Waiting sheet: every waiting vessel with her ranks, readiness and remarks. "B'TODAY" and an X in the rank columns mean she is being berthed.
- Expected sheet: ETA of vessels not yet arrived.
- New vessel: add her record, and look up her gear once.
- A vessel that has left the list has sailed; her exact hour comes from the DPR.

## 3. Daily performance report — DPR (position 0700)

- When a later list re-states a vessel's quantity, the DPR balance is out of date: no finishing time is taken from it until the next DPR. When a programme shifts a working vessel, the hours of the shift are added to her finish. *(board, 26 Nov — Safi Alfa; Asian Summit, Blue Shark)*
- The DPR's "Stevd." column gives the stevedore of every working vessel. After each DPR the board's stevedore list is rebuilt from all the DPRs on file and shown beside the agent *(Mihir, 25 Nov)*.

- For each vessel: work in the last 24 hours, total so far, balance, gangs and hooks.
- Remarks give the actual hours: made fast, commenced, completed, left the berth.
- Midstream and mooring rows go to the barge record.
- A vessel that worked only part of the day is marked so; her figure is not a day's rate.

## 4. Movement programme (after the 11:00 meeting)

- Who berths and who sails in the window 18:00 to 18:00.
- The board's call for that meeting is scored against it: named right, berth right.
- The call is never rebuilt after the meeting hour.

## 5. Harbour master's signal sheets (photos)

- Each row: pilot, hour, IN / OUT / SHIFT, vessel, from, to.
- For an IN from OTB the hour is the pilot boarding; she is alongside about two hours later.
- A sheet can have two pages. An amended sheet replaces the earlier one.

## 6. Timber desk sheet

- CBM, origin, ETA and expected berthing date of every log vessel.
- Laytime and demurrage are counted on the desk's CBM.

## 7. After every paper

- The record of each vessel in the data book is updated: nothing is deleted; a sailed vessel stays in the record.
- The rule book is applied to give the next berth and date for every ready vessel.
- If the result for a Mihir & Company vessel moves, it is said plainly with the reason.
- Checks are run before anything is published.
- The display board is published, and the data book is rebuilt from it with one command: `node tools/build_db.js <board> ` then `python3 tools/build_books.py`.

## 8. Asking the data book

- Examples: average waiting of salt vessels; every call at CJ-13 this month; how many days a vessel took against her norm; what was predicted and what happened.
- The answer is worked out from the data book files, not from memory.

## 9. Where things are kept

- **Data book:** `db/databook.json` in the repository, and the Data book page.
- **Rule book and process book:** `book/` in the repository, and the same page.
- **Every paper received:** `data/YYYY-MM-DD/` in the repository.
- **Display board:** the DPA Berth Board page.

## Header of the board (from 21 Nov)

- Under the title: "Board owned by @mk", the last-updated time, and one small box per paper — List, Programme, DPR, Signals — with the date the board is updated to.
- "Sources & tide" holds one sentence naming the day's papers, and the tide. The full log of every paper received is kept in `handover/SOURCES_LOG.md`, newest first; add a line there with every update.


## Timber vessels — load port (standing, Mihir 27 Nov 2026)

For every timber vessel, when she first appears: find her load port from public AIS port calls (Maritime Optima public page, last 3 calls) and put it on her `TIMBER.rows` entry as `lp` with the note `lpn`. Take the last log port, not a bunker stop. Not sure → add "?"; nothing reliable → leave `lp` empty (the tab shows "port not found") and try again at the next update. The agent's paper or Mihir's word overrides what the web shows.
