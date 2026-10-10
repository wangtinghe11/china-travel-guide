# China Travel Guide — Site Configuration
# English-language China travel guide for Western tourists (visa-free cities).
# Edit this file to add cities, guides, or articles. Then run: python3 build_site.py

SITE = {
    "name": "China Travel Guide",
    "tagline": "Deep, practical guides to China's visa-free cities — written for Western travelers.",
    "url": "https://chinatravelguide.example.com",  # TODO: replace with real domain
    "description": "Deep, practical travel guides to China's visa-free cities: Beijing, Shanghai, Xi'an, Chengdu, Chongqing, Guangzhou, Shenzhen, Hangzhou, Guilin, Zhangjiajie. Visas, payments, high-speed rail, eSIM, safety.",
    "language": "en",
    "locale": "en_US",
    "author": "China Travel Guide Editorial Team",
    "publisher": "China Travel Guide",
    "logo": "/static/img/logo.svg",
    "social": {
        "twitter": "@chinatravelguide",
        "facebook": "chinatravelguide",
    },
}

# 10 visa-free cities (first batch)
CITIES = [
    {
        "slug": "beijing",
        "name": "Beijing",
        "cn_name": "北京",
        "tagline": "Imperial capital: Forbidden City, Great Wall, hutongs",
        "intro": "China's political and cultural heart. Start with the Forbidden City and Great Wall, then get lost in the hutongs.",
        "keywords": "Beijing travel guide, Beijing visa free, Great Wall, Forbidden City, Beijing itinerary",
        "hero": "forbidden-city",
        "featured": True,
    },
    {
        "slug": "shanghai",
        "name": "Shanghai",
        "cn_name": "上海",
        "tagline": "Cosmopolitan skyline: Bund, Yu Garden, French Concession",
        "intro": "China's most international city — art-deco Bund, futuristic Pudong, leafy former French Concession.",
        "keywords": "Shanghai travel guide, Shanghai visa free, Bund, Yu Garden, Shanghai itinerary",
        "hero": "bund",
        "featured": True,
    },
    {
        "slug": "xian",
        "name": "Xi'an",
        "cn_name": "西安",
        "tagline": "Ancient capital: Terracotta Army, city walls, Muslim Quarter",
        "intro": "Start of the Silk Road and home of the Terracotta Army. Ride a bike on the best-preserved city wall in China.",
        "keywords": "Xi'an travel guide, Xi'an visa free, Terracotta Army, Xi'an city wall, Muslim Quarter",
        "hero": "terracotta",
        "featured": True,
    },
    {
        "slug": "chengdu",
        "name": "Chengdu",
        "cn_name": "成都",
        "tagline": "Panda capital: giant pandas, teahouses, Sichuan food",
        "intro": "Home of giant pandas, slow teahouse culture, and the world's best Sichuan food. A city that knows how to relax.",
        "keywords": "Chengdu travel guide, Chengdu visa free, pandas, Sichuan food, teahouse",
        "hero": "panda",
        "featured": True,
    },
    {
        "slug": "chongqing",
        "name": "Chongqing",
        "cn_name": "重庆",
        "tagline": "Mountain city: cyberpunk skyline, hotpot, Yangtze",
        "intro": "A vertical megacity of neon, bridges and hotpot. The Yangtze River cruise starts here.",
        "keywords": "Chongqing travel guide, Chongqing visa free, hotpot, Yangtze cruise, Hongya Cave",
        "hero": "hongya",
        "featured": True,
    },
    {
        "slug": "guangzhou",
        "name": "Guangzhou",
        "cn_name": "广州",
        "tagline": "Canton: dim sum, Canton Tower, Pearl River",
        "intro": "Southern China's trading hub — legendary dim sum, the Canton Tower, and the Pearl River at night.",
        "keywords": "Guangzhou travel guide, Guangzhou visa free, dim sum, Canton Tower, Pearl River",
        "hero": "canton-tower",
        "featured": True,
    },
    {
        "slug": "shenzhen",
        "name": "Shenzhen",
        "cn_name": "深圳",
        "tagline": "Tech city: futuristic skyline, theme parks, border with HK",
        "intro": "From fishing village to tech metropolis in 40 years. Futuristic skyline, great parks, and a day-trip gateway to Hong Kong.",
        "keywords": "Shenzhen travel guide, Shenzhen visa free, tech city, Window of the World, Hong Kong day trip",
        "hero": "shenzhen",
        "featured": True,
    },
    {
        "slug": "hangzhou",
        "name": "Hangzhou",
        "cn_name": "杭州",
        "tagline": "West Lake: tea fields, pagodas, Marco Polo's favorite",
        "intro": "Marco Polo called it the finest city in the world. West Lake, Longjing tea fields, and quiet temples.",
        "keywords": "Hangzhou travel guide, Hangzhou visa free, West Lake, Longjing tea, Lingyin Temple",
        "hero": "west-lake",
        "featured": True,
    },
    {
        "slug": "guilin",
        "name": "Guilin",
        "cn_name": "桂林",
        "tagline": "Karst peaks: Li River, rice terraces, countryside",
        "intro": "The postcard landscape of China — limestone karst peaks, the Li River cruise, and the Longji rice terraces.",
        "keywords": "Guilin travel guide, Guilin visa free, Li River, Longji rice terraces, karst",
        "hero": "li-river",
        "featured": True,
    },
    {
        "slug": "zhangjiajie",
        "name": "Zhangjiajie",
        "cn_name": "张家界",
        "tagline": "Avatar mountains: sandstone pillars, glass bridge, national park",
        "intro": "The floating mountains that inspired Avatar. Glass bridges, cable cars, and the world's tallest outdoor elevator.",
        "keywords": "Zhangjiajie travel guide, Zhangjiajie visa free, Avatar mountains, glass bridge, national forest park",
        "hero": "avatar",
        "featured": True,
    },
]

# Practical guides (pain-point keywords, independent of cities)
GUIDES = [
    {
        "slug": "visa-free-china",
        "title": "China Visa-Free Entry 2026: Complete Guide for Western Travelers",
        "short_title": "Visa-Free Entry",
        "description": "Which nationalities can enter China visa-free, for how long, and the exact rules at immigration. Updated for 2026.",
        "keywords": "China visa free 2026, China visa free countries, 240 hour transit, China visa policy",
        "icon": "passport",
        "order": 1,
    },
    {
        "slug": "payments-in-china",
        "title": "How to Pay in China: Alipay, WeChat Pay & Cash for Foreigners",
        "short_title": "Payments",
        "description": "China is nearly cashless. Set up Alipay and WeChat Pay with a foreign card, and know when cash still matters.",
        "keywords": "Alipay foreign card, WeChat Pay setup, pay in China, China cashless, foreigner payment China",
        "icon": "card",
        "order": 2,
    },
    {
        "slug": "high-speed-rail-china",
        "title": "China High-Speed Rail: How to Book Tickets & Ride the Trains",
        "short_title": "High-Speed Rail",
        "description": "The world's largest high-speed rail network. How to book with a passport, read a ticket, and ride like a local.",
        "keywords": "China high speed rail, book train tickets China, 12306, China bullet train, G train",
        "icon": "train",
        "order": 3,
    },
    {
        "slug": "esim-china",
        "title": "eSIM & Internet in China: Stay Connected Without a VPN Headache",
        "short_title": "eSIM & Internet",
        "description": "Google, WhatsApp and Instagram are blocked. Here's how to stay connected with an eSIM, VPN, and offline maps.",
        "keywords": "China eSIM, internet in China, VPN China, Google blocked China, best eSIM China",
        "icon": "wifi",
        "order": 4,
    },
    {
        "slug": "safety-in-china",
        "title": "Is China Safe for Tourists? Practical Safety Guide 2026",
        "short_title": "Safety",
        "description": "China is one of the safest countries for tourists. What to watch for, scams to avoid, and emergency numbers.",
        "keywords": "China safety, China scams, China emergency number, is China safe for tourists",
        "icon": "shield",
        "order": 5,
    },
]

# Article template sections (used by the article template and content checklist)
ARTICLE_SECTIONS = [
    "overview",
    "getting-there",
    "getting-around",
    "where-to-stay",
    "what-to-see",
    "food-and-drink",
    "itineraries",
    "practical-tips",
    "faq",
]

# Ad slots: article top / middle / bottom + sidebar. Placeholders only (not enabled).
AD_SLOTS = {
    "article_top": {"enabled": False, "label": "Ad slot — article top"},
    "article_middle": {"enabled": False, "label": "Ad slot — article middle"},
    "article_bottom": {"enabled": False, "label": "Ad slot — article bottom"},
    "sidebar": {"enabled": False, "label": "Ad slot — sidebar"},
}

# Affiliate link placeholders (Booking / Agoda / Klook). Not enabled yet.
AFFILIATE = {
    "enabled": False,
    "booking": {"label": "Booking.com", "url": "https://www.booking.com/"},
    "agoda": {"label": "Agoda", "url": "https://www.agoda.com/"},
    "klook": {"label": "Klook", "url": "https://www.klook.com/"},
}
