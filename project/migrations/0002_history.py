# Generated by Django 3.2.3 on 2021-06-11 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(null=True)),
                ('longtitude', models.FloatField(null=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('stalltype', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('hours', models.CharField(blank=True, max_length=300, null=True)),
                ('reco', models.CharField(blank=True, max_length=100)),
                ('details', models.CharField(blank=True, max_length=1000)),
                ('contributor', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
