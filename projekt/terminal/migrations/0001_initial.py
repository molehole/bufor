# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etykieta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr', models.IntegerField()),
                ('pozycja', models.IntegerField(null=True)),
                ('element', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kolejnosc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tura', models.TextField()),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Pole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pole', models.IntegerField()),
                ('data_dodania', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_wydania', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('szwalnia', models.BooleanField(default=False)),
                ('stolarnia', models.BooleanField(default=False)),
                ('tapicernia', models.BooleanField(default=False)),
                ('szwalnia_ilosc', models.IntegerField(default=1)),
                ('stolarnia_ilosc', models.IntegerField(default=1)),
                ('tapicernia_ilosc', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr', models.IntegerField()),
                ('elementy', models.TextField()),
                ('zakonczone', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr', models.IntegerField()),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Wozek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wozek', models.IntegerField()),
                ('data_dodania', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_wydania', models.DateTimeField(null=True)),
                ('ta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.TA')),
            ],
        ),
        migrations.AddField(
            model_name='ta',
            name='tura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.Tura'),
        ),
        migrations.AddField(
            model_name='status',
            name='ta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.TA'),
        ),
        migrations.AddField(
            model_name='pole',
            name='ta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.TA'),
        ),
        migrations.AddField(
            model_name='etykieta',
            name='ta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.TA'),
        ),
    ]
