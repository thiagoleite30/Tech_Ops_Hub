# Generated by Django 5.1 on 2024-08-13 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tech_assets', '0005_alter_asset_modelo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='site',
        ),
    ]
