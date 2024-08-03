# Generated by Django 5.0.7 on 2024-08-03 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physicalInterface_id', models.CharField(max_length=100)),
                ('rate', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_id', models.CharField(max_length=100, unique=True)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='LowLevelDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lld_id', models.CharField(max_length=100, unique=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client')),
            ],
        ),
        migrations.CreateModel(
            name='ManagementInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logicalInterface_id', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('vlan', models.IntegerField()),
                ('connectedTo', models.GenericIPAddressField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('physicalInterface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logicalInterfaces_management', to='main.physicalinterface')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface4G',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logicalInterface_id', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('vlan', models.IntegerField()),
                ('connectedTo', models.GenericIPAddressField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('physicalInterface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logicalInterfaces_4g', to='main.physicalinterface')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface3G',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logicalInterface_id', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('vlan', models.IntegerField()),
                ('connectedTo', models.GenericIPAddressField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('physicalInterface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logicalInterfaces_3g', to='main.physicalinterface')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface2G',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logicalInterface_id', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('vlan', models.IntegerField()),
                ('connectedTo', models.GenericIPAddressField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('physicalInterface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logicalInterfaces_2g', to='main.physicalinterface')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RadioSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('lld', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_sites', to='main.lowleveldesign')),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lld', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routers', to='main.lowleveldesign')),
            ],
        ),
        migrations.AddField(
            model_name='physicalinterface',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physicalInterfaces', to='main.router'),
        ),
    ]
