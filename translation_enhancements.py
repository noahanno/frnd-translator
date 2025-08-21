# COMBINED TRANSLATION ENHANCEMENTS - All 3 Layers + Team Training
# This file contains all translation quality patterns and can be updated daily
# without modifying the main app.py file

import re

# -------------------- LAYER 1: MEETING & LIVE SESSION PATTERNS -------------------- #

# Training patterns extracted from your Google Sheet examples
QUALITY_TRAINING_PATTERNS = {
    "hindi": {
        "preferred_mixing": [
            ("meeting", "meeting"), ("join", "join karo"), ("live", "LIVE"), ("tips", "tips"),
            ("call", "call"), ("earnings", "earnings"), ("update", "update"), ("session", "session"),
        ],
        "natural_connectors": [
            ("We're", "Hum"), ("Let's talk about", "Chalo baat karte hain"),
            ("Join now", "Abhi join karo"), ("Don't miss", "Miss mat karna"),
            ("Click & Join", "Click karo aur join karo"),
        ],
        "emotional_expressions": [
            ("awesome", "awesome"), ("amazing", "amazing"), ("super", "super"),
            ("really help", "bohot kaam aayega"),
        ]
    },
    "tamil": {
        "preferred_mixing": [
            ("meeting", "meeting"), ("live", "LIVE"), ("tips", "tips"), ("call", "call"),
            ("join", "join பண்ணுங்க"), ("miss", "miss பண்ணாதீங்க"), ("update", "update"), ("session", "session"),
        ],
        "natural_connectors": [
            ("We're", "நாங்க"), ("Let's talk", "பேசலாம்"), ("Join now", "இப்போவே join பண்ணுங்க"),
            ("Don't miss", "miss பண்ணாதீங்க"), ("Click & Join", "Click பண்ணி join பண்ணுங்க"),
        ],
        "emotional_expressions": [
            ("awesome", "awesome ஆக்கிச்சு"), ("amazing", "அருமையா"), ("super", "super"),
            ("really help", "definitely உங்களுக்கு help ஆகும்"),
        ]
    },
    "telugu": {
        "preferred_mixing": [
            ("meeting", "meeting"), ("live", "LIVE"), ("tips", "tips"), ("call", "call"),
            ("join", "join avvandi"), ("miss", "miss avvakandi"), ("update", "update"),
        ],
        "natural_connectors": [
            ("We're", "Manam"), ("Let's talk", "Maatladukundam"),
            ("Join now", "Ipude join avvandi"), ("Don't miss", "Miss avvakandi"),
        ],
        "emotional_expressions": [
            ("awesome", "awesome"), ("amazing", "chala baagundi"), ("super", "super"),
            ("really help", "chala useful ga untundi"),
        ]
    },
    "malayalam": {
        "preferred_mixing": [
            ("meeting", "മീറ്റിംഗ്"), ("live", "LIVE"), ("tips", "ടിപ്സ്"), ("call", "കോൾ"),
            ("join", "ജോയിൻ ചെയ്യൂ"), ("update", "അപ്ഡേറ്റ്"), ("tap", "ടാപ്പ് ചെയ്യൂ"),
        ],
        "natural_connectors": [
            ("We're", "ഞങ്ങൾ"), ("Let's talk", "നമുക്ക് സംസാരിക്കാം"),
            ("Join now", "ഇപ്പോൾ ജോയിൻ ചെയ്യൂ"), ("Don't miss", "നഷ്ടപ്പെടുത്തരുത്"),
            ("right now", "ഇപ്പോൾ തന്നെ"), ("Tap to join", "ജോയിൻ ചെയ്യാൻ ടാപ്പ് ചെയ്യൂ"),
        ],
        "meeting_specific": [
            ("FRND Meeting", "FRND മീറ്റിംഗ്"), ("is LIVE", "LIVE ആണ്"), ("happening now", "ഇപ്പോൾ നടക്കുന്നു"),
            ("Jump in now", "ഇപ്പോൾ തന്നെ ചേരൂ"), ("from call tips to earnings", "കോൾ ടിപ്സ് മുതൽ എർണിങ്സ് വരെ"),
        ]
    },
    "kannada": {
        "preferred_mixing": [
            ("meeting", "ಮೀಟಿಂಗ್"), ("live", "LIVE"), ("tips", "ಸಲಹೆಗಳು"), ("call", "ಕರೆ"),
            ("join", "ಸೇರಿ"), ("update", "ಅಪ್ಡೇಟ್"), ("channel", "ಚಾನೆಲ್"),
        ],
        "natural_connectors": [
            ("We're", "ನಾವು"), ("Let's talk", "ಮಾತನಾಡೋಣ"),
            ("Join now", "ಈಗಲೇ ಸೇರಿ"), ("Don't miss", "ತಪ್ಪಿಸಿಕೊಳ್ಳಬೇಡಿ"),
            ("Hi [Name]", "ನಮಸ್ಕಾರ [Name]"), ("guess what", "ಗೆಸ್ ಮಾಡಿ"),
        ],
        "whatsapp_specific": [
            ("WhatsApp Channel", "WhatsApp ಚಾನೆಲ್"), ("special invite list", "ಸ್ಪೆಷಲ್ ಲಿಸ್ಟ್"),
            ("completely free", "ಫ್ರೀ ಆಗಿದೆ"), ("numbers will not be visible", "ಫೋನ್ ನಂಬರ್ ಪ್ರೈವೇಟ್ ಆಗಿರುತ್ತೆ"),
            ("Join Channel", "ಜಾಯಿನ್ ಚಾನೆಲ್"), ("tap on follow", "ಫಾಲೋ ಮಾಡಿ"),
        ]
    }
}

# -------------------- LAYER 2: WHATSAPP CHANNEL & PRIVACY PATTERNS -------------------- #

ADDITIONAL_QUALITY_PATTERNS = {
    "hindi": {
        "whatsapp_patterns": [
            ("WhatsApp Channel", "WhatsApp Channel"), ("join now", "abhi join karo"),
            ("click to join", "click karke join karo"), ("all tips", "saare tips"),
            ("pro tips", "pro tips"), ("100% Private", "100% Private"), ("Number Privacy", "Number Privacy"),
        ],
        "earnings_patterns": [
            ("₹40K/month", "mahine ka ₹40K"), ("big earnings", "achhi kamai"),
            ("earn smarter", "kamao smarter"), ("small earnings", "kam earnings"),
            ("more money", "zyada kamaai"), ("start earning", "kamai shuru karo"),
        ],
        "casual_connectors": [
            ("Hey!", "Hey!"), ("Tired of", "thak gaye hoge na"), ("Let's fix that", "Chinta mat karo"),
            ("ready to level up", "ready for level up"), ("You're not alone", "Don't worry, hum hai na"),
            ("New here?", "Naye ho?"),
        ],
        "app_tech_terms": [
            ("audio & video calls", "audio & video calls"), ("badge", "badge"), ("level up", "level up"),
            ("go online", "online jao"), ("tap here", "tap karo"), ("click here", "click karo"),
        ]
    },
    "tamil": {
        "whatsapp_patterns": [
            ("WhatsApp Channel", "WhatsApp Channel"), ("join now", "இப்போவே join பண்ணுங்க"),
            ("click to join", "Click பண்ணி join பண்ணுங்க"), ("all tips", "எல்லா tips-உம்"),
            ("pro tips", "pro tips"), ("100% Private", "100% Private & Safe"),
            ("Number Privacy", "Number Privacy assured"),
        ],
        "earnings_patterns": [
            ("₹40K/month", "₹40K/month"), ("big earnings", "பெரிய income"),
            ("earn smarter", "smarter earn பண்ண"), ("small earnings", "கம்மி earnings"),
            ("more money", "more money"), ("start earning", "earn பண்ண ஆரம்பிக்கலாம்"),
        ],
        "casual_connectors": [
            ("Hey!", "Hey!"), ("Tired of", "bore ஆகிட்டீங்களா"), ("Let's fix that", "இப்போ fix பண்ணலாம்"),
            ("ready to level up", "next level போக தயாரா"), ("You're not alone", "நீங்கள் தனியா இல்ல"),
            ("New here?", "இது உங்க first time-a?"),
        ],
        "app_tech_terms": [
            ("audio & video calls", "Audio & Video calls"), ("badge", "Badge"), ("level up", "level up"),
            ("go online", "Go Online போங்க"), ("tap here", "இங்கே tap பண்ணுங்க"),
        ]
    },
    "telugu": {
        "whatsapp_patterns": [
            ("WhatsApp Channel", "WhatsApp Channel"), ("join now", "ipude join avvandi"),
            ("click to join", "Click chesi join avvandi"), ("all tips", "All tips"), ("100% Private", "100% Private"),
        ],
        "earnings_patterns": [
            ("₹40K/month", "₹40K/month"), ("start earning", "earning start cheyyali"), ("level up", "level up"),
        ],
        "casual_connectors": [
            ("New here?", "App ki new ah?"), ("ready to level up", "ready to level up?"), ("few days", "Few days aiyayi kadha"),
        ],
        "app_tech_terms": [
            ("go online", "online vellandi"), ("audio & video calls", "audio & video calls"), ("badge", "badge"),
        ]
    },
    "malayalam": {
        "whatsapp_patterns": [
            ("WhatsApp Channel", "WhatsApp ചാനൽ"), ("join now", "ഇപ്പോൾ ജോയിൻ ചെയ്യൂ"),
            ("click to join", "ജോയിൻ ചെയ്യാൻ ക്ലിക്ക് ചെയ്യൂ"), ("all tips", "എല്ലാ ടിപ്പുകളും"),
            ("pro tips", "പ്രൊ ടിപ്പുകൾ"), ("100% Private", "100% സ്വകാര്യവും സുരക്ഷിതവുമാണ്"),
            ("special invite list", "സ്പെഷ്യൽ ഇൻവൈറ്റ് ലിസ്റ്റ്"), ("brand-new", "പുതിയ"),
            ("completely free", "പൂർണ്ണമായും സൗജന്യം"), ("numbers will not be visible", "നമ്പർ മറ്റാരും കാണില്ല"),
        ],
        "earnings_patterns": [
            ("₹40K/month", "മാസം 40K"), ("big earnings", "വലിയ വരുമാനം"),
            ("small earnings", "ചെറിയ വരുമാനം"), ("start earning", "സമ്പാദിക്കാൻ ആരംഭിക്കാം"),
        ],
        "casual_connectors": [
            ("New here?", "പുതിയ ആളാണോ?"), ("You're not alone", "നിങ്ങൾ ഒറ്റയ്ക്കല്ല"),
            ("ready to level up", "ലെവൽ അപ്പ് ചെയ്യണ്ടേ"), ("Hi [Name]", "നമസ്കാരം [പേര്]"),
            ("guess what", "ഒന്ന് Guess ചെയാമോ"), ("and guess what", "ഒന്ന് Guess ചെയാമോ"),
        ],
        "channel_specific": [
            ("Be the first to know", "ആദ്യം അറിയാം"), ("Learn simple ways", "എളുപ്പ മാർഗങ്ങൾ പഠിക്കാം"),
            ("Get news on", "വാർത്തകൾ അറിയാം"), ("discounts", "ഓഫറുകളുടെ വിവരങ്ങൾ"),
            ("favourite trainer", "ഇഷ്ടപ്പെട്ട ട്രെയിനർ"), ("connect with", "കണക്റ്റ് ചെയ്യാൻ"),
            ("surprise rewards", "സർപ്രൈസ് സമ്മാനങ്ങൾ"), ("dont forget to tap on follow", "Follow അമർത്താൻ മറക്കരുത്"),
            ("never miss anything fun", "ഒരിക്കലും ഫൺ മിസ്സ് ആവില്ല"),
        ]
    },
    "kannada": {
        "whatsapp_patterns": [
            ("WhatsApp Channel", "WhatsApp ಚಾನಲ್"), ("join now", "ಈಗಲೇ ಸೇರಿ"),
            ("all tips", "ಎಲ್ಲಾ ಟಿಪ್ಸ್"), ("pro tips", "ಪ್ರೊ ಟಿಪ್ ಗಳು"), ("100% Private", "100% ಪ್ರೈವೇಟ್"),
            ("brand-new", "ಹೊಚ್ಚ ಹೊಸ"), ("special invite list", "ಸ್ಪೆಷಲ್ ಲಿಸ್ಟ್"),
            ("completely free", "ಫ್ರೀ"), ("numbers will not be visible", "ನಂಬರ್ ಪ್ರೈವೇಟ್ ಆಗಿರುತ್ತೆ"),
        ],
        "earnings_patterns": [
            ("₹40K/month", "ತಿಂಗಳಿಗೆ ₹40K"), ("small earnings", "ಸಣ್ಣ ಗಳಿಕೆ"), ("start earning", "ಗಳಿಸಲು ಪ್ರಾರಂಭಿಸಿ"),
        ],
        "casual_connectors": [
            ("New here?", "ಇಲ್ಲಿ ಹೊಸಬರೇ?"), ("You're not alone", "ನೀವು ಒಬ್ಬಂಟಿಯಲ್ಲ"),
            ("ready to level up", "ಮುಂದಿನ ಹಂತಕ್ಕೆ ಹೋಗಲು ಸಿದ್ಧರಿದ್ದೀರಾ"),
            ("guess what", "ಗೆಸ್ಸ್ ಮಾಡಿ"), ("Hi [Name]", "ನಮಸ್ಕಾರ [Name]"),
        ],
        "channel_specific": [
            ("Be the first to know", "ಫಸ್ಟ್ ಆಗಿ ತಿಳಿಯಿರಿ"), ("Learn simple ways", "ಸರಳ ಮಾರ್ಗಗಳನ್ನು ತಿಳಿಯಿರಿ"),
            ("Get news on", "ನ್ಯೂಸ್ ತಿಳಿಯಿರಿ"), ("discounts", "ಡಿಸ್ಕೌಂಟ್ಸ್"),
            ("favourite trainer", "ಟ್ರೈನರ್ಸ್"), ("connect with", "ಕನೆಕ್ಟ್ ಆಗುವಾಕ್ಕ್"),
            ("surprise rewards", "ಸುಪ್ರಿಸೆ ಗಾಲ"), ("dont forget to tap on follow", "ಫಾಲೋ ಮಾಡೋದನ್ನ ಮರೀಬೇಡಿ"),
            ("never miss anything fun", "ಮಜಾ ಯಾವತ್ತೂ ಮಿಸ್ ಆಗೋದು ಇಲ್ಲ"), ("that simple", "ಇಷ್ಟು ಸಿಂಪಲ್"),
        ]
    }
}

# -------------------- LAYER 3: FESTIVAL & HOLIDAY PATTERNS -------------------- #

FESTIVAL_QUALITY_PATTERNS = {
    "hindi": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "Raksha Bandhan"), ("Rakhi", "Rakhi"), ("your brother", "apne bhai ko"),
            ("Gift Your Bhai", "Apne Bhai ko do"), ("Protection", "Protection"),
            ("₹1000 Hamper", "₹1000 ka Hamper"), ("₹1000 Gift", "₹1000 ka Gift"),
        ],
        "holiday_patterns": [
            ("Holiday", "Holiday"), ("It's a holiday", "Aaj chhutti hai"), ("Holiday =", "Holiday ="),
            ("time to earn", "kamaane ka time"), ("peak time", "peak time"), ("long weekend", "lamba weekend"),
            ("Good Morning", "Good Morning"), ("Happy Raksha Bandhan", "Happy Raksha Bandhan"),
        ],
        "gift_earning_patterns": [
            ("Just by being online", "Sirf Online aakar"), ("earn real money", "kamao real money"),
            ("in your wallet", "apne wallet mein"), ("More time = More", "Jitna zyada time = Utne zyada"),
            ("Make this Rakhi extra special", "Iss Rakhi ko banao extra special"),
            ("Your time = Your earnings", "Tumhara time = Tumhari earning"),
        ],
        "encouragement_patterns": [
            ("Tonight's the Night", "Aaj ki raat hai khaas"), ("Beautiful!", "Beautiful!"),
            ("Don't miss out", "Miss mat karo"), ("Why wait?", "Toh phir rukna kyu?"),
            ("Go online now", "Abhi online jao"), ("Let the spotlight find YOU", "spotlight aap tak khud aa jaayegi"),
        ]
    },
    "tamil": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "Raksha Bandhan"), ("Rakhi", "Rakhi"), ("your brother", "உங்க அண்ணன்/தம்பிக்கு"),
            ("₹1000 Gift", "₹1000 Gift"), ("₹1000 Hamper", "₹1000 Gift"), ("Protection", "பாதுகாப்பு"),
        ],
        "holiday_patterns": [
            ("Holiday", "Holiday"), ("It's a holiday", "இன்று விடுமுறை"), ("Holiday =", "Holiday ="),
            ("time to earn", "earn பண்ண நேரம்"), ("peak time", "Peak Time"),
            ("Good Morning", "Good Morning"), ("Happy Raksha Bandhan", "Happy Raksha Bandhan"),
        ],
        "gift_earning_patterns": [
            ("Just by being online", "FRND-ல Onlineல இருந்தாலே போதும்"), ("earn real money", "நேரடி பணம் சேரும்"),
            ("in your wallet", "Wallet-ல"), ("More time = More", "அதிக நேரம் = அதிக"),
            ("Make this Rakhi extra special", "இந்த Rakhi-யை Special-aa ஆக்குங்க"),
            ("Your time = Your earnings", "உங்க நேரம் = உங்க சம்பாதிப்பு"),
        ],
        "encouragement_patterns": [
            ("Tonight's the Night", "இன்று இரவு தான் உங்களுக்கு வாய்ப்பு"), ("Beautiful!", "Beautiful!"),
            ("Don't miss out", "Miss பண்ணாதீங்க"), ("Why wait?", "Why Wait?"),
            ("Go online now", "இப்போதே Online போங்க"), ("Let the spotlight find YOU", "உங்களை spotlight find பண்ண விடுங்க"),
        ]
    },
    "telugu": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "Raksha Bandhan"), ("your brother", "మీ బ్రదర్ కి"),
            ("₹1000 Hamper", "₹1000 హ్యాంపర్"), ("Protection", "రక్షణ"),
        ],
        "holiday_patterns": [
            ("Holiday", "Holiday"), ("It's a holiday", "ఇవాళ హాలిడే"),
            ("time to earn", "సంపాదించే సమయం"), ("peak time", "Peak Time"),
        ],
        "gift_earning_patterns": [
            ("Just by being online", "FRND యాప్ లో ఆన్లైన్ ఉండడం ద్వారా"),
            ("earn real money", "నిజమైన డబ్బు సంపాదించుకోవచ్చు"),
            ("Your time = Your earnings", "మీ సమయం = మీ సంపాదన"),
        ],
        "encouragement_patterns": [
            ("Don't miss out", "Miss avvakandi"), ("Go online now", "ఇప్పుడే ఆన్లైన్ వెళ్ళండి"),
        ]
    },
    "malayalam": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "രക്ഷാ ബന്ധൻ"), ("your brother", "നിങ്ങളുടെ സഹോദരന്"), ("Protection", "പ്രൊട്ടക്ഷൻ"),
        ],
        "holiday_patterns": [
            ("Holiday", "ഹോളിഡേ"), ("time to earn", "സമ്പാദിക്കാനുള്ള സമയം"), ("peak time", "പീക്ക് സമയം"),
        ],
        "gift_earning_patterns": [
            ("earn real money", "റിയൽ പണം സമ്പാദിക്കൂ"), ("in your wallet", "നിങ്ങളുടെ വാലറ്റിൽ"),
        ],
        "encouragement_patterns": [
            ("Don't miss out", "നഷ്ടപ്പെടുത്തരുത്"), ("Go online now", "ഇപ്പോൾ ഓൺലൈനിൽ പോകൂ"),
        ]
    },
    "kannada": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "ರಕ್ಷಾ ಬಂಧನ"), ("your brother", "ನಿಮ್ಮ ಸಹೋದರನಿಗೆ"), ("Protection", "ರಕ್ಷಣೆ"),
        ],
        "holiday_patterns": [
            ("Holiday", "ಹಾಲಿಡೇ"), ("time to earn", "ಗಳಿಸುವ ಸಮಯ"), ("peak time", "ಪೀಕ್ ಟೈಮ್"),
        ],
        "gift_earning_patterns": [
            ("earn real money", "ನಿಜವಾದ ಹಣವನ್ನು ಗಳಿಸಿ"), ("in your wallet", "ನಿಮ್ಮ ವ್ಯಾಲೆಟ್ನಲ್ಲಿ"),
        ],
        "encouragement_patterns": [
            ("Don't miss out", "ತಪ್ಪಿಸಿಕೊಳ್ಳಬೇಡಿ"), ("Go online now", "ಈಗಲೇ ಆನ್ಲೈನ್ಗೆ ಹೋಗಿ"),
        ]
    },
    "odia": {
        "rakhi_patterns": [
            ("Raksha Bandhan", "Raksha Bandhan"), ("your brother", "ତୁମ ଭାଇଙ୍କୁ"), ("Protection", "ସୁରକ୍ଷା"),
        ],
        "holiday_patterns": [
            ("Holiday", "ହଲିଡେ"), ("time to earn", "କମେଇବାର ସମୟ"),
        ],
        "gift_earning_patterns": [
            ("earn real money", "ଟଙ୍କା କମାନ୍ତୁ"), ("Go online now", "ଏବେ ଅନଲାଇନ୍ ଆସନ୍ତୁ"),
        ]
    }
}

# -------------------- NEW: TEAM TRAINING CORRECTIONS -------------------- #

# Based on the training data provided by your team
TEAM_TRAINING_CORRECTIONS = {
    "ml-IN": {
        # From Malayalam training data - key issues identified
        "meeting_corrections": [
            # Issue: Over-explaining instead of direct translation
            ("explained version", "direct translation"),
            # Issue: Missing last line or incomplete sentences
            ("incomplete_pattern", "complete_all_sentences"),
            # Correct patterns from team corrections
            ("The FRND Meeting is happening now", "FRND മീറ്റിംഗ് ഇപ്പോൾ നടക്കുന്നു"),
            ("From call tips to earnings", "കോൾ ടിപ്സ് മുതൽ എർണിങ്സ് വരെ ഡിസ്കസ് ചെയ്യുന്നു"),
            ("Jump in now if you haven't already", "ഇപ്പോൾ തന്നെ ചേരൂ"),
            ("FRND Meeting is LIVE right now", "FRND മീറ്റിംഗ് ഇപ്പോൾ LIVE ആണ്"),
            ("Tap to join – useful tips being shared", "ജോയിൻ ചെയ്യാൻ ടാപ്പ് ചെയ്യൂ"),
        ],
        "whatsapp_corrections": [
            # More natural greeting and structure from team version
            ("Hi [Name]", "നമസ്കാരം [പേര്]"),
            ("brand-new WhatsApp Channel", "പുതിയ WhatsApp ചാനൽ"),
            ("guess what", "ഒന്ന് Guess ചെയാമോ"),
            ("special invite list", "സ്പെഷ്യൽ ഇൻവൈറ്റ് ലിസ്റ്റ്"),
            ("Be the first to know about discounts", "ഓഫറുകളുടെ വിവരങ്ങൾ ആദ്യം അറിയാം"),
            ("Learn simple ways to connect", "എളുപ്പ മാർഗങ്ങൾ പഠിക്കാം"),
            ("favourite trainer", "ഇഷ്ടപ്പെട്ട ട്രെയിനർ"),
            ("Get news on campaign, events & surprise rewards", "ക്യാമ്പെയ്ൻ, ഇവന്റ്സ് & സർപ്രൈസ് സമ്മാനങ്ങളുടെ വാർത്തകൾ അറിയാം"),
            ("completely free", "പൂർണ്ണമായും സൗജന്യം"),
            ("numbers will not be visible", "നമ്പർ മറ്റാരും കാണില്ല"),
            ("dont forget to tap on follow", "Follow അമർത്താൻ മറക്കരുത്"),
            ("never miss anything fun", "ഒരിക്കലും ഫൺ മിസ്സ് ആവില്ല"),
        ]
    },
    "kn-IN": {
        # From Kannada training data - key issues identified
        "whatsapp_corrections": [
            # Issue: Missing words, mixed up order, incomplete sentences
            ("Hi [Name]", "ನಮಸ್ಕಾರ [Name]"),
            ("brand-new WhatsApp Channel", "ಹೊಚ್ಚ ಹೊಸ WhatsApp ಚಾನೆಲ್"),
            ("guess what", "ಗೆಸ್ಸ್ ಮಾಡಿ"),
            ("special invite list", "ಸ್ಪೆಷಲ್ ಲಿಸ್ಟ್"),
            ("Be the first to know about discounts", "ಡಿಸ್ಕೌಂಟ್ಸ್ ಬಗ್ಗೆ ಫಸ್ಟ್ ಆಗಿ ತಿಳಿಯಿರಿ"),
            ("Learn simple ways to connect", "ಟ್ರೈನರ್ಸ್ ಜೊತೆ ಕನೆಕ್ಟ್ ಆಗುವ ಸರಳ ಮಾರ್ಗಗಳನ್ನು ತಿಳಿಯಿರಿ"),
            ("favourite trainer", "ಟ್ರೈನರ್ಸ್"),
            ("Get news on campaign, events & surprise rewards", "ಕ್ಯಾಂಪೇನ್, ಈವೆಂಟ್ಸ್ ಮತ್ತು ಸುಪ್ರಿಸೆ ರಿವಾರ್ಡ್ಸ್ ಬಗ್ಗೆ ನ್ಯೂಸ್ ತಿಳಿಯಿರಿ"),
            ("completely free", "ಫ್ರೀ ಆಗಿದೆ"),
            ("numbers will not be visible", "ಫೋನ್ ನಂಬರ್ ಪ್ರೈವೇಟ್ ಆಗಿರುತ್ತೆ"),
            ("Click on Join Channel", "ಜಾಯಿನ್ ಚಾನೆಲ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ"),
            ("dont forget to tap on follow", "ಫಾಲೋ ಮಾಡೋದನ್ನ ಮರೀಬೇಡಿ"),
            ("that simple", "ಇಷ್ಟು ಸಿಂಪಲ್"),
            ("never miss anything fun on FRND", "FRND‌ನಲ್ಲಿ ಮಜಾ ಯಾವತ್ತೂ ಮಿಸ್ ಆಗೋದು ಇಲ್ಲ"),
        ]
    }
}

# -------------------- COMBINED TRAINING FIXES -------------------- #

LAYER1_TRAINING_FIXES = {
    "hi-IN": {
        "We're LIVE": "Hum LIVE hain", "Join now": "Abhi join karo", "Don't miss": "Miss mat karna",
        "Click & Join": "Click karo aur join karo", "Let's talk": "Chalo baat karte hain",
        "Tips, updates": "Tips, updates", "Really help": "Bohot kaam aayega",
        "Amazing session": "Amazing session tha", "We're waiting": "Hum wait kar rahe hain",
    },
    "ta-IN": {
        "We're LIVE": "நாங்க LIVE ஆ இருக்கோம்", "Join now": "இப்போவே join பண்ணுங்க",
        "Don't miss": "miss பண்ணாதீங்க", "Let's talk": "பேசலாம்",
        "Really help": "definitely உங்களுக்கு help ஆகும்", "Amazing session": "session awesome ஆக்கிச்சு",
        "We're waiting": "உங்களுக்காக wait பண்ணிட்டு இருக்காங்க",
    },
    "te-IN": {
        "We're LIVE": "Manam LIVE lo unnam", "Join now": "Ipude join avvandi", "Don't miss": "Miss avvakandi",
        "Let's talk": "Maatladukundam", "Really help": "Chala useful ga untundi", "We're waiting": "Meeku wait chesthunnaru",
    },
    "ml-IN": {
        "We're LIVE": "ഞങ്ങൾ LIVE ആണ്", "Join now": "ഇപ്പോൾ ജോയിൻ ചെയ്യൂ", "Don't miss": "നഷ്ടപ്പെടുത്തരുത്",
        "Let's talk": "നമുക്ക് സംസാരിക്കാം", "Really help": "ശരിക്കും സഹായിക്കും",
        # Team training additions
        "The FRND Meeting is happening now": "FRND മീറ്റിംഗ് ഇപ്പോൾ നടക്കുന്നു",
        "FRND Meeting is LIVE right now": "FRND മീറ്റിംഗ് ഇപ്പോൾ LIVE ആണ്",
        "Tap to join": "ജോയിൻ ചെയ്യാൻ ടാപ്പ് ചെയ്യൂ",
        "Jump in now": "ഇപ്പോൾ തന്നെ ചേരൂ",
        "from call tips to earnings": "കോൾ ടിപ്സ് മുതൽ എർണിങ്സ് വരെ",
    },
    "kn-IN": {
        "We're LIVE": "ನಾವು ಲೈವ್ ಆಗಿದ್ದೇವೆ", "Join now": "ಈಗಲೇ ಸೇರಿ", "Don't miss": "ತಪ್ಪಿಸಿಕೊಳ್ಳಬೇಡಿ",
        "Let's talk": "ಮಾತನಾಡೋಣ", "Really help": "ನಿಜವಾಗಿಯೂ ಸಹಾಯ ಮಾಡುತ್ತದೆ",
    }
}

LAYER2_TRAINING_FIXES = {
    "hi-IN": {
        "Want to earn ₹40K/month": "₹40K/month kamaana hai", "Join our new WhatsApp Channel": "Naya WhatsApp Channel join karo",
        "All tips here": "Saare tips yahin milenge", "Click to join": "Click karke join karo",
        "100% Number Privacy": "100% Number Privacy Guarantee", "Hey! Secret to": "Hey! Secret",
        "Tired of small earnings": "Kam earnings se thak gaye hoge na", "Let's fix that": "Chinta mat karo",
        "New here? You're not alone": "Naye ho? Don't worry, hum hai na", "Ready to level up": "Ready for level up",
        "Few days in now": "Ab toh kuch din hogaye hai",
    },
    "ta-IN": {
        "₹40K/month FRND": "₹40K/month FRND-ல", "join new WhatsApp Channel": "New WhatsApp Channel-la join பண்ணுங்க",
        "All pro tips here": "Pro tips-லாம் இங்க இருக்கு", "Click to join": "Click பண்ணி join பண்ணுங்க",
        "100% Number Privacy": "100% Number Privacy Guarantee!", "Hey! Secret to big": "Hey! பெரிய income-க்கு secret",
        "Tired of small earnings": "கம்மி earnings-ல bore ஆகிட்டீங்களா", "Let's fix that": "இப்போ fix பண்ணலாம்",
        "New here? You're not alone": "இது உங்க first time-a? நீங்கள் தனியா இல்ல",
        "Ready to level up": "next level போக தயாரா", "Few days in now": "இப்போ உங்கள் journey start ஆகிவிட்டது",
    },
    "te-IN": {
        "₹40K/month": "₹40K/month sampadinchala", "join new WhatsApp Channel": "kotha WhatsApp Channel join avvandi",
        "New here?": "App ki new ah?", "Ready to level up": "ready to level up?", "Few days in now": "Few days aiyayi kadha",
    },
    "ml-IN": {
        "Want to earn ₹40K/month": "മാസം 40K സമ്പാദിക്കാൻ ആഗ്രഹിക്കുന്നുണ്ടോ",
        "join new WhatsApp Channel": "പുതിയ WhatsApp ചാനലിൽ ചേരാൻ",
        "New here? You're not alone": "പുതിയ ആളാണോ? നിങ്ങൾ ഒറ്റയ്ക്കല്ല",
        # Team training additions
        "Hi [Name]": "നമസ്കാരം [പേര്]", "brand-new WhatsApp Channel": "പുതിയ WhatsApp ചാനൽ",
        "guess what": "ഒന്ന് Guess ചെയാമോ", "special invite list": "സ്പെഷ്യൽ ഇൻവൈറ്റ് ലിസ്റ്റ്",
        "Be the first to know about discounts": "ഓഫറുകളുടെ വിവരങ്ങൾ ആദ്യം അറിയാം",
        "Learn simple ways to connect": "എളുപ്പ മാർഗങ്ങൾ പഠിക്കാം",
        "favourite trainer": "ഇഷ്ടപ്പെട്ട ട്രെയിനർ",
        "completely free": "പൂർണ്ണമായും സൗജന്യം",
        "numbers will not be visible": "നമ്പർ മറ്റാരും കാണില്ല",
        "dont forget to tap on follow": "Follow അമർത്താൻ മറക്കരുത്",
        "never miss anything fun": "ഒരിക്കലും ഫൺ മിസ്സ് ആവില്ല",
    },
    "kn-IN": {
        "Want to earn ₹40K/month": "ತಿಂಗಳಿಗೆ ₹40K ಗಳಿಸಲು ಬಯಸುವಿರಾ",
        "join new WhatsApp Channel": "ಹೊಸ WhatsApp ಚಾನಲ್‌ಗೆ ಸೇರಲು",
        "New here? You're not alone": "ಇಲ್ಲಿ ಹೊಸಬರೇ? ನೀವು ಒಬ್ಬಂಟಿಯಲ್ಲ",
        # Team training additions  
        "Hi [Name]": "ನಮಸ್ಕಾರ [Name]", "brand-new WhatsApp Channel": "ಹೊಚ್ಚ ಹೊಸ WhatsApp ಚಾನೆಲ್",
        "guess what": "ಗೆಸ್ಸ್ ಮಾಡಿ", "special invite list": "ಸ್ಪೆಷಲ್ ಲಿಸ್ಟ್",
        "Be the first to know about discounts": "ಡಿಸ್ಕೌಂಟ್ಸ್ ಬಗ್ಗೆ ಫಸ್ಟ್ ಆಗಿ ತಿಳಿಯಿರಿ",
        "Learn simple ways to connect": "ಟ್ರೈನರ್ಸ್ ಜೊತೆ ಕನೆಕ್ಟ್ ಆಗುವ ಸರಳ ಮಾರ್ಗಗಳನ್ನು ತಿಳಿಯಿರಿ",
        "completely free": "ಫ್ರೀ ಆಗಿದೆ", "numbers will not be visible": "ಫೋನ್ ನಂಬರ್ ಪ್ರೈವೇಟ್ ಆಗಿರುತ್ತೆ",
        "that simple": "ಇಷ್ಟು ಸಿಂಪಲ್", "never miss anything fun on FRND": "FRND‌ನಲ್ಲಿ ಮಜಾ ಯಾವತ್ತೂ ಮಿಸ್ ಆಗೋದು ಇಲ್ಲ",
    }
}

LAYER3_TRAINING_FIXES = {
    "hi-IN": {
        "Gift Your Bhai": "Apne Bhai ko do", "₹1000 Hamper": "₹1000 ka Hamper",
        "Just by Being Online": "Sirf Online aakar", "Yes, really!": "Haan, sach mein!",
        "earn real money in your wallet": "apne wallet mein kamao real money",
        "More time = More Yellow Roses": "Jitna zyada time = Utne zyada Yellow Roses",
        "Make this Rakhi extra special": "Iss Rakhi ko banao extra special",
        "It's a holiday today": "Aaj chhutti hai", "Holiday = Time to Earn": "Holiday = kamaane ka time",
        "Tonight's the Night": "Aaj ki raat hai khaas", "peak time": "peak time",
        "Why wait?": "Toh phir rukna kyu?", "Challenge is ON": "Challenge shuru ho chuka hai",
        "Top earners": "Top earners", "Let the spotlight find YOU": "spotlight aap tak khud aa jaayegi",
    },
    "ta-IN": {
        "Gift Your Bhai": "உங்க அண்ணன்/தம்பிக்கு Gift கொடுக்கலாமா",
        "Just by Being Online": "FRND-ல Onlineல இருந்தாலே போதும்", "earn real money": "நேரடி பணம் சேரும்",
        "in your wallet": "Wallet-ல", "More time = More": "அதிக நேரம் = அதிக",
        "Make this Rakhi extra special": "இந்த Rakhi-யை Special-aa ஆக்குங்க",
        "It's a holiday today": "இன்று விடுமுறை", "Holiday = Extra Earnings": "Holiday = Extra Earnings Time",
        "Tonight's the Night": "இன்று இரவு தான் உங்களுக்கு வாய்ப்பு", "Why wait?": "Why Wait?",
        "Challenge is ON": "Challenge ஆரம்பம் ஆகி இருக்கு", "Let the spotlight find YOU": "உங்களை spotlight find பண்ண விடுங்க",
    },
    "te-IN": {
        "Gift Your Bhai": "మీ బ్రదర్ కి Gift చేయొచ్చు", "₹1000 Hamper": "₹1000 హ్యాంపర్",
        "Just by Being Online": "FRND యాప్ లో ఆన్లైన్ ఉండడం ద్వారా",
        "earn real money": "నిజమైన డబ్బు సంపాదించుకోవచ్చు", "in your wallet": "మీ వాలెట్లో",
        "It's a holiday": "ఇవాళ హాలిడే", "peak time": "Peak Time", "Why wait?": "ఎందుకు వెయిట్ చేస్తున్నారూ?",
    },
    "ml-IN": {
        "Raksha Bandhan": "രക്ഷാ ബന്ധൻ", "your brother": "നിങ്ങളുടെ സഹോദരന്",
        "earn real money": "റിയൽ പണം സമ്പാദിക്കൂ", "in your wallet": "നിങ്ങളുടെ വാലറ്റിൽ",
        "Why wait?": "എന്തിന് കാത്തിരിക്കണം?",
    },
    "kn-IN": {
        "Raksha Bandhan": "ರಕ್ಷಾ ಬಂಧನ", "your brother": "ನಿಮ್ಮ ಸಹೋದರನಿಗೆ",
        "earn real money": "ನಿಜವಾದ ಹಣವನ್ನು ಗಳಿಸಿ", "in your wallet": "ನಿಮ್ಮ ವ್ಯಾಲೆಟ್ನಲ್ಲಿ",
        "Why wait?": "ಏಕೆ ಕಾಯಬೇಕು?",
    },
    "or-IN": {
        "Raksha Bandhan": "Raksha Bandhan", "your brother": "ତୁମ ଭାଇଙ୍କୁ",
        "earn real money": "ଟଙ୍କା କମାନ୍ତୁ", "Go online now": "ଏବେ ଅନଲାଇନ୍ ଆସନ୍ତୁ", "peak time": "peak time",
    }
}

# -------------------- TEAM TRAINING QUALITY ISSUES -------------------- #

TEAM_IDENTIFIED_ISSUES = {
    "over_explanation": [
        "giving explained version instead of direct translation",
        "adding meta-commentary about the message",
        "describing what the message is about rather than translating it",
    ],
    "incomplete_translation": [
        "missing last line or sentences", 
        "not translating all parts of the original",
        "truncating content without completing translation",
    ],
    "word_order_issues": [
        "mixed up word order",
        "jumbled sentence structure",
        "incorrect phrase sequencing",
    ],
    "missing_words": [
        "few words missing in translation",
        "skipping important terms or phrases",
        "incomplete sentence components",
    ],
    "segmentation_issues": [
        "poor line break handling",
        "incorrect paragraph structure", 
        "losing original formatting",
    ]
}

# -------------------- CONTEXT DETECTION FUNCTIONS -------------------- #

def detect_message_context_type(text):
    """Detect the type of message for better context application"""
    text_lower = text.lower()
    
    # Festival/Holiday context (highest priority)
    if any(word in text_lower for word in ["rakhi", "raksha bandhan", "brother", "bhai"]):
        return "rakhi_festival"
    if any(word in text_lower for word in ["holiday", "weekend", "vacation"]):
        return "holiday_celebration"
    if any(word in text_lower for word in ["gift", "hamper", "surprise"]):
        return "gift_giving"
    if any(word in text_lower for word in ["challenge", "top earner", "rank", "spotlight"]):
        return "festival_competition"
    if any(word in text_lower for word in ["tonight", "peak time", "4am", "bonus"]):
        return "time_sensitive_promo"
    
    # WhatsApp Channel promotion
    if "whatsapp channel" in text_lower or "channel" in text_lower:
        return "whatsapp_promotion"
    
    # Meeting/Live context  
    if any(word in text_lower for word in ["meeting", "live", "happening now", "tap to join"]):
        return "meeting_live"
    
    # Earnings/Money focused
    if any(word in text_lower for word in ["earn", "₹", "money", "income", "salary"]):
        return "earnings_focused"
    
    # Welcome/Onboarding
    if any(word in text_lower for word in ["welcome", "new here", "first time"]):
        return "welcome_onboarding"
    
    # App feature explanation
    if any(word in text_lower for word in ["tap here", "click", "go online", "badge", "level up"]):
        return "app_features"
    
    # Privacy/Safety messaging
    if any(word in text_lower for word in ["private", "privacy", "safe", "secure"]):
        return "privacy_safety"
    
    return "general"

def detect_team_quality_issues(text, translated_text):
    """Detect quality issues based on team training data"""
    issues = []
    
    # Check for over-explanation patterns
    if any(phrase in translated_text.lower() for phrase in [
        "this message is about", "regarding", "concerning", "കുറിച്ചാണ്", "ବିଷୟରେ"
    ]):
        issues.append("over_explanation")
    
    # Check for incomplete translation
    original_sentences = len([s for s in text.split('.') if s.strip()])
    translated_sentences = len([s for s in translated_text.split('.') if s.strip()])
    if original_sentences > translated_sentences + 1:
        issues.append("incomplete_translation")
    
    # Check for missing emoji preservation
    original_emojis = len([c for c in text if ord(c) > 127])
    translated_emojis = len([c for c in translated_text if ord(c) > 127])
    if original_emojis > translated_emojis:
        issues.append("missing_formatting")
    
    return issues

# -------------------- PATTERN APPLICATION FUNCTIONS -------------------- #

def apply_quality_training_patterns(text, target_lang):
    """Apply Layer 1 training patterns with team corrections"""
    lang_code = target_lang.split('-')[0].lower()
    if lang_code not in ["hi", "ta", "te", "ml", "kn"]:
        return text
    
    pattern_map = {"hi": "hindi", "ta": "tamil", "te": "telugu", "ml": "malayalam", "kn": "kannada"}
    pattern_key = pattern_map.get(lang_code)
    if not pattern_key or pattern_key not in QUALITY_TRAINING_PATTERNS:
        return text
    
    patterns = QUALITY_TRAINING_PATTERNS[pattern_key]
    message_context = detect_message_context_type(text)
    
    # Apply basic patterns
    if "preferred_mixing" in patterns:
        for english_word, preferred_translation in patterns["preferred_mixing"]:
            text = re.sub(f"\\b{re.escape(english_word)}\\b", preferred_translation, text, flags=re.IGNORECASE)
    
    # Apply meeting-specific patterns for Malayalam (from team training)
    if target_lang == "ml-IN" and message_context == "meeting_live":
        if "meeting_specific" in patterns:
            for english_phrase, preferred_translation in patterns["meeting_specific"]:
                text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    return text

def apply_additional_quality_patterns(text, target_lang):
    """Apply Layer 2 training patterns with team corrections"""
    lang_code = target_lang.split('-')[0].lower()
    if lang_code not in ["hi", "ta", "te", "ml", "kn"]:
        return text
    
    pattern_map = {"hi": "hindi", "ta": "tamil", "te": "telugu", "ml": "malayalam", "kn": "kannada"}
    pattern_key = pattern_map.get(lang_code)
    if not pattern_key or pattern_key not in ADDITIONAL_QUALITY_PATTERNS:
        return text
    
    patterns = ADDITIONAL_QUALITY_PATTERNS[pattern_key]
    message_context = detect_message_context_type(text)
    
    # Apply context-specific patterns
    if message_context == "whatsapp_promotion" and "whatsapp_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["whatsapp_patterns"]:
            text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    # Apply channel-specific patterns for Malayalam and Kannada (from team training)
    if message_context == "whatsapp_promotion":
        if target_lang == "ml-IN" and "channel_specific" in patterns:
            for english_phrase, preferred_translation in patterns["channel_specific"]:
                text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
        elif target_lang == "kn-IN" and "channel_specific" in patterns:
            for english_phrase, preferred_translation in patterns["channel_specific"]:
                text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    if message_context == "earnings_focused" and "earnings_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["earnings_patterns"]:
            text = re.sub(f"\\b{re.escape(english_phrase)}\\b", preferred_translation, text, flags=re.IGNORECASE)
    
    if message_context in ["welcome_onboarding", "general"] and "casual_connectors" in patterns:
        for english_phrase, preferred_translation in patterns["casual_connectors"]:
            text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    if message_context == "app_features" and "app_tech_terms" in patterns:
        for english_phrase, preferred_translation in patterns["app_tech_terms"]:
            text = re.sub(f"\\b{re.escape(english_phrase)}\\b", preferred_translation, text, flags=re.IGNORECASE)
    
    return text

def apply_festival_quality_patterns(text, target_lang):
    """Apply Layer 3 festival patterns"""
    lang_code = target_lang.split('-')[0].lower()
    if lang_code not in ["hi", "ta", "te", "ml", "kn", "or"]:
        return text
    
    pattern_map = {"hi": "hindi", "ta": "tamil", "te": "telugu", "ml": "malayalam", "kn": "kannada", "or": "odia"}
    pattern_key = pattern_map.get(lang_code)
    if not pattern_key or pattern_key not in FESTIVAL_QUALITY_PATTERNS:
        return text
    
    patterns = FESTIVAL_QUALITY_PATTERNS[pattern_key]
    festival_context = detect_message_context_type(text)
    
    # Apply context-specific patterns
    if festival_context == "rakhi_festival" and "rakhi_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["rakhi_patterns"]:
            text = re.sub(f"\\b{re.escape(english_phrase)}\\b", preferred_translation, text, flags=re.IGNORECASE)
    
    if festival_context in ["holiday_celebration", "time_sensitive_promo"] and "holiday_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["holiday_patterns"]:
            text = re.sub(f"\\b{re.escape(english_phrase)}\\b", preferred_translation, text, flags=re.IGNORECASE)
    
    if festival_context == "gift_giving" and "gift_earning_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["gift_earning_patterns"]:
            text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    if festival_context in ["festival_competition", "time_sensitive_promo"] and "encouragement_patterns" in patterns:
        for english_phrase, preferred_translation in patterns["encouragement_patterns"]:
            text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    return text

def apply_team_training_corrections(text, target_lang):
    """Apply team-specific corrections based on training data"""
    if target_lang not in TEAM_TRAINING_CORRECTIONS:
        return text
    
    corrections = TEAM_TRAINING_CORRECTIONS[target_lang]
    message_context = detect_message_context_type(text)
    
    # Apply meeting corrections for Malayalam
    if target_lang == "ml-IN" and message_context == "meeting_live":
        if "meeting_corrections" in corrections:
            for english_phrase, preferred_translation in corrections["meeting_corrections"]:
                text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    # Apply WhatsApp corrections
    if message_context == "whatsapp_promotion" and "whatsapp_corrections" in corrections:
        for english_phrase, preferred_translation in corrections["whatsapp_corrections"]:
            text = re.sub(re.escape(english_phrase), preferred_translation, text, flags=re.IGNORECASE)
    
    return text

# -------------------- CONTEXT HINTS FUNCTIONS -------------------- #

def add_quality_context_hints(text, target_lang):
    """Add Layer 1 context hints with team training insights"""
    lang_code = target_lang.split('-')[0].lower()
    context_hints = []
    
    if "meeting" in text.lower() or "meet" in text.lower():
        if lang_code == "hi":
            context_hints.append("meeting/meet pattern")
        elif lang_code == "ta":
            context_hints.append("meeting pattern with Tamil mixing")
        elif lang_code == "ml":
            context_hints.append("direct translation, avoid over-explanation")
    
    if "live" in text.lower():
        context_hints.append("LIVE should stay in caps")
    
    if "join" in text.lower():
        if lang_code == "hi":
            context_hints.append("join karo/join pattern")
        elif lang_code == "ta":
            context_hints.append("join பண்ணுங்க pattern")
        elif lang_code == "te":
            context_hints.append("join avvandi pattern")
        elif lang_code == "ml":
            context_hints.append("ജോയിൻ ചെയ്യൂ pattern")
    
    if "don't miss" in text.lower():
        if lang_code == "hi":
            context_hints.append("miss mat karna pattern")
        elif lang_code == "ta":
            context_hints.append("miss പण்ணാതീங்க pattern")
    
    # Team training: Ensure complete translation
    if len(text.split('.')) > 1:
        context_hints.append("translate ALL sentences completely")
    
    if context_hints:
        hint_text = f"[Apply quality patterns: {', '.join(context_hints)}] "
        return hint_text + text
    
    return text

def add_advanced_context_hints(text, target_lang):
    """Add Layer 2 context hints with team corrections"""
    lang_code = target_lang.split('-')[0].lower()
    message_context = detect_message_context_type(text)
    context_hints = []
    
    # WhatsApp Channel specific hints
    if message_context == "whatsapp_promotion":
        if lang_code == "hi":
            context_hints.append("WhatsApp Channel promotion - keep 'Channel' in English, use 'abhi join karo'")
        elif lang_code == "ta":
            context_hints.append("WhatsApp Channel promotion - Tamil mixing with 'join பண்ணुங்க' pattern")
        elif lang_code == "ml":
            context_hints.append("WhatsApp Channel - use team-approved natural greetings and structure")
        elif lang_code == "kn":
            context_hints.append("WhatsApp Channel - maintain proper word order, translate all components")
    
    # Earnings context
    if message_context == "earnings_focused":
        if lang_code == "hi":
            context_hints.append("earnings context - use 'kamai/kamao' patterns")
        elif lang_code == "ta":
            context_hints.append("earnings context - use Tamil-English mixing for money terms")
    
    # Casual conversation
    if "hey" in text.lower() or "tired" in text.lower():
        if lang_code == "hi":
            context_hints.append("casual tone - use 'Hey!' and conversational Hindi")
        elif lang_code == "ta":
            context_hints.append("casual tone - Tamil conversational mixing")
    
    # Privacy/Safety messaging
    if message_context == "privacy_safety":
        context_hints.append("privacy messaging - keep 'Privacy' and '100%' in English")
    
    # Team training: Avoid common issues
    context_hints.append("avoid over-explanation, direct translation only")
    
    if context_hints:
        hint_text = f"[Context: {message_context}, Apply: {', '.join(context_hints)}] "
        return hint_text + text
    
    return text

def add_festival_context_hints(text, target_lang):
    """Add Layer 3 festival context hints - OPTIMIZED"""
    lang_code = target_lang.split('-')[0].lower()
    festival_context = detect_message_context_type(text)
    hints = []
    
    if festival_context == "rakhi_festival":
        hints.append("rakhi context")
    elif festival_context == "holiday_celebration":
        hints.append("holiday context")
    elif festival_context == "gift_giving":
        hints.append("gift context")
    elif festival_context == "time_sensitive_promo":
        hints.append("urgent promo")
    
    if hints:
        return f"[{festival_context}: {', '.join(hints)}] {text}"
    return text

# -------------------- TRAINING FIXES APPLICATION FUNCTIONS -------------------- #

def apply_training_based_quality_fixes(text, target_lang):
    """Apply Layer 1 training fixes with team corrections"""
    if target_lang not in LAYER1_TRAINING_FIXES:
        return text
    
    fixes = LAYER1_TRAINING_FIXES[target_lang]
    for english_phrase, quality_translation in fixes.items():
        text = re.sub(re.escape(english_phrase), quality_translation, text, flags=re.IGNORECASE)
    
    return text

def apply_additional_training_fixes(text, target_lang):
    """Apply Layer 2 training fixes with team corrections"""
    if target_lang not in LAYER2_TRAINING_FIXES:
        return text
    
    fixes = LAYER2_TRAINING_FIXES[target_lang]
    for english_phrase, quality_translation in fixes.items():
        text = re.sub(re.escape(english_phrase), quality_translation, text, flags=re.IGNORECASE)
    
    return text

def apply_festival_training_fixes(text, target_lang):
    """Apply Layer 3 festival training fixes"""
    if target_lang not in LAYER3_TRAINING_FIXES:
        return text
    
    fixes = LAYER3_TRAINING_FIXES[target_lang]
    for english_phrase, quality_translation in fixes.items():
        text = re.sub(re.escape(english_phrase), quality_translation, text, flags=re.IGNORECASE)
    
    return text

# -------------------- MAIN ENHANCEMENT FUNCTIONS -------------------- #

def enhanced_preprocess_input_for_completeness(text, target_lang):
    """Main preprocessing function that applies all training layers + team corrections - OPTIMIZED"""
    
    # Layer 1: Original training (Meeting/Live sessions) + team corrections
    enhanced_text = apply_quality_training_patterns(text, target_lang)
    enhanced_text = add_quality_context_hints(enhanced_text, target_lang)
    
    # Layer 2: WhatsApp Channel/Privacy training + team corrections
    enhanced_text = apply_additional_quality_patterns(enhanced_text, target_lang)
    enhanced_text = add_advanced_context_hints(enhanced_text, target_lang)
    
    # Layer 3: Festival/Holiday training
    enhanced_text = apply_festival_quality_patterns(enhanced_text, target_lang)
    enhanced_text = add_festival_context_hints(enhanced_text, target_lang)
    
    # NEW: Team training corrections
    enhanced_text = apply_team_training_corrections(enhanced_text, target_lang)
    
    # CRITICAL: Clean hints before API call
    enhanced_text = clean_enhancement_hints_for_api(enhanced_text)
    
    return enhanced_text

def clean_enhancement_hints_for_api(text):
    """Remove all enhancement hints before sending to Sarvam API"""
    
    hint_patterns = [
        r'\[.*?\]\s*',  # Remove all bracketed hints
        r'^\s*:\s*',    # Remove leading colons
    ]
    
    for pattern in hint_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    return text.strip()

def enhanced_postprocess_translation_output(text, target_lang):
    """Main post-processing function that applies all training fixes + team corrections"""
    
    # Layer 1: Original training fixes + team corrections
    result = apply_training_based_quality_fixes(text, target_lang)
    
    # Layer 2: Additional training fixes + team corrections
    result = apply_additional_training_fixes(result, target_lang)
    
    # Layer 3: Festival training fixes
    result = apply_festival_training_fixes(result, target_lang)
    
    # Enhanced emoji and formatting
    result = enhance_emoji_and_formatting_based_on_training(result, target_lang)
    
    # NEW: Apply team-specific issue fixes
    result = fix_team_identified_issues(result, target_lang)
    
    return result

def fix_team_identified_issues(text, target_lang):
    """Fix issues identified by team training data"""
    
    # Remove over-explanation patterns
    over_explanation_patterns = [
        r'This message is about.*?\.',
        r'.*?കുറിച്ചാണ്.*?\.',
        r'.*?regarding.*?\.',
        r'.*?concerning.*?\.',
    ]
    
    for pattern in over_explanation_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Ensure proper emoji preservation 
    text = re.sub(r'\s+([👋🎉💥💬🎯👉])', r' \1', text)
    
    # Fix segmentation issues - ensure proper line breaks
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Remove excessive line breaks
    text = re.sub(r'([.!?])\s*([A-Za-z])', r'\1\n\n\2', text)  # Add breaks after sentences where needed
    
    return text.strip()

def enhance_emoji_and_formatting_based_on_training(text, target_lang):
    """Enhance emoji and formatting based on training examples + team corrections"""
    
    # Ensure LIVE stays in caps and gets proper treatment
    text = re.sub(r'\blive\b', 'LIVE', text, flags=re.IGNORECASE)
    
    # Ensure proper emoji spacing (observed in examples)
    text = re.sub(r'(\d+)\s*PM', r'\1 PM', text)  # Proper PM spacing
    text = re.sub(r'₹\s*(\d+)', r'₹\1', text)    # Proper rupee spacing
    
    # Add missing exclamation marks where appropriate (pattern from examples + team data)
    if "join" in text.lower() and not text.strip().endswith(('!', '?')):
        text = text.strip() + '!'
    
    # Preserve bullet points and structure from team corrections
    text = re.sub(r'(\n)(💥|💬|🎯)', r'\1\n\2', text)  # Ensure proper spacing for bullet emojis
    
    return text

# -------------------- QUALITY ASSESSMENT FUNCTIONS -------------------- #

def calculate_enhanced_translation_confidence(original, translated, source_lang, target_lang):
    """Calculate confidence score with enhanced quality checks + team training insights"""
    if not translated or translated.startswith("❌") or not original:
        return 0.0
    
    confidence = 1.0
    
    # Universal issue checks
    if re.search(r'\[+[^\[\]]*\]+', translated):
        confidence -= 0.3
    
    # Check for incomplete translations (team training insight)
    original_sentences = len(re.findall(r'[.!?]+', original))
    translated_sentences = len(re.findall(r'[.!?।]+', translated))
    if original_sentences > translated_sentences + 1:
        confidence -= 0.4
    
    # Check length ratio
    length_ratio = len(translated) / len(original) if original else 1
    if length_ratio > 3.0 or length_ratio < 0.3:
        confidence -= 0.2
    
    # Check for repeated phrases
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                confidence -= 0.3
                break
    
    # Enhanced checks for training pattern compliance
    message_context = detect_message_context_type(original)
    lang_code = target_lang.split('-')[0].lower()
    
    # Check if key training patterns were applied correctly
    if message_context == "rakhi_festival":
        if "rakhi" in original.lower() and "Rakhi" not in translated:
            confidence -= 0.2
        if "brother" in original.lower() and lang_code == "hi" and "bhai" not in translated.lower():
            confidence -= 0.1
    
    if message_context == "whatsapp_promotion":
        if "whatsapp channel" in original.lower() and "WhatsApp Channel" not in translated:
            confidence -= 0.2
    
    if "live" in original.lower() and "LIVE" not in translated:
        confidence -= 0.1
    
    # NEW: Team training specific checks
    team_issues = detect_team_quality_issues(original, translated)
    if "over_explanation" in team_issues:
        confidence -= 0.3
    if "incomplete_translation" in team_issues:
        confidence -= 0.4
    if "missing_formatting" in team_issues:
        confidence -= 0.2
    
    return max(0.0, min(1.0, confidence))

def analyze_enhanced_translation_quality(original, translated, source_lang, target_lang):
    """Enhanced quality analysis with training pattern compliance + team insights"""
    quality_flags = []
    
    if not translated or translated.startswith("❌"):
        return quality_flags, 0.0
    
    confidence = calculate_enhanced_translation_confidence(original, translated, source_lang, target_lang)
    
    # Universal quality checks
    if re.search(r'\[+[^\[\]]*\]+', translated):
        quality_flags.append("🔧 Brand name formatting issue detected - brackets around text")
    
    # Check for incomplete sentence translation (enhanced with team training)
    original_sentences = len(re.findall(r'[.!?]+', original))
    translated_sentences = len(re.findall(r'[.!?।]+', translated))
    if original_sentences > translated_sentences + 1:
        quality_flags.append("📝 Incomplete translation detected - missing sentences (team training insight)")
    
    # Check dramatic length changes
    if original and translated:
        length_ratio = len(translated) / len(original)
        if length_ratio > 3.0:
            quality_flags.append("📏 Translation much longer than original - possible over-explanation (team insight)")
        elif length_ratio < 0.3:
            quality_flags.append("📏 Translation much shorter than original - may be missing content")
    
    # Check for repeated phrases
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                quality_flags.append("🔄 Repeated phrases detected - may indicate translation error")
                break
    
    # Enhanced training pattern compliance checks
    message_context = detect_message_context_type(original)
    lang_code = target_lang.split('-')[0].lower()
    
    # Festival pattern compliance
    if message_context == "rakhi_festival":
        if "rakhi" in original.lower() and "Rakhi" not in translated:
            quality_flags.append("🎊 Festival context: 'Rakhi' should be preserved in English")
        if "brother" in original.lower() and lang_code == "hi" and "bhai" not in translated.lower():
            quality_flags.append("👨‍👧‍👦 Missing cultural term: should use 'bhai' for brother in Hindi")
    
    # WhatsApp pattern compliance
    if message_context == "whatsapp_promotion":
        if "whatsapp channel" in original.lower() and "WhatsApp Channel" not in translated:
            quality_flags.append("📱 WhatsApp Channel should be preserved in mixed case")
    
    # Live session compliance
    if "live" in original.lower() and "LIVE" not in translated:
        quality_flags.append("📺 'LIVE' should be preserved in all caps")
    
    # NEW: Team training specific quality checks
    team_issues = detect_team_quality_issues(original, translated)
    if "over_explanation" in team_issues:
        quality_flags.append("🎯 Over-explanation detected - should be direct translation (team insight)")
    if "incomplete_translation" in team_issues:
        quality_flags.append("⚠️ Incomplete translation - missing content (team training pattern)")
    
    return quality_flags, confidence

# -------------------- CHATGPT ENHANCEMENT FUNCTIONS -------------------- #

def get_enhanced_chatgpt_prompt_with_training(original_text, sarvam_translation, target_lang, mode, context_type, audience, formality_level):
    """Build enhanced ChatGPT prompt with all training examples + team corrections"""
    
    # Build training examples including team corrections
    training_examples = build_comprehensive_chatgpt_training_examples(target_lang)
    
    # Language-specific instructions
    lang_instructions = {
        "hi-IN": "Hindi with Roman script (Hinglish) and English code-mixing. Example: 'weekend ON ho gaya hai'",
        "ta-IN": "Tamil script with selective English words preserved. Example: 'Saturday – weekend OFFICIALLY ON!'", 
        "te-IN": "Telugu with Roman script and English code-mixing. Example: 'weekend officially ON lo undhi'",
        "ml-IN": "Malayalam script with simple English terms preserved where natural. CRITICAL: Direct translation only, avoid over-explanation",
        "kn-IN": "Kannada script with simple English terms preserved where natural. CRITICAL: Maintain proper word order, translate ALL components",
        "or-IN": "Odia script with simple English terms preserved where natural"
    }
    
    # Mode instructions
    mode_instructions = {
        "modern-colloquial": "modern, casual, conversational style",
        "formal": "formal, professional, respectful tone",
        "classic-colloquial": "literal, word-for-word accuracy prioritized",
        "code-mixed": "heavy English-local language mixing, trendy expressions"
    }
    
    # Formality mapping
    formality_descriptions = {
        1: "very casual, informal", 2: "casual, friendly", 3: "neutral, balanced",
        4: "respectful, semi-formal", 5: "very formal, professional"
    }
    
    # Build language context
    language_context = f"""
Language Target: {lang_instructions.get(target_lang, "the target language")}
Style Mode: {mode_instructions.get(mode, mode)}
Formality Level: {formality_descriptions.get(formality_level, "balanced")}
"""
    
    # Add team training warnings
    team_warnings = """
TEAM TRAINING CRITICAL RULES:
- NO over-explanation or meta-commentary about the message
- Translate ALL sentences completely - do not skip any content
- Maintain proper word order and sentence structure
- Preserve ALL emojis and formatting exactly
- Direct translation only - avoid describing what the message is about
"""
    
    prompt = f"""TASK: Fix and improve this translation following the quality patterns shown in ALL training examples + team corrections.

ORIGINAL ENGLISH:
{original_text}

TRANSLATION TO FIX:
{sarvam_translation}

REQUIREMENTS:
{language_context}

{team_warnings}

{training_examples}

CRITICAL RULES (UPDATED WITH TEAM TRAINING):
1. Follow the EXACT patterns shown in ALL training examples above (all 3 layers + team corrections)
2. Fix any bracket issues around brand names (FRND}}]], Team FRND}}]] should be FRND, Team FRND)
3. Complete any incomplete sentences - translate EVERYTHING
4. Use the same mixing patterns as training examples
5. Keep exact same script (Roman/Native) and formality level
6. Preserve all emojis and formatting exactly
7. Apply festival/holiday context if relevant
8. Apply WhatsApp channel context if relevant  
9. Apply meeting/live session context if relevant
10. NO over-explanation - direct translation only
11. Maintain proper word order and structure
12. DO NOT add explanations or comments
13. ONLY return the corrected translation text

CORRECTED TRANSLATION:"""

    return prompt

def build_comprehensive_chatgpt_training_examples(target_lang):
    """Build training examples for ChatGPT that include all 3 layers + team corrections"""
    
    lang_code = target_lang.split('-')[0].lower()
    
    if lang_code == "hi":
        return """
TRAINING EXAMPLES (follow these patterns exactly):

LAYER 1 - Meeting/Live patterns:
English: "We're LIVE! Join now!"
Quality Hindi: "Hum LIVE hain! Abhi join karo!"

English: "Don't miss it!"
Quality Hindi: "Miss mat karna!"

LAYER 2 - WhatsApp Channel patterns:
English: "Join our new WhatsApp Channel"
Quality Hindi: "Naya WhatsApp Channel join karo"

English: "Tired of small earnings? Let's fix that"
Quality Hindi: "Kam earnings se thak gaye hoge na? Chinta mat karo"

LAYER 3 - Festival patterns:
English: "Gift Your Bhai ₹1000 Hamper"
Quality Hindi: "Apne Bhai ko do ₹1000 ka Hamper"

English: "Just by Being Online earn real money"
Quality Hindi: "Sirf Online aakar kamao real money"

English: "Tonight's the Night! Why wait?"
Quality Hindi: "Aaj ki raat hai khaas! Toh phir rukna kyu?"
"""
    elif lang_code == "ta":
        return """
TRAINING EXAMPLES (follow these patterns exactly):

LAYER 1 - Meeting/Live patterns:
English: "We're LIVE! Join now!"
Quality Tamil: "நாங்க LIVE ஆ இருக்கோம்! இப்போவே join பண்ணுங்க!"

English: "Really helpful session"
Quality Tamil: "session definitely உங்களுக்கு help ஆகும்!"

LAYER 2 - WhatsApp Channel patterns:
English: "New here? You're not alone"
Quality Tamil: "இது உங்க first time-a? நீங்கள் தனியா இல்ல"

LAYER 3 - Festival patterns:
English: "Just by Being Online earn real money"
Quality Tamil: "FRND-ல Onlineல இருந்தாலே போதும் நேரடி பணம் சேரும்"

English: "Make this Rakhi extra special"
Quality Tamil: "இந்த Rakhi-யை Special-aa ஆக்குங்க"
"""
    elif lang_code == "te":
        return """
TRAINING EXAMPLES (follow these patterns exactly):

LAYER 1 - Meeting/Live patterns:
English: "We're LIVE! Join now!"
Quality Telugu: "Manam LIVE lo unnam! Ipude join avvandi!"

LAYER 2 - WhatsApp Channel patterns:
English: "New here?"
Quality Telugu: "App ki new ah?"

LAYER 3 - Festival patterns:
English: "Gift Your Bhai ₹1000 Hamper"
Quality Telugu: "మీ బ్రదర్ కి Gift చేయొచ్చు ₹1000 హ్యాంపర్"
"""
    elif lang_code == "ml":
        return """
TRAINING EXAMPLES + TEAM CORRECTIONS (follow these patterns exactly):

LAYER 1 - Meeting/Live patterns + TEAM TRAINING:
English: "💛 The FRND Meeting is happening now! From call tips to earnings to what's new on the app — it's all being discussed live! 🎯 Jump in now if you haven't already!"
WRONG (Sarvam): "ഫ്രണ്ട്" മീറ്റിംഗ് ഇപ്പോൾ നടക്കുന്നു. "കോൾ" ഫീച്ചർ എങ്ങനെ യൂസ് ചെയ്യാമെന്നുള്ള ടിപ്സ് ഷെയർ ചെയ്യുന്നു...
TEAM CORRECTED: "💛 FRND മീറ്റിംഗ് ഇപ്പോൾ നടക്കുന്നു! കോൾ ടിപ്സ് മുതൽ എർണിങ്സ് വരെ ഡിസ്കസ് ചെയ്യുന്നു, ആപ്പിലെ ലേറ്റസ്റ്റ് അപ്ഡേറ്റ്സിനെ കുറിച്ചും സംസാരിക്കുന്നു. 🎯 ഇപ്പോൾ തന്നെ ചേരൂ!"

English: "FRND Meeting is LIVE right now! Tap to join – useful tips being shared!"
WRONG (Sarvam): ഇപ്പോൾ ലൈവ് ആയിട്ടുള്ള ഒരു മീറ്റിങ്ങിനെ കുറിച്ചാണീ മെസ്സേജ്...
TEAM CORRECTED: "FRND മീറ്റിംഗ് ഇപ്പോൾ LIVE ആണ്! ജോയിൻ ചെയ്യാൻ ടാപ്പ് ചെയ്യൂ"

LAYER 2 - WhatsApp Channel patterns + TEAM TRAINING:
English: "Hi [Name]! 👋 FRND's brand-new WhatsApp Channel is here… and guess what? You're on the special invite list! 🎉"
TEAM CORRECTED: "നമസ്കാരം [പേര്]! 👋 FRND-ന്റെ പുതിയ WhatsApp ചാനൽ എത്തിയിരിക്കുന്നു ഒന്ന് Guess ചെയാമോ? നിങ്ങൾ സ്പെഷ്യൽ ഇൻവൈറ്റ് ലിസ്റ്റിലുണ്ട്! 🎉"

CRITICAL TEAM TRAINING RULES:
- NO over-explanation (avoid "കുറിച്ചാണ്" patterns)
- Direct translation only
- Complete ALL sentences
- Preserve ALL emojis exactly
"""
    elif lang_code == "kn":
        return """
TRAINING EXAMPLES + TEAM CORRECTIONS (follow these patterns exactly):

LAYER 2 - WhatsApp Channel patterns + TEAM TRAINING:
English: "Hi [Name]! 👋 FRND's brand-new WhatsApp Channel is here… and guess what? You're on the special invite list! 🎉"
TEAM CORRECTED: "ನಮಸ್ಕಾರ [Name]! 👋 FRND ನ ಹೊಚ್ಚ ಹೊಸ WhatsApp ಚಾನೆಲ್ ಇಲ್ಲಿದೆ...ಮತ್ತು ಗೆಸ್ಸ್ ಮಾಡಿ ? ನೀವು ಸ್ಪೆಷಲ್ ಲಿಸ್ಟಲ್ಲಿ ಇದ್ದೀರಿ! 🎉"

English: "Be the first to know about discounts"
TEAM CORRECTED: "ಡಿಸ್ಕೌಂಟ್ಸ್ ಬಗ್ಗೆ ಫಸ್ಟ್ ಆಗಿ ತಿಳಿಯಿರಿ"

English: "It's that simple & never miss anything fun on FRND!"
TEAM CORRECTED: "ಇಷ್ಟು ಸಿಂಪಲ್, FRND‌ನಲ್ಲಿ ಮಜಾ ಯಾವತ್ತೂ ಮಿಸ್ ಆಗೋದು ಇಲ್ಲ!"

CRITICAL TEAM TRAINING RULES:
- Maintain proper word order
- Translate ALL components
- No missing words or lines
- Preserve structure and formatting
"""
    
    return ""

# -------------------- HELPER FUNCTIONS -------------------- #

def clean_instruction_leaks_from_result(text):
    """Clean all possible instruction leaks from translation result + team training patterns"""
    
    instruction_patterns = [
        r'\[INSTRUCTION:.*?\]\s*', r'\[INST:.*?\]\s*', r'\[Translate completely including:.*?\]\s*',
        r'\[translate from:.*?\]\s*', r'\[.*?translate.*?from.*?\]\s*', r'^\[.*?\]\s*',
        r'\[Context:.*?\]\s*', r'\[Apply quality patterns:.*?\]\s*', r'\[Festival context:.*?\]\s*',
        r'\[Apply:.*?\]\s*',
        # Team training: Remove over-explanation patterns
        r'This message is about.*?\.',
        r'.*?കുറിച്ചാണ്.*?\.',
        r'.*?regarding.*?\.',
    ]
    
    for pattern in instruction_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    return text

# -------------------- VERSION INFO -------------------- #

TRANSLATION_ENHANCEMENTS_VERSION = "3.1"
LAST_UPDATED = "2025-08-22"
SUPPORTED_LANGUAGES = ["hi-IN", "ta-IN", "te-IN", "ml-IN", "kn-IN", "or-IN"]
TRAINING_LAYERS = ["Meeting/Live Sessions", "WhatsApp Channel/Privacy", "Festival/Holiday", "Team Training Corrections"]

def get_enhancement_info():
    """Get information about the current enhancement version"""
    return {
        "version": TRANSLATION_ENHANCEMENTS_VERSION,
        "last_updated": LAST_UPDATED,
        "supported_languages": SUPPORTED_LANGUAGES,
        "training_layers": TRAINING_LAYERS,
        "total_patterns": len(QUALITY_TRAINING_PATTERNS) + len(ADDITIONAL_QUALITY_PATTERNS) + len(FESTIVAL_QUALITY_PATTERNS) + len(TEAM_TRAINING_CORRECTIONS),
        "total_fixes": len(LAYER1_TRAINING_FIXES) + len(LAYER2_TRAINING_FIXES) + len(LAYER3_TRAINING_FIXES),
        "team_training_languages": list(TEAM_TRAINING_CORRECTIONS.keys()),
        "key_improvements": [
            "Direct translation patterns (no over-explanation)",
            "Complete sentence translation enforcement", 
            "Proper word order maintenance",
            "Enhanced emoji and formatting preservation",
            "Team-validated natural language patterns"
        ]
    }
