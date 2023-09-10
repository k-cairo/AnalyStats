# Generated by Django 4.2.3 on 2023-08-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0006_alter_e5leaguetable_iframe_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='E5Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('logo', models.URLField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.AddField(
            model_name='e5league',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
