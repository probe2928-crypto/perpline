# 아이디어 시안: Perpline '수수료 감사(Fee audit)' — 거래 내역 CSV로 실제 낸 수수료 계산

전략기획 2026-11-18 1위 아이디어의 '돈·외부 발송 없는 첫걸음'. main 아님, 공개 안 됨(noindex, 사이트 빌드에 미포함).

- 무엇: 거래소에서 내려받은 선물 거래 내역 CSV를 브라우저에서만 읽어(서버 업로드 없음) 수수료 열 합계와 '리베이트였다면 돌려받았을 금액'을 보여 줌.
- 왜: 계산기(/tools/)는 '가정' 숫자, 이건 '내 실제 숫자' → 리베이트 가입 설득력이 가장 강한 지점. 세준 강점(거래소 7년: 거래소별 내보내기 형식·수수료 열 이름을 앎).
- 근거(검색 결과 제목·URL 확인 수준, 가격·이용자 수 미확인): CoinTracking 'Trade Analysis'·'Trading Fees' 보고서(https://cointracking.freshdesk.com/en/support/solutions/articles/29000049938-trade-analysis, https://www.cointracking.info/fees.php), Crypto Tax Calculator 선물 수동 가져오기 문서(https://help.cryptotaxcalculator.io/en/articles/8574793-importing-margin-futures-and-derivatives-manually), FeeEdge(https://peerpush.com/p/feeedge). 경쟁은 세금·포트폴리오 도구 안의 부속 기능 → '수수료만, 무료, 업로드 없음'으로 차별.
- 2주 검증: main에 /tools/fee-audit.html로 올린 뒤(세준 OK) 기존 계산기 대비 pl_signup_click 비교. 통과 기준: 사용 10회 중 가입 클릭 1회 이상. 단, 지금 유입이 거의 0이라 11/21 색인 확인 뒤 시작.
- 위험: 거래소마다 CSV 열 이름이 다름(Bitget·BloFin·OKX 샘플 내보내기 확인 필요 — 세준 계정 내보내기 1개면 됨), 개인 거래 내역이라 '업로드 없음' 문구 필수, 투자 권유 없음.
- 확인한 것: 샘플 CSV 2종(헤더 'Fee'+'Fee Coin' / 'Trading Fee' 단위 붙은 값)으로 Playwright 테스트 — 아래 커밋 메시지 참조.
