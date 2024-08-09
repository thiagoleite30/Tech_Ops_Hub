# Generated by Django 5.1 on 2024-08-09 23:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GPOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_gpos_mtvd_bd', models.IntegerField()),
                ('pos_number', models.IntegerField()),
                ('primary', models.BooleanField(default=True)),
                ('mac_address', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('loja', models.CharField(max_length=100)),
                ('pdv', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_modificacao', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gpos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdv_atual', models.CharField(max_length=100)),
                ('loja_atual', models.CharField(max_length=100)),
                ('novo_pdv', models.CharField(max_length=100)),
                ('fila', models.BooleanField(default=False)),
                ('concluida', models.BooleanField(default=False)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_modificacao', models.DateTimeField(auto_now=True)),
                ('gpos', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request', to='move_gpos.gpos')),
                ('usuario', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
