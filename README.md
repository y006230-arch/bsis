# BSIS — 플랜티넷 손익 대시보드

`26년04월.gbapal리회계_플랜티넷_v0_0519.xlsx`의 **월별손익** 시트 데이터를 기반으로 한 HTML 손익 대시보드입니다.

## 대시보드

| 파일 | 설명 |
|------|------|
| `손익요약_대시보드.html` | 사업부 / 임대 / 회사 롤업 손익 요약 |
| `사업부통합_대시보드.html` | 부서별(5팀 + 임대) 손익 통합 |
| `월별손익_대시보드.html` | 월별 상세 손익 (부문·부서) |

브라우저에서 HTML 파일을 더블클릭하면 바로 열립니다. (데이터가 HTML에 포함됨)

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
