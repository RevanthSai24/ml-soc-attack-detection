from flask import Flask, request, jsonify
import joblib
import re
import html
import sqlite3
from datetime import datetime
import requests

# Load ML model
model = joblib.load("attack_final.pkl")

app = Flask(__name__)

SAFE_WORDS = {
    "hi", "hello", "hey", "thanks",
    "thank you", "welcome",
    "good morning", "good evening"
}

USERNAME_PATTERN = r'^[a-zA-Z0-9@._#-]{2,30}$'


# -------------------------
# Get Client IP Address
# -------------------------
def get_client_ip():

    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr

    return ip


# -------------------------
# Get Geo Location
# -------------------------
def get_location(ip):

    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "success":
                return (
                    data.get("country"),
                    data.get("city"),
                    data.get("lat"),
                    data.get("lon")
                )

    except Exception as e:
        print("Location lookup failed:", e)

    return None, None, None, None


# -------------------------
# IP Intelligence (VPN/Proxy)
# -------------------------
def get_ip_intelligence(ip):

    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            data = response.json()
            org = data.get("org", "")

            vpn = False
            proxy = False
            hosting = False

            if "VPN" in org or "DigitalOcean" in org or "Amazon" in org or "Google" in org:
                vpn = True
                hosting = True

            return {
                "org": org,
                "vpn": vpn,
                "proxy": proxy,
                "hosting": hosting
            }

    except Exception as e:
        print("IP intelligence failed:", e)

    return {
        "org": None,
        "vpn": False,
        "proxy": False,
        "hosting": False
    }


# -------------------------
# Log attack
# -------------------------
def log_attack(attack_type, ip_address, payload, confidence):

    country, city, lat, lon = get_location(ip_address)
    intel = get_ip_intelligence(ip_address)

    try:

        conn = sqlite3.connect("attack_logs.db", timeout=10)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attacks (
                timestamp,
                attack_type,
                ip_address,
                payload,
                confidence,
                country,
                city,
                latitude,
                longitude,
                organization,
                vpn,
                proxy,
                hosting
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            attack_type,
            ip_address,
            payload,
            float(confidence),
            country,
            city,
            lat,
            lon,
            intel["org"],
            int(intel["vpn"]),
            int(intel["proxy"]),
            int(intel["hosting"])

        ))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Database log failed:", e)


# -------------------------
# Clean text
# -------------------------
def clean_text(text):

    text = html.unescape(text)
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


# -------------------------
# ML Detection
# -------------------------
def check_input(text):

    text = clean_text(text)

    if text in SAFE_WORDS:
        return "NORMAL", 0.99

    if re.match(USERNAME_PATTERN, text):
        return "NORMAL", 0.99

    probs = model.predict_proba([text])[0]
    pred = probs.argmax()
    prob = probs[pred]

    labels = {
        0: "NORMAL",
        1: "XSS",
        2: "SQL_INJECTION"
    }

    result = labels[pred]

    if result != "NORMAL" and prob < 0.75:
        result = "NORMAL"

    return result, prob


# -------------------------
# Map Statistics
# -------------------------
def generate_attack_map():

    import folium

    conn = sqlite3.connect("attack_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attack_type, latitude, longitude, country, city, vpn, proxy, hosting
        FROM attacks
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
    """)

    rows = cursor.fetchall()

    total = len(rows)
    sql_count = sum(1 for r in rows if r[0] == "SQL_INJECTION")
    xss_count = sum(1 for r in rows if r[0] == "XSS")

    vpn_count = sum(1 for r in rows if r[5] == 1)
    proxy_count = sum(1 for r in rows if r[6] == 1)
    hosting_count = sum(1 for r in rows if r[7] == 1)

    # 🌍 Create world map
    m = folium.Map(location=[20, 0], zoom_start=2)

    for attack_type, lat, lon, country, city, vpn, proxy, hosting in rows:

        # Color based on attack type
        if attack_type == "SQL_INJECTION":
            color = "red"
        else:
            color = "orange"

        folium.CircleMarker(
            location=[float(lat), float(lon)],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"""
            Attack: {attack_type}<br>
            Location: {city}, {country}<br>
            VPN: {vpn}<br>
            Proxy: {proxy}<br>
            Hosting: {hosting}
            """
        ).add_to(m)

    # 💾 Save map
    m.save("templates/attack_map.html")

    conn.close()

    return total, sql_count, xss_count, vpn_count, proxy_count, hosting_count

# -------------------------
# Attack Map Dashboard
# -------------------------
@app.route("/attack-map")
def attack_map():

    total, sql_count, xss_count, vpn_count, proxy_count, hosting_count = generate_attack_map()

    html = open("templates/attack_map.html", encoding="utf-8").read()

    stats_box = f"""
    <div style="
        position:absolute;
        top:10px;
        right:10px;
        width:220px;
        background:white;
        padding:12px;
        border-radius:10px;
        box-shadow:0px 0px 10px rgba(0,0,0,0.25);
        font-family:Arial;
        z-index:9999;
    ">
    <b>Attack Monitor</b><br>
    Total Attacks: {total}<br>
    SQL Injection: {sql_count}<br>
    XSS Attacks: {xss_count}<br>
    <br>
    VPN Attacks: {vpn_count}<br>
    Proxy Attacks: {proxy_count}<br>
    Hosting Attacks: {hosting_count}
    </div>
    """

    

    return html + stats_box


# -------------------------
# Prediction API
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input"}), 400

    username = data.get("username", "")
    password = data.get("password", "")

    ip_address = get_client_ip()

    print("Incoming request from:", ip_address)

    pred_u, conf_u = check_input(username)

    if pred_u != "NORMAL":

        log_attack(pred_u, ip_address, username, conf_u)

        return jsonify({
            "prediction": pred_u,
            "confidence": round(float(conf_u), 3)
        })

    pred_p, conf_p = check_input(password)

    if pred_p != "NORMAL":

        log_attack(pred_p, ip_address, password, conf_p)

        return jsonify({
            "prediction": pred_p,
            "confidence": round(float(conf_p), 3)
        })

    return jsonify({
        "prediction": "NORMAL",
        "confidence": 0.99
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)