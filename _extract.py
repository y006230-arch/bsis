import pandas as pd
import json

fn = "26년04월 관리회계_플랜티넷_v0_0519.xlsx"
df = pd.read_excel(fn, sheet_name="월별손익", header=None)
df = df.where(pd.notnull(df), None)

def num(i, j):
    v = df.iat[i, j]
    try:
        f = float(v)
        return f
    except (TypeError, ValueError):
        return 0.0

def label(i):
    v = df.iat[i, 1]
    return "" if v is None else str(v).strip()

def group(i):
    v = df.iat[i, 0]
    return "" if v is None else str(v).strip()

MONTHS = list(range(1, 13))

def seg_cols(m, half):
    start = 2 + 68 * (m - 1)
    off = 29 if half == "A" else 63
    base = start + off
    return {"cust": base, "biz": base + 1, "moa": base + 2, "rent": base + 3, "total": base + 4}

# Curated row set for the dashboard
ROWS = {
    "revenue": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "direct_cost": [22, 23, 24, 25, 26],
    "gross_profit": [27],
    "profit_lines": [70, 115, 160, 205, 250],
}

# Build a record for each labeled row
def row_record(i):
    rec = {"row": i, "label": label(i), "group": group(i), "monthly": {}, "cum": {}}
    for m in MONTHS:
        a = seg_cols(m, "A")
        b = seg_cols(m, "B")
        rec["monthly"][m] = {k: num(i, c) for k, c in a.items()}
        rec["cum"][m] = {k: num(i, c) for k, c in b.items()}
    return rec

data = {"months": MONTHS, "segments": ["cust", "biz", "moa", "rent"],
        "segment_labels": {"cust": "커스터머", "biz": "비즈", "moa": "모아진", "rent": "임대"},
        "rows": {}}

all_rows_of_interest = set()
for v in ROWS.values():
    all_rows_of_interest.update(v)
# also include all labeled rows for full P&L table
for i in range(df.shape[0]):
    if label(i) and i >= 6:
        all_rows_of_interest.add(i)

for i in sorted(all_rows_of_interest):
    data["rows"][i] = row_record(i)

# Department revenue (current month, row 6 매출)
# dept layout per month half A: C(start)..: Customer(커,비,모)=+0,+1,+2 ; M본부=+3,+4,+5 ; Biz=+6,+7,+8 ; 해외=+9,+10,+11 ; 경영지원=+27
dept_defs = [("Customer사업팀", 0), ("M_2본부영업팀", 3), ("Biz사업팀", 6), ("해외사업팀", 9)]
def dept_rev(i, m, half):
    start = 2 + 68 * (m - 1)
    base = start + (0 if half == "A" else 34)
    res = {}
    for name, off in dept_defs:
        res[name] = num(i, base + off) + num(i, base + off + 1) + num(i, base + off + 2)
    res["경영지원팀"] = num(i, base + 27)
    return res

data["dept_revenue_monthly"] = {m: dept_rev(6, m, "A") for m in MONTHS}
data["dept_opincome_monthly"] = {m: dept_rev(250, m, "A") for m in MONTHS}

with open("dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print("rows extracted:", len(data["rows"]))
print("sample 매출 monthly total:", {m: data["rows"][6]["monthly"][m]["total"] for m in MONTHS})
print("OK")
