# Generated by Django 3.1.3 on 2021-05-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lubricentro_myc", "0024_auto_20210217_1435"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="email",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
