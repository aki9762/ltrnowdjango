# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_users_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='isExtrafield',
            field=models.BooleanField(default=False),
        ),
    ]
