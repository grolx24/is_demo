# Generated by Django 4.2.13 on 2024-07-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('data', models.JSONField()),
            ],
        ),
    ]
