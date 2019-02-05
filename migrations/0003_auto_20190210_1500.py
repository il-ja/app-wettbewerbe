# Generated by Django 2.1.4 on 2019-02-10 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0002_auto_20181207_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='kommentarliste',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_Tag', to='Kommentare.Liste'),
        ),
        migrations.AlterField(
            model_name='veranstaltung',
            name='kommentarliste',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_Veranstaltung', to='Kommentare.Liste'),
        ),
        migrations.AlterField(
            model_name='wettbewerbkonkret',
            name='kommentarliste',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_WettbewerbKonkret', to='Kommentare.Liste'),
        ),
        migrations.AlterField(
            model_name='wettbewerbprinzipiell',
            name='kommentarliste',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_WettbewerbPrinzipiell', to='Kommentare.Liste'),
        ),
    ]
