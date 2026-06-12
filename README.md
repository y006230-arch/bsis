# BSIS — 플랜티넷 손익 대시보드

`26년04월 관리회계_플랜티넷_v0_0519.xlsx`의 **월별손익** 시트 데이터를 기반으로 한 HTML 손익 대시보드입니다.

## 대시보드

| 파일 | 설명 |
|------|------|
| `손익요약_대시보드.html` | 사업부 / 임대 / 회사 롤업 손익 요약 |
| `사업부통합_대시보드.html` | 부서별(5팀 + 임대) 손익 통합 |
| `월별손익_대시보드.html` | 월별 상세 손익 (부문·부서) |

브라우저에서 HTML 파일을 더블클릭하면 바로 열립니다. (로컬 파일은 인증 없음)

## 접속 인증 (Vercel 배포)

**라이브 URL:** https://bsis-pearl.vercel.app

로그인 · 비밀번호 · **허용 IP** 가 모두 일치해야 대시보드에 접속할 수 있습니다.

Vercel 프로젝트 → **Settings → Environment Variables** 에 아래 값을 설정하세요:

| 변수 | 설명 |
|------|------|
| `AUTH_USER` | 로그인 아이디 |
| `AUTH_PASSWORD` | 로그인 비밀번호 |
| `AUTH_SECRET` | 세션 암호화용 임의 문자열 (32자 이상 권장) |
| `ALLOWED_IPS` | 허용 IP (쉼표 구분, 예: `123.45.67.89,203.0.113.1`) |

IP가 등록되지 않으면 로그인 화면에 **현재 IP**가 표시됩니다. 해당 IP를 `ALLOWED_IPS`에 추가한 뒤 재배포하세요.

`.env.example` 참고.

## Vercel 배포

**라이브 URL:** https://bsis-pearl.vercel.app

- GitHub 저장소와 Vercel이 연동되어 `main` 브랜치 푸시 시 자동 재배포됩니다.

## 데이터 재생성

엑셀 파일을 수정한 경우:

```powershell
pip install pandas openpyxl

# 손익 요약 대시보드
python _extract.py
python _build2.py

# 사업부 통합 대시보드
python _extract_dept.py
python _build_bu.py
```

## 참고

- 단위: 백만원
- 4~5월 이후 동일값 반복 구간은 **계획(추정)** 으로 표시
- 목표(P) / 전년(LY) 데이터는 원본 시트에 없어 대시보드에 미포함
