# Generated by Django 2.1.7 on 2019-02-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0003_auto_20190210_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='kommentarliste_erstellen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='veranstaltung',
            name='kommentarliste_erstellen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wettbewerbkonkret',
            name='kommentarliste_erstellen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wettbewerbprinzipiell',
            name='kommentarliste_erstellen',
            field=models.BooleanField(default=False),
        ),
    ]