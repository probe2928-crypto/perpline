# Perpline 그로스 실험 장부

담당: Perpline 그로스 매니저(매일 예약 작업). 실험 1개 = 병목 1개. '가입 클릭'은 가입이 아니다 — 실제 가입은 세준이 월요일에 주는 거래소 대시보드 숫자(+BTCC 주간 메일)만.
측정: Savri site_mvvy2a4d_govfksp 목표(`pl_signup_click`, `pl_signup_<거래소>`, `pl_claim_click`, `/perpline/start.html`). 랜딩 클릭률 = pl_signup_click ÷ start.html 방문.

| ID | 시작 | 병목(근거) | 가설 | 변경 | 지표 | 판정일 | 결과 · 결정 |
|---|---|---|---|---|---|---|---|
| E1 | 2026-11-03 | 광고 랜딩 이탈: 11/2~ start.html 방문 12 → 가입 클릭 3(25%, 전부 BTCC 히어로 버튼), 신청 클릭 1. 사이트 전체 이탈 85.7%(10/31~11/1). 모바일 첫 화면엔 '얼마 돌려받나'가 %만 있고 금액·'비밀번호 불필요'가 숨겨져 있음 | 차가운 배너 유입은 %보다 달러 금액 예시와 안전 문구를 버튼 바로 아래서 보면 클릭이 는다 | start.html 히어로 CTA 아래 1줄: "Example: $100,000 traded in a month on BTCC is $45 in taker fees, so $27 comes back to you. No password or API key needed." (BTCC 표준 taker 0.045% × 60%, build.py에서 자동 계산, data-place=hero-example). 모바일에서도 표시 | 1차: pl_signup_click ÷ start.html 방문(기준 25%, n=12). 2차: pl_claim_click, start.html 이탈 | 2026-11-10 | (대기) n이 작아 랜딩 방문 50 미만이면 판정 7일 연장 |

## 다음 실험 후보
- 가이드 페이지(exchanges/*.html·guides/*) 검색 유입이 생기면 그 페이지 가입 클릭 비교 — 3단계 띠는 고도화 작업(수) 담당이라 겹치지 않게.
- 광고 잔액 소진으로 11/2 클릭 19 → 트래픽이 끊기면 실험 판정 불가. 충전은 세준 결정(광고팀이 이미 요청 중).
