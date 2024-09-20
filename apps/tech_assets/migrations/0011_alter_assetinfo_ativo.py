# Generated by Django 5.1 on 2024-09-20 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_assets', '0010_alter_movement_data_movimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinfo',
            name='ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assetinfo', to='tech_assets.asset'),
        ),
    ]
