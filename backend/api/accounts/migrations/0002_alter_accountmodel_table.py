# Generated by Django 4.1.7 on 2023-03-30 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='accountmodel',
            table='users_table',
        ),
    ]
