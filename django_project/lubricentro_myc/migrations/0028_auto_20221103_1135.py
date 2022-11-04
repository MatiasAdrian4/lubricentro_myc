# Generated by Django 4.1.1 on 2022-11-03 11:35

from django.db import migrations


def reset_product_code_auto_increment(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT oid FROM pg_class where relname='lubricentro_myc_producto_codigo_seq'"
        )
        if cursor.fetchone():
            cursor.execute(
                "ALTER SEQUENCE lubricentro_myc_producto_codigo_seq RESTART WITH 100000"
            )


class Migration(migrations.Migration):

    dependencies = [
        ("lubricentro_myc", "0027_productpricehistory"),
    ]

    operations = [migrations.RunPython(reset_product_code_auto_increment)]
