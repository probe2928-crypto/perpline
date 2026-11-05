# AlphaX 유료 광고 테스트 — 인수인계 (2026-11-05)

세준 결정 (11/5 12:58): AlphaX 유료 홍보 진행, 첫 테스트 예산 150달러. 유저에게 따로 페이백은 안 함 (거래소 이벤트 혜택이 큼).
수익 구조: 수수료는 0%지만 AlphaX가 추천 유저 거래량에 따라 세준에게 지급.

## 링크 (모두 확인 완료)
- 가입 링크: https://www.alphax.com/partner/7lxP6X → 로그아웃 상태에서 가입 화면 + 코드 7lxP6X 자동 입력
- 예전 링크 https://www.alphax.com/user/invite/7lxP6X 도 가입 양식 + 코드 자동 입력 (SNS 게시물은 그대로 둬도 됨)
- 채널별 추적 링크: https://perpline.tech/go/ax-{tg1,tg2,tg3,tg4,x1,x2,bm,meta,cb}.html
  → GA4(G-8YQ1BGBDR7) 이벤트 `pl_signup_alphax` (source=채널) 기록 후 바로 가입 화면으로 이동

## 채널 계획
1. 텔레그램 채널 유료 게시물 — Telega.io (에스크로, 미게시 시 환불). **150달러 전부 여기**
   - 세준이 telega.io 가입 + USDT/TON으로 150달러 충전 → 알려주면 진행
   - 채널 2~3곳 고르기: 영어권 선물·트레이딩, 조회수 대비 반응률(ERR) 비정상(60%↑)인 채널 제외, 인도·케냐 '펌프/시그널' 채널 주의
   - 채널명·구독자·가격·합계 먼저 세준에게 보여주고 OK 받은 뒤 주문 (결제·주문은 승인 필수)
2. Bitmedia — 최소 충전 300달러라 1차 제외, 결과 좋으면 2차
3. X 인플루언서 유료 포스팅 — USDT 직접 송금(에스크로 없음), 2차
4. 메타 — 예산 변경 없음. 체인브리프 텔레그램 채널 구독자만 늘리고 AlphaX는 채널 게시물에서 소개.
   메타·구글·X 광고에 AlphaX 링크 직접 걸지 않기 (계정 제재 위험)

## 광고 문구 원칙
- 0% maker · 0% taker 강조, 이벤트 조건 디테일은 넣지 않기, 코드 7lxP6X
- "Not available in South Korea or the US. Leveraged trading can lose all your margin." 반드시 포함
- 한국 채널·한국어 페이지(ko/)에는 AlphaX 노출 금지 (ko/에서 제거 완료)

## 측정
- 1주 후 AlphaX 어필리에이트 포털(가입자·거래량·지급액) vs 광고비 비교 → 남으면 증액, 아니면 중단
- GA4에서 `pl_signup_alphax` source별 클릭 수
- 참고: Savri는 요금제상 probe2928-crypto.github.io만 집계 (perpline.tech·chainbrief.app 방문은 Savri에 안 잡힘 → GA4 사용).
  chainbrief.app도 같은 문제, 별도 조치 필요.

## 사이트 반영 내역 (11/5)
- 홈 띠배너·흐르는 목록·큰 0% 배너·거래소 목록 Pick·AlphaX 페이지·특집 페이지 → 전부 가입 링크로 직접 연결
- 가입 클릭 집계 버그 수정 (live 체크가 github.io만 허용하던 것 → perpline.tech 포함), AlphaX 클릭은 'alphax'로 분류

## Telega.io 후보 (11/5 13:30 조사, 세준 충전·승인 대기)
| 채널 | 구독자 | 실제 평균 조회 | 1/24 가격 | 판단 |
|---|---|---|---|---|
| Crypto Asset Report (@CryptoAssetReport) | 111K | 22.5K | $120 | 추천. 속보 뉴스, 광고 월 2회뿐, 4년 5개월 채널, 구독자 월 -2.8K 감소 중 |
| ✪ Crypto Scalp Signals (@crypto_scalp_signals) | 29K | 4.2K | $24 | 추천. BTC·ETH 단타 분석 = 선물 유저, 남성 90%, Telega 주문 1,764건·재주문 549건 |
| Crypto News (@CryptosNews_Pro) | 23.6K | 3.0K | $10.10 | 저가 보조. 광고 월 41회로 많고 성인 광고도 섞임 |
| 제외 | | | | Crypto News Update™·Crypto Breaking News™·CryptoNews_proo(조회/구독 70~80%, 광고글만 조회 1/5 → 봇 의심), Blockipedia(구독자 한 달 +9.9K 구매 의심), 에어드롭 채널들(선물 유저 아님) |
- 추천안: Crypto Asset Report + Crypto Scalp Signals = $144 (예상 조회 약 2.7만, CPM 약 $5.4) → 추적 링크 ax-tg1(CAR), ax-tg2(Scalp)
- 대안(분산): Scalp $24 + Crypto News $10.10 + (2차용 잔액 보관)
