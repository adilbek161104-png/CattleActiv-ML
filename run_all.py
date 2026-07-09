import subprocess
import time
import os
import re
import sys

def kill_port_5000():
    print("Checking if port 5000 is occupied...")
    try:
        output = subprocess.check_output("netstat -ano", shell=True).decode()
        for line in output.splitlines():
            if ":5000 " in line and "LISTENING" in line:
                parts = line.strip().split()
                pid = parts[-1]
                print(f"Killing process {pid} on port 5000")
                subprocess.call(f"taskkill /F /PID {pid}", shell=True)
    except Exception as e:
        print(f"Error killing port 5000: {e}")

def kill_cloudflared():
    print("Killing existing cloudflared instances...")
    subprocess.call("taskkill /F /IM cloudflared.exe", shell=True)

# 1. Cleanup
kill_port_5000()
kill_cloudflared()

# Open log files
flask_log = open("flask.log", "w", encoding="utf-8")
iot_log = open("iot.log", "w", encoding="utf-8")

# 2. Start flask app
print("Starting Flask app...")
# Redirect output to file to prevent buffer blocks
flask_proc = subprocess.Popen([sys.executable, "app.py"], stdout=flask_log, stderr=flask_log)

# Wait a moment for Flask to bind
time.sleep(3)

# 3. Start cloudflared
print("Starting Cloudflare tunnel...")
cf_cmd = [os.path.join(".", "cloudflared.exe"), "tunnel", "--url", "http://127.0.0.1:5000"]
cf_proc = subprocess.Popen(cf_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding="utf-8", errors="ignore")

# 4. Start IoT Simulation
print("Starting IoT Simulator...")
# Redirect output to file to prevent buffer blocks
iot_proc = subprocess.Popen([sys.executable, "simulate_iot_device.py"], stdout=iot_log, stderr=iot_log)

# 5. Extract Cloudflare URL
url = None
start_time = time.time()
print("Extracting Cloudflare tunnel URL...")
while time.time() - start_time < 30:
    line = cf_proc.stdout.readline()
    if not line:
        if cf_proc.poll() is not None:
            print("cloudflared process terminated early.")
            break
        time.sleep(0.5)
        continue
    
    line_str = line.strip()
    print(f"[Cloudflare] {line_str}")
    match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line_str)
    if match:
        url = match.group(0)
        print(f"\nSUCCESS! Tunnel URL: {url}\n")
        with open("tunnel_url.txt", "w") as f:
            f.write(url)
        break

if not url:
    print("Failed to get Cloudflare URL within 30 seconds.")
    remaining = cf_proc.stdout.read(1000)
    print(f"Remaining output: {remaining}")

# Close log files (handles will remain open for the subprocesses until they exit, but Python file objects can be closed)
flask_log.close()
iot_log.close()
