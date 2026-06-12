import json
import os

import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
fn = next(f for f in os.listdir(".") if f.endswith(".xlsx"))
df = pd.read_excel(fn, sheet_name="월별손익", header=None)
df = df.where(pd.notnull(df), None)

MONTHS = list(range(1, 13))

DEPTS = [
    {"id": "customer", "label": "Customer사업팀", "kind": "triple", "offset": 0},
    {"id": "m2", "label": "M_2본부영업팀", "kind": "triple", "offset": 3},
    {"id": "biz", "label": "Biz사업팀", "kind": "triple", "offset": 6},
    {"id": "overseas", "label": "해외사업팀", "kind": "triple", "offset": 9},
    {"id": "support", "label": "경영지원팀", "kind": "single", "offset": 27},
    {"id": "rent", "label": "임대", "kind": "rent", "offset": 32},
    {"id": "total", "label": "합계", "kind": "segment_total", "offset": 33},
]

KEY_ROWS = {
    "revenue": {"row": 6, "label": "매출"},
    "gross_profit": {"row": 27, "label": "매출총이익"},
    "dept_operating": {"row": 70, "label": "매출부서 영업이익"},
    "after_direct": {"row": 115, "label": "직접지원 차감 후"},
    "after_indirect": {"row": 160, "label": "간접지원 차감 후"},
    "division_profit": {"row": 205, "label": "연구소 차감 후"},
    "operating_income": {"row": 250, "label": "영업이익"},
}


def num(i, j):
    v = df.iat[i, j]
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def month_base(m, half):
    start = 2 + 68 * (m - 1)
    return start + (0 if half == "A" else 34)


def dept_value(row, m, half, dept):
    base = month_base(m, half)
    kind = dept["kind"]
    if kind == "triple":
        o = dept["offset"]
        return num(row, base + o) + num(row, base + o + 1) + num(row, base + o + 2)
    if kind == "single":
        return num(row, base + dept["offset"])
    if kind == "rent":
        return num(row, base + dept["offset"])
    if kind == "segment_total":
        seg_base = month_base(m, half) + 29
        return num(row, seg_base + 4)
    return 0.0


def row_dept_record(row_idx):
    rec = {"row": row_idx, "monthly": {}, "cum": {}}
    for m in MONTHS:
        rec["monthly"][m] = {d["id"]: dept_value(row_idx, m, "A", d) for d in DEPTS}
        rec["cum"][m] = {d["id"]: dept_value(row_idx, m, "B", d) for d in DEPTS}
    return rec


data = {
    "source": fn,
    "sheet": "월별손익",
    "months": MONTHS,
    "departments": [{"id": d["id"], "label": d["label"]} for d in DEPTS],
    "metrics": KEY_ROWS,
    "rows": {key: row_dept_record(meta["row"]) for key, meta in KEY_ROWS.items()},
    "meta": {
        "note": "6.사업부 통합 시트는 본 워크북에 없어 월별손익 부서열 기준으로 재구성",
        "plan_start_hint": 5,
    },
}

with open("dept_dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

# quick verification print
m = 3
rev = data["rows"]["revenue"]["cum"][m]
gp = data["rows"]["gross_profit"]["cum"][m]
dp = data["rows"]["division_profit"]["cum"][m]
print("Q1 cum verify (백만원):")
print("  매출 total", round(rev["total"] / 1e6))
print("  매출 depts", round(sum(rev[d["id"]] for d in DEPTS if d["id"] not in ("total",)) / 1e6))
print("  사업부이익(R205) total", round(dp["total"] / 1e6))
print("  Customer R205", round(dp["customer"] / 1e6))
print("OK")
