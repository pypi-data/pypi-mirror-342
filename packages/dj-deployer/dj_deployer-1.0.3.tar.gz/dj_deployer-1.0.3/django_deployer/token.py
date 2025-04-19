import os
import json
import uuid
import shutil
from pathlib import Path

# Paths for project root and deploy folder
PROJECT_ROOT = Path(os.getcwd())
DEPLOY_FOLDER = PROJECT_ROOT / ".deploy"
TOKEN_FILE = DEPLOY_FOLDER / "tokens.json"

def init_host():
    """Initialize the host by generating a deploy token and setting up config files."""
    # Ensure .deploy exists
    DEPLOY_FOLDER.mkdir(exist_ok=True)
    
    # Create token
    token = str(uuid.uuid4())
    print(f"Generated token: {token}")

    # Save the token to .deploy/tokens.json
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            tokens = json.load(f)
    else:
        tokens = {}

    tokens[token] = {"user": "host"}  # Can be extended to store more data like time, users, etc.

    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

    print(f"Token saved in {TOKEN_FILE}")

    # Auto-populate .env or .venv paths
    setup_env()

def setup_env():
    """Auto-populate .env with paths and other default values."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path, "a") as f:
            f.write("\n# Auto-configured for deployment\n")
            f.write(f"PROJECT_ROOT={PROJECT_ROOT}\n")
            f.write(f"VENV_PATH={PROJECT_ROOT}/.venv\n")
            f.write("DEPLOY_TOKEN=<your-token-here>\n")
            f.write(f"DEPLOY_DIR={PROJECT_ROOT}/.deploy\n")

def use_token(token):
    """Validate the token and deploy from remote PC."""
    # Validate token
    if not TOKEN_FILE.exists():
        print("No token file found. Please initialize the host first.")
        return

    with open(TOKEN_FILE, "r") as f:
        tokens = json.load(f)

    if token not in tokens:
        print("Invalid token.")
        return

    print(f"Valid token. Deploying with token: {token}")
    # Proceed with deployment logic
    deploy_project()

def deploy_project():
    """Handle the actual deployment process."""
    print("Deploying project...")
    # Add the actual deployment logic here, like pulling updates, running migrations, etc.
