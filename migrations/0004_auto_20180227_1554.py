# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-27 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0003_wettbewerbprinzipiell_slug_prefix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wettbewerbkonkret',
            name='name',
        ),
        migrations.RemoveField(
            model_name='wettbewerbkonkret',
            name='slug',
        ),
    ]
