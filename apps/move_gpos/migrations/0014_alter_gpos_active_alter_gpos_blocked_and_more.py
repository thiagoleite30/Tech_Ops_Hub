# Generated by Django 5.1 on 2024-09-20 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('move_gpos', '0013_alter_request_data_conclusao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpos',
            name='active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='gpos',
            name='blocked',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='gpos',
            name='is_mac',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='gpos',
            name='last_logon_date',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='Data último logon MV'),
        ),
    ]
