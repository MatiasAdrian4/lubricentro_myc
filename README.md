# Lubricentro M&C

## Instalación

#### Clonar Repositorio
```bash
git clone https://github.com/MatiasAdrian4/lubricentro_myc.git
```
#### Crear Ambiente e Instalar Dependencias

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

#### Correr Migraciones y Levantar el Servidor
```bash
python manage.py migrate
python manage.py runserver
```

#### Migrar Antigua Base de Datos
```bash
python manage.py runscript migrate_old_database
```