# Generated by Django 4.2.3 on 2023-09-04 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0035_alter_e5fixture_options_alter_e5fixture_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='e5fixture',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
    ]