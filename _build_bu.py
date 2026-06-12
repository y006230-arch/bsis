import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("_template_bu.html", "r", encoding="utf-8") as f:
    tpl = f.read()
with open("dept_dashboard_data.json", "r", encoding="utf-8") as f:
    data = f.read()

out = tpl.replace("/*__DATA__*/", data)
with open("사업부통합_대시보드.html", "w", encoding="utf-8") as f:
    f.write(out)

print("built 사업부통합_대시보드.html:", len(out), "bytes")
