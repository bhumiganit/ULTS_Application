# Generated by Django 4.0.6 on 2023-04-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building_Details',
            fields=[
                ('Serial_NUmber', models.AutoField(primary_key=True, serialize=False)),
                ('Name_of_Building', models.CharField(max_length=100)),
                ('Location', models.CharField(max_length=100)),
            ],
        ),
    ]
