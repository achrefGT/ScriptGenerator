# Generated by Django 5.0.7 on 2024-08-03 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='interface2g',
            name='logicalInterface_id',
        ),
        migrations.RemoveField(
            model_name='interface3g',
            name='logicalInterface_id',
        ),
        migrations.RemoveField(
            model_name='interface4g',
            name='logicalInterface_id',
        ),
        migrations.RemoveField(
            model_name='lowleveldesign',
            name='lld_id',
        ),
        migrations.RemoveField(
            model_name='managementinterface',
            name='logicalInterface_id',
        ),
        migrations.RemoveField(
            model_name='physicalinterface',
            name='physicalInterface_id',
        ),
        migrations.RemoveField(
            model_name='radiosite',
            name='site_id',
        ),
        migrations.RemoveField(
            model_name='script',
            name='script_id',
        ),
    ]
