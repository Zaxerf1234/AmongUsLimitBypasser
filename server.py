from flask import Flask, render_template_string, request, send_from_directory, redirect, url_for
import threading
import platform
import sys
import os

def windows_check(): # Detecting android and other systems
    try:
        is_windows = platform.platform()
        if "windows" in is_windows.lower():
            return True
        return False
    except Exception:
        return False

app = Flask(__name__)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icons_dir = resource_path("icons")
os.makedirs(icons_dir, exist_ok=True)

crewmate_roles = ["Engineer", "Guardian Angel", "Scientist", "Tracker", "Noisemaker", "Detective"]
impostor_roles = ["Shapeshifter", "Phantom", "Viper"]
roles = ["ALL"] + crewmate_roles + impostor_roles

submitted_data = None
submitted_data_event = threading.Event()
window = None

role_fields = {
    "Engineer": ["vent_use_cooldown", "max_time_in_vents"],
    "Guardian Angel": ["protect_cooldown", "protection_duration"],
    "Scientist": ["vitals_display_cooldown", "battery_duration"],
    "Tracker": ["tracking_cooldown", "tracking_delay", "tracking_duration"],
    "Noisemaker": ["alert_duration"],
    "Detective": ["suspects_per_case"],
    "Shapeshifter": ["shapeshift_duration", "shapeshift_cooldown"],
    "Phantom": ["vanish_duration", "vanish_cooldown"],
    "Viper": ["dissolve_time"],
}


def uint(val):
    try:
        n = int(val)
    except Exception:
        return 0
    if n < 0: 
        return 0
    if n > 255:
        return 255
    return n

def slug(role: str) -> str:
    return role.lower().replace(" ", "_")

def build_icon_urls():
    urls = {"ALL": None}
    for r in crewmate_roles + impostor_roles:
        base = slug(r)
        for ext in [".png"]:
            candidate = os.path.join(icons_dir, base + ext)
            if os.path.exists(candidate):
                urls[r] = f"/uploads/{base}.png"
                break
            else:
                urls[r] = None  # If missing, show text
    return urls

@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(icons_dir, filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(icons_dir, 'favicon.ico')

@app.route("/", methods=["GET", "POST"])
def index():
    global submitted_data
    if request.method == "POST":
        roles_settings = {}

        # All tab per-role count and chance
        for r in crewmate_roles + impostor_roles:
            roles_settings[r] = {
                "count": uint(request.form.get(f"{slug(r)}_count", "0")),
                "chance": uint(request.form.get(f"{slug(r)}_chance", "0")),
            }

        # Per-role advanced fields
        for role, fields in role_fields.items():
            for f in fields:
                key = f"{slug(role)}_{f}"
                v = uint(request.form.get(key, "0"))
                roles_settings[role][f] = v

        submitted_data = roles_settings

        return redirect(url_for("close"))

    icon_urls = build_icon_urls()
    with open(resource_path("roles.html"), "r", encoding="utf-8") as f:
        html = f.read()

    return render_template_string(html, roles=roles, crewmate_roles=crewmate_roles, impostor_roles=impostor_roles, role_fields=role_fields, icons=icon_urls)

@app.route("/close")
def close():
    global submitted_data_event
    submitted_data_event.set()

    return redirect(url_for("index"))

@app.context_processor
def inject_helpers():
    return dict(slug=slug)

def run(type):
    global submitted_data, submitted_data_event, window

    def data_flag_changed():
        global window

        submitted_data_event.wait()
        print("Data submitted, closing window...")
        if window:
            window.destroy()
            window = None
        submitted_data_event.clear()

    if type == "main":
        app.run(host="127.0.0.1", port=8080)
    elif type == "window":
        server_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False))
        server_thread.daemon = True
        server_thread.start()

        if windows_check():
            import webview
            threading.Thread(target=data_flag_changed, daemon=True).start()
            window = webview.create_window("Roles form", "http://127.0.0.1:8080")
            webview.start()
        else:
            print(f"Webview window unavailable. Open link http://127.0.0.1:8080 in your browser to continue. Make sure your IDE runs in the background and it won't get terminated after switching to another window!")
            	
            data_flag_changed()
            while True:
                if submitted_data: break
        
        return submitted_data

if __name__ == "__main__":
    run("main")