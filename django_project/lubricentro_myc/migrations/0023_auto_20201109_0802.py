# Generated by Django 3.1.3 on 2020-11-09 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lubricentro_myc', '0022_auto_20200216_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
