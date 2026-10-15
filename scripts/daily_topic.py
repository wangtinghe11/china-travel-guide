#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily content generator state manager for the China Travel Guide site.

Picks the next un-written topic from a prioritized pool, so the daily cron job
never duplicates an article. Records published topics in a JSON state file.

Usage:
    python3 scripts/daily_topic.py next      # print the next topic (slug|title|keywords)
    python3 scripts/daily_topic.py done <slug>  # mark slug as written
    python3 scripts/daily_topic.py status    # show remaining/used counts
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "scripts", "daily_topic_state.json")
ARTICLES = os.path.join(ROOT, "src", "content", "articles")

# Prioritized topic pool. Each entry: slug | title | category | primary keywords
# Front-loaded with high-search-volume evergreen queries the site doesn't cover yet.
TOPICS = [
    # --- Visa & entry (evergreen, high volume) ---
    ("china-visa-free-transit-240-hours", "China's 240-Hour Visa-Free Transit: Who Qualifies and How", "visa",
     "240 hour visa free transit china, visa free china 10 days"),
    ("china-tourist-visa-application-guide", "China Tourist Visa (L Visa) Application Guide 2026", "visa",
     "china tourist visa application, l visa china requirements"),
    ("china-visa-on-arrival-cities", "China Visa on Arrival: Cities, Eligibility, and Rules", "visa",
     "china visa on arrival, port visa china"),
    ("hk-macau-visa-free-china-entry", "Entering China from Hong Kong or Macau: Visa Rules", "visa",
     "hong kong to china visa, macau china entry"),
    # --- Payments & money ---
    ("alipay-for-tourists-setup-guide", "How to Set Up Alipay for Tourists (Step by Step)", "payment",
     "alipay for tourists, alipay setup foreign card"),
    ("wechat-pay-tourists-guide", "WeChat Pay for Tourists: Link Your Card and Pay Like a Local", "payment",
     "wechat pay for tourists, wechat pay foreign card"),
    ("cash-vs-digital-payment-china", "Cash vs Digital Payments in China: What Actually Works in 2026", "payment",
     "cash in china, digital payment china tourists"),
    ("china-currency-exchange-atm-guide", "Getting Cash in China: ATMs, Exchange, and Fees", "payment",
     "currency exchange china, atm china foreign card"),
    ("tipping-in-china-guide", "Tipping in China: When, Where, and How Much", "payment",
     "tipping in china, do you tip in china"),
    # --- Transport ---
    ("china-train-ticket-booking-guide", "How to Book China Train Tickets as a Foreigner (12306 Guide)", "transport",
     "china train tickets, 12306 booking foreigner"),
    ("china-domestic-flights-guide", "Domestic Flights in China: Booking, Airports, and Tips", "transport",
     "domestic flights china, china airlines booking"),
    ("didi-china-guide-foreigners", "Using Didi in China: The Foreigner's Complete Guide", "transport",
     "didi china, didi foreigner guide"),
    ("china-metro-subway-guide", "China's Metro Systems: How to Ride Like a Local", "transport",
     "china metro, china subway guide"),
    ("china-airport-transfer-guide", "Airport Transfers in China: Taxis, Trains, and Apps", "transport",
     "china airport transfer, beijing airport to city"),
    ("china-high-speed-rail-vs-flights", "High-Speed Rail vs Flights in China: Which to Choose", "transport",
     "china train vs flight, high speed rail or plane china"),
    # --- Connectivity & tech ---
    ("best-vpn-for-china-guide", "Best VPN for China 2026: What Works and What Doesn't", "sim",
     "best vpn china, vpn for china travel"),
    ("china-apps-you-need-guide", "The Only Apps You Need for China Travel", "sim",
     "apps for china travel, essential china apps"),
    ("google-maps-in-china-alternatives", "Google Maps Doesn't Work in China: What to Use Instead", "sim",
     "google maps china, china map app"),
    # --- Practical / culture ---
    ("chinese-phrases-for-travelers", "Essential Chinese Phrases for Travelers (with Pronunciation)", "guide",
     "chinese phrases for travel, basic mandarin travel"),
    ("china-sim-card-buying-guide", "Buying a SIM Card in China: Airports, Stores, and Prices", "sim",
     "china sim card, buy sim card china"),
    ("china-plug-adapter-voltage-guide", "China Power Plugs and Voltage: What Adapter You Need", "guide",
     "china plug adapter, china voltage"),
    ("china-travel-insurance-guide", "Travel Insurance for China: What You Need to Know", "guide",
     "china travel insurance, insurance for china trip"),
    ("china-travel-with-kids-guide", "Traveling to China with Kids: A Family Guide", "guide",
     "china with kids, family travel china"),
    ("china-travel-budget-guide", "How Much Does a China Trip Cost? Budget Breakdown 2026", "guide",
     "china travel cost, china trip budget"),
    ("best-time-to-visit-china", "Best Time to Visit China: Month-by-Month Guide", "guide",
     "best time visit china, china weather by month"),
    ("china-travel-etiquette-tips", "China Travel Etiquette: Do's and Don'ts", "guide",
     "china etiquette, chinese customs travelers"),
    ("china-food-safety-guide", "Eating in China: Food Safety and What to Try", "guide",
     "china food safety, what to eat china"),
    ("china-solo-female-travel-guide", "Solo Female Travel in China: Safety and Tips", "guide",
     "solo female travel china, china safe for women"),
    ("china-tourist-scams-guide", "Common Tourist Scams in China and How to Avoid Them", "guide",
     "china scams, tourist scams china"),
    ("china-language-translation-apps", "Translation Apps for China: Bridging the Language Gap", "sim",
     "translation app china, chinese translator app"),
    ("china-temple-etiquette-guide", "Visiting Chinese Temples: Etiquette and Meaning", "guide",
     "chinese temple etiquette, temple visit china"),
    ("china-panda-guide", "Seeing Pandas in China: Chengdu and Beyond", "guide",
     "see pandas china, chengdu panda base"),
    ("china-great-wall-guide", "The Great Wall of China: Sections, Tickets, and Tips", "guide",
     "great wall of china, mutianyu badaling great wall"),
    ("china-train-station-guide", "Navigating Chinese Train Stations: A Survival Guide", "transport",
     "china train station guide, chinese railway station"),
    ("china-weather-packing-guide", "What to Pack for China: Seasonal Packing List", "guide",
     "packing list china, what to wear china"),
    ("china-internet-censorship-explained", "The Great Firewall Explained for Travelers", "sim",
     "great firewall china, china internet censorship"),
]


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {"done": [], "started": None}


def save_state(state):
    with open(STATE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    state = load_state()
    done = set(state.get("done", []))

    if cmd == "next":
        for slug, title, cat, kw in TOPICS:
            if slug in done:
                continue
            if os.path.exists(os.path.join(ARTICLES, f"{slug}.md")):
                continue
            print(f"{slug}|{title}|{cat}|{kw}")
            return 0
        print("EXHAUSTED")
        return 0

    if cmd == "done":
        if len(sys.argv) < 3:
            print("usage: daily_topic.py done <slug>")
            return 1
        slug = sys.argv[2]
        if slug not in done:
            done.add(slug)
            state["done"] = sorted(done)
            state["started"] = state.get("started")
            save_state(state)
        print(f"marked done: {slug} (total {len(done)})")
        return 0

    if cmd == "status":
        remaining = [s for s, *_ in TOPICS if s not in done
                     and not os.path.exists(os.path.join(ARTICLES, f"{s}.md"))]
        print(f"pool total: {len(TOPICS)} | done: {len(done)} | remaining: {len(remaining)}")
        print("next 5:")
        for s in remaining[:5]:
            print("  ", s)
        return 0

    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
