# Perpline 그로스 실험 장부

담당: Perpline 그로스 매니저(매일 예약 작업). 실험 1개 = 병목 1개. '가입 클릭'은 가입이 아니다 — 실제 가입은 세준이 월요일에 주는 거래소 대시보드 숫자(+BTCC 주간 메일)만.
측정: Savri site_mvvy2a4d_govfksp 목표(`pl_signup_click`, `pl_signup_<거래소>`, `pl_claim_click`, `/perpline/start.html`). 랜딩 클릭률 = pl_signup_click ÷ start.html 방문.

| ID | 시작 | 병목(근거) | 가설 | 변경 | 지표 | 판정일 | 결과 · 결정 |
|---|---|---|---|---|---|---|---|
| E1 | 2026-11-03 | 광고 랜딩 이탈: 11/2~ start.html 방문 12 → 가입 클릭 3(25%, 전부 BTCC 히어로 버튼), 신청 클릭 1. 사이트 전체 이탈 85.7%(10/31~11/1). 모바일 첫 화면엔 '얼마 돌려받나'가 %만 있고 금액·'비밀번호 불필요'가 숨겨져 있음 | 차가운 배너 유입은 %보다 달러 금액 예시와 안전 문구를 버튼 바로 아래서 보면 클릭이 는다 | start.html 히어로 CTA 아래 1줄: "Example: $100,000 traded in a month on BTCC is $45 in taker fees, so $27 comes back to you. No password or API key needed." (BTCC 표준 taker 0.045% × 60%, build.py에서 자동 계산, data-place=hero-example). 모바일에서도 표시 | 1차: pl_signup_click ÷ start.html 방문(기준 25%, n=12). 2차: pl_claim_click, start.html 이탈 | 2026-11-10 | (대기) n이 작아 랜딩 방문 50 미만이면 판정 7일 연장 |
| E2 | 2026-11-04 | 홈 첫 화면에 가입 버튼 없음: 7일 /perpline/+index.html 방문 7 → 가입 클릭 0(현재 가입 클릭 3건 전부 start.html BTCC 히어로). 모바일 홈 첫 '가입' 버튼이 y≈1,579px(약 2화면 아래), 히어로 버튼 2개는 모두 페이지 내 이동. 반면 첫 화면 직결 버튼이 있는 start.html은 11/2~ 14방문 → 3클릭(21%) | 홈 방문자(직접·IG·FB·검색)도 첫 화면에서 바로 1위 거래소를 열 수 있으면 클릭이 0에서 벗어난다 | index.html 1번 슬라이드 버튼: 'Choose an exchange'(#venues) + 'How the rebate works' → **'Open BTCC · 60% back'(레퍼럴 링크 그대로, data-place=home-hero)** + 'Compare all 11 exchanges'(#venues). '어떻게 받나'는 2번 슬라이드·본문에 그대로. 측정용 이벤트 `pl_signup_home`(홈 경로에서 가입 클릭 시) + Savri 목표 추가 | 1차: pl_signup_home ÷ 홈 방문(기준 0/7). 2차: 홈 pl_claim_click | 2026-11-11 | (대기) 홈 방문 30 미만이면 7일 연장 |

## 회차 메모
- 2026-11-05(목): 새 실험 보류. 근거: 11/2~ start.html 22방문→가입 클릭 5(23%, BTCC 4·BloFin 1), 홈 6방문→pl_signup_home 2, 신청 클릭 1. 하루 유입이 49(11/3)까지 줄어 E1·E2가 아직 판정 표본에 못 미침. 같은 화면에 세 번째 변경을 얹으면 효과를 가를 수 없어 건드리지 않음. 마키 로고는 CoinGecko 핫링크라 이 환경(프록시 403)에선 배포본 렌더 확인 불가 — 확인되면 assets/logos/<slug>.png로 자체 호스팅 후보. 판정일(11/10·11/11)은 그대로.

## 다음 실험 후보
- 마키(거래소 띠) 로고 이미지가 캡처에서 깨져 alt 글자('O','G')만 보임 — 실제 배포본에서도 깨지는지 확인 필요(신뢰 요소). 로컬 캡처 환경 탓일 수 있음.
- 가이드(guides/bitget-futures-fees.html) 모바일 첫 가입 버튼이 y≈7,371/8,793px(84% 지점). 검색 유입이 생기면 '짧은 요약' 바로 아래 가입 박스 실험.
- 가이드 페이지(exchanges/*.html·guides/*) 검색 유입이 생기면 그 페이지 가입 클릭 비교 — 3단계 띠는 고도화 작업(수) 담당이라 겹치지 않게.
- 광고 잔액 소진으로 11/2 클릭 19 → 트래픽이 끊기면 실험 판정 불가. 충전은 세준 결정(광고팀이 이미 요청 중).
