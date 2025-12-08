# %%
import psutil
import tkinter as tk
import threading
import pystray
from plyer import notification
from PIL import Image, ImageDraw
import datetime

# Allowed applications list
ALLOWED_APPS = {"zoom.exe", "teams.exe", "skype.exe"}

# History + state
usage_history = {"camera": [], "microphone": []}
alert_log = []
camera_active = False
mic_active = False

LOG_FILE = "privacy_log.txt"

# ------------------ Logging -------------------
def log_event(message):
    """Write events with timestamp into log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# ------------------ Sensors -------------------
def get_running_processes():
    """Return dict of running processes {pid: name}"""
    processes = {}
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        processes[proc.info['pid']] = proc.info['name'].lower()
    return processes

def check_device_usage():
    running = get_running_processes()
    suspicious = []

    # Simulated: certain apps request camera/mic
    for pid, name in running.items():
        if any(x in name for x in ["chrome", "malware", "zoom", "teams"]):
            suspicious.append(name)
            usage_history["camera"].append(name)
            usage_history["microphone"].append(name)

    return suspicious

# ------------------ Notifications -------------------
def send_notification(title, msg):
    notification.notify(
        title=title,
        message=msg,
        timeout=5
    )

# ------------------ GUI -------------------
class PrivacyGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Privacy Guard – Camera & Microphone Monitor")
        self.root.geometry("600x420")
        self.root.configure(bg="#1e1e1e")

        # Title
        tk.Label(root, text="Privacy Guard", font=("Arial", 18, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=10)

        # Current Activity
        tk.Label(root, text="Currently Active Apps:", font=("Arial", 14, "bold"),
                 fg="#00ffff", bg="#1e1e1e").pack(anchor="w", padx=10)
        self.active_list = tk.Listbox(root, height=5, font=("Consolas", 12),
                                      bg="#252526", fg="white", selectbackground="#007acc")
        self.active_list.pack(fill="x", padx=10, pady=5)

        # Usage History
        tk.Label(root, text="Usage History:", font=("Arial", 14, "bold"),
                 fg="#00ff00", bg="#1e1e1e").pack(anchor="w", padx=10)
        self.history_list = tk.Listbox(root, height=5, font=("Consolas", 12),
                                       bg="#252526", fg="white", selectbackground="#007acc")
        self.history_list.pack(fill="x", padx=10, pady=5)

        # Alerts
        tk.Label(root, text="Alerts / Logs:", font=("Arial", 14, "bold"),
                 fg="#ff5555", bg="#1e1e1e").pack(anchor="w", padx=10)
        self.alerts_list = tk.Listbox(root, height=5, font=("Consolas", 12),
                                      bg="#252526", fg="white", selectbackground="#007acc")
        self.alerts_list.pack(fill="x", padx=10, pady=5)

        # Start monitoring
        self.update_loop()

    def update_loop(self):
        global camera_active, mic_active
        suspicious = check_device_usage()
        self.active_list.delete(0, tk.END)

        if suspicious:
            if not camera_active:
                msg = f"{suspicious[0]} is using the camera"
                send_notification("📷 Camera Active", msg)
                log_event(f"Camera ON - {msg}")
                camera_active = True
            if not mic_active:
                msg = f"{suspicious[0]} is using the mic"
                send_notification("🎤 Microphone Active", msg)
                log_event(f"Microphone ON - {msg}")
                mic_active = True
        else:
            if camera_active:
                send_notification("📷 Camera Off", "Camera is no longer in use")
                log_event("Camera OFF")
            if mic_active:
                send_notification("🎤 Microphone Off", "Microphone is no longer in use")
                log_event("Microphone OFF")
            camera_active = False
            mic_active = False

        for app in suspicious:
            if app in ALLOWED_APPS:
                self.active_list.insert(tk.END, f"✅ {app} (Allowed)")
            else:
                self.active_list.insert(tk.END, f"❌ {app} (Blocked)")
                if app not in alert_log:
                    alert_log.append(app)
                    self.alerts_list.insert(tk.END, f"Blocked: {app}")
                    send_notification("🚨 Privacy Alert", f"{app} blocked from using camera/mic")
                    log_event(f"Blocked {app} from using camera/mic")

        # Update history
        self.history_list.delete(0, tk.END)
        for cam_user in set(usage_history["camera"]):
            self.history_list.insert(tk.END, f"📷 {cam_user}")
        for mic_user in set(usage_history["microphone"]):
            self.history_list.insert(tk.END, f"🎤 {mic_user}")

        self.root.after(3000, self.update_loop)

# ------------------ Tray -------------------
def create_image():
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill=(200, 50, 50))  # camera red dot
    return img

def run_tray(app_root):
    def on_quit(icon, item):
        icon.stop()
        app_root.quit()
    icon = pystray.Icon("privacy_guard", create_image(), "Privacy Guard", 
                        menu=pystray.Menu(pystray.MenuItem("Quit", on_quit)))
    icon.run()

# ------------------ Main -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyGuardApp(root)
    tray_thread = threading.Thread(target=run_tray, args=(root,), daemon=True)
    tray_thread.start()
    root.mainloop()


# %%



