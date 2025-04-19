import yaml
import os
import click

def load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)

def create_config_if_missing(path):
    """Prompt user for deploy info and save to deploy.yaml."""
    click.echo("✨ Let's set up your deployment config:")

    data = {
        'host': click.prompt("SSH host (e.g. user@host.com)"),
        'remote_dir': click.prompt("Remote project path (e.g. /home/user/project)"),
        'branch': click.prompt("Git branch to pull", default='main'),
        'env_file': click.prompt("Path to your .env file", default='.env'),
        'venv_activate': click.prompt("Virtualenv activate command", default='source venv/bin/activate'),
        'django_manage_path': click.prompt("Django manage.py command", default='python manage.py'),
        'restart_command': click.prompt("Command to restart service (leave empty if none)", default='')
    }

    with open(path, 'w') as f:
        yaml.dump(data, f)

    click.echo(f"✅ Config saved to {path}")
