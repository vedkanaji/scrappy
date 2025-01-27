# Web Scraping on a Schedule with Django & Celery


technologies used:

- Django
- Celery
- Selenium
- Scraped Data to Database via Django
- Reliable Web Scraping with Selenium + Bright Data

## Getting Started

```shell
git clone https://github.com/vedkanaji/scrappy.git
mv Django-Celery-Redis scrape-scheduler
cd scrape-scheduler
```

`macos/linux`

```
python3 -m venv venv
source venv/bin/activate
```

`windows`

```
c:\Python311\python.exe -m venv venv
.\venv\Scripts\activate
```

Install requirements

```shell
python -m pip install pip --upgrade
python -m pip install -r requirements.txt
```

Run a local redis instance via Docker Compose

```shell
docker compose -f compose.yaml up -d
```

This will give us `redis://localhost:6379`

Create `.env` in `src/.env` with:

```shell
CELERY_BROKER_REDIS_URL="redis://localhost:6379"
DEBUG=True
```

Navigate into your Django root:

```shell
cd src/
ls
```

You should see at least `config/` and `manage.py`.

Run your project in 2 terminals:

- `python manage.py runserver`
- `celery -A config worker --beat`
