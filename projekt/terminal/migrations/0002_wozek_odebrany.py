# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wozek',
            name='odebrany',
            field=models.BooleanField(default=False),
        ),
    ]
