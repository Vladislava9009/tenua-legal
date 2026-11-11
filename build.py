#!/usr/bin/env python3
"""Builds the Tenua legal pages: privacy.html, health-data.html, terms.html, support.html.

Same layout as ~/Developer/nocte-legal (docs/REUSE.md), English for 1.0.
NOT PUBLISHED. Publishing is the owner's call (OWNER_TODO). After publishing,
put the privacy address into PRIVACY_URL (src/services/links.ts) and replace
PRIVACY_URL_PENDING in store/metadata/*/description.txt.
"""
import html
import os

EMAIL = "vladislava.bogaturova@gmail.com"
DEV = "Vladyslava Ostapchuk"
UPDATED = "2026-11-11"
APP = "Tenua"

# Colours from src/theme.ts.
CSS = """
:root{--bg:#F3EFE8;--fg:#26231F;--muted:#5F5951;--accent:#5E4F98;--rule:#E2DCD1}
@media (prefers-color-scheme:dark){:root{--bg:#121316;--fg:#E4E0D8;--muted:#ADA8A0;--accent:#A69CD8;--rule:#25282E}}
*{box-sizing:border-box}
body{margin:0;font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
header{border-bottom:1px solid var(--rule);padding:22px 16px}
header .in,main{max-width:760px;margin:0 auto}
header h1{margin:0;font-size:28px;letter-spacing:-.4px}
header p{margin:4px 0 0;color:var(--muted)}
main{padding:8px 16px 48px}
h2{margin:28px 0 6px;font-size:19px}
main h1{font-size:24px;margin:20px 0 4px}
em{color:var(--muted)}
a{color:var(--accent)}
ul{padding-left:22px}
footer{max-width:760px;margin:0 auto;padding:0 16px 32px;font-size:14px;color:var(--muted)}
"""

PRIVACY = [
    ("The short version", [
        "Tenua is a headache diary that keeps your entries on your iPhone. We have no servers, no accounts and no analytics, and we never receive your diary.",
        "One thing leaves your iPhone, and only if you choose a city for air pressure: the city's coordinates are sent to Apple Weather to get the air pressure around an attack.",
        "Purchases are handled by Apple. We never see your payment details or your Apple ID.",
    ]),
    ("What stays on your iPhone", [
        "Your attacks (start, end, strength, side, symptoms, aura, what you noted before them, notes and the words you typed), the medicines you take and your doses, your day summaries, your period days, your reminders and settings.",
        "This information is stored only in the app's storage on your device. We cannot see it. Your device's own backup (for example iCloud Backup) may include it according to your device settings; that is between you and Apple. If you delete the app, this information is deleted with it, unless you saved a backup file yourself.",
        "When you type in “In your own words”, the text is read by Apple's on-device model (Apple Intelligence) on your iPhone. It is not sent to us or to anyone else.",
    ]),
    ("Air pressure (Apple Weather)", [
        "If you choose a city in Settings → Air pressure, Tenua asks Apple Weather (WeatherKit) for the hourly air pressure of that city for the 3 days before an attack, once per attack. The request carries the city's coordinates rounded to about one kilometre and the time range. It does not carry your location, your diary or anything that identifies you. Apple states that WeatherKit does not track your location between requests: https://developer.apple.com/weatherkit/",
        "If you don't choose a city, no request is made. You can remove the city at any time.",
    ]),
    ("Apple Health", [
        "If you connect Apple Health, Tenua can save your attacks there as headaches (start, end and severity) and read your sleep, your period days and, on iOS 26, the medicines you choose to share. You decide each of these in the Health permission sheet and can change it any time in the Health app. Health data read by Tenua stays on your iPhone and is never used for advertising or shared with anyone.",
    ]),
    ("Reports, exports and backups", [
        "Reports (PDF), CSV exports and backup files are created on your iPhone. Tenua shows the iOS share sheet; you decide where the file goes. We don't receive a copy.",
    ]),
    ("Purchases", [
        "Tenua Pro is sold through the App Store. Apple processes the payment and tells the app, on your device, whether you have an active subscription or a lifetime purchase. We do not receive your name, email, payment details or Apple ID. Apple's privacy policy applies to purchases: https://www.apple.com/legal/privacy/",
    ]),
    ("Notifications", [
        "Reminders you turn on (day summary, month in numbers, “Is the attack over?”, “Did it help?”, the doctor's visit, a day of your cycle) and notices about a free trial or an offer are scheduled locally on your iPhone. They are not sent from a server.",
    ]),
    ("Contacting us", [
        "If you choose “Send feedback”, the app opens a draft email in your mail app with the app version, iOS version and language filled in. Your diary is not attached. If you send it, we receive your email address and what you wrote, and use them only to reply. We delete your messages on request.",
    ]),
    ("Children", [
        "Tenua is not directed at children under 13.",
    ]),
    ("Your rights", [
        "Because we don't receive your diary, there is nothing for us to access, correct or delete, apart from emails you send us. You can delete all your entries by deleting the app. If you are in the EU or UK, you can also complain to your data protection authority.",
    ]),
    ("Changes", [
        "If this policy changes, we will update this page and the date above. If the app ever starts collecting data, we will say so here and in the App Store before it does.",
    ]),
]

HEALTH = [
    ("Consumer Health Data Privacy Policy", [
        "This page is written for laws such as the Washington My Health My Data Act and Nevada SB 370. The short answer: Tenua does not collect, share or sell consumer health data.",
    ]),
    ("What health data the app handles", [
        "Headache attacks, symptoms, medicines and doses, sleep, period days, day summaries and air pressure around attacks. All of it is processed and stored on your iPhone. We, the developer, never receive it.",
    ]),
    ("Sources", [
        "What you enter yourself; Apple Health, if you connect it; Apple Weather for air pressure, if you choose a city (only the city's coordinates are sent, see the Privacy Policy).",
    ]),
    ("Sharing and selling", [
        "We don't share consumer health data with anyone and don't sell it. Files you share yourself (a report for your doctor, a CSV, a backup) go where you send them.",
    ]),
    ("Your rights", [
        "You can see, export and delete all your data in the app (Settings → Your data, or by deleting the app). As we hold none of it, a request to us can only cover emails you sent. Write to the address below.",
    ]),
]

TERMS = [
    ("Licence", [
        "Tenua is licensed under Apple's Standard Licensed Application End User License Agreement: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/",
    ]),
    ("Not medical advice", [
        "Tenua is a diary. It does not diagnose, predict, prevent or treat any condition and does not replace advice from a doctor. Numbers such as medicine days and their reference values come from published sources (ICHD-3) and describe your entries only. Don't start, stop or change any medicine without talking to your doctor. In an emergency, call your local emergency number.",
    ]),
    ("Patterns", [
        "Patterns shown in the app describe your own entries. They don't show what causes your headaches.",
    ]),
    ("Subscriptions", [
        "Tenua Pro is offered as a yearly or monthly auto-renewing subscription, or as a one-time lifetime purchase. Prices are shown in the app before you buy. Payment is charged to your Apple ID. A subscription renews unless cancelled at least 24 hours before the end of the period; you can manage or cancel it in iPhone Settings → your name → Subscriptions. A free trial, if offered, ends when you buy a subscription. Everything that is free when you install Tenua stays free.",
    ]),
]

SUPPORT = [
    ("Restore a purchase", [
        "Open Tenua, go to Settings → Tenua Pro → Restore purchases, signed in with the Apple ID you used to buy.",
    ]),
    ("Cancel a subscription", [
        "In Tenua: Settings → Tenua Pro → Manage subscription. Or in iPhone Settings → your name → Subscriptions → Tenua. Cancel at least 24 hours before the end of the period. Tenua reminds you two days before a free trial ends, if notifications are allowed.",
    ]),
    ("Refunds", [
        "Refunds are handled by Apple: https://reportaproblem.apple.com",
    ]),
    ("Where your diary is kept", [
        "Only on your iPhone. We keep no copy, so we can't restore a deleted diary. Make a backup file in Settings → Your data → Back up to a file, and keep it in Files or iCloud Drive.",
    ]),
    ("The “It hurts” button outside the app", [
        "Add the Tenua widget to your Home Screen or Lock Screen, or add the “It hurts” control to Control Center or the Action Button. You can also say “Log a headache in Tenua” to Siri.",
    ]),
    ("“In your own words” is missing", [
        "It needs an iPhone with Apple Intelligence turned on. Without it, logging works the same with the buttons.",
    ]),
]


def e(s):
    return html.escape(s, quote=False)


def link(s):
    out = []
    for word in e(s).split(" "):
        if word.startswith("https://"):
            url = word.rstrip(".,;)")
            out.append(f'<a href="{url}">{url}</a>{word[len(url):]}')
        else:
            out.append(word)
    return " ".join(out)


PAGES = {
    "privacy": ("Privacy Policy", PRIVACY),
    "health-data": ("Consumer Health Data Privacy Policy", HEALTH),
    "terms": ("Terms of Use", TERMS),
    "support": ("Support", SUPPORT),
}


def page(kind):
    title, sections = PAGES[kind]
    parts = [f"<h1>{title}</h1>", f"<p><em>Last updated: {UPDATED}. App: Tenua: Migraine Tracker (iOS). Developer: {e(DEV)}.</em></p>"]
    if kind == "support":
        parts.append(f'<p>Questions, problems or ideas: <a href="mailto:{EMAIL}">{EMAIL}</a>. We read every message.</p>')
    for h, paras in sections:
        if h == title:
            parts.extend(f"<p>{link(p)}</p>" for p in paras)
            continue
        parts.append(f"<h2>{e(h)}</h2>")
        if h == "The short version":
            parts.append("<ul>" + "".join(f"<li>{link(p)}</li>" for p in paras) + "</ul>")
        else:
            parts.extend(f"<p>{link(p)}</p>" for p in paras)
    parts.append(f'<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{APP}: {title}</title><meta name="robots" content="index,follow"><style>{CSS}</style></head><body>
<header><div class="in"><h1>{APP}</h1><p>Migraine &amp; headache diary · {e(DEV)}</p></div></header>
<main>{''.join(parts)}</main>
<footer><a href="privacy.html">Privacy</a> · <a href="health-data.html">Health data</a> · <a href="terms.html">Terms</a> · <a href="support.html">Support</a><br>© 2026 {e(DEV)}</footer></body></html>"""
    with open(os.path.join(os.path.dirname(__file__) or ".", f"{kind}.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print("built", f"{kind}.html")


if __name__ == "__main__":
    for k in PAGES:
        page(k)
