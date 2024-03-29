# Generated by Django 2.2.3 on 2019-08-20 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lubricentro_myc", "0008_auto_20190808_0258"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElementoRemito",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_remito", models.IntegerField()),
                ("cantidad", models.IntegerField()),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lubricentro_myc.Producto",
                    ),
                ),
            ],
        ),
    ]
