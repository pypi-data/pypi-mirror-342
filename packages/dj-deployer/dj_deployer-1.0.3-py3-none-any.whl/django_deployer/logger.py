import os
from datetime import datetime

VERSION_FILE = "VERSION"

def update_version_log():
    count = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith("deploy_count:"):
                    count = int(line.split(":")[1].strip())

    count += 1
    with open(VERSION_FILE, "w") as f:
        f.write(f"deploy_count: {count}\\n")
        f.write(f"last_deploy: {now}\\n")

    print(f"📘 Deploy #{count} logged at {now}")
