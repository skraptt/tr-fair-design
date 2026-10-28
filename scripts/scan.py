#!/usr/bin/env python3
"""tr-fair-design candidate scanner.

Flags *candidate* dark patterns and KVKK issues in a codebase using regex
heuristics, for review under Turkish law (see references/kaliplar.md for the
TR-xx pattern catalogue). Output is a starting point for contextual review by an
agent or a human, not a list of confirmed findings, and never a legal
assessment.

Usage:
    python3 scan.py <project_root> [--out candidates.json] [--format json|md]

Stdlib only. Suppress a line with a `fair-design-ignore` comment on that line or
the line above.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field

VERSION = "0.1.1"

SCAN_EXT = {
    ".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".mjs", ".cjs", ".vue", ".svelte",
    ".astro", ".php", ".erb", ".twig", ".liquid", ".hbs", ".njk", ".json", ".py",
    ".rb", ".yaml", ".yml",
}
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "out",
    "vendor", "coverage", "__pycache__", ".venv", "venv", "fair-design-review",
    ".turbo", ".cache", "target", "fair-design-reviews",
}
# Test, e2e and Storybook code is not shipped UI. Skipped unless --include-tests.
TEST_DIRS = {"__tests__", "__mocks__", "test", "tests", "e2e", "e2e-live", "cypress", "playwright", "stories", "fixtures", "spec", "loadtest", "evals"}
TEST_FILE = re.compile(r"\.(test|spec|stories|e2e)\.[a-z]+$|_test\.py$|^test_.*\.py$", re.IGNORECASE)
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "candidates.json", "adaylar.json"}
UI_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".php", ".erb", ".twig", ".liquid", ".hbs", ".njk"}
MAX_BYTES = 1_000_000
IGNORE_MARK = "fair-design-ignore"

I = re.IGNORECASE


@dataclass
class Candidate:
    rule: str
    patterns: list[str]
    file: str
    line: int
    snippet: str
    confidence: str  # low | medium | high
    note: str


@dataclass
class Rule:
    id: str
    patterns: list[str]
    regex: re.Pattern
    confidence: str
    note: str
    # optional: another regex that must match within +/- `window` lines
    near: re.Pattern | None = None
    window: int = 0
    exts: set[str] | None = None  # restrict to these extensions
    exclude: re.Pattern | None = None  # skip line if this matches


# --------------------------------------------------------------------------- rules

LINE_RULES: list[Rule] = [
    Rule(
        id="prechecked-checkbox",
        patterns=["TR-01", "TR-02", "TR-14"],
        regex=re.compile(
            r"\bdefaultChecked\b(?!\s*=\s*\{\s*(false|\w))"
            r"|<input\b[^>]*\bchecked\b(?!\s*=\s*\{)"
            r"|\bchecked\s*=\s*(\{\s*true\s*\}|[\"'](checked|true)?[\"'])"
            r"|:checked\s*=\s*[\"']true[\"']",
            I,
        ),
        near=re.compile(r"checkbox|toggle|switch|consent|newsletter|insurance|add-?on|extra|onay|rıza|riza|kampanya|ileti|bilgilendirme|bülten|bulten|sms|e-?posta|sigorta|bağış|bagis|ek hizmet|hızlı kargo|üyeliğimi|uyeligimi|otomatik", I),
        window=3,
        confidence="medium",
        note="Önceden işaretli kutu. Bir ücret mi (TR-01, MSY m.19), bir ticari ileti onayı mı (TR-02, TİY m.7/8), otomatik üyelik mi (TR-14) ekliyor, kontrol et.",
        exts={".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".php", ".erb", ".twig", ".liquid", ".hbs", ".njk", ".js", ".ts"},
    ),
    Rule(
        id="consent-default-granted",
        patterns=["TR-02", "TR-23"],
        regex=re.compile(
            r"\b(consent|tracking|analytics|marketing|personali[sz]\w*|newsletter|iys|ticariIleti|ticari_ileti|kampanyaOnay|acikRiza|acik_riza|ad_?storage|ad_?personali[sz]ation|ad_?user_?data|share_?data|public_?profile|location_?sharing)[\"']?\s*:\s*(true\b|[\"']granted[\"'])"
            r"|\b\w*(consent|tracking|analytics|marketing|newsletter|optin)(enabled|granted|allowed|given|accepted)?\s*=\s*(true\b|[\"']granted[\"'])"
            r"|\[\s*\w*(consent|tracking|marketing|analytics|newsletter|optIn|optin)\w*\s*,\s*\w+\s*\]\s*=\s*useState\(\s*true\s*\)",
            I,
        ),
        confidence="medium",
        note="Onay / takip / mahremiyet ayarı varsayılan olarak açık başlıyor. Kullanıcı etkin bir eylemle onaylayana kadar kapalı olmalı (TİY m.7/8, Çerez Rehberi).",
        exclude=re.compile(r"\b(required|essential|necessary|strictly)\b", I),
    ),
    Rule(
        id="countdown-timer",
        patterns=["TR-07"],
        regex=re.compile(r"(Date\.now\(\)|new Date\(\)\.getTime\(\)|time\.time\(\))\s*\+\s*[\w(]", I),
        near=re.compile(r"countdown|offer|deal|\bsale\b|discount|promo|indirim|kampanya|fırsat|firsat|geri ?sayım|kalan süre|bitiyor|ends in", I),
        window=6,
        confidence="high",
        note="Bitiş zamanı sayfanın açılışına göre hesaplanıyor. Sayfa yenilenince baştan başlıyorsa gerçek bir süre değildir (TR-07).",
        exts=UI_EXT | {".js", ".ts"},
        exclude=re.compile(r"ttl|timeout|expires?_?(at|in)\b|token|retry|poll|cache|session|oauth|invit|lease|backoff|refresh", I),
    ),
    Rule(
        id="urgency-text",
        patterns=["TR-07"],
        regex=re.compile(
            r"offer ends in|ends in \{|expires in|only today|today only|hurry|last chance"
            r"|endet in|nur heute|nur noch heute|beeil dich|letzte chance"
            r"|sadece bugün|yalnızca bugün|son fırsat|acele et|kampanya bitiyor|fırsatı kaçırma|indirim bitiyor|son \d+ saat"
            r"|se termine dans|dépêchez",
            I,
        ),
        # Legal and admin texts are full of deadlines ("sürenin son günü"); only
        # flag urgency next to a sale, price or cart.
        near=re.compile(r"indirim|kampanya|fırsat|firsat|teklif|sepet|satın al|satin al|fiyat|stok|ürün|offer|deal|\bsale\b|discount|price|cart|checkout|buy", I),
        window=3,
        confidence="low",
        note="Aciliyet ifadesi. Sürenin gerçek ve sunucu tarafında uygulanıyor olduğunu doğrula (TR-07).",
    ),
    Rule(
        id="scarcity-message",
        patterns=["TR-08"],
        regex=re.compile(
            r"only\s+(\{[^}]*\}|\$\{[^}]*\}|\{\{[^}]*\}\}|\d+)\s+(left|remaining|in stock)"
            r"|almost sold out|selling fast|low stock|limited stock"
            r"|nur noch\s+(\{[^}]*\}|\d+)|fast ausverkauft|nur noch wenige"
            r"|son\s+(\{[^}]*\}|\$\{[^}]*\}|\d+)\s+(ürün|adet|kişi)|tükenmek üzere|stokta son|sınırlı stok|stokta (sadece|yalnızca)"
            r"|plus que\s+(\{[^}]*\}|\d+)|presque épuisé",
            I,
        ),
        confidence="medium",
        note="Kıtlık ifadesi. Gerçek stok verisinden gelmeli (TR-08).",
    ),
    Rule(
        id="random-number-in-ui",
        patterns=["TR-08", "TR-09"],
        regex=re.compile(r"Math\.random\(\)|random\.randint\(|\brand\(\s*\d", I),
        near=re.compile(r"viewing|viewers|watching|watchers|visitors|buyers|\bleft\b|in stock|people|bought|purchas|\bsold\b|kişi|kisi|bakan|izleyen|ziyaret|satıl|satil|alıcı|stok|reviews?\b|rating|yorum|puan", I),
        exclude=re.compile(r"suffix|\bid\b|uuid|nonce|jitter|toString\(\s*(16|36)\s*\)", I),
        window=8,
        confidence="high",
        note="Stok veya etkinlik ifadesinin yakınında rastgele sayı: uydurma kıtlık ya da sosyal kanıt olabilir (TR-08, TR-09).",
    ),
    Rule(
        id="social-proof-message",
        patterns=["TR-09"],
        regex=re.compile(
            r"(people|users|visitors|shoppers)\s+(are\s+)?(viewing|looking at|watching)"
            r"|just (bought|purchased|ordered)|bought in the last|recently purchased"
            r"|(personen|leute)\s+(sehen sich|schauen)|hat gerade (gekauft|bestellt)"
            r"|kişi (şu an |şu anda )?(bu ürüne |bu ürünü )?(bakıyor|inceliyor|görüntülüyor)|az önce satın aldı|sepetine ekledi|son 24 saatte"
            r"|personnes regardent|vient d'acheter",
            I,
        ),
        confidence="medium",
        note="Etkinlik / sosyal kanıt bildirimi. Gerçek ve güncel veriden gelmeli (TR-09).",
    ),
    Rule(
        id="confirmshaming-text",
        patterns=["TR-12"],
        regex=re.compile(
            r"no,?\s*thanks?,?\s*i\s*(don'?t|do not|hate|prefer|like|'d rather|would rather)"
            r"|i\s*(don'?t|do not)\s*(want|like)\s*(to\s*)?(sav|deal|discount|money|free|be healthy|grow)"
            r"|i('d| would)? rather pay (full|more)|i prefer (to )?pay(ing)? (full|more)"
            r"|nein,?\s*danke,?\s*ich\s*(will|möchte|zahle|verzichte)"
            r"|ich zahle lieber|ich verzichte auf (rabatt|ersparnis)"
            r"|hayır,?\s*(teşekkürler,?)?\s*.{0,30}(istemiyorum|tercih ederim)|tasarruf etmek istemiyorum|tam fiyat(ı)? ödemeyi tercih|kazanmak istemiyorum|fırsatları kaçırmak istiyorum|indirimden vazgeçiyorum"
            r"|non merci,?\s*je\s*(ne veux|préfère)",
            I,
        ),
        confidence="high",
        note="Reddetme seçeneği kullanıcıyı utandıracak ya da suçlu hissettirecek şekilde yazılmış (TR-12).",
    ),
    Rule(
        id="order-button-wording",
        patterns=["TR-19"],
        regex=re.compile(
            r">\s*(\{?\s*t\(\s*[\"'])?(continue|next|devam( et)?|ileri|sonraki|tamamla|onayla|bitir|complete|submit|confirm)([\"']\s*\)\s*\})?\s*<",
            I,
        ),
        near=re.compile(r"checkout|place_?order|placeOrder|submitOrder|payment|\bpay\b|kasse|bestell|zahlung|ödeme|sipariş|commande|paiement|purchase", I),
        window=12,
        confidence="medium",
        note="Son sipariş / ödeme butonu olabilecek bir yerde genel ifade. Siparişin ödeme yükümlülüğü doğurduğu açıkça bildirilmeli (TR-19, MSY m.8/1).",
    ),
    Rule(
        id="fake-reference-price",
        patterns=["TR-20"],
        regex=re.compile(
            r"(original|old|was|compare|regular|list|before|strike)_?price\w*\s*[:=]\s*[\w.\[\]]*price\w*\s*\*\s*\d"
            r"|(eski|önceki|onceki|liste|ustu_?cizili|üstü_?çizili)_?fiyat\w*\s*[:=]\s*[\w.\[\]]*fiyat\w*\s*\*\s*\d"
            r"|(price|fiyat)\w*\s*\*\s*(1\.\d+|2(\.\d+)?)\b",
            I,
        ),
        near=re.compile(r"line-through|<s>|<del>|strike|original|was|compare|eski|önceki|yerine|discount|indirim|%", I),
        window=6,
        confidence="high",
        note="'Önceki' fiyat güncel fiyat çarpılarak hesaplanıyor. Önceki fiyat, indirimden önceki 10 günün gerçek en düşük fiyatı olmalı (TR-20, TRHTUY m.14/3).",
    ),
    Rule(
        id="free-trial-text",
        patterns=["TR-16"],
        regex=re.compile(
            r"free trial|try (it )?(for )?free|start (your )?free|free for \d+\s*(days|months)"
            r"|kostenlos testen|gratis testen|\d+ tage (kostenlos|gratis)"
            r"|ücretsiz dene|ücretsiz deneme|ilk ay ücretsiz|\d+ gün ücretsiz|bedava dene",
            I,
        ),
        confidence="low",
        note="Ücretsiz deneme. Deneme sonrası fiyat, tarih ve iptal yolu çağrının hemen yanında yazmalı; kart bilgisi isteniyorsa özellikle kontrol et (TR-16).",
    ),
    Rule(
        id="late-fee",
        patterns=["TR-18"],
        regex=re.compile(
            r"(service|booking|handling|processing|convenience|platform|admin)[\s_-]?(fee|charge)"
            r"|hizmet bedeli|işlem ücreti|islem_ucreti|servis ücreti|platform hizmet bedeli|kapıda ödeme ücreti|hizmetBedeli",
            I,
        ),
        confidence="low",
        note="Ek ücret. İlk gösterilen fiyata dahil olmalı, son adımda eklenmemeli (TR-18, MSY m.5/1(d)).",
        exclude=re.compile(r"^\s*(import|from|//|#)", I),
    ),
    Rule(
        id="manipulative-ai-prompt",
        patterns=["TR-22"],
        regex=re.compile(
            r"(never|don'?t|do not)\s+(reveal|admit|say|tell|mention|disclose)\b.{0,40}\b(ai|bot|assistant|language model|llm|machine)"
            r"|pretend\s+(to be|you are|you're)\s+(a\s+)?(human|real person)"
            r"|create (a )?(sense of )?urgency|pressure (the )?(user|customer|them)"
            r"|exploit\b.{0,30}(emotion|fear|lonel|insecur|vulnerab)"
            r"|make (them|the user|the customer) feel (guilty|ashamed|afraid)"
            r"|don'?t let (them|the user|the customer) (leave|cancel)"
            r"|yapay zek[aâ] olduğunu (söyleme|belli etme|gizle|asla)|bot olduğunu (söyleme|belli etme|gizle)"
            r"|insan gibi davran|gerçek bir insan(mış)? gibi|aciliyet (hissi )?(yarat|oluştur)|baskı (kur|yap)"
            r"|iptal etmesine izin verme|ayrılmasına izin verme|duygularını kullan",
            I,
        ),
        confidence="medium",
        note="Yapay zekâya verilmiş, manipülatif olabilecek ya da yapay zekâ olduğunu gizleyen bir talimat (TR-22).",
    ),
    Rule(
        id="required-consent",
        patterns=["TR-03"],
        # An attribute, not a word: `required`, `required={true}`, aria-required,
        # or a schema flag. Never `=== "required"` or prose in a translation file.
        regex=re.compile(r"(?<![\"'\w.-])required(?=\s*(=\s*\{\s*true\s*\}|=\s*[\"']?required|/?>|\s+[\w-]+=|\s*$))|aria-required=[\"']true[\"']|\brequired:\s*true", I),
        near=re.compile(r"açık rıza|acik riza|acikRiza|ticari (elektronik )?ileti|kampanya|pazarlama|marketing|hedefli reklam|profil(leme)?|kişiselleştiril|reklam amaçlı|iys|e-?bülten|newsletter|sms ile|e-?posta ile bilgi", I),
        window=3,
        confidence="medium",
        note="Pazarlama, ticari ileti ya da açık rıza onayı zorunlu tutuluyor olabilir. Onay hizmet şartına bağlanamaz (TR-03, TİY m.7/9, KVKK m.3/1(a)).",
        exts=UI_EXT,
        exclude=re.compile(r"kullanım koşul|kullanim kosul|üyelik sözleşme|uyelik sozlesme|mesafeli satış|on bilgilendirme|ön bilgilendirme|terms", I),
    ),
    Rule(
        id="combined-notice-consent",
        patterns=["TR-04"],
        regex=re.compile(r"aydınlatma|aydinlatma", I),
        near=re.compile(r"açık rıza|acik riza|onay veriyorum|onaylıyorum|onayliyorum|kabul ediyorum|rıza gösteriyorum|riza gosteriyorum|izin veriyorum", I),
        window=1,
        confidence="medium",
        note="Aydınlatma metni bir onay ifadesiyle ya da açık rızayla aynı yerde. İkisi ayrı metinler ve ayrı beyanlar olmalı; aydınlatma için onay istenmemeli (TR-04, İlke Kararı 2026/347).",
        exts=UI_EXT | {".js", ".ts", ".json"},
        exclude=re.compile(r"\b(import|export)\b.*\bfrom\b", I),
    ),
    Rule(
        id="popularity-badge",
        patterns=["TR-11"],
        regex=re.compile(r"en popüler|en populer|en çok tercih edilen|en cok tercih edilen|en çok satan|en cok satan|most popular|best ?seller|popularBadge|isPopular\s*[:=]\s*true", I),
        confidence="low",
        note="'En popüler' türü bir etiket. Şeffaf ve gerçek bir ölçüte dayanmalı (TR-11, RK-2024 s.13-14).",
        exts=UI_EXT | {".js", ".ts", ".json"},
    ),
    Rule(
        id="hardcoded-reviews",
        patterns=["TR-10"],
        regex=re.compile(r"\b(rating|puan|stars|yildiz|yıldız)[\"']?\s*:\s*[45](\.\d)?\s*[,}]", I),
        near=re.compile(r"\b(comment|yorum|review|text|author|isim|kullanici|customer)[\"']?\s*:\s*[\"'`]", I),
        window=2,
        confidence="medium",
        note="Koda gömülü, yüksek puanlı bir tüketici yorumu olabilir. Yorumlar yalnızca satın alanlardan gelmeli ve yönlendirilmeden yayınlanmalı (TR-10, TRHTUY m.28/B).",
        exts=UI_EXT | {".js", ".ts", ".json"},
    ),
    Rule(
        id="required-sensitive-field",
        patterns=["TR-15"],
        regex=re.compile(r"(name|id|field|register)\s*[=(:]\s*\{?\s*[\"'](gender|cinsiyet|birth_?date|birthday|dogum_?tarihi|dogumTarihi|tc_?kimlik(_?no)?|tckn|tcKimlikNo|identity_?number)[\"']", I),
        # Same line only: a neighbouring field's `required` must not count.
        near=re.compile(r"\brequired\b(?!\s*=\s*\{\s*false)|aria-required=[\"']true|required:\s*true|\.required\(|zorunlu", I),
        window=0,
        confidence="medium",
        note="Hizmet için gerekli olmayabilecek bir bilgi zorunlu tutuluyor. Veriler amaçla sınırlı ve ölçülü olmalı (TR-15, KVKK m.4/2(ç)).",
        exts=UI_EXT | {".js", ".ts"},
    ),
]

# File-level rules: checked once per file.
ACCEPT_ALL = re.compile(r"accept all|accept cookies|allow all|tümünü kabul|tumunu kabul|hepsini kabul|kabul et|çerezleri kabul", I)
REJECT = re.compile(r"reject|decline|deny|refuse|only necessary|necessary only|essential only|reddet|hepsini reddet|tümünü reddet|yalnızca (zorunlu|gerekli)|sadece (zorunlu|gerekli)", I)
COMMENT_LINE = re.compile(r"^\s*(//|#|/\*|\*|<!--|\{/\*)")
COOKIE_CTX = re.compile(r"cookie|consent|tracking|çerez", I)
TRACKER = re.compile(r"googletagmanager\.com|google-analytics\.com|gtag\(|fbq\(|connect\.facebook\.net|static\.hotjar\.com|clarity\.ms|snap\.licdn\.com|analytics\.tiktok\.com", I)
CONSENT_GATE = re.compile(r"consent|rıza|riza|cerezOnay|çerez onay|cookiebot|onetrust|usercentrics|klaro|cookieyes|iubenda|borlabs|data-cookieconsent|type=[\"']text/plain[\"']", I)

# Project-level signals.
SUBSCRIBE = re.compile(r"subscri(be|ption)|recurring|abonelik|abone ol|aylık plan|yıllık plan|otomatik yenile|mode:\s*[\"']subscription", I)
CANCEL = re.compile(r"cancel[\s_-]?(subscription|plan|membership)|cancelSubscription|subscriptions?\.(cancel|del)|abonelik(ten)? (iptal|çık)|aboneliği(mi|nizi)? (iptal|sonlandır|feshet)|üyeliği(mi|nizi)? (iptal|sonlandır)|/cancel\b|/iptal\b|end[\s_-]?subscription|fesih", I)

# Services usually hosted outside Turkey: personal data sent to them is a
# transfer abroad under KVKK m.9 and must be documented (TR-21).
FOREIGN_SERVICES: dict[str, re.Pattern] = {
    "Google Analytics / Tag Manager": re.compile(r"googletagmanager\.com|google-analytics\.com|gtag\(|@next/third-parties/google|react-ga4?\b", I),
    "Sentry": re.compile(r"@sentry/|ingest\.(\w+\.)?sentry\.io|sentry_sdk", I),
    "Meta Pixel": re.compile(r"connect\.facebook\.net|fbq\(", I),
    "Hotjar": re.compile(r"static\.hotjar\.com|@hotjar/", I),
    "Microsoft Clarity": re.compile(r"clarity\.ms", I),
    "Mixpanel": re.compile(r"mixpanel", I),
    "Segment": re.compile(r"@segment/|cdn\.segment\.(com|io)|analytics\.segment", I),
    "Amplitude": re.compile(r"@amplitude/|amplitude\.com", I),
    "PostHog": re.compile(r"posthog", I),
    "Firebase": re.compile(r"\bfirebase/|firebase-admin|firebaseio\.com", I),
    "OpenAI": re.compile(r"api\.openai\.com|from [\"']openai[\"']|require\([\"']openai[\"']\)|^\s*import openai|^\s*from openai", I),
    "Anthropic": re.compile(r"@anthropic-ai/sdk|api\.anthropic\.com|^\s*import anthropic|^\s*from anthropic", I),
    "Google Gemini / Vertex": re.compile(r"@google/(generative-ai|genai)|generativelanguage\.googleapis\.com|aiplatform\.googleapis", I),
    "Intercom": re.compile(r"widget\.intercom\.io|@intercom/", I),
    "HubSpot": re.compile(r"js\.hs-scripts\.com|@hubspot/", I),
    "Mailchimp": re.compile(r"mailchimp", I),
    "SendGrid": re.compile(r"@sendgrid/|api\.sendgrid\.com", I),
    "Twilio": re.compile(r"\btwilio\b", I),
}


def iter_files(root: str, include_tests: bool = False):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".") and (include_tests or d.lower() not in TEST_DIRS)
        ]
        for name in filenames:
            if name in SKIP_FILES or name.endswith((".min.js", ".map")):
                continue
            if not include_tests and TEST_FILE.search(name):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in SCAN_EXT:
                continue
            path = os.path.join(dirpath, name)
            try:
                if os.path.getsize(path) > MAX_BYTES:
                    continue
                with open(path, encoding="utf-8", errors="replace") as fh:
                    yield path, ext, fh.read()
            except OSError:
                continue


def suppressed(lines: list[str], idx: int) -> bool:
    if IGNORE_MARK in lines[idx]:
        return True
    return idx > 0 and IGNORE_MARK in lines[idx - 1]


def clip(s: str, n: int = 160) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def scan(root: str, include_tests: bool = False) -> dict:
    root = os.path.abspath(root)
    cands: list[Candidate] = []
    files_scanned = 0
    subscribe_hits: list[tuple[str, int]] = []
    cancel_found = False
    foreign_hits: dict[str, tuple[str, int, str]] = {}

    for path, ext, text in iter_files(root, include_tests):
        files_scanned += 1
        rel = os.path.relpath(path, root)
        lines = text.splitlines()

        # line rules
        for rule in LINE_RULES:
            if rule.exts and ext not in rule.exts:
                continue
            for i, line in enumerate(lines):
                if COMMENT_LINE.match(line) and rule.id != "manipulative-ai-prompt":
                    continue
                if not rule.regex.search(line):
                    continue
                if rule.exclude and rule.exclude.search(line):
                    continue
                if rule.near is not None:
                    lo, hi = max(0, i - rule.window), min(len(lines), i + rule.window + 1)
                    if not rule.near.search("\n".join(lines[lo:hi])) and not rule.near.search(rel):
                        continue
                if suppressed(lines, i):
                    continue
                cands.append(Candidate(rule.id, rule.patterns, rel, i + 1, clip(line), rule.confidence, rule.note))

        # file rules: cookie banner asymmetry
        if COOKIE_CTX.search(text):
            accept_line = next((i for i, l in enumerate(lines) if ACCEPT_ALL.search(l)), None)
            code_only = "\n".join(l for l in lines if not COMMENT_LINE.match(l))
            if accept_line is not None and not REJECT.search(code_only) and not suppressed(lines, accept_line):
                cands.append(Candidate(
                    "cookie-accept-without-reject", ["TR-05", "TR-13"], rel, accept_line + 1,
                    clip(lines[accept_line]), "medium",
                    "Onay arayüzünde 'kabul' var ama bu dosyada reddetme seçeneği yok. İlk katmanda kabulle eşit ağırlıkta bir 'Reddet' olmalı (TR-05, Çerez Rehberi).",
                ))

        # file rules: trackers loaded without any consent gating in the same file
        if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".php", ".erb", ".twig", ".liquid", ".hbs", ".njk"}:
            t_line = next((i for i, l in enumerate(lines) if TRACKER.search(l)), None)
            if t_line is not None and not CONSENT_GATE.search(text) and not suppressed(lines, t_line):
                cands.append(Candidate(
                    "tracker-before-consent", ["TR-06", "TR-21"], rel, t_line + 1, clip(lines[t_line]), "medium",
                    "Üçüncü taraf takip kodu, bu dosyada görünür bir onay kontrolü olmadan yükleniyor. Yalnızca açık rızadan sonra çalıştığını doğrula (TR-06, Çerez Rehberi).",
                ))

        # project-level signals
        for i, l in enumerate(lines):
            if SUBSCRIBE.search(l) and len(subscribe_hits) < 5:
                subscribe_hits.append((rel, i + 1))
        if not cancel_found and CANCEL.search(text):
            cancel_found = True
        if ext != ".json" or os.path.basename(path) == "package.json":
            for i, l in enumerate(lines):
                if COMMENT_LINE.match(l):
                    continue
                for service, rx in FOREIGN_SERVICES.items():
                    if service not in foreign_hits and rx.search(l) and not suppressed(lines, i):
                        foreign_hits[service] = (rel, i + 1, l)

    if subscribe_hits and not cancel_found:
        f, ln = subscribe_hits[0]
        cands.append(Candidate(
            "cancellation-missing", ["TR-17"], f, ln, "(proje geneli)", "medium",
            "Abonelik kodu var ama projede çevrim içi iptal yolu bulunamadı. Fesih, sözleşmenin kurulmasından daha zor olamaz (TR-17, TKHK m.52). "
            f"Abonelik izleri: {', '.join(f'{a}:{b}' for a, b in subscribe_hits)}.",
        ))

    for service, (f, ln, l) in sorted(foreign_hits.items()):
        cands.append(Candidate(
            "foreign-data-transfer", ["TR-21"], f, ln, clip(l), "low",
            f"{service}: genellikle yurt dışında barındırılan bir servis. Kişisel veri gidiyorsa KVKK m.9 kapsamında aktarım dayanağı belirlenmeli, standart sözleşme imzalanıp 5 iş günü içinde Kurula bildirilmeli ve aydınlatma metninde yer almalı (TR-21).",
        ))

    cands.sort(key=lambda c: (c.file, c.line, c.rule))
    by_rule: dict[str, int] = {}
    for c in cands:
        by_rule[c.rule] = by_rule.get(c.rule, 0) + 1

    return {
        "tool": "tr-fair-design",
        "version": VERSION,
        "root": root,
        "files_scanned": files_scanned,
        "candidate_count": len(cands),
        "by_rule": dict(sorted(by_rule.items(), key=lambda kv: -kv[1])),
        "disclaimer": "İnceleme için sezgisel adaylar. Bulgu değildir, hukuki görüş değildir.",
        "candidates": [asdict(c) for c in cands],
    }


def to_markdown(result: dict) -> str:
    out = [
        f"# tr-fair-design adayları ({result['candidate_count']})",
        "",
        f"Taranan dosya: {result['files_scanned']}. {result['disclaimer']}",
        "",
        "| Kural | Kalıplar | Konum | Güven | Kod |",
        "|---|---|---|---|---|",
    ]
    for c in result["candidates"]:
        snip = c["snippet"].replace("|", "\\|")
        out.append(f"| {c['rule']} | {', '.join(c['patterns'])} | `{c['file']}:{c['line']}` | {c['confidence']} | `{snip}` |")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Scan a codebase for candidate dark patterns and KVKK issues (Turkish law).")
    ap.add_argument("root", help="project root to scan")
    ap.add_argument("--out", help="write results to this file")
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("--include-tests", action="store_true", help="also scan test, e2e and Storybook files")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2

    result = scan(args.root, args.include_tests)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) if args.format == "json" else to_markdown(result)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(rendered)
    else:
        print(rendered)

    # summary to stderr so stdout stays machine-readable
    print(f"\ntr-fair-design {VERSION}: {result['files_scanned']} dosya, {result['candidate_count']} aday", file=sys.stderr)
    for rule, n in result["by_rule"].items():
        print(f"  {n:>3}  {rule}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
