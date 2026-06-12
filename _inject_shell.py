"""Inject ERP-style shell header into 월별손익_대시보드.html"""
from pathlib import Path

SHELL_HEAD = '''<link rel="stylesheet" href="/assets/shell.css">
</head>
<body>
<header class="site-hdr">
  <div class="site-hdr-inner">
    <a href="/dashboard" class="site-brand">
      <span class="site-logo">B</span>
      <div>
        <div class="site-brand-title">플랜티넷 BSIS</div>
        <div class="site-brand-sub">관리회계 · 손익 분석</div>
      </div>
    </a>
    <nav class="site-nav">
      <a href="/dashboard">대시보드</a>
      <div class="nav-dd">
        <button type="button" class="nav-dd-btn" aria-expanded="false">손익 대시보드 ▾</button>
        <div class="nav-dd-menu">
          <a href="/손익요약_대시보드">손익 요약</a>
          <a href="/사업부통합_대시보드">사업부 통합</a>
          <a href="/월별손익_대시보드">월별손익 상세</a>
        </div>
      </div>
    </nav>
  </div>
</header>
<main class="site-main">
'''

SHELL_TAIL = '''
</main>
<script src="/assets/shell.js" defer></script>
</body>'''

def inject(path: Path):
    html = path.read_text(encoding='utf-8')
    if 'site-hdr' in html:
        print(path.name, 'already has shell')
        return
    html = html.replace('</head>\n<body>\n<div class="wrap">', SHELL_HEAD + '<div class="wrap">', 1)
    if 'site-hdr' not in html:
        html = html.replace('</head>\n<body>\n', SHELL_HEAD, 1)
    html = html.replace('</body>', SHELL_TAIL, 1)
    path.write_text(html, encoding='utf-8')
    print('injected', path.name)

if __name__ == '__main__':
    inject(Path('월별손익_대시보드.html'))
