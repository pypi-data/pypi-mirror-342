import os
from pathlib import Path
from .utils import write_env, print_header

def init_host():
    print_header("🌐 Initializing Host")
    cwd = Path.cwd()
    env_path = cwd / '.env'

    if not env_path.exists():
        print("🛠  No .env found. Creating one...")
        env_vars = {
            'DEBUG': 'false',
            'IS_ON_HOST': 'true',
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

    ssh_key = os.popen("whoami").read().strip() + '@' + os.popen("hostname -I").read().split()[0]
    print(f"\n🔑 Use this on your client machine:\n\n\t{ssh_key}\n")
