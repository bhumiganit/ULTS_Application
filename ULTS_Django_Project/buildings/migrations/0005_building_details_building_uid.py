# Generated by Django 4.0.6 on 2023-04-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0004_rename_serial_number_building_details_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='building_details',
            name='Building_UID',
            field=models.UUIDField(null=True),
        ),
    ]
