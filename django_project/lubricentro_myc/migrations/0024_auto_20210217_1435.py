# Generated by Django 3.1.3 on 2021-02-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lubricentro_myc', '0023_auto_20201109_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.FloatField(default=0.0),
        ),
    ]
