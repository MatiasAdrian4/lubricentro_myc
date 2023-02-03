# Generated by Django 4.1.1 on 2022-11-03 11:35

from django.db import migrations

PRODUCT_CODE_SEQUENCE_NAME = "lubricentro_myc_producto_codigo_seq"


def reset_product_code_auto_increment(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            f"SELECT oid FROM pg_class where relname='{PRODUCT_CODE_SEQUENCE_NAME}'"
        )
        if cursor.fetchone():
            cursor.execute(
                f"ALTER SEQUENCE {PRODUCT_CODE_SEQUENCE_NAME} RESTART WITH 100000"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("lubricentro_myc", "0027_productpricehistory"),
    ]

    operations = [migrations.RunPython(reset_product_code_auto_increment)]
