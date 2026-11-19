# Perpline 배포 기록 (2026-11-19 결정: 회의·분석 대신 밖에 실제로 올리는 일만)

목표: 11/25까지 실제 가입 1명 이상. 게시는 세준 로그인 계정으로만(X @chainbrief_hq, 텔레그램 @chainbrief_global, 허용되는 그룹/서브레딧).

## 게시 기록
날짜 | 채널 | 글 링크 | 클릭 | 비고
--- | --- | --- | --- | ---
2026-11-19 | X @chainbrief_hq | x.com/chainbrief_hq/status/2123264799907946955 | 확인 불가 | 메이커·테이커 스레드 4/4 (실무이사 게시)
2026-11-19 | 텔레그램 CHAINBRIEF | (링크 미기록) | 확인 불가 | 계산기 공유, utm_campaign=sejun_share
2026-11-19 | (전환수 회차) | 없음 | - | 내장 브라우저 도구 미연결로 게시 못 함 → 아래 대기 글

2026-11-20 10:13 | X @chainbrief_hq (Typefully 예약 12032521) | 예약 | - | 대기2 break-even 스레드 3
2026-11-21 10:13 | X @chainbrief_hq (Typefully 예약 12032523) | 예약 | - | 대기3 funding 스레드 3

## 대기 글 (브라우저 연결되면 채널당 하루 1건씩 게시)
공통: 광고 문구·수익 약속·가격 예측 금지. 마지막 줄에만 링크. utm_source는 게시 채널명으로 교체.

### 대기 1 — X / 텔레그램용 (가이드: maker-vs-taker-fees)
Same $10,000 futures position, same 40 round trips a month. Only the order type changes.

Assumed example rates (check your exchange's current schedule): maker 0.02%, taker 0.05% per side.

- All maker: $2 open + $2 close = $4 per round trip → $160/month
- All taker: $5 open + $5 close = $10 per round trip → $400/month
- Gap: $240/month, before any profit or loss on the trades themselves

Fees don't care whether the trade won. If you trade often, order type is a real line item.

Not available in South Korea or the US. Leveraged trading can lose all your margin.
How the two fee types work: https://perpline.tech/guides/maker-vs-taker-fees.html?utm_source=x

### 대기 2 (→ Typefully 예약 11/20) — X / 레딧(허용 시)용 (가이드: futures-break-even-price)
Quick math on why a trade can be "right" and still lose money.

$1,000 margin at 10x = $10,000 position. With an example 0.05% taker fee each side, round-trip fees are $10, which is 1% of your margin. Price has to move about 0.10% in your favor just to get back to zero.

With maker orders at 0.02% per side, the same trade costs $4 (0.4% of margin), so break-even is about 0.04%.

Same idea, different numbers at 20x or 50x: the fee is a fixed share of the position, so it eats a bigger share of margin as leverage goes up.

Not available in South Korea or the US. Leveraged trading can lose all your margin.
Break-even calculator and the formula: https://perpline.tech/guides/futures-break-even-price.html?utm_source=x

### 대기 3 (→ Typefully 예약 11/21) — X / 텔레그램용 (가이드: how-funding-fees-work)
Holding cost people forget: funding.

Example only: a $10,000 long with a funding rate of 0.01% per 8 hours pays about $1 each interval, $3 a day, about $30 over 10 days (if the rate stays the same; it changes, and it can flip sign so shorts pay instead).

Compare that with the $10 round-trip taker fee on the same position. For a short scalp, trading fees dominate. For a multi-day hold, funding can add up to a similar size.

Check the live funding rate on your exchange before holding overnight.

Not available in South Korea or the US. Leveraged trading can lose all your margin.
How funding works: https://perpline.tech/guides/how-funding-fees-work.html?utm_source=x
