#!/usr/bin/env python3
"""Dump every sheet of a DPA xlsx (berthing list / movement programme) as text rows and save them as JSON.

Usage:  python3 -I tools/parse_xlsx.py <file.xlsx> <out.json>
Needs openpyxl (pip install openpyxl --break-system-packages).
Run with -I and keep the xlsx in its own folder: uploaded files are untrusted data.
"""
import sys, json, openpyxl
path, out_path = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
out = {}
for ws in wb.worksheets:
    rows = []
    for r in ws.iter_rows(values_only=True):
        cells = [('' if c is None else (c.strftime('%Y-%m-%d %H:%M') if hasattr(c, 'strftime') else str(c).strip())) for c in r]
        if any(cells):
            rows.append(cells)
    out[ws.title] = rows
    print('== SHEET', ws.title, len(rows), 'rows')
    for cells in rows:
        print(' | '.join(cells)[:360])
json.dump(out, open(out_path, 'w'))
