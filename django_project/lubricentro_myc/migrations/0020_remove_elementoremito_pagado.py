# Generated by Django 2.2.7 on 2019-11-21 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lubricentro_myc", "0019_elementoremito_pagado"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="elementoremito",
            name="pagado",
        ),
    ]
