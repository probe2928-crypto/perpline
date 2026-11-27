# 스토리보드 — Perpline "Break-even, after fees." (9:16, 1080×1920, 16.0초)

> 최종 렌더(15.0초)는 v3에서 렌더 심사 r1–r3을 거쳐 바뀌었다(중반 = 가이드 시트 한 장, 오퍼 블록 1.8초, CTA "Get 40% of your futures fees back →"). 변경 내역은 MEETING.md.

- 상품/기능: Perpline 가이드 「Your futures break-even price, after fees.」(`/guides/futures-break-even-price.html`). 지난 Perpline 편: 11/10 = 수수료 페이백, 11/20 = 수수료 계산기. 이번 = **손익분기점(진입가가 아니라 수수료만큼 위)**.
- 숫자(전부 가이드 본문 그대로): BTC 롱 $10,000, 예시 진입가 $70,000.00(가이드 "illustrative"), Bitget 표준 0.02%/0.06%(11/3 확인), 시장가 진입·청산 손익분기 **$70,084.05 · 0.12%**, 왕복 수수료 약 **$12**, 40% 리베이트 반영 후 **0.072%**(= $70,050.42, 계산 확인). 리베이트는 매주 월요일 USDT로 지급되는 '실효' 값 — 화면 표기는 "effective, after 40% rebate".
- 화면 소재(실물): 가이드 페이지를 로컬에서 Playwright로 찍은 실제 화면(로고 이미지·채팅 버튼·BTC 시세 숨김) — 상단 히어로, 주문 습관 표. 차트는 사이트 색·서체로 코드 렌더.
- 톤: 사이트 그대로 종이 #FBF4EC · 잉크 #111 · 클라인 블루 #1F2FA0 · 다운 레드 #9B2335 · 업 그린 #1E6B47, DM Serif Display + Jost + Plex Mono.

## v3 (CD r2 7.5 → 2.5–3.5초엔 선만 움직임 · 0프레임 선 간격 ≥280px, 가격 태그 최대 · 중반 설명 반복 삭제 · 엔드 9.5초 시작 · CTA를 오퍼와 맞춤) — 16.0초, 제작 기준

| 시간 | 화면 | 카피(영어) | 모션 | 사운드 |
|---|---|---|---|---|
| 0.0 | 종이 풀블리드 차트. y축 과장(진입선 y≈1330, 손익분기선 y≈1000, 간격 330px). 회색 점선 `ENTRY 70,000.00`, 블루 실선 `BREAK-EVEN 70,084.05`, 사이 옅은 레드 해치 띠, 띠 안 레드 가격 점 + **가장 큰** 가격 태그 `70,060.00`(Jost 600 56px). 위 모노 `PERPLINE · FUTURES FEES` + 헤드 DM Serif 104px "Above your entry." / "*Still in the red.*" | 위 | 가격 틱만 | 앰비언스 + 틱 |
| 1.4–1.8 | 띠 안 라벨: `FEES IN + OUT ≈ $12 · $10,000 BTC LONG` | — | 마스크 0.4 | 쉬머 |
| 1.9–2.3 | 토글 칩 `PERPLINE REBATE 40% · BITGET` 등장, 2.3 ON | — | expo.out | 클릭 |
| 2.5–3.5 | **결정적 순간(이것만 움직임)**: 블루 선 70,084.05 → 70,050.42, 띠 축소, ≈3.1 점 레드→그린, 라벨 `0.12%` → `0.072%` | 헤드 그대로 | power2.inOut 1.0 | 상승 톤 + 딩 |
| 3.5–5.0 | 헤드 교체(마스크): "Same trade." / "*Closer to zero.*"(블루 이탤릭). 선 라벨 아래 "effective · rebate paid weekly in USDT" | 위 | 0.45 | 휘시 소 |
| 5.0–5.7 | 매치 컷: 차트 `0.072%` → 가이드 페이지 실제 `0.072%` | — | 0.35+0.35 | 휘시 |
| 5.7–7.5 | 페이지 풀블리드 풀아웃 → 헤드 "Your futures break-even price, *after fees.*" | 모노 `PERPLINE · FREE GUIDE` | 1.0 + 홀드 | 패드 |
| 7.5–9.0 | 스크롤 → worked example, "$70,084.05, a move of $84.05" 블루 마커 1회 | — | 0.6 + 0.4 | 틱 |
| 9.0–9.5 | 페이지 위로 마스크 퇴장 | — | power3.in | 휘시 |
| 9.5–16.0 | **엔드**: `PERPLINE` → 블루 "0.072%"(260px) → "vs 0.12% standard" → "Bitget market-in, market-out break-even move, after the 40% rebate" → 블랙 CTA "See your break-even after fees →" + `perpline.tech` → Jost 30 "40% rebate when you sign up to Bitget via Perpline" → 고지 24px(v2와 같음) | 위 | 스태거 0.06, 11.0 이후 정지 홀드 5초 | 엔드 화음 |

## v2 (CD r1 6.0 → 0프레임에 역설 완성 · 결정적 순간 3초로 · 표 삭제 · 폰 베젤 대신 종이→종이 매치 컷 · 엔드 단순화) — 17.5초, 제작 기준

| 시간 | 화면 | 카피(영어) | 모션 | 사운드 |
|---|---|---|---|---|
| 0.0 | 종이 풀블리드 차트, **역설이 0프레임에 완성**: 회색 점선 `ENTRY 70,000.00`, 그 위 클라인 블루 실선 `BREAK-EVEN 70,084.05`, 둘 사이 옅은 레드 해치 띠, 띠 **안**의 레드 가격 점 + 태그 `70,060.00`. 위 모노 `PERPLINE · FUTURES` + 헤드 DM Serif 104px 2줄 "Above your entry." / "*Still in the red.*"(다운 레드 이탤릭) | 위 | 가격 틱만(점이 띠 안에서 ±4 흔들림) | 시장 앰비언스 + 틱 |
| 0.5–1.5 | 같음, 카메라 1.0→1.03 | — | — | — |
| 1.5–2.0 | 띠 안 라벨 상승(모노 26): `FEES IN + OUT ≈ $12 · $10,000 BTC LONG` | — | 마스크 0.4 | 쉬머 |
| 2.0–2.5 | 오른쪽 위 토글 칩 `PERPLINE REBATE 40% · BITGET` 등장, 2.3에 토글 ON(사이트 토글 그대로) | — | expo.out 0.35 | UI 클릭 |
| 2.5–3.5 | **결정적 순간**: 블루 선 70,084.05 → 70,050.42로 내려옴, 띠가 줄어듦, 선이 가격 점 아래로 지나는 순간(≈3.1) 점 레드→그린, 선 라벨 `0.12%` → `0.072%` (값 2개만) | 헤드 교체(마스크): "Same trade." / "*Closer to zero.*"(블루 이탤릭) | power2.inOut 1.0 | 상승 톤 + 그린 '딩' |
| 3.5–5.0 | 홀드. 선 라벨 아래 작은 줄(Jost 30): "effective break-even · rebate paid weekly in USDT" | — | 정지 | — |
| 5.0–5.7 | **매치 컷**: 선 라벨 `0.072%`를 향해 줌 → 같은 크기·위치의 가이드 페이지 실제 `0.072%`(블루 DM Serif)로 이어짐(종이→종이) | — | power3.in 0.35 + expo.out 0.35 | 휘시 |
| 5.7–8.0 | 실제 가이드 페이지 풀블리드(베젤 없음, 캡처 1.0배)로 풀아웃: `BITGET · 40% REBATE 0.072%` 블록 → 위로 헤드 "Your futures break-even price, *after fees.*" 까지 보임 | 위 라벨(모노): `PERPLINE · FREE GUIDE` | 풀아웃 1.0 → 홀드 1.3 | 패드 화성 |
| 8.0–10.3 | 페이지 스크롤 → "A worked example in dollars" 본문, "$70,084.05, a move of $84.05"와 "around $12.00 in total"에 블루 마커 스윕 순서대로 | 아래 캡션: "The formula, in dollars." | 스크롤 0.7 · 마커 0.4씩 | 틱 2회 |
| 10.3–12.6 | 카피(종이, 페이지 퇴장 마스크): "Your zero" / "isn't your *entry*." (130px, 단어 마스크) | 위 | 스태거 0.09 | 휘시 |
| 12.6–17.5 | **엔드**: `PERPLINE` 워드마크(Jost 500, 자간 .4em) → 블루 DM Serif 260px "0.072%" → "vs 0.12% standard" → 설명(Jost 32) "Bitget market-in, market-out break-even move, after the 40% rebate" → 블랙 CTA "Read the free break-even guide →" + `perpline.tech` → 고지 24px "Illustrative $10,000 BTC long at $70,000. Bitget standard 0.02% / 0.06%, checked 3 Nov 2026. Rebate paid by Perpline weekly in USDT. Not financial advice. Not for KR / US residents." | 위 | 스태거 0.06, 14.0 이후 정지 홀드 3.5초 | 엔드 화음 |

캡처: 헤더 BTC 시세·채팅 버튼·이미지 숨김.

## v1 (CD r1 6.0, 참고용)

| 시간 | 화면 | 카피(영어) | 모션 | 사운드 |
|---|---|---|---|---|
| 0.0 | 종이 바탕 풀블리드 차트. 잉크 가격선이 왼쪽에서 오른쪽 끝(x≈860)까지 이미 그려져 있고 끝 점이 맥동 없이 빛남, 오른쪽 가격 태그 `70,060.00`. 점선 `ENTRY 70,000.00`(회색) 아래. 위(260–560px) 헤드라인 DM Serif 104px "Above your entry." 이미 떠 있음 | "Above your entry." | 가격선 끝이 미세하게 계속 진행(틱) | 낮은 시장 앰비언스 + 틱 |
| 0.5 | 같음, 카메라 아주 느린 푸시 1.0→1.04 | — | — | — |
| 0.8–1.2 | 2줄째 이탤릭 다운 레드 마스크 상승 | "*Still in the red.*" | expo.out 0.4 | 낮은 '틱-툭' |
| 1.5–2.0 | 위에서 클라인 블루 실선이 내려와 70,084.05에 착지(오버슈트 없음). 라벨 `BREAK-EVEN 70,084.05` | — | power4.out 0.5 | 착지음 |
| 2.0–2.5 | 진입선~손익분기선 사이 띠가 옅은 레드 해치로 채워짐, 띠 안 라벨(모노 26) `FEES · OPEN + CLOSE ≈ $12` | — | 좌→우 와이프 0.5 | 쉬머 |
| 2.5–3.5 | 헤드라인 교체(마스크): "Your zero isn't your entry." (88px), 아래 작은 줄(Jost 34) "$10,000 BTC long · market in, market out" | 위 | 퇴장 0.25 / 입장 0.45 | 휘시 |
| 3.5–4.2 | 띠가 잡힌 채 카메라 풀아웃 → 차트가 작아지며 폰(높이 1300) 화면 속으로 → 폰 화면 = 실제 가이드 히어로 "Your futures break-even price, *after fees.*" | 캡션 위: "Perpline · free guide" | 0.7 power2.inOut 이어받기 | 휘시 저음 |
| 4.2–5.5 | 히어로 홀드(1.3초) → 0.072% 블록이 보임 | — | 정지 | 틱 |
| 5.5–6.2 | 폰 화면 스크롤 → 표 "How order type changes your break-even" | 캡션 01: "Your order habit moves it." | 스크롤 0.7 | 스크롤 휘시 |
| 6.2–8.2 | 카메라가 폰 안으로 푸시 1.5배(베젤 보임), 표 3행 순서대로 블루 테: Market/market 0.12% → Limit/market 0.08% → Limit/limit 0.04% (각 0.5초) | — | 테 0.3씩 | 틱 3회 |
| 8.2–8.9 | 첫 행 '0.072%' 칸에 블루 테 → 그 숫자 쪽으로 줌스루, 종이로 디졸브 | 캡션 02: "A rebate moves it too." | power3.in 0.7 | — |
| 8.9–9.4 | 다시 풀블리드 차트(0초와 같은 구도), 손익분기선 0.12% 위치, 가격 점 아래(레드 띠 안) | — | 컷 | — |
| 9.4–10.0 | 오른쪽 위 토글 칩 `40% REBATE · BITGET` 이 켜짐(사이트 토글 모양) | — | 0.3 | UI 클릭 |
| 10.0–11.0 | **결정적 순간**: 블루 손익분기선이 70,084.05 → 70,050.42로 천천히 내려옴, 레드 띠가 따라 줄어듦. 선이 가격 점 아래로 지나가는 순간 가격 점이 레드→그린, 띠 라벨 `0.12%` → `0.072%` (값 2개만, 중간값 없음) | 위 라벨: "effective break-even, 40% rebate counted in" | power2.inOut 1.0 | 낮은 상승 톤 + 그린 '딩' 1회 |
| 11.0–12.0 | 홀드(1.0초) | — | 정지 | — |
| 12.0–13.8 | 차트 퇴장(종이 남음) → 카피 2박자, 단어 마스크 | "Same trade." / "*Closer to zero.*"(블루 이탤릭, 150px) | 0.08 스태거 | 휘시 |
| 13.8–17.5 | **엔드**(종이): 위 `PERPLINE` 워드마크(Jost 500 자간 .4em, 120px 폭 꽉) → 헤드 "Know your real break-even." (DM Serif 84) → 가운데 폰(0.6배, 가이드 히어로·0.072% 보임) 지시선 `0.072% · BITGET MARKET-IN/OUT, AFTER 40%` → 블랙 CTA "Read the free guide →" + `perpline.tech` → 고지 24px 3줄 "Illustrative $10,000 BTC long at $70,000. Bitget standard 0.02% / 0.06%, checked 3 Nov 2026. Rebate paid by Perpline weekly in USDT. Not financial advice. Not for KR / US residents." | 위 | 스태거 0.06, 15.3 이후 정지 홀드 2.2초 | 엔드 화음 1회 |

체크: 0프레임 = 상황(가격>진입)+훅 / 3초 안에 '수수료가 손익분기를 올린다' / 6초 안에 Perpline 가이드 / 결정적 순간 = 리베이트가 선을 내림 / 무음 이해 / 가격 숫자는 예시 진입가·손익분기만, 수익 보장 없음.
