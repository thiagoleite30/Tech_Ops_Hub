# Generated by Django 5.1 on 2024-08-13 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_assets', '0014_loan_ativos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanasset',
            name='ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset'),
        ),
    ]
