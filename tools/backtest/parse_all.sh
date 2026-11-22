set -e
cd /home/claude/berth-board
p(){ python3 -I tools/parse_xlsx.py "$1" "/home/claude/work/bt/$2.json" >/dev/null 2>&1 && echo "ok $2"; }
p data/2026-11-10/list_10.11_0700.xlsx l10
p data/2026-11-11/list_11.11_0700.xlsx l11
p data/2026-11-12/list_12.11_0700.xlsx l12
p data/2026-11-13/list_13.11_0700.xlsx l13
p data/2026-11-14/DAILY_BERTHING_LIST_14.11.2026.xlsx l14
p data/2026-11-16/DAILY_BERTHING_LIST_16.11.2026_morning_issue.xlsx l16
p data/2026-11-17/DAILY_BERTHING_LIST_17.11.2026.xlsx l17
p data/2026-11-18/DAILY_BERTHING_LIST_18.11.2026.xlsx l18
p data/2026-11-19/DAILY_BERTHING_LIST_19.11.2026.xlsx l19
p data/2026-11-20/DAILY_BERTHING_LIST_20.11.2026.xlsx l20
p data/2026-11-21/Daily_Berthing_List_21.11.2026.xlsx l21
p data/2026-11-21/Daily_Berthing_List_21.11.2026_revised.xlsx l21r
