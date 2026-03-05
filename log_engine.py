import os
import time
import random
from datetime import datetime

# ---------------------------------------------------------
# Absolute paths (never break)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "live_app.log")

# ---------------------------------------------------------
# Apache-style log components
# ---------------------------------------------------------
IPS = ["192.168.1.10", "10.0.0.5", "172.16.0.3", "127.0.0.1"]
METHODS = ["GET", "POST", "PUT", "DELETE"]
ENDPOINTS = [
    "/api/login",
    "/api/logout",
    "/api/products",
    "/api/cart",
    "/api/checkout",
    "/api/profile",
    "/api/search",
]
STATUSES = [200, 200, 200, 404, 500]
USER_AGENTS = [
    "Mozilla/5.0",
    "curl/7.68.0",
    "PostmanRuntime/7.28.4",
]

# ---------------------------------------------------------
# Ensure logs directory exists
# ---------------------------------------------------------
def ensure_log_directory():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"[log_engine] Created directory: {LOG_DIR}")

# ---------------------------------------------------------
# Generate a valid Apache access log line
# ---------------------------------------------------------
def generate_log_line():
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    endpoint = random.choice(ENDPOINTS)
    status = random.choice(STATUSES)
    size = random.randint(200, 2000)
    ua = random.choice(USER_AGENTS)

    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S -0600")

    return f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status} {size} "-" "{ua}"\n'

# ---------------------------------------------------------
# Continuous log writer
# ---------------------------------------------------------
def start_log_stream(interval_range=(0.5, 2.0)):
    ensure_log_directory()

    print("[log_engine] Generator writing to:", LOG_FILE)
    print("[log_engine] Starting log stream...\n")

    while True: 
        line = generate_log_line()
        print("[log_engine] Generated:", line.strip())

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())

        time.sleep(random.uniform(*interval_range))

# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    start_log_stream()