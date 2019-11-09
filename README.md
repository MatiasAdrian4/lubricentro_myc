# Lubricentro M&C

## Installation

#### Clone Repository
```bash
git clone https://github.com/MatiasAdrian4/lubricentro_myc.git
```
#### Create Environment and Install Dependencies

##### conda
```bash
conda create --name lubricentro_myc python=3.7
conda activate lubricentro_myc
pip install -r requirements.txt
```

##### virtualenv
```bash
virtualenv -p python3 lubricentro_myc
source lubricentro_myc/bin/activate
pip install -r requirements.txt
```

#### Run Migrations and Run Server
```bash
python manage.py migrate
python manage.py runserver
```

#### Migrate Old Database
```bash
python manage.py runscript migrate_old_database
```
