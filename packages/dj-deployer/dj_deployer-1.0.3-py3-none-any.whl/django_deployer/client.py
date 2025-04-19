import yaml
from pathlib import Path
from .utils import write_env, print_header

def init_client():
    print_header("💻 Initializing Client")
    cwd = Path.cwd()
    config_path = cwd / 'deploy.yaml'
    env_path = cwd / '.env'

    ssh = input("Paste SSH string from host (e.g. user@1.2.3.4): ")
    host_path = input("Path to project on host (absolute): ")

    deploy_config = {
        'ssh': ssh,
        'host_project_path': host_path,
        'venv_path': f"{host_path}/.venv"
    }

    with open(config_path, 'w') as f:
        yaml.dump(deploy_config, f)

    print("✅ deploy.yaml created.")

    if not env_path.exists():
        print("🛠  No .env found. Creating one...")
        env_vars = {
            'DEBUG': 'true',
            'IS_ON_HOST': 'false',
            'SECRET_KEY': input("SECRET_KEY: "),
            'DB_NAME': input("DB_NAME: "),
            'DB_USER': input("DB_USER: "),
            'DB_PASS': input("DB_PASS: "),
            'DB_PORT': input("DB_PORT [default 3306]: ") or "3306",
            'ALLOWED_HOST_0': input("ALLOWED_HOST_0 [localhost]: ") or "localhost",
            'ALLOWED_HOST_1': input("ALLOWED_HOST_1 [127.0.0.1]: ") or "127.0.0.1"
        }
        write_env(env_path, env_vars)
        print(f"✅ .env created at {env_path}")
    else:
        print("✅ .env already exists.")
