# Generated by Django 4.2.3 on 2023-08-19 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0015_e5bttsiframes_btts_bh_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='e5bttsiframes',
            name='type',
        ),
    ]