# ============================================================
# NANI KE NUSHKE - Traditional Home Remedies Chatbot
# Built with Flask (Python Web Framework)
# ============================================================
# HOW THIS WORKS (Simple Explanation):
# 1. Flask starts a web server on your computer
# 2. The user types a message on the HTML page
# 3. JavaScript sends that message to Flask
# 4. Flask checks the message using simple Python logic:
#       - Is it a greeting?     → Reply warmly
#       - Is it an emergency?   → Warn to see a doctor
#       - Is it a symptom?      → Give a home remedy
#       - Nothing matched?      → Ask for more info
# 5. Flask sends back a reply, which is shown on screen
# ============================================================

from flask import Flask, request, jsonify, render_template
import datetime
import random

# Create the Flask app (this is the main object that runs the website)
app = Flask(__name__)


# ============================================================
# GREETING KEYWORDS
# If the user types any of these words, we greet them back
# ============================================================
greeting_keywords = [
    "hi", "hello", "namaste", "hey", "hii", "helo",
    "good morning", "good afternoon", "good evening", "good night",
    "namaskar", "start"
]


# ============================================================
# REMEDY DICTIONARY
# This is a Python dictionary where:b0
#   KEY   = keyword we search for in the user's message
#   VALUE = the remedy Nani suggests
# We loop through all keys and check if any appear in the message
# ============================================================
remedies = {

    # ---------- RESPIRATORY ----------
    "cough":        "🍵 Boil fresh ginger + tulsi leaves in water. Add honey and drink warm twice a day.",
    "cold":         "🧄 Eat 2 raw garlic cloves in the morning. Drink warm water with a pinch of haldi (turmeric).",
    "sore throat":  "🧂 Gargle with warm salt water 3 times a day. Sip warm honey-ginger tea.",
    "throat":       "🧂 Gargle with warm salt water 3 times a day. Add turmeric for extra relief.",
    "phlegm":       "🌿 Mix half teaspoon of turmeric in warm milk. Drink before sleeping.",
    "mucus":        "🌿 Steam inhalation with a few drops of eucalyptus oil helps clear mucus.",
    "blocked nose": "🫧 Steam inhalation — boil water, cover head with towel, breathe steam for 5–10 min.",
    "stuffy nose":  "🫧 Steam inhalation — boil water, cover head with towel, breathe steam for 5–10 min.",
    "runny nose":   "🫧 Drink warm ginger tea with honey. Steam inhalation also helps.",
    "running nose": "🫧 Drink warm ginger tea with honey. Steam inhalation also helps.Keep hydrating yourself.",
    "sneeze":       "☀️ Drink warm water with a pinch of black pepper powder. Avoid cold food.",
    "sneezing":     "☀️ Drink warm water with a pinch of black pepper powder. Avoid cold food.",
    "breathe":      "⚠️ Breathing problems should be checked by a doctor. If mild, try steam inhalation.",

    # ---------- HEAD & EYES ----------
    "headache":     "🌿  Massage temples with mustard oil gently. Rest in dark room.",
    "head pain":    "🌿 Apply sandalwood paste on forehead. Massage temples with mustard oil gently.",
    "migraine":     "❄️ Apply ice pack on forehead for 15 minutes. Drink ginger tea and rest.",
    "dizziness":    "🧃 Drink lemon water with a pinch of salt. Sit down, avoid sudden movements.",
    "dizzy":        "🧃 Drink lemon water with a pinch of salt. Sit down, avoid sudden movements.",
    "vertigo":      "🧃 Sit or lie still. Drink ginger tea slowly. Avoid quick head movements.",
    "eyes":         "🥒 Place cold cucumber slices on eyes for 10–15 minutes.",
    "eye pain":     "🥒 Place chilled cucumber slices or cold tea bags on closed eyes for 10 minutes.",
    "eye strain":   "🥒 Place chilled cucumber slices or cold tea bags on closed eyes for 10 minutes.",
    "eye infection":"🌸 Wash eyes with clean rose water using an eye cup. Avoid touching eyes.",
    "puffy eyes":   "🥒 Place chilled cucumber slices or cold spoons on eyes for 10 minutes.",
    "dark circles": "🥛 Apply raw cold milk under eyes with cotton. Sleep 8 hours. Stay hydrated.",

    # ---------- STOMACH & DIGESTION ----------
    "stomach":        "💛 Drink ajwain boiled in water. Add a pinch of black salt for quick relief.",
    "stomachache":    "💛 Drink ajwain boiled in water. Add a pinch of black salt.",
    "stomach pain":   "💛 Drink ajwain boiled in water. Add a pinch of black salt.",
    "stomach ache":   "💛 Drink ajwain boiled in water. Add a pinch of black salt.",
    "tummy":          "💛 Drink ajwain boiled in water. Add a pinch of black salt for quick relief.",
    "acidity":        "🥛 Drink cold milk or mix one teaspoon of baking soda in water. Eat a banana.",
    "acid reflux":    "🥛 Drink cold milk or mix baking soda in water. Eat a banana.",
    "heartburn":      "🥛 Drink cold milk or eat a small banana. Avoid spicy food.",
    "indigestion":    "🌿 Chew fresh ginger after meals. Or drink jeera (cumin) water.",
    "gas":            "🌱 Boil ajwain and jeera in water. Drink after meals.",
    "bloating":       "🌱 Boil ajwain and jeera in water. Drink after meals.",
    "constipation":   "🌙 Drink warm water with one teaspoon of ghee before sleeping.",
    "diarrhea":       "🍌 Eat bananas and curd. Drink ORS to stay hydrated.",
    "loose motions":  "🍌 Eat bananas and curd. Drink ORS to stay hydrated.",
    "vomiting":       "🍋 Sip ginger tea or lemon water slowly. Avoid solid food. Rest.",
    "nausea":         "🍋 Sip ginger tea or smell a fresh lemon. Breathe slowly.",
    "feel sick":      "🍋 Sip ginger tea or lemon water slowly. Rest and breathe deeply.",
    "burp":           "🌱 Drink jeera water after meals. Avoid carbonated drinks.",

    # ---------- SKIN & HAIR ----------
    "pimples":   "🌼 Apply neem paste or tulsi paste. Leave 20 min, wash with cold water.",
    "acne":      "🌼 Apply neem paste or tulsi paste. Drink neem water daily.",
    "skin":      "🌹 Apply aloe vera gel on affected area. Soothes irritation.",
    "rash":      "🌿 Apply sandalwood powder mixed with rose water. Avoid scratching.",
    "itching":   "💛 Apply coconut oil with a pinch of turmeric on itchy area.",
    "itchy":     "💛 Apply coconut oil with a pinch of turmeric on itchy area.",
    "burn":      "🧴 Run cold water over burn for 10 minutes. Apply fresh aloe vera gel.",
    "sunburn":   "🧴 Apply chilled aloe vera gel or cold yogurt on sunburned skin.",
    "dandruff":  "🥥 Massage warm coconut oil + lemon juice into scalp. Leave an hour, wash.",
    "hair fall": "🥥 Massage warm coconut oil into scalp twice a week. Eat iron-rich foods.",
    "hair loss": "🥥 Massage warm coconut oil into scalp twice a week. Eat iron-rich foods.",
    "dry skin":  "🌹 Apply warm coconut oil or aloe vera before sleeping. Drink 8 glasses water.",

    # ---------- PAIN & BODY ----------
    "joint pain":    "🌡️ Apply warm mustard oil on painful joint and massage gently . Drink turmeric milk daily.",
    "knee pain":     "🌡️ Apply warm mustard oil on knee and massage gently. Avoid cold foods.",
    "knee":          "🌡️ Warm mustard oil massage on the knee daily. Drink turmeric milk at night.",
    "back pain":     "💪 Apply warm mustard oil, massage gently. Sleep on firm mattress.",
    "muscle pain":   "🧂 Soak in warm water with Epsom salt. Massage with warm sesame oil.",
    "body pain":     "🛁 Add salt to warm bath water and soak 15 min. Drink turmeric milk.",
    "tooth pain":    "🧄 Apply clove oil on the aching tooth with cotton. Natural painkiller.",
    "toothache":     "🧄 Apply clove oil on tooth. Hold raw ginger against the gum.",
    "tooth ache":    "🧄 Apply clove oil on tooth. Hold raw ginger against the gum.",
    "ear pain":      "🫒 Warm a few drops of sesame oil and put 2 drops in ear.",
    "ear ache":      "🫒 Warm a few drops of sesame oil and put 2 drops in ear.",
    "shoulder pain": "💪 Apply warm mustard oil and massage in circular motion.",
    "neck pain":     "🌿 Apply warm mustard oil on neck. Use a low pillow. Avoid long phone use.",
    "leg pain":      "🌡️ Massage warm sesame oil on legs before sleeping. Stretch every morning.",
    "ankle pain":    "🌡️ Elevate the foot and apply warm mustard oil massage.",
    "wrist pain":    "🧂 Soak wrist in warm salt water for 10 minutes. Apply turmeric paste.",
    "swelling":      "🧊 Apply turmeric + water paste on the swollen area. Keep area elevated.",
    "arthritis":     "🌿 Drink warm water with methi seeds every morning. Massage with mustard oil.",
    "mother":        "👵 For elders, warm mustard oil massage on painful joints works wonders. Turmeric milk daily!",
    "pain":          "🥵Massage it with firm hands",

    # ---------- ENERGY & IMMUNITY ----------
    "tired":            "🍯 Mix honey + lemon in warm water every morning. Get 7–8 hours sleep.",
    "fatigue":          "🍯 Mix honey + lemon in warm water. Eat banana for quick energy.",
    "weakness":         "🥛 Drink warm turmeric milk daily. Eat dates, bananas, and nuts.",
    "weak":             "🥛 Drink warm turmeric milk daily. Eat dates, bananas, and nuts.",
    "fever":            "🌡️ Apply wet cloth on forehead. Drink plenty of fluids. Rest well.",
    "temperature":      "🌡️ Apply wet cloth on forehead. Drink warm ginger tea. See doctor if very high.",
    "high temperature": "🌡️ Apply wet cloth on forehead. Drink warm ginger tea. See doctor if above 103°F.",
    "insomnia":         "🌙 Drink warm milk with a pinch of nutmeg before sleeping.",
    "sleep":            "🌙 Drink warm milk with honey before sleeping. Try deep breathing.",
    "cant sleep":       "🌙 Drink warm milk with a pinch of nutmeg. Avoid screens 1 hour before bed.",
    "stress":           "🧘 Deep breathing: inhale 4 counts, hold 4, exhale 4. Drink ashwagandha milk.",
    "anxiety":          "🧘 Try 5-4-3-2-1 grounding. Drink chamomile tea. Talk to someone.",
    "tension":          "🧘 Deep breathing helps a lot. Also try warm ashwagandha milk at night.",

    # ---------- DIABETES & BLOOD SUGAR ----------
    "diabetes":    "🌿 Drink bitter gourd (karela) juice every morning. Eat methi seeds soaked overnight.",
    "sugar":       "🌿 Karela juice daily. Soak methi seeds overnight and eat in morning. Avoid sugary food.",
    "blood sugar": "🌿 Bitter gourd juice every morning. Soak methi seeds overnight and eat in morning.",
    "high sugar":  "🌿 Karela juice + methi seeds daily. Walk 30 minutes. Avoid white rice and sugar.",

    # ---------- BLOOD PRESSURE ----------
    "blood pressure":   "🧄 Eat 2 raw garlic cloves daily. Drink coconut water. Reduce salt intake.",
    "bp":               "🧄 Eat 2 raw garlic cloves daily. Drink coconut water. Reduce salt intake.",
    "high bp":          "🧄 Raw garlic daily. Coconut water. Avoid stress. Walk 30 min daily.",
    "low bp":           "☕ Drink a cup of black coffee or strong tea. Eat salty snacks. Lie down and rest.",
    "low blood pressure":"☕ Drink black coffee or strong tea. Eat salty snacks. Lie down and rest.",
    "hypertension":     "🧄 Garlic + coconut water daily. Reduce salt and stress. Sleep well.",

    # ---------- COMMON EVERYDAY ----------
    "period pain":  "🌿 Drink ajwain water with jaggery. Apply warm cloth on lower abdomen.",
    "period":       "🌿 Drink ajwain water with jaggery. Apply warm cloth on lower abdomen.",
    "cramps":       "🌿 Drink warm ajwain water. Massage lower belly with warm castor oil gently.",
    "hiccups":      "💧 Drink a full glass of water slowly without stopping. Or hold breath 30 sec.",
    "hiccup":       "💧 Drink a full glass of water slowly without stopping. Or hold breath 30 sec.",
    "bad breath":   "🌿 Chew fresh mint leaves or fennel seeds (saunf) after meals.",
    "mouth ulcer":  "🧂 Apply honey directly on ulcer. Rinse with warm salt water twice a day.",
    "mouth sore":   "🧂 Apply honey directly on sore. Rinse with warm salt water twice a day.",
    "nose bleed":   "🧊 Pinch your nose and tilt head slightly forward. Apply ice on nose bridge.",
    "nosebleed":    "🧊 Pinch your nose and tilt head slightly forward. Apply ice on nose bridge.",
    "lips":         "🍯 Apply pure desi ghee or honey on dry/cracked lips before sleeping.",
    "dry lips":     "🍯 Apply desi ghee or honey on lips every night. Drink plenty of water.",
    "chapped lips": "🍯 Apply desi ghee or honey on lips every night. Stay hydrated.",
}


# ============================================================
# EMERGENCY KEYWORDS
# If any of these phrases appear in the message,
# we immediately tell the user to see a doctor — no remedy
# ============================================================
emergency_keywords = [
    "chest pain", "chest hurts", "heart pain",
    "can't breathe", "cannot breathe", "difficulty breathing",
    "severe bleeding", "unconscious", "fainted", "stroke",
    "paralysis", "can't move", "seizure", "fits",
    "very high fever", "loss of consciousness",
    "blood in urine", "blood in stool", "blood" ,
    "coughing blood", "vomiting blood", "broken bone","cancer","asthma"
]


# ============================================================
# RANDOM RESPONSES FOR "NOT FOUND"
# When no remedy matches, we pick one randomly
# This makes the bot feel more natural and friendly
# ============================================================
not_found_responses = [
    "🤔 Hmm, I couldn't find a remedy for that. Can you describe more? Like where exactly is the problem?",
    "😅 I didn't quite understand! Is it pain, itching, swelling, or something else?",
    "🌿 Could you give a bit more detail? Which part of the body is bothering you?",
    "👵 Nani couldn't understand! Try saying like 'knee pain', 'stomach ache', or 'headache'.",
    "🙈 Oops! I couldn't catch that. Can you describe your symptoms in simple words?",
    "🤷 I didn't get that! Try typing something like 'fever', 'back pain', or 'cough'.",
]


# ============================================================
# HELPER FUNCTION: get_time_greeting
# Returns a greeting based on the current time of day
# datetime.datetime.now().hour gives the current hour (0–23)
# ============================================================
def get_time_greeting():
    hour = datetime.datetime.now().hour  # e.g. 14 means 2 PM
    if 5 <= hour < 12:
        return "Good Morning ☀️"
    elif 12 <= hour < 17:
        return "Good Afternoon 🌤️"
    elif 17 <= hour < 21:
        return "Good Evening 🌙"
    else:
        return "Good Night 🌛"


# ============================================================
# HELPER FUNCTION: check_emergency
# Loops through emergency_keywords list
# Returns True if any keyword is found in the message
# ============================================================
def check_emergency(message):
    message_lower = message.lower()        # Convert to lowercase so "CHEST PAIN" = "chest pain"
    for keyword in emergency_keywords:
        if keyword in message_lower:
            return True                    # Emergency found — stop checking
    return False                           # No emergency


# ============================================================
# HELPER FUNCTION: find_remedy
# Loops through the remedies dictionary
# Returns the remedy text if a keyword matches, else None
# ============================================================
def find_remedy(message):
    message_lower = message.lower()
    found_remedies = []
    matched_keywords = []

    for keyword in remedies:
        if keyword in message_lower and keyword not in matched_keywords:
            found_remedies.append(f"<strong>🌿 For {keyword}:</strong><br>{remedies[keyword]}")
            matched_keywords.append(keyword)

    if found_remedies:
        return "<br><br>".join(found_remedies)
    return None                           # No match found


# ============================================================
# FLASK ROUTE: Home Page "/"
# When user opens the website, this runs and shows index.html
# ============================================================
@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# FLASK ROUTE: Chat API "/chat"  (POST request)
# JavaScript calls this when the user sends a message
# We process the message and return a JSON reply
# ============================================================
@app.route("/chat", methods=["POST"])
def chat():
    # Read the JSON data sent by the browser
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # If the user sent an empty message, ask them to type something
    if not user_message:
        return jsonify({"reply": "Please type your problem or symptoms.", "type": ""})
    


    # ----------------------------------------------------------
    # STEP 1: Check for GREETINGS (hi, hello, namaste, etc.)
    # ----------------------------------------------------------
    message_lower = user_message.lower()
    word_count = len(user_message.strip().split())

    if word_count <= 2:
        for keyword in greeting_keywords:
            if keyword in message_lower:
                time_greeting = get_time_greeting()
                reply = (
                    f"{time_greeting}! 🙏<br><br>"
                    "Welcome to <strong>Nani ke Nushke</strong>! 👵<br><br>"
                    "Tell me your problem and I'll suggest the best traditional remedy!<br>"
                    "<em>Example: 'I have a cough' or 'My stomach hurts'</em>"
                )
                return jsonify({"reply": reply, "type": "greeting"})

    # ----------------------------------------------------------
    # STEP 2: Check for EMERGENCY keywords (highest safety priority)
    # ----------------------------------------------------------
    if check_emergency(user_message):
        reply = (
            "🚨 <strong>This sounds like a medical emergency!</strong><br><br>"
            "Please consult a doctor or go to the nearest hospital immediately.<br>"
            "Do not rely on home remedies for serious symptoms."
        )
        return jsonify({"reply": reply, "type": "emergency"})

    # ----------------------------------------------------------
    # STEP 3: Search for a HOME REMEDY using keyword matching
    # ----------------------------------------------------------
    remedy = find_remedy(user_message)
    if remedy:
        reply = (
            f"🌿 <strong>Nani ka Nuskha:</strong><br><br>"
            f"{remedy}<br><br>"
            f"<em>💛 Take care! If symptoms persist, please consult a doctor.</em>"
        )
        return jsonify({"reply": reply, "type": "remedy"})

    # ----------------------------------------------------------
    # STEP 4: Nothing matched — pick a random "not found" reply
    # random.choice() picks one item randomly from a list
    # ----------------------------------------------------------
    return jsonify({"reply": random.choice(not_found_responses), "type": "not_found"})





# ============================================================
# RUN THE APP
# This starts the Flask web server on your computer
# debug=True shows helpful error messages while developing
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)