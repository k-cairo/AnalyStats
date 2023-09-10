# Generated by Django 4.2.3 on 2023-08-18 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0012_e5teamranking'),
    ]

    operations = [
        migrations.CreateModel(
            name='E5BttsIframe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=500)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.e5season')),
            ],
            options={
                'verbose_name': 'BTTS Iframe',
                'verbose_name_plural': 'BTTS Iframes',
            },
        ),
    ]
