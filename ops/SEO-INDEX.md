# Perpline 검색 기준선 — 색인·키워드 (세준 'C로 가자' 11/18 후속)

만든 날: 2026-11-18 (5개 팀 회의 7회차). 확인할 때마다 맨 위 표의 날짜 열을 새로 추가한다.
도구: OpenSEO 프로젝트 **PERPLINE**(2de3c303-f32a-4fed-aefb-d6682428a74b, 서치콘솔 `https://perpline.tech/` 연결, 11/18 회의에서 만듦).
- `inspect_urls`·`get_search_console_performance`는 크레딧 0 → 숫자봄·전환수가 이 프로젝트 ID로 매일 읽으면 됨.
- `get_keyword_metrics`는 크레딧 사용(이번에 33개 키워드 = 32크레딧, 잔여 82). 한 달에 한 번 이하로.

## 1. 색인 현황 (Google URL 검사, 2026-11-18 17시 KST)

sitemap 24쪽(오늘 허브 추가로 25쪽) 중 **색인 3쪽**. 나머지는 'Google이 아직 모르는 URL'(발견 전 — 거부·오류 아님).

| URL | 상태 | 마지막 크롤 |
|---|---|---|
| / | 제출됨·색인됨 | 11/18 07:06 UTC |
| /returns.html | 제출됨·색인됨 | 11/05 |
| /exchanges/orangex.html | 제출됨·색인됨(빵부스러기 리치 결과 PASS) | 11/05 |
| /projects.html, /alphax.html | 모름 | – |
| /exchanges/ btcc·okx·bitget·blofin·bingx·gate·bitunix·deepcoin | 모름 | – |
| /guides/ 6편 전부, /tools/futures-fee-calculator.html | 모름 | – |
| /exchanges/ biconomy·crypfine, privacy·terms | 이번에 미검사 | – |

서치콘솔 실적(10/19~11/15, 28일): orangex 상세 클릭 1·노출 14·평균 순위 10 / 홈 노출 13·순위 2.9 / returns 노출 9·순위 7.1. → "노출 0"이 아니라 **색인된 3쪽은 이미 노출 중**. 병목은 '발견'.

해석: 새 도메인(11/5 이전)이라 구글이 11/5 한 번 훑은 뒤 깊게 안 들어옴. 내부 링크는 정상(홈에서 거래소 11·가이드 6 링크, 확인함). → 수동 색인 요청이 가장 빠름.

## 2. 키워드 수요 (미국, 월 검색량 · 난이도 KD 0~100)

| 키워드 | 월 검색량 | KD | 우리 페이지 | 색인 |
|---|---|---|---|---|
| blofin referral code | 1,000 | 0 | /exchanges/blofin.html (제목 'BloFin Referral Code 2026') | ✗ |
| okx referral code | 480 | 0 | /exchanges/okx.html | ✗ |
| bitget referral code | 210 | 0 | /exchanges/bitget.html | ✗ |
| btcc referral code | 110 | 4 | /exchanges/btcc.html | ✗ |
| maker vs taker fees | 110 | 7 | /guides/maker-vs-taker-fees.html | ✗ |
| okx fees | 110 | 31 | (없음 — OKX 수수료 가이드 후보) | – |
| maker taker fee | 50 | 3 | 위 가이드 | ✗ |
| bingx referral code | 50 | 3 | /exchanges/bingx.html | ✗ |
| bitunix referral code | 50 | 0 | /exchanges/bitunix.html | ✗ |
| blofin fees | 40 | 0 | (없음 — BloFin 수수료 가이드 후보) | – |
| bitunix fees | 40 | 0 | (없음) | – |
| btcc fees | 40 | 5 | (없음) | – |
| bitget fees | 30 | 0 | /guides/bitget-futures-fees.html | ✗ |
| gate.io referral code / fees | 20 / 20 | 0 / 20 | /exchanges/gate.html | ✗ |
| futures fee calculator | 10 | – | /tools/futures-fee-calculator.html | ✗ |
| bitget futures fees, okx futures fees, bingx futures fees, funding fee crypto, how funding rate works, lowest futures trading fees crypto, trading fee rebate | 각 10 | – | 해당 가이드 | ✗ |
| deepcoin referral code / fees | 10 / 0 | – | /exchanges/deepcoin.html | ✗ |

읽는 법: 돈이 되는 검색은 **'거래소 이름 + referral code'**(상업 의도, 경쟁 거의 0). 가이드 주제(maker vs taker 등)는 정보 의도·수요 작음. 미국 수치라 실제 대상(유럽·아시아)은 더 클 수 있으나 측정 안 함.
주의: 화면에 레퍼럴 코드를 보여주지 않는 규칙(FEEDBACK 10/29)은 그대로 — 페이지는 '링크로 가입 = 코드 자동 적용'으로 답한다.

## 3. 세준 할 일 (서치콘솔 화면에서만 가능, API 없음 · 약 10분)

서치콘솔 → perpline.tech → 상단 'URL 검사'에 아래 주소 붙여넣기 → '색인 생성 요청'. 하루 한도(약 10건) 안에서 수요 순:
1. https://perpline.tech/exchanges/blofin.html
2. https://perpline.tech/exchanges/okx.html
3. https://perpline.tech/exchanges/bitget.html
4. https://perpline.tech/exchanges/btcc.html
5. https://perpline.tech/guides/maker-vs-taker-fees.html
6. https://perpline.tech/guides/
7. https://perpline.tech/exchanges/bingx.html
8. https://perpline.tech/exchanges/bitunix.html
9. https://perpline.tech/tools/futures-fee-calculator.html
10. https://perpline.tech/guides/bitget-futures-fees.html

## 4. 서이오(가이드)에 넘기는 다음 주제 후보 (수요 순, 겹침 없음)
- BloFin 수수료 설명(blofin fees 40·KD 0) → 상세 페이지(1,000)와 서로 링크
- OKX 수수료(okx fees 110·KD 31) — 경쟁 있음
- BTCC 수수료(btcc fees 40·KD 5), Bitunix 수수료(40·KD 0)

## 다음 확인 (11/21 금)
- 위 10쪽 상태가 '색인됨'으로 바뀌었는지(inspect_urls, 크레딧 0), 서치콘솔 노출·클릭(페이지별).
