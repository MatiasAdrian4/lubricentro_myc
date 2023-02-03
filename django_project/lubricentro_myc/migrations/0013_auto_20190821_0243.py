# Generated by Django 2.2.3 on 2019-08-21 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lubricentro_myc", "0012_remito_cliente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="remito",
            name="cliente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="lubricentro_myc.Cliente",
            ),
        ),
    ]
