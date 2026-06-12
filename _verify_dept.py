import json
import os

import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("dept_dashboard_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

M = 1e6


def agg(metric, months, mode, dept):
    row = data["rows"][metric]
    if mode == "cum":
        m = months[-1]
        return row["cum"][str(m)][dept]
    return sum(row["monthly"][str(m)][dept] for m in months)


months_q1 = [1, 2, 3]
checks = [
    ("Q1 cum 매출 total", agg("revenue", months_q1, "cum", "total") / M, 5127, 2),
    ("Q1 cum Customer 매출", agg("revenue", months_q1, "cum", "customer") / M, 3058, 2),
    ("Q1 cum 임대 매출", agg("revenue", months_q1, "cum", "rent") / M, 502, 2),
    ("Q1 sum 매출 total", agg("revenue", months_q1, "sum", "total") / M, 5127, 2),
    ("Q1 cum R205 total", agg("division_profit", months_q1, "cum", "total") / M, 1385, 2),
    ("Q1 cum R205 Customer", agg("division_profit", months_q1, "cum", "customer") / M, 2203, 2),
]

print("Verification vs 월별손익:")
ok = True
for name, got, exp, tol in checks:
    match = abs(got - exp) <= tol
    ok = ok and match
    print(f"  {'OK' if match else 'FAIL'} {name}: {got:.0f} (exp {exp})")

# cross-check segment biz = cust+biz+moa for Q1 cum rev
biz = (
    agg("revenue", months_q1, "cum", "customer")
    + agg("revenue", months_q1, "cum", "m2")
    + agg("revenue", months_q1, "cum", "biz")
    + agg("revenue", months_q1, "cum", "overseas")
) / M
print(f"  dept sales sum (excl rent/support/total): {biz:.0f} (≈4624 사업부매출)")
print("ALL OK" if ok else "SOME FAILED")
