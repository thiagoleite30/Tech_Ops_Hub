# Generated by Django 5.1 on 2024-10-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_persons', '0002_alter_useremployee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='data_registro',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ultima_alteracao',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
