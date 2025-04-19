import subprocess
import yaml
from pathlib import Path
from .utils import print_header

def deploy_project():
    print_header("🚀 Deploying")

    try:
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Git push failed. Resolve errors then try again.")
        return

    config = yaml.safe_load(open("deploy.yaml"))
    ssh = config["ssh"]
    project_path = config["host_project_path"]
    venv_path = config["venv_path"]

    remote_cmd = (
        f"cd {project_path} && "
        f"git pull && "
        f"source {venv_path}/bin/activate && "
        f"python manage.py makemigrations && "
        f"python manage.py migrate && "
        f"python manage.py collectstatic --noinput"
    )

    print("📡 Connecting to host...")
    subprocess.run(["ssh", ssh, remote_cmd])
    print("✅ Deployment complete.")
    