# Backtest on the port's own lists

Started 22 Nov 2026 (Mihir: "last 10 din ke kaunse vessel kyun lage — wahan se rule nikalo").

- `parse_all.sh` parses the archived daily berthing lists (`data/YYYY-MM-DD/`) into JSON (work folder `bt/`).
- `load.py` reads a parsed list: the AT BERTH sheet (each vessel under the priority heading the port prints) and the WAITING / ETA sheets (rank in each priority column).
- `bt.py` lists every new berthing between two lists: the priority heading it berthed under, its rank in that column on the list of the day before, and who stood ahead of it.

Add each new day's list to `parse_all.sh` and to `tags` in `bt.py`, run, and compare with what the board had shown.
