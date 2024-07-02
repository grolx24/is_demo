# Generated by Django 4.2.13 on 2024-06-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone', models.CharField(max_length=20)),
                ('user_id', models.IntegerField()),
                ('phone_number', models.CharField(max_length=50)),
                ('call_date', models.DateTimeField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Исходящий'), (2, 'Входящий'), (3, 'Входящий с перенаправлением'), (4, 'Обратный')])),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('add_to_chat', models.IntegerField(blank=True, choices=[(0, 'Не уведомлять'), (1, 'Уведомлять')], null=True)),
                ('call_id', models.CharField(blank=True, max_length=255, null=True)),
                ('show_call', models.IntegerField(choices=[(0, 'Не показывать карточку звонка'), (1, 'Показывать карточку звонка')])),
                ('create_crm', models.IntegerField(choices=[(0, 'Не создавать CRM сущность, связанную со звонком'), (1, 'Создать CRM сущность, связанную со звонком')])),
                ('file', models.FileField(blank=True, null=True, upload_to='rings/')),
            ],
        ),
    ]
