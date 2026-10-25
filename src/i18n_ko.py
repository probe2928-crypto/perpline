"""Korean translation layer for Perpline (owner-only view under /ko/, noindex).
The English HTML is generated first, then every visible text node and a few
attributes are translated with the tables below. Anything not in the tables
stays in English, so new text never breaks the build.

When the market note changes, add its new sentences to NOTE below.
"""
import re, html as _h

EXACT = {
    "Perpline — Crypto Futures Referral Codes & Up to 50% Fee Rebate": "Perpline — 코인 선물 레퍼럴 코드 & 최대 50% 수수료 페이백",
    # hero carousel + marquees
    "Perpline highlights": "Perpline 하이라이트", "La remise": "페이백", "La sélection": "셀렉션", "Le marché": "시황",
    "of your futures fees,": "선물 거래 수수료를,", "back every Monday.": "매주 월요일 돌려드려요.",
    "Eleven exchanges,": "11개 거래소,", "ranked by what they cost.": "수수료 순으로 정렬.",
    "From BTCC at 0.045% to the 0.022% you pay after our rebate.": "BTCC 0.045%부터, 페이백 후 실제 부담 0.022%까지.",
    "See the ranking": "순위 보기", "Bitcoin, read": "비트코인,", "three times a week.": "주 3회 읽어드려요.",
    "· desk notes every Monday, Wednesday and Friday.": "· 매주 월·수·금 시황 노트.", "Read the note": "시황 노트 보기",
    "Choose slide": "슬라이드 선택", "Previous slide": "이전 슬라이드", "Next slide": "다음 슬라이드", "Pause slideshow": "슬라이드 멈춤",
    "Slide 1": "슬라이드 1", "Slide 2": "슬라이드 2", "Slide 3": "슬라이드 3", "Slide 4": "슬라이드 4",
    "Exchanges and rebates": "거래소와 페이백",
    "Paid every Monday": "매주 월요일 지급", "In USDT": "USDT로 지급", "No password": "비밀번호 불필요", "No API keys": "API 키 불필요",
    "Up to 50% back": "최대 50% 페이백", "Eleven exchanges": "11개 거래소", "Ranked by fee": "수수료 순 정렬",
    # header / nav / footer
    "Exchanges": "거래소", "Rebate": "페이백", "Market": "시황", "Community": "커뮤니티",
    "Sections": "섹션", "Support": "고객지원", "How can we help?": "무엇을 도와드릴까요?",
    "Chat on Telegram": "텔레그램으로 문의", "Claim a rebate or ask about sign-up": "페이백 신청 또는 가입 문의",
    "Join the community": "커뮤니티 참여", "Market notes and new listings": "시황 노트와 신규 상장 소식",
    "Send a support request": "문의 남기기", "We reply on Telegram": "텔레그램으로 답변드려요",
    "Fee-first guides to crypto perpetual futures venues, with up to 50% of your trading fees returned.":
        "수수료 기준으로 고른 코인 무기한 선물거래소 가이드. 거래 수수료의 최대 50%를 돌려드려요.",
    "Support:": "고객지원:", "on Telegram · Community:": "(텔레그램) · 커뮤니티:", "on Telegram": "(텔레그램)", "Perpline Community": "Perpline 커뮤니티",
    "Exchange guides": "거래소 가이드",
    "Restricted jurisdictions": "이용 제한 지역",
    "Not directed at residents of the Republic of Korea, the United States, or any jurisdiction where the listed exchanges are not licensed or registered to serve local users. If you live in one of these places, do not use the links on this site.":
        "대한민국, 미국 및 소개된 거래소가 현지 이용자 대상 인가·등록을 받지 않은 지역의 거주자를 대상으로 하지 않습니다. 해당 지역에 거주한다면 이 사이트의 링크를 이용하지 마세요.",
    "Risk & disclosure": "위험 고지 및 공시",
    "Leveraged derivatives carry a high risk of losing all of your margin. Nothing here is financial advice. Links are referral links; we earn a commission and share part of it with you as a fee rebate. Rebates are paid by Perpline, not by the exchanges. © 2026 Perpline.":
        "레버리지 파생상품은 증거금 전액을 잃을 위험이 큽니다. 이 사이트의 어떤 내용도 투자 조언이 아닙니다. 링크는 레퍼럴 링크이며, 저희가 받는 커미션의 일부를 수수료 페이백으로 돌려드립니다. 페이백은 거래소가 아니라 Perpline이 지급합니다. © 2026 Perpline.",

    # hero
    "Édition No. 01 · Octobre 2026": "에디션 No. 01 · 2026년 10월",
    "Your trading fees,": "당신의 거래 수수료,", "returned.": "돌려드립니다.",
    "Sign up to a futures exchange through Perpline and we send 30–50% of the fees you pay back to you, in USDT, every week.":
        "Perpline을 통해 선물거래소에 가입하면, 낸 수수료의 30–50%를 매주 USDT로 돌려드려요.",
    "Choose an exchange": "거래소 고르기", "How the rebate works": "페이백 방식 보기",
    "Venues": "거래소 수", "Top rebate": "최대 페이백", "Lowest taker after rebate": "페이백 후 최저 테이커",

    # list
    "I · La sélection": "I · 셀렉션", "The exchanges": "거래소 목록",
    'Ranked by headline taker fee, the rate most market orders pay. "You pay" is the taker fee after your Perpline rebate. Open a name for the full guide and referral code.':
        '시장가 주문 대부분이 내는 테이커 수수료 순으로 정렬했어요. "실제 부담"은 Perpline 페이백을 받은 뒤의 테이커 수수료예요. 이름을 누르면 상세 가이드와 레퍼럴 코드가 나와요.',
    "Venue type": "거래소 유형", "Perp DEX": "무기한 DEX",
    "Centralized exchanges. You register with email, verify identity where required, and the exchange holds your funds.":
        "중앙화 거래소(CEX). 이메일로 가입하고 필요하면 신원 인증을 하며, 자금은 거래소가 보관해요.",
    "Exchange": "거래소", "Maker": "메이커", "Taker": "테이커", "You pay": "실제 부담",
    "Lowest headline taker": "테이커 수수료 최저", "Sign up": "가입하기", "Check site": "사이트 확인",
    "On-chain perpetual exchanges. You trade from your own wallet and keep custody of your funds.":
        "온체인 무기한 선물거래소. 내 지갑으로 거래하고 자금도 직접 보관해요.",
    "Bientôt": "곧 오픈", "Perp DEX listings are on the way": "무기한 DEX 목록을 준비 중이에요",
    "On-chain perpetual exchanges with the same fee-first ranking and rebate. Join the community to hear when they go live.":
        "같은 수수료 기준 순위와 페이백으로 온체인 거래소도 곧 추가돼요. 오픈 소식은 커뮤니티에서 먼저 알려드려요.",
    'Standard (non-VIP) USDT-margined perpetual fees as listed by each exchange or TradersUnion, checked Oct 2026. Your live account rate applies. "Check site" means we could not verify the current rate.':
        '각 거래소 또는 TradersUnion에 게시된 일반(비 VIP) USDT 무기한 선물 수수료이며, 2026년 10월에 확인했어요. 실제로는 계정에 적용된 요율이 우선해요. "사이트 확인"은 현재 요율을 검증하지 못했다는 뜻이에요.',

    # rebate
    "II · La remise": "II · 페이백",
    "Exchanges pay us a commission on the fees our referred traders pay. We pass 30–50% of your fees back to you. We never ask for your password, API keys or funds.":
        "거래소는 저희가 소개한 트레이더가 낸 수수료에서 커미션을 지급해요. 저희는 그중 당신이 낸 수수료의 30–50%를 돌려드려요. 비밀번호, API 키, 자금은 절대 요구하지 않아요.",
    "Sign up through our link": "저희 링크로 가입",
    "Register a new account using the Sign up button or referral code on this site. The rebate only works for accounts created through our link.":
        "이 사이트의 가입 버튼이나 레퍼럴 코드로 새 계정을 만드세요. 페이백은 저희 링크로 만든 계정에만 적용돼요.",
    "Send us your UID": "UID 보내기",
    "Send the exchange name and your account UID to": "거래소 이름과 계정 UID를",
    "on Telegram. We confirm the link within 24 hours.": "에게 텔레그램으로 보내주세요. 24시간 안에 연결을 확인해 드려요.",
    "Get paid every Monday": "매주 월요일 지급",
    "Trade as usual. Every Monday we send your rebate for the previous week in USDT to your exchange UID or wallet.":
        "평소처럼 거래하면 돼요. 매주 월요일, 지난주 페이백을 USDT로 거래소 UID나 지갑에 보내드려요.",
    "Rebate rate": "페이백 비율", "30–50% of trading fees, by exchange": "거래소별 거래 수수료의 30–50%",
    "Paid in": "지급 통화", "Schedule": "지급 주기", "Weekly, every Monday (UTC)": "매주 월요일 (UTC)",
    "Minimum payout": "최소 지급액", "10 USDT; smaller amounts roll over": "10 USDT, 미만은 다음 주로 이월",
    "Covers": "적용 대상", "Futures trading fees on accounts linked to us": "저희와 연결된 계정의 선물 거래 수수료",
    "Not covered": "제외 대상", "Wash trading, self-referral, fee-free promotions": "자전거래, 셀프 레퍼럴, 수수료 무료 이벤트",
    "Rebates are calculated from the commission reports each exchange gives us and are paid by Perpline, not by the exchange. Rates can change with 7 days' notice in our Telegram community.":
        "페이백은 각 거래소가 제공하는 커미션 리포트로 계산하며, 거래소가 아니라 Perpline이 지급해요. 비율은 텔레그램 커뮤니티에 7일 전 공지 후 바뀔 수 있어요.",

    # calculator
    "III · Le calcul": "III · 계산기", "What a month of trading costs": "한 달 거래 비용",
    "Opening and closing a position each pay a fee on the full position size, leverage included. Compare venues before and after your rebate.":
        "포지션을 열 때와 닫을 때 각각, 레버리지를 포함한 전체 포지션 크기에 수수료가 붙어요. 페이백 전후로 거래소를 비교해 보세요.",
    "Position size, USDT": "포지션 크기 (USDT)", "Margin × leverage. 1,000 at 10× is 10,000.": "증거금 × 레버리지. 1,000을 10배로 잡으면 10,000.",
    "Order type": "주문 유형", "Market order": "시장가", "Limit order": "지정가",
    "Round trips per month": "월 왕복 거래 횟수", "Include Perpline rebate": "Perpline 페이백 포함",

    # market chrome
    "BTC / USD ·": "BTC / USD ·", "24h low": "24시간 최저", "24h high": "24시간 최고", "Updated": "업데이트",
    "Key price levels": "주요 가격대", "Levels in play": "주요 가격대",
    "Price ladder showing support and resistance levels": "지지·저항 가격대",
    "Key numbers": "핵심 수치",
    "If it reclaims": "회복하면", "If it chops": "횡보하면", "If it loses": "이탈하면",
    "low conviction": "확신 없는 흐름", "long liquidations": "롱 청산",

    # community / form
    "V · La communauté": "V · 커뮤니티", "Community & support": "커뮤니티 & 고객지원",
    "Market notes and new listings go to the community first. For rebates and sign-up help, message us directly or send a request.":
        "시황 노트와 신규 상장 소식은 커뮤니티에 먼저 올라가요. 페이백이나 가입 문의는 직접 메시지를 보내거나 문의를 남겨주세요.",
    "Desk notes three times a week, new exchange listings, rebate updates and trader discussion.":
        "주 3회 시황 노트, 신규 거래소 소식, 페이백 공지, 트레이더 토론.",
    "Direct support": "1:1 고객지원",
    "Send your UID to claim a rebate, or ask anything about a listed exchange.": "UID를 보내 페이백을 신청하거나, 거래소에 대해 무엇이든 물어보세요.",
    "Message on Telegram": "텔레그램으로 메시지", "Support request": "문의하기",
    "Your Telegram username": "텔레그램 아이디", "Topic": "주제",
    "Claim my rebate": "페이백 신청", "Sign-up help": "가입 도움", "Referral not applied": "레퍼럴 미적용",
    "Question about an exchange": "거래소 관련 질문", "Partnership / listing": "제휴 / 상장 문의", "Other": "기타",
    "Message": "메시지", "Exchange, your UID, and what you need.": "거래소, UID, 필요한 내용을 적어주세요.",
    "Send request": "문의 보내기",

    # FAQ (home)
    "VI · Questions": "VI · 자주 묻는 질문", "Before you trade": "거래 전에",
    "How much rebate will I get?": "페이백은 얼마나 받나요?",
    "Between 30% and 50% of the futures trading fees you pay, depending on the exchange. Each exchange's rate is shown in the list and on its guide page.":
        "거래소에 따라 낸 선물 거래 수수료의 30%~50%예요. 거래소별 비율은 목록과 각 가이드 페이지에 나와 있어요.",
    "Do you need my password or API key?": "비밀번호나 API 키가 필요한가요?",
    "No. We only need the exchange name and your account UID to match your trades to our commission report. Never share your password, 2FA codes or API keys with anyone.":
        "아니요. 거래 내역을 커미션 리포트와 맞추는 데 거래소 이름과 계정 UID만 있으면 돼요. 비밀번호, 2FA 코드, API 키는 누구에게도 알려주지 마세요.",
    "I already have an account. Can I still get the rebate?": "이미 계정이 있어요. 그래도 페이백을 받을 수 있나요?",
    "Usually not. Exchanges link a referral only when the account is created. You would need to open a new account through our link.":
        "보통은 안 돼요. 거래소는 계정을 만들 때만 레퍼럴을 연결해요. 저희 링크로 새 계정을 만들어야 해요.",
    "What is a perpetual future?": "무기한 선물이 뭔가요?",
    "A contract that tracks an asset's price with no expiry date. You post margin and can go long or short with leverage. A funding payment between longs and shorts, usually every 8 hours, keeps the price close to spot.":
        "만기 없이 자산 가격을 따라가는 계약이에요. 증거금을 넣고 레버리지로 롱이나 숏을 잡을 수 있어요. 보통 8시간마다 롱과 숏 사이에 오가는 펀딩비가 가격을 현물 근처로 유지해요.",
    "How does liquidation work?": "청산은 어떻게 되나요?",
    "If losses eat your margin down to the maintenance level, the exchange closes your position. At 10× leverage, a move of roughly 9–10% against you can wipe out isolated margin.":
        "손실로 증거금이 유지 증거금 수준까지 줄면 거래소가 포지션을 강제로 닫아요. 10배 레버리지라면 반대 방향으로 9–10% 정도만 움직여도 격리 증거금이 사라질 수 있어요.",
    "CEX or perp DEX?": "CEX와 무기한 DEX, 뭘 써야 하나요?",
    "A centralized exchange is easier to start with and usually has deeper liquidity, but it holds your funds. A perp DEX lets you trade from your own wallet, so you keep custody, but you manage your own keys and pay network fees.":
        "중앙화 거래소는 시작하기 쉽고 보통 유동성이 더 깊지만, 자금을 거래소가 보관해요. 무기한 DEX는 내 지갑으로 거래해서 자금을 직접 보관하지만, 키 관리와 네트워크 수수료는 직접 감당해야 해요.",
    "Can I use these exchanges where I live?": "제가 사는 곳에서도 이용할 수 있나요?",
    "Maybe not. Each exchange decides who it serves. Check the exchange's terms for your country before registering. This site is not for residents of the jurisdictions listed below.":
        "안 될 수도 있어요. 서비스 대상 국가는 각 거래소가 정해요. 가입 전에 거래소 약관에서 거주 국가를 확인하세요. 이 사이트는 아래 제한 지역 거주자를 대상으로 하지 않아요.",

    # exchange pages: shared
    "Breadcrumb": "경로", "Referral code &": "레퍼럴 코드 &", "Claim the rebate": "페이백 신청",
    "Referral code": "레퍼럴 코드", "Copy": "복사", "Fee rebate": "페이백", "Maker / taker": "메이커 / 테이커",
    "Taker you pay": "실제 테이커", "Paid weekly in": "매주 지급",
    "Applied automatically": "자동 적용", "Use our sign-up link and the referral is attached for you.": "저희 가입 링크를 쓰면 레퍼럴이 자동으로 붙어요.",
    "I · L'essentiel": "I · 핵심", "II · Le calcul": "II · 계산", "III · L'inscription": "III · 가입", "IV · La remise": "IV · 페이백",
    "V · Questions": "V · 질문", "VI · Ailleurs": "VI · 다른 거래소",
    "Position size": "포지션 크기", "Net cost per month": "월 순비용",
    "Example at the standard taker rate. Funding payments not included.": "일반 테이커 요율 기준 예시예요. 펀딩비는 포함하지 않았어요.",
    "How to sign up": "가입 방법",
    "Use the Sign up button on this page so the referral is attached to your new account.": "이 페이지의 가입 버튼을 써야 새 계정에 레퍼럴이 연결돼요.",
    "Register": "회원가입", "Create the account with your email or phone and set a strong password and 2FA.": "이메일이나 휴대폰으로 계정을 만들고, 강한 비밀번호와 2FA를 설정하세요.",
    "Verify if asked": "요청 시 인증",
    "Fund and open futures": "입금 후 선물 시작", "Deposit USDT, transfer it to your futures account and start with low leverage.": "USDT를 입금해 선물 계정으로 옮기고, 낮은 레버리지로 시작하세요.",
    "Find your UID": "UID 찾기", "Send it on Telegram": "텔레그램으로 보내기",
    "Your rebate for the previous week arrives in USDT. Minimum 10 USDT; smaller amounts roll over.": "지난주 페이백이 USDT로 들어와요. 최소 10 USDT, 미만은 이월돼요.",
    "Send my UID": "UID 보내기", "Do you need my password or API key?": "비밀번호나 API 키가 필요한가요?",
    "No. We only need the exchange name and your account UID. Never share your password, 2FA codes or API keys with anyone.":
        "아니요. 거래소 이름과 계정 UID만 있으면 돼요. 비밀번호, 2FA 코드, API 키는 누구에게도 알려주지 마세요.",
    "Other exchanges": "다른 거래소", "Every venue is ranked on the home page by fee, with its rebate.": "모든 거래소는 홈에서 수수료와 페이백 기준으로 비교할 수 있어요.",
    "fee rebate": "수수료 페이백",
}

# per-exchange notes (list) and about paragraphs
EXACT.update({
    "Running since 2011, one of the longest-operating crypto exchanges.": "2011년부터 운영된, 가장 오래된 거래소 중 하나.",
    "Lv.1 rate. Deep BTC liquidity and a full options venue.": "Lv.1 요율. BTC 유동성이 깊고 옵션까지 거래 가능.",
    "VIP0 rate. One of the widest altcoin futures lists.": "VIP0 요율. 알트코인 선물 종목이 가장 많은 편.",
    "Copy trading built in alongside standard perps.": "일반 무기한 선물에 카피트레이딩 내장.",
    "Standard 0.02% / 0.05% perpetual rate.": "일반 무기한 요율 0.02% / 0.05%.",
    "Fee depends on account level; BGB holders get discounts.": "계정 레벨별 수수료, BGB 보유 시 할인.",
    "Standard 0.02% / 0.06% perpetual rate.": "일반 무기한 요율 0.02% / 0.06%.",
    "Higher maker fee than most; better suited to market orders.": "메이커 수수료가 높은 편이라 시장가 위주에 적합.",
    "Lists crypto, gold and stock perpetuals.": "코인·금·주식 무기한 선물 상장.",
    "Check the fee schedule on the site.": "수수료표는 사이트에서 확인.",
    "BTCC has been operating since 2011, which makes it one of the oldest names in crypto trading. Its standard futures taker fee of 0.045% is the lowest on our list.":
        "BTCC는 2011년부터 운영돼 온, 코인 거래소 중 가장 오래된 이름 중 하나예요. 일반 선물 테이커 수수료 0.045%는 목록에서 가장 낮아요.",
    "OKX is one of the largest derivatives venues by volume, with perpetuals, dated futures and options in one account. The rate shown is its Lv.1 (entry) fee tier.":
        "OKX는 거래량 기준 최대 파생상품 거래소 중 하나로, 무기한·만기 선물·옵션을 한 계정에서 거래해요. 표시된 요율은 Lv.1(기본) 등급이에요.",
    "Gate has operated since 2013 and lists one of the widest ranges of altcoin perpetuals. The rate shown is its VIP0 (entry) tier for USDT-margined perpetuals.":
        "Gate는 2013년부터 운영됐고 알트코인 무기한 선물 종목이 가장 많은 편이에요. 표시된 요율은 USDT 무기한 VIP0(기본) 등급이에요.",
    "BingX combines standard USDT-margined perpetuals with built-in copy trading, so you can follow other traders' positions from the same account.":
        "BingX는 일반 USDT 무기한 선물에 카피트레이딩이 내장돼 있어서, 같은 계정에서 다른 트레이더의 포지션을 따라갈 수 있어요.",
    "OrangeX charges the common 0.02% maker / 0.05% taker rate on perpetuals. With our rebate, the taker fee you actually pay drops below most of the market.":
        "OrangeX는 무기한 선물에 일반적인 메이커 0.02% / 테이커 0.05%를 받아요. 페이백을 받으면 실제 테이커 수수료가 시장 대부분보다 낮아져요.",
    "Bitget is known for copy trading and a large futures market. Fees fall with account level, and holding its BGB token unlocks further discounts.":
        "Bitget은 카피트레이딩과 큰 선물 시장으로 알려져 있어요. 계정 레벨이 오를수록 수수료가 내려가고, BGB 토큰을 보유하면 추가 할인이 있어요.",
    "Bitunix charges 0.02% maker and 0.06% taker on perpetuals. A 45% rebate brings the taker fee you actually pay to 0.033%, cheaper than every listed headline rate.":
        "Bitunix는 무기한 선물에 메이커 0.02%, 테이커 0.06%를 받아요. 45% 페이백을 받으면 실제 테이커가 0.033%로, 목록의 어떤 기본 요율보다 싸져요.",
    "BloFin charges 0.02% maker and 0.06% taker on perpetuals. With a 45% rebate, your effective taker fee falls to 0.033%.":
        "BloFin은 무기한 선물에 메이커 0.02%, 테이커 0.06%를 받아요. 45% 페이백을 받으면 실제 테이커는 0.033%로 떨어져요.",
    "Deepcoin's maker fee of 0.04% is higher than most venues here, so it suits traders who mainly use market orders. A 45% rebate cuts the taker fee you pay to 0.033%.":
        "Deepcoin은 메이커 수수료 0.04%로 다른 곳보다 높아서, 주로 시장가를 쓰는 트레이더에게 맞아요. 45% 페이백으로 실제 테이커는 0.033%가 돼요.",
    "Biconomy lists perpetuals on crypto as well as gold and US stock tickers. We could not verify its current published futures fee, so check the fee page after you sign up.":
        "Biconomy는 코인뿐 아니라 금, 미국 주식 종목 무기한 선물도 상장해요. 현재 공시된 선물 수수료를 확인하지 못했으니, 가입 후 수수료 페이지를 확인하세요.",
    "Crypfine is the newest venue on our list. We could not verify its current published futures fee, so check the fee schedule on the site before trading.":
        "Crypfine은 목록에서 가장 새로운 거래소예요. 현재 공시된 선물 수수료를 확인하지 못했으니, 거래 전에 사이트의 수수료표를 확인하세요.",
})

# market note (update when the note changes)
NOTE = {
    "Snapshot · Oct 25, 2026": "스냅샷 · 2026년 10월 25일", "Oct 25, 2026": "2026년 10월 25일",
    "IV · Le marché · Sunday, Oct 25, 2026": "IV · 시황 · 2026년 10월 25일 (일)",
    "Longs flushed under $80K. The Fed decides the next leg.": "8만 달러 아래 롱 청산. 다음 방향은 연준이 정한다.",
    "Bitcoin slipped below $80,000 late in the week and is holding around $80,300. The move was driven by forced selling, not fresh shorts: more than nine in ten BTC liquidations over the last 24 hours hit long positions. When the selling is mostly liquidations, it often runs out once over-leveraged longs are cleared.":
        "비트코인은 주 후반 8만 달러 아래로 밀렸다가 8만 300달러 근처에서 버티고 있어요. 새로운 숏이 아니라 강제 매도가 끌어내린 하락이에요. 지난 24시간 BTC 청산의 90% 이상이 롱 포지션이었어요. 매도가 대부분 청산이면, 과도한 레버리지 롱이 정리되고 나서 힘이 빠지는 경우가 많아요.",
    "The pressure came from outside crypto. US spot Bitcoin ETFs posted their largest single-day outflow since late June on Oct 22, the same day the Nasdaq had its worst session since early June on worries about AI spending. Oil also climbed to its highest level since May, which pushes back against hopes for rate cuts.":
        "압력은 코인 밖에서 왔어요. 10월 22일 미국 현물 비트코인 ETF에서 6월 말 이후 하루 최대 순유출이 나왔고, 같은 날 나스닥은 AI 투자 우려로 6월 초 이후 최악의 하루를 보냈어요. 유가도 5월 이후 최고치로 올라 금리 인하 기대를 꺾고 있어요.",
    "The next catalyst is the Fed. The FOMC meets Oct 27–28 with the decision on Wednesday. Until then, the $79.3K low and the $81.0–81.4K band are the lines that matter. Leverage is still the main risk in both directions, so size positions so a single wick can't liquidate you.":
        "다음 변수는 연준이에요. FOMC는 10월 27–28일에 열리고 수요일에 결정이 나와요. 그때까지는 7만 9,300달러 저점과 8만 1,000–8만 1,400달러 구간이 핵심이에요. 양방향 모두 레버리지가 가장 큰 위험이니, 꼬리 한 번에 청산되지 않게 포지션 크기를 잡으세요.",
    "BTC liquidations, 24h": "BTC 청산 (24시간)", "Share that were longs": "그중 롱 비중",
    "All-crypto liquidations, 24h": "전체 코인 청산 (24시간)",
    "Spot ETF net flow, Oct 22": "현물 ETF 순유입, 10/22", "Spot ETF net flow, Oct 23": "현물 ETF 순유입, 10/23",
    "Spot ETF net flow, Oct 21": "현물 ETF 순유입, 10/21", "FOMC decision": "FOMC 결정", "Wed, Oct 28": "10/28 (수)",
    "Close above $81.4K": "8만 1,400달러 위 마감", "Pressure shifts to shorts.": "압력이 숏 쪽으로 넘어가요.",
    "and then the": "다음으로", "rebound high from Oct 21 come back into view.": "(10/21 반등 고점)이 다시 시야에 들어와요.",
    "$79.3K – $81.4K": "7만 9,300 – 8만 1,400달러",
    "Most likely into the Fed. Expect": "연준 발표 전까지 가장 유력한 시나리오. 펀딩비가 재조정되는 동안",
    "and fake breaks on both sides while funding resets.": "과 양방향 속임 돌파를 예상하세요.",
    "Close below $79.3K": "7만 9,300달러 아래 마감", "A fresh round of": "새로운",
    "is likely. Watch whether ETF outflows continue after the decision.": "이 나올 가능성이 커요. 결정 이후에도 ETF 유출이 이어지는지 보세요.",
    "Market commentary for information only. Not investment advice. Data: CoinGecko, CoinGlass and SoSoValue figures as reported Oct 24–25, 2026.":
        "정보 제공용 시황이며 투자 조언이 아니에요. 데이터: CoinGecko, CoinGlass, SoSoValue (2026년 10월 24–25일 기준).",
    "Oct 21 rebound high": "10/21 반등 고점", "Oct 23 level": "10/23 가격대",
    "24h high · resistance": "24시간 고점 · 저항", "24h low · support": "24시간 저점 · 지지",
}
EXACT.update(NOTE)

N = r"(?P<n>[A-Za-z][A-Za-z0-9 .]*?)"
PATTERNS = [
    (rf"^{N} referral code$", r"\g<n> 레퍼럴 코드"),
    (rf"^{N} Referral Code 2026: (?P<r>\d+)% Fee Rebate \| Perpline$", r"\g<n> 레퍼럴 코드 2026: \g<r>% 수수료 페이백 | Perpline"),
    (rf"^Sign up for {N}$", r"\g<n> 가입하기"),
    (rf"^{N} logo$", r"\g<n> 로고"),
    (r"^Perpline · Édition (?P<t>.+)$", r"Perpline · 에디션 \g<t>"),
    (r"^(?P<r>\d+)% fee rebate$", r"\g<r>% 수수료 페이백"),
    (r"^(?P<r>\d+)% of your fees, returned$", r"수수료의 \g<r>%를 돌려드려요"),
    (rf"^Sign up to {N}$", r"\g<n> 가입하기"),
    (rf"^About {N}$", r"\g<n> 소개"),
    (rf"^A month on {N}$", r"\g<n>에서의 한 달"),
    (rf"^Taker fees paid to {N}$", r"\g<n>에 낸 테이커 수수료"),
    (r"^Perpline rebate \((?P<r>\d+)%\)$", r"Perpline 페이백 (\g<r>%)"),
    (rf"^Open our {N} link$", r"저희 \g<n> 링크 열기"),
    (rf"^Complete identity verification if {N} requires it for your country or for futures access\.$", r"\g<n>에서 거주 국가나 선물 이용을 위해 요구하면 신원 인증을 완료하세요."),
    (r"^Claim your (?P<r>\d+)% rebate$", r"\g<r>% 페이백 받기"),
    (rf"^In {N}, open your profile\. Your UID is the account number shown there\.$", r"\g<n>에서 프로필을 열면 보이는 계정 번호가 UID예요."),
    (rf'^Send "{N} \+ your UID" to$', r'"\g<n> + UID"를'),
    (r"^on Telegram\. We confirm within 24 hours\.$", r"에게 텔레그램으로 보내주세요. 24시간 안에 확인해 드려요."),
    (rf"^{N} referral FAQ$", r"\g<n> 레퍼럴 FAQ"),
    (rf"^What is the {N} referral code\?$", r"\g<n> 레퍼럴 코드는 뭔가요?"),
    (rf"^Our {N} referral code is (?P<c>\S+)\. Register through our link, then send your UID to @(?P<h>\w+) on Telegram to activate the (?P<r>\d+)% fee rebate\.$",
        r"저희 \g<n> 레퍼럴 코드는 \g<c>예요. 저희 링크로 가입한 뒤 텔레그램 @\g<h>에게 UID를 보내면 \g<r>% 수수료 페이백이 활성화돼요."),
    (rf"^Our {N} referral is applied through our sign-up link, so there is no code to type\. Register through our link, then send your UID to @(?P<h>\w+) on Telegram to activate the (?P<r>\d+)% fee rebate\.$",
        r"저희 \g<n> 레퍼럴은 가입 링크로 자동 적용돼서 따로 입력할 코드가 없어요. 저희 링크로 가입한 뒤 텔레그램 @\g<h>에게 UID를 보내면 \g<r>% 수수료 페이백이 활성화돼요."),
    (rf"^How much rebate do I get on {N}\?$", r"\g<n>에서는 페이백을 얼마나 받나요?"),
    (rf"^Perpline returns (?P<r>\d+)% of the futures trading fees you pay on {N}, paid weekly in USDT\. On the standard taker fee of (?P<t>[\d.]+%), that brings your effective rate to (?P<e>[\d.]+%)\.$",
        r"Perpline은 \g<n>에서 낸 선물 거래 수수료의 \g<r>%를 매주 USDT로 돌려드려요. 일반 테이커 수수료 \g<t> 기준으로 실제 요율은 \g<e>가 돼요."),
    (rf"^Perpline returns (?P<r>\d+)% of the futures trading fees you pay on {N}, paid weekly in USDT\.$",
        r"Perpline은 \g<n>에서 낸 선물 거래 수수료의 \g<r>%를 매주 USDT로 돌려드려요."),
    (rf"^What are {N} futures fees\?$", r"\g<n> 선물 수수료는 얼마인가요?"),
    (rf"^The standard \(non-VIP\) USDT-margined perpetual fee on {N} is (?P<m>[\d.]+%) maker and (?P<t>[\d.]+%) taker, checked Oct 2026\. Your live account rate applies\.$",
        r"\g<n>의 일반(비 VIP) USDT 무기한 선물 수수료는 메이커 \g<m>, 테이커 \g<t>예요 (2026년 10월 확인). 실제로는 계정에 적용된 요율이 우선해요."),
    (rf"^We could not verify {N}'s current published futures fee\. Check the fee page on the exchange after signing up\.$",
        r"\g<n>의 현재 공시 선물 수수료는 확인하지 못했어요. 가입 후 거래소 수수료 페이지를 확인하세요."),
    (rf"^Can I add a {N} referral code to an existing account\?$", r"기존 \g<n> 계정에 레퍼럴 코드를 추가할 수 있나요?"),
    (rf"^Usually not\. Exchanges link a referral when the account is created, so the rebate requires a new {N} account opened through our link\.$",
        r"보통은 안 돼요. 거래소는 계정을 만들 때 레퍼럴을 연결하므로, 페이백을 받으려면 저희 링크로 새 \g<n> 계정을 만들어야 해요."),
    (rf"^Is {N} available in my country\?$", r"제 국가에서도 \g<n> 이용이 가능한가요?"),
    (rf"^{N} decides which countries it serves\. Check its terms for your country before registering\. This site is not for residents of the Republic of Korea or the United States\.$",
        r"서비스 국가는 \g<n>에서 정해요. 가입 전에 거주 국가 관련 약관을 확인하세요. 이 사이트는 대한민국과 미국 거주자를 대상으로 하지 않아요."),
    (rf"^{N}'s headline taker fee ranks No\. (?P<p>\d+) of (?P<k>\d+) venues with a verified fee\. After the (?P<r>\d+)% rebate, the (?P<e>[\d.]+%) you actually pay is below the headline taker fee of every other venue on our list\.$",
        r"\g<n>의 기본 테이커 수수료는 수수료가 확인된 \g<k>곳 중 \g<p>위예요. \g<r>% 페이백을 받으면 실제로 내는 \g<e>는 목록의 다른 모든 거래소의 기본 테이커 수수료보다 낮아요."),
    (rf"^{N}'s headline taker fee ranks No\. (?P<p>\d+) of (?P<k>\d+) venues with a verified fee\. After the (?P<r>\d+)% rebate, the (?P<e>[\d.]+%) you actually pay is below the headline taker fee of (?P<c>\d+) of the other (?P<o>\d+) venues\.$",
        r"\g<n>의 기본 테이커 수수료는 수수료가 확인된 \g<k>곳 중 \g<p>위예요. \g<r>% 페이백을 받으면 실제로 내는 \g<e>는 다른 \g<o>곳 중 \g<c>곳의 기본 테이커 수수료보다 낮아요."),
    (r"^(?P<r>\d+)% rebate · taker (?P<t>.+)$", r"페이백 \g<r>% · 테이커 \g<t>"),
    (rf"^{N} referral code(?P<c> \S+)?: sign up through Perpline and get (?P<r>\d+)% of your (?P<n2>.+?) futures trading fees back in USDT every week\. Fees, sign-up steps and FAQ\.$",
        r"\g<n> 레퍼럴 코드\g<c>: Perpline으로 가입하고 선물 거래 수수료의 \g<r>%를 매주 USDT로 돌려받으세요. 수수료, 가입 방법, FAQ."),
    (r"^/ (?P<n>.+)$", r"/ \g<n>"),
    (rf"^We'll add a worked example once {N}'s fee is verified\. The (?P<r>\d+)% rebate applies to whatever futures fee you pay\.$",
        r"\g<n>의 수수료가 확인되면 계산 예시를 추가할게요. \g<r>% 페이백은 실제로 낸 선물 수수료 전체에 적용돼요."),
]
PATTERNS = [(re.compile(p), r) for p, r in PATTERNS]

# raw replacements inside <script> (dynamic strings)
JS = [
    ('p?"Play slideshow":"Pause slideshow"', 'p?"슬라이드 재생":"슬라이드 멈춤"'),
    ('"Copied"', '"복사됨"'), ('"Copy"', '"복사"'), ('"Selected"', '"선택됨"'),
    ('round trips a month at $${fmt(n)}, after rebate. The faint line is the fee before rebate; on average the rebate saves ${money(saved)} a month. Funding not included.',
     '회 왕복 · 포지션 $${fmt(n)} · 페이백 적용 후 금액이에요. 흐린 선은 페이백 전 수수료이고, 페이백으로 한 달 평균 ${money(saved)}를 아껴요. 펀딩비 제외.'),
    ('round trips a month at $${fmt(n)}, before rebate. Funding not included.', '회 왕복 · 포지션 $${fmt(n)} · 페이백 전 금액이에요. 펀딩비 제외.'),
    ('"Live":"Snapshot · "+SNAP.when', '"실시간":"스냅샷 · "+SNAP.when'),
    ('"Enter your Telegram username, like @username, so we can reply."', '"답변을 드릴 수 있게 텔레그램 아이디(@username)를 입력해 주세요."'),
    ('"Add a few more details to your message."', '"메시지를 조금만 더 자세히 적어주세요."'),
    ('"Request sent. We\'ll message "+tg+" on Telegram."', '"문의가 접수됐어요. 텔레그램 "+tg+"(으)로 연락드릴게요."'),
    ('"Couldn\'t send right now. Message us directly on Telegram @"+CONTACT.telegram+"."', '"지금은 전송이 안 돼요. 텔레그램 @"+CONTACT.telegram+"으로 직접 메시지 주세요."'),
    ('"Message us directly on Telegram @"+CONTACT.telegram+" and paste your question there."', '"텔레그램 @"+CONTACT.telegram+"으로 직접 메시지를 보내 질문을 붙여넣어 주세요."'),
]
for k, v in NOTE.items():
    JS.append((f'label:"{k}"', f'label:"{v}"'))
JS.append(('when:"Oct 25, 2026"', 'when:"2026년 10월 25일"'))


def lookup(t):
    if t in EXACT:
        return EXACT[t]
    for rx, rep in PATTERNS:
        if rx.match(t):
            return rx.sub(rep, t)
    return None


def _text(m):
    raw = m.group(1)
    t = _h.unescape(" ".join(raw.split()))
    if not t:
        return m.group(0)
    k = lookup(t)
    return ">" + (raw.replace(raw.strip(), _h.escape(k, quote=False)) if k else raw) + "<"


def _attr(m):
    k = lookup(_h.unescape(m.group(2)))
    return f'{m.group(1)}="{_h.escape(k)}"' if k else m.group(0)


def translate(html):
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", html, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("<script"):
            if "application/ld+json" not in p:
                for a, b in JS:
                    p = p.replace(a, b)
            out.append(p)
        elif p.startswith("<style"):
            out.append(p)
        else:
            p = re.sub(r">([^<]+)<", _text, p)  # includes <title> text
            p = re.sub(r'(aria-label|placeholder|alt|content)="([^"]+)"', _attr, p)
            out.append(p)
    return "".join(out)
