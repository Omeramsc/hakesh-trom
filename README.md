# hakesh-trom
This project aims to technologize the knock-on-the-door fund-raising practice!


## Run locally

### Prerequisite

* [Python 3.X](https://www.python.org/downloads/windows/)
* pip
* [Postgres](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows)

### How to run without Heroku

```bash
# Install requirements
pip install -r requirements.txt

# Run the server
python app.py
```

### How to run with Heroku

> This is the preferred method

Make sure you installed [Heroku](https://cli-assets.heroku.com/heroku-x64.exe) before hand.

```bash
heroku local web -f Procfile.windows
```

## Local DB

## Fix issues
* Use py3.7
* Add pg to PATH

### Create new migration
```bash
set "APP_SETTINGS=config.DevelopmentConfig" && set "DATABASE_URL=postgresql://localhost/hakes_trom?user=postgres&password=Aa123456" && python manage.py db migrate
```

### Update local DB
```bash
set "APP_SETTINGS=config.DevelopmentConfig" && set "DATABASE_URL=postgresql://localhost/hakes_trom?user=postgres&password=Aa123456" && python manage.py db upgrade 
```

### View local DB
```bash
psql -U postgres
```