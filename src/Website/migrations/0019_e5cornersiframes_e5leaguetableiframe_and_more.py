# Generated by Django 4.2.3 on 2023-08-19 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0018_e5over35goalsiframe_e5over25goalsiframe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='E5CornersIframes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('team_corners_for_1h_url', models.URLField(max_length=500)),
                ('team_corners_against_1h_url', models.URLField(max_length=500)),
                ('team_corners_for_2h_url', models.URLField(max_length=500)),
                ('team_corners_against_2h_url', models.URLField(max_length=500)),
                ('team_corners_for_ft_url', models.URLField(max_length=500)),
                ('team_corners_against_ft_url', models.URLField(max_length=500)),
                ('match_corners_1h_url', models.URLField(max_length=500)),
                ('match_corners_2h_url', models.URLField(max_length=500)),
                ('match_corners_ft_url', models.URLField(max_length=500)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.e5season')),
            ],
            options={
                'verbose_name': 'Corners Iframe',
                'verbose_name_plural': 'Corners Iframes',
            },
        ),
        migrations.CreateModel(
            name='E5LeagueTableIframe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=500)),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.e5season')),
            ],
            options={
                'verbose_name': 'League Table Iframe',
                'verbose_name_plural': 'League Tables Iframes',
            },
        ),
        migrations.DeleteModel(
            name='E5LeagueTable',
        ),
    ]