#### Apply new changes in ec2:

```bash
cd django
source lub-myc-env/bin/activate
cd lubricentro_myc
git stash
git pull origin master
git stash pop
rm -rf django_project/static/*
python django_project/manage.py collectstatic
sudo service apache2 restart
```

#### Dump database:
```bash
pg_dump -Fc -v -d lubricentro_myc -h localhost -U matiasadrian4 > lubricentro_myc_12_1_2021.sql
```

#### Generate Swagger Typescript client:
```bash
openapi-generator-cli generate \
    -i ./docs/swagger.yaml \
    -o ./docs/lmyc_client \
    -g typescript-axios \
    --additional-properties=supportsES6=true,npmVersion=6.9.0,typescriptThreePlus=true
```