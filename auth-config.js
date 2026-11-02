/* 회원 로그인 설정 (Perpline) — 2026-11-02
   · url·anonKey 가 비어 있는 지금은 아무것도 표시하지 않고, 아무 파일도 더 불러오지 않는다(화면 변화 0).
   · 켜는 법: Supabase → Project Settings → API 의 Project URL 과 anon(또는 publishable) 키를 아래 두 칸에 넣고 저장.
     서비스 롤(service_role / secret) 키는 절대 넣지 않는다.
   · 공용 로그인 모듈: https://probe2928-crypto.github.io/chainbrief/auth/auth.js (chainbrief 저장소 public/auth/auth.js)
   · 설명서: chainbrief 저장소 ops/auth/SETUP_GUIDE.md
   · 영문·외국인 대상이라 카카오는 기본에서 뺌. /ko/ 페이지는 자동으로 한국어. */
(function () {
  var c = window.SITE_AUTH = window.SITE_AUTH || {
    "url": "",
    "anonKey": "",
    "site": "perpline",
    "lang": "en",
    "providers": [
      "google",
      "apple",
      "email"
    ],
    "naver": "hidden",
    "mimic": "header.top .right a.hide-sm",
    "brand": "Perpline",
    "links": {
      "terms": "https://probe2928-crypto.github.io/perpline/terms.html",
      "privacy": "https://probe2928-crypto.github.io/perpline/privacy.html"
    },
    "versions": {
      "terms": "2026-11-02",
      "privacy": "2026-11-02",
      "marketing": "2026-11-02"
    },
    "channels": [
      "email"
    ],
    "night": true,
    "theme": {
      "ink": "#111111",
      "paper": "#FBF4EC",
      "accent": "#111111",
      "muted": "#655D55",
      "line": "#E4D5C4",
      "radius": "10px"
    },
    "iapNotice": false
  };
  if (/\/ko(\/|$)/.test(location.pathname)) c.lang = "ko";
  if (!c.url || !c.anonKey) return;
  var s = document.createElement("script");
  s.src = "https://probe2928-crypto.github.io/chainbrief/auth/auth.js";
  s.defer = true;
  document.head.appendChild(s);
})();
