# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import entity.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eId', models.CharField(default=entity.models.getentityId, max_length=200, unique=True)),
                ('entityName', models.TextField(blank=True, null=True)),
                ('domain', models.TextField(blank=True, null=True)),
                ('emailid', models.TextField(blank=True, null=True)),
                ('logo', models.FileField(blank=True, max_length=500, null=True, upload_to=entity.models.get_upload_filepath)),
                ('status', models.TextField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('createdBy', models.TextField(blank=True, null=True)),
                ('modifiedBy', models.TextField(blank=True, null=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='entityUUID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuidNumber', models.BigIntegerField(default=0)),
            ],
        ),
    ]
