# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_users_parentusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
