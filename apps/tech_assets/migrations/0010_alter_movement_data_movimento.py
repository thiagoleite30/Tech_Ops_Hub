# Generated by Django 5.1 on 2024-09-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_assets', '0009_alter_movement_data_movimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='data_movimento',
            field=models.DateTimeField(),
        ),
    ]
