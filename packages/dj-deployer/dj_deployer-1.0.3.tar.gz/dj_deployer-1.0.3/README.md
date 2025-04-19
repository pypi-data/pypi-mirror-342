# Django Deployer

A universal deployment CLI for Django projects via SSH.

## 🔧 Features
- Git pull
- Upload `.env`
- Run `makemigrations`, `migrate`, `collectstatic`
- Restart services
- Track deploy history (count + timestamp)

## 🚀 Usage

```bash
pip install django-deployer

# Run it from any Django project with a deploy.yaml
django-deploy
