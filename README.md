# Lubricentro M&C

## Setup

#### Create Environment and Install Dependencies

```bash
virtualenv -p python3.10 lubricentro_myc
source lubricentro_myc/bin/activate
pip install -r django_project/requirements.txt
```

#### Run Migrations and Run Server

```bash
python manage.py migrate
python manage.py runserver
```

## Setup Using Docker

#### Build Image and Run Containers

```bash
docker-compose build
docker-compose up
```

#### Run Migrations

```bash
docker exec -it lubricentro_myc_web_1 python manage.py migrate
```

or

```bash
docker compose run web python manage.py migrate
```
