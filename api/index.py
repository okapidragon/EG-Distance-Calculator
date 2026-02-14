from flask import Flask, render_template, request
import os
import math
from word2number import w2n
from num2words import num2words

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        return round((math.acos(math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + 
                     math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
                     math.cos(math.radians(lon2 - lon1))) * 6371), 2)
    except:
        return 0

@app.route("/", methods=["GET", "POST"])
def home():
    output_message = ""
    if request.method == "POST":
        try:
            # 1. Get basic info from form
            eliminated_count = w2n.word_to_num(request.form.get('eliminated'))
            round_num = request.form.get('round_number')
            sl_coords = request.form.get('sl_coords')
            sl_lat = sl_coords.split(',')[0].strip()
            sl_lon = sl_coords.split(',')[1].strip()

            # 2. Process the big list of guesses
            # Expecting format: Username, Location, Coordinates (one per line)
            guesses_raw = request.form.get('guesses').strip().split('\n')
            
            scoreboard = []
            for line in guesses_raw:
                parts = line.split('|') # Using pipe to separate values safely
                if len(parts) < 3: continue
                
                uname, loc, g_coords = parts[0].strip(), parts[1].strip(), parts[2].strip()
                g_lat = g_coords.split(',')[0].strip()
                g_lon = g_coords.split(',')[1].strip()
                
                dist = calculate_distance(g_lat, g_lon, sl_lat, sl_lon)
                scoreboard.append((uname, loc, dist, g_coords))

            # 3. Sort and Generate Results
            scoreboard.sort(key=lambda x: x[2])
            elim_list = scoreboard[-eliminated_count:]
            stay_list = scoreboard[:-eliminated_count]

            # 4. Build the output string (Replaces your print statements)
            output_message += f"**Round {round_num.proper()} End:**\nThese {eliminated_count} people have unfortunaely been eliminated:\n"
            for u, l, d, c in elim_list:
                output_message += f"@{u} - {l} ({c})\n"
            
            output_message += f"\n\These {len(scoreboard)-eliminated_count} are still in:\n"
            for u, l, d, c in stay_list:
                output_message += f"@{u} - {l} ({c})\n"

            output_message += f"\n\n\n\nGAME LOG:\n"
            for u, l, d, c in scoreboard:
                output_message += f"@{u} - {l} ({c}) **{d} km**\n"

        except Exception as e:
            output_message = f"Error: {str(e)}. Please check your input format."

    return render_template("index.html", result=output_message)
