import sqlite3
import folium

# Connect to database
conn = sqlite3.connect("attack_logs.db")
cursor = conn.cursor()

# Get attack locations
cursor.execute("""
SELECT attack_type, latitude, longitude, country, city
FROM attacks
WHERE latitude IS NOT NULL
ORDER BY timestamp DESC
""")

rows = cursor.fetchall()

# Create base world map
attack_map = folium.Map(location=[20,0], zoom_start=2)

# Add markers for each attack
for attack_type, lat, lon, country, city in rows:

    popup_text = f"""
    Attack: {attack_type}
    Location: {city}, {country}
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color="red",
        fill=True,
        fill_color="red",
        popup=popup_text
    ).add_to(attack_map)

# Save map
attack_map.save("attack_map.html")

print("Attack map generated: attack_map.html")