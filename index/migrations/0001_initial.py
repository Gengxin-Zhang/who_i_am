# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-23 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('one', models.CharField(max_length=100)),
                ('two', models.CharField(max_length=100)),
                ('three', models.CharField(max_length=100)),
                ('four', models.CharField(max_length=100)),
                ('five', models.CharField(max_length=100)),
                ('six', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=20)),
                ('raw_info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Numbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('num', models.IntegerField(default=0)),
            ],
        ),
    ]