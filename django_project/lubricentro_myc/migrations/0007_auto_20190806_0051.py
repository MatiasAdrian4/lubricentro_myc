# Generated by Django 2.2.3 on 2019-08-06 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lubricentro_myc', '0006_auto_20190806_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='codigo_postal',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cuit',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(default='', max_length=13),
        ),
    ]
