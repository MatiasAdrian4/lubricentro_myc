# Generated by Django 2.2.7 on 2020-02-16 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lubricentro_myc', '0021_elementoremito_pagado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='precio_venta_contado',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='precio_venta_cta_cte',
        ),
        migrations.AddField(
            model_name='producto',
            name='agregado_cta_cte',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='producto',
            name='flete',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='producto',
            name='ganancia',
            field=models.FloatField(default=40.0),
        ),
        migrations.AddField(
            model_name='producto',
            name='iva',
            field=models.FloatField(default=21.0),
        ),
    ]
