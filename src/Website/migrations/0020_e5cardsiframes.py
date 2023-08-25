# Generated by Django 4.2.3 on 2023-08-19 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0019_e5cornersiframes_e5leaguetableiframe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='E5CardsIframes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('yellow_cards_for_url', models.URLField(max_length=500)),
                ('yellow_cards_against_url', models.URLField(max_length=500)),
                ('red_cards_for_url', models.URLField(max_length=500)),
                ('red_cards_against_url', models.URLField(max_length=500)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.e5season')),
            ],
            options={
                'verbose_name': 'Cards Iframe',
                'verbose_name_plural': 'Cards Iframes',
            },
        ),
    ]
