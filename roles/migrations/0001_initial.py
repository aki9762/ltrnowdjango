# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 11:48
from __future__ import unicode_literals

from django.db import migrations, models
import roles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pId', models.CharField(default=roles.models.getPermId, max_length=200, unique=True)),
                ('entityId', models.TextField(blank=True, null=True)),
                ('roleId', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('permission', models.TextField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('createdBy', models.TextField(blank=True, null=True)),
                ('modifiedBy', models.TextField(blank=True, null=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='perUUID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuidNumber', models.BigIntegerField(default=0)),
            ],
        ),
    ]