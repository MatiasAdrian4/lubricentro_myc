# Generated by Django 2.2.3 on 2019-08-03 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lubricentro_myc', '0002_auto_20190714_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]