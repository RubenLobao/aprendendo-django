# aprendendo-django

Projeto de aprendizado do framework Django em Python, com deploy em produção na AWS (EC2 + nginx + uWSGI + systemd).

## Aplicações

| App          | Descrição                                                        |
|--------------|------------------------------------------------------------------|
| `app`        | Configurações do projeto (settings, WSGI, URLs principais)       |
| `accounts`   | Autenticação de usuários (login, logout, registro)               |
| `cars`       | CRUD de carros com forms, signals e templates                    |
| `openai_api` | Integração com a API da OpenAI                                   |

## Stack

- Python 3.14 / Django 6.0
- SQLite em desenvolvimento (`db.sqlite3`); `psycopg2-binary` disponível para PostgreSQL
- uWSGI + nginx para servir a aplicação em produção
- OpenAI API e Pillow (imagens)

## Rodando localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` (e `http://127.0.0.1:8000/admin/` para o admin).

## Deploy em produção (EC2 + nginx + uWSGI + systemd)

Arquitetura: **navegador → nginx (:8000) → socket Unix → uWSGI → Django**

O projeto vive em `/var/www/aprendendo-django` no servidor, com seu próprio `venv`.

### 1. uWSGI

Configuração em `aprendendo-django_wsgi.ini` (neste repositório):

```ini
[uwsgi]
chdir = /var/www/aprendendo-django
module = app.wsgi
home = /var/www/aprendendo-django/venv
master = true
processes = 10
socket = /var/www/aprendendo-django/aprendendo-django.sock
chmod-socket = 666
vacuum = true
```

Teste manual (foreground):

```bash
cd /var/www/aprendendo-django
./venv/bin/uwsgi --socket aprendendo-django.sock --module app.wsgi --chmod-socket=666
```

### 2. nginx

Site em `/etc/nginx/sites-available/aprendendo-django.conf`, com symlink em `sites-enabled`:

```nginx
server {
    listen 8000;
    server_name 34.228.145.82;

    location /static/ {
        alias /var/www/aprendendo-django/static/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///var/www/aprendendo-django/aprendendo-django.sock;
    }
}
```

```bash
sudo ln -sf /etc/nginx/sites-available/aprendendo-django.conf /etc/nginx/sites-enabled/aprendendo-django.conf
python manage.py collectstatic --noinput
sudo nginx -t && sudo /etc/init.d/nginx restart
```

### 3. systemd (inicialização automática)

Service em `/etc/systemd/system/aprendendo-django.service`:

```ini
[Unit]
Description=uWsgi instance to serve aprendendo-django
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/aprendendo-django
ExecStart=/var/www/aprendendo-django/venv/bin/uwsgi --ini /var/www/aprendendo-django/aprendendo-django_wsgi.ini

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now aprendendo-django
sudo systemctl status aprendendo-django
sudo journalctl -u aprendendo-django -f   # logs em tempo real
```

### Comandos úteis no servidor

```bash
sudo systemctl restart aprendendo-django   # após alterar código Python
sudo /etc/init.d/nginx restart             # após alterar config do nginx
python manage.py collectstatic --noinput   # após alterar arquivos estáticos
```

## Estrutura do projeto

```
aprendendo-django/
├── app/                  # settings, wsgi, urls do projeto
├── accounts/             # app de autenticação
├── cars/                 # app de CRUD de carros
├── openai_api/           # client da API da OpenAI
├── media/                # arquivos enviados por usuários
├── static/               # STATIC_ROOT (collectstatic)
├── manage.py
├── aprendendo-django_wsgi.ini
└── requirements.txt
```

## Segurança

- Nunca commite chaves privadas (`.pem`) ou credenciais; mantenha-as fora do repositório via `.gitignore`
- Mantenha `DEBUG = False` no servidor
- Em produção, prefira rodar o uWSGI com um usuário dedicado (`--uid`/`--gid`) em vez de root
