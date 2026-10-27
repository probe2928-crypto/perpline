# Perpline 유료 광고 키트

## 채널: Bitmedia (메인)
- 국가 화이트·블랙리스트 가능 → **한국(KR)·미국(US) 반드시 제외**
- CPC 최저 입찰 $0.25, CPM 최저 $0.30
- 최소 충전 $300 (BTC 포함 모든 결제수단. FAQ의 BTC 예외 문구는 실제 앱과 다름)
- 애드그룹 일 한도 최소 $50 → 지출 상한은 캠페인 잔액으로 조절 ($50씩 충전)
- 소재 승인 전에는 캠페인을 켤 수 없음 (승인 후 소재 → 애드그룹 → 캠페인 순서로 켜기)

## 현재 집행 (2026-10-27)
- 캠페인 "Perpline Rebate Global" / 애드그룹 "Display CPC - EN crypto"
- CPC $0.25 수동, 영어, VPN·데이터센터 제외, 균등 소진
- 제외 국가: KR, KP, US, CA, UK, SG, HK, JP, CN, IR, CU, SY, RU
- 소재: Ivory 10사이즈, 캠페인 잔액 $50 (메인 잔액 $250 남음)
- 배너: 이미지 200KB 이하, GIF 400KB 이하. 텍스트 광고도 가능

## 채널: AADS (보조, 선택)
- 국가 타기팅이 없고 언어·카테고리만 가능 → 미국 노출을 막을 수 없음. 쓴다면 소액 테스트만

## 랜딩
https://probe2928-crypto.github.io/perpline/start.html?utm_source=bitmedia&utm_medium=banner&utm_campaign=rebate

## 배너 (banners/)
3가지 톤(ivory · klein · noir) × 10개 사이즈 + 애니메이션 GIF 3종(300x250, 728x90, 160x600)

## 텍스트 광고 문구
- Your trading fees, returned. Get up to 50% of your futures fees back in USDT, every Monday.
- 11 futures exchanges ranked by fee. Sign up through Perpline and get 30–50% back weekly.
- Trade futures? Get part of every fee back. Paid in USDT. No password, no API keys.

## 전환 측정 (2026-10-27)
- Bitmedia 전환 "Exchange sign-up click" (Custom, event id `signupclick`, conversionID `6ae072e08c8ba13fe33ec70b`)
- 영어 공개 페이지 전체(start.html·index·거래소 가이드·404)에 Bitmedia 스크립트가 들어가고, 거래소 가입 링크(rel="sponsored")를 누르면 전환 1건으로 잡힘
- 세준 전용 한국어 페이지(ko/)에는 넣지 않음 → 본인 클릭은 전환에 안 잡힘
- 설정 위치: src/build.py CONFIG의 bm_conversion_id (비우면 꺼짐)
- 확인: Bitmedia → Conversions 의 Count, Reports에서 사이트별 전환당 비용
