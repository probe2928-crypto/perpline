# X 스레드 초안 — 가이드 3편 (2026-11-11, 5개 팀 회의 결정 3 · 마케팅)

상태: **초안. 게시 안 함 — 세준 OK 필요.** 게시하면 아래 UTM으로 GA에서 x → 가이드 → 가입 클릭을 처음으로 따로 본다.
규칙 점검: 레퍼럴 코드 없음(링크만) · 가격 예측·투자 권유 없음 · 숫자는 가이드 본문(Bitget 공식 FAQ, 11/3 확인)과 산수만 · 해시태그·멘션 스팸 없음 · 한국 대상 아님.
공유 카드: 이번 회차에 가이드별 OG 이미지(assets/og/<slug>.png)를 붙였으므로 링크만 넣어도 제목 카드가 뜬다.
산수 확인(python): $10,000 × 0.06% = $6.00 · 진입+청산 $12.00 · 40% 페이백 $4.80 · 실효 테이커 0.036%. 메이커 0.02% → $2.00/회.

---

## 스레드 A — Maker vs taker (가장 넓은 검색어)
링크: https://perpline.tech/guides/maker-vs-taker-fees.html?utm_source=x&utm_medium=social&utm_campaign=guide_maker_taker

1/ Most futures traders pay the taker rate on more of their volume than they think. Stop-losses and fast exits are almost always taker fills.

2/ On Bitget's standard USDT perps that is 0.06% taker vs 0.02% maker. On a $10,000 position: $6.00 to take, $2.00 to make. In and out as a taker: $12.00.

3/ A limit order is not automatically a maker order. If it crosses the spread, it fills at once and is charged as a taker. "Post-only" is the simple fix on entries.

4/ We wrote the whole thing out in dollars, with a realistic month: (링크)

## 스레드 B — Funding fees (오해가 많은 주제)
링크: https://perpline.tech/guides/how-funding-fees-work.html?utm_source=x&utm_medium=social&utm_campaign=guide_funding

1/ Funding is not a trading fee. It is a payment between traders, set by the exchange, to keep a perpetual close to spot.

2/ Positive rate: longs pay shorts. Negative: shorts pay longs. You only pay or receive it if you hold a position at the settlement time.

3/ The payment = position value × funding rate at that moment. The longer you hold, the more it can matter next to your entry and exit fees.

4/ One thing people get wrong: a fee rebate is a share of trading fees, so it never covers funding. Plain-number walkthrough: (링크)

## 스레드 C — Bitget futures fees (거래소 이름 검색어)
링크: https://perpline.tech/guides/bitget-futures-fees.html?utm_source=x&utm_medium=social&utm_campaign=guide_bitget

1/ Bitget's standard futures rate is 0.02% maker / 0.06% taker (from Bitget's own fee FAQ, checked 3 Nov 2026). VIP tiers go lower.

2/ The fee is charged on order value, not margin. Leverage does not change the rate, but it changes how big an order your margin opens.

3/ Through Perpline, 40% of those trading fees come back to you in USDT every week, so a 0.06% taker fill works out to 0.036%.

4/ The full breakdown, with a normal month in dollars: (링크)
   Not available to residents of Korea or the US.

---

## 모션 광고 X 캡션 (perpline ads/video "Your trading fees, returned." — 게시 OK 대기 건에 붙일 문구)
Every futures trade has a fee. Up to 60% of it can come back to you, in USDT, every Monday. 11 exchanges, ranked by what you actually pay.
https://perpline.tech/start.html?utm_source=x&utm_medium=social&utm_campaign=motion_fees_returned

## 게시 순서 제안(세준 OK 시)
B(펀딩비, 11/10 신규) → A → C, 하루 1개. 같은 문구를 여러 계정·커뮤니티에 뿌리지 않는다(스팸 금지). Reddit 답변형은 이번엔 만들지 않음(서브레딧 홍보 규칙 위험).
