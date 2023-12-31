# Generated by Django 4.2.3 on 2023-08-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0021_e5over05goalsstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_matches_played',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_1h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_1h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_2h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_2h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_bh',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_bh_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='away_over_05_goals_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_matches_played',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_1h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_1h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_2h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_2h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_bh',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_bh_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='home_over_05_goals_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_matches_played',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_1h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_1h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_2h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_2h_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_bh',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_bh_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e5over05goalsstats',
            name='overall_over_05_goals_percent',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
