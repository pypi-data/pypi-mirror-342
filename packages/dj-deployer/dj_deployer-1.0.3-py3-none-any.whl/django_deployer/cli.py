# Entry: cli.py
import click
from .host import init_host
from .client import init_client
from .deployer import deploy_project

@click.group()
def main():
    """🔥 Django Deployment CLI with remote auto-deploy via SSH."""
    pass

@main.command()
def host_init():
    """Run this on the host to prepare it for deployment."""
    init_host()

@main.command()
def init():
    """Run this on your local machine to configure remote deployment."""
    init_client()

@main.command()
def deploy():
    """Push to GitHub and trigger host to pull and apply updates."""
    deploy_project()
