# Generated by Django 5.1 on 2024-08-27 19:28

import datetime
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
            name='AssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('descricao', models.TextField(blank=True, max_length=400, null=True)),
            ],
            options={
                'verbose_name': 'Tipo de Ativo',
                'verbose_name_plural': 'Tipos de Ativo',
            },
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('responsavel', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.CharField(unique=True)),
            ],
            options={
                'verbose_name': 'Centro de Custo',
                'verbose_name_plural': 'Centros de Custo',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Fabricante',
                'verbose_name_plural': 'Fabricantes',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('versao', models.CharField(max_length=50)),
                ('licenca', models.CharField(max_length=100)),
                ('data_expiracao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AssetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, max_length=400, null=True)),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tech_assets.assettype')),
                ('fabricante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tech_assets.manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('patrimonio', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('numero_serie', models.CharField(max_length=100, unique=True)),
                ('data_aquisicao', models.DateField(blank=True, null=True)),
                ('valor_aquisicao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('em_uso', 'Em Uso'), ('em_manutencao', 'Em Manutenção'), ('em_estoque', 'Em Estoque'), ('descartado', 'Descartado'), ('separado', 'Separado')], default='em_estoque', max_length=20)),
                ('modelo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech_assets.assetmodel')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech_assets.assettype')),
            ],
            options={
                'verbose_name': 'Ativo',
                'verbose_name_plural': 'Ativos',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True)),
                ('usuario_sessao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_user_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssetCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset')),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('local_pai', models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_locations', to='tech_assets.location')),
            ],
            options={
                'verbose_name': 'Localização',
                'verbose_name_plural': 'Localizações',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='localizacao',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech_assets.location'),
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_manutencao', models.CharField(choices=[('interna', 'Interna'), ('externa', 'Externa')], default='interna', max_length=100)),
                ('data_inicio', models.DateField()),
                ('data_prevista_fim', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('chamado_top_desk', models.CharField(max_length=100)),
                ('chamado_externo', models.CharField(blank=True, max_length=100, null=True)),
                ('descricao', models.TextField()),
                ('custo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.BooleanField(default=True)),
                ('dias_atraso', models.IntegerField(default=0)),
                ('ativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manutenção',
                'ordering': ['-data_inicio'],
            },
        ),
        migrations.CreateModel(
            name='AssetInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memoria', models.CharField(blank=True, max_length=100, null=True)),
                ('armazenamento', models.CharField(blank=True, max_length=100, null=True)),
                ('processador', models.CharField(blank=True, max_length=100, null=True)),
                ('so', models.CharField(blank=True, max_length=100, null=True)),
                ('versao_so', models.CharField(blank=True, max_length=100, null=True)),
                ('licenca_so', models.CharField(blank=True, max_length=100, null=True)),
                ('data_instalacao_so', models.DateField(blank=True, default='', null=True)),
                ('data_garantia', models.DateField(blank=True, default='', null=True)),
                ('endereco_mac', models.CharField(blank=True, max_length=40, null=True)),
                ('ultimo_logon', models.DateField(blank=True, default='', null=True)),
                ('ultimo_scan', models.DateField(blank=True, default='', null=True)),
                ('ativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset')),
                ('fabricante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech_assets.manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('perifericos', 'Periférico(s) (E/S)'), ('mochilas', 'Mochila(s)'), ('carregadores', 'Carregador(es)'), ('cabos', 'Cabo(s)'), ('outros', 'Outro(s)')], max_length=50)),
                ('fabricante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech_assets.manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('transferencia', 'Transferência'), ('emprestimo', 'Empréstimo'), ('baixa', 'Baixa')], default='emprestimo', max_length=50)),
                ('data_movimento', models.DateTimeField(default=datetime.datetime.now)),
                ('data_devolucao_prevista', models.DateTimeField(blank=True, null=True)),
                ('data_devolucao_real', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pendente_aprovacao', 'Aprovação Pendente'), ('em_andamento', 'Em Andamento'), ('concluido', 'Concluído'), ('atrasado', 'Atrasado')], default='pendente_aprovacao', max_length=20)),
                ('chamado_top_desk', models.CharField(default=None, max_length=100)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('centro_de_custo_cedente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cc_send', to='tech_assets.costcenter')),
                ('centro_de_custo_recebedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cc_recept', to='tech_assets.costcenter')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_recept', to=settings.AUTH_USER_MODEL)),
                ('usuario_cedente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_send', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Alocação de Ativo',
                'ordering': ['-data_movimento'],
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_aprovacao', models.CharField(choices=[('aprovado', 'Aprovado'), ('reprovado', 'Reprovado'), ('pendente', 'Pendente')], default='pendente', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_modificacao', models.DateTimeField(auto_now=True)),
                ('data_conclusao', models.DateTimeField(blank=True, null=True)),
                ('aprovador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver', to=settings.AUTH_USER_MODEL)),
                ('movimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approver', to='tech_assets.movement')),
            ],
        ),
        migrations.CreateModel(
            name='MovementAccessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('acessorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.accessory')),
                ('movimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.movement')),
            ],
        ),
        migrations.AddField(
            model_name='movement',
            name='acessorios',
            field=models.ManyToManyField(blank=True, through='tech_assets.MovementAccessory', to='tech_assets.accessory'),
        ),
        migrations.CreateModel(
            name='MovementAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_condition', models.CharField(blank=True, max_length=100, null=True)),
                ('ativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset')),
                ('movimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.movement')),
            ],
        ),
        migrations.AddField(
            model_name='movement',
            name='ativos',
            field=models.ManyToManyField(through='tech_assets.MovementAsset', to='tech_assets.asset'),
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('switch', 'Switch'), ('roteador', 'Roteador'), ('firewall', 'Firewall')], max_length=20)),
                ('endereco_ip', models.GenericIPAddressField()),
                ('mascara_rede', models.CharField(max_length=15)),
                ('ativo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tech_assets.asset')),
            ],
            options={
                'verbose_name': 'Dispositivo de Rede',
                'verbose_name_plural': 'Dispositivos de Rede',
            },
        ),
        migrations.CreateModel(
            name='ReturnTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_devolucao', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('movimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returned', to='tech_assets.movement')),
            ],
        ),
        migrations.CreateModel(
            name='TermRes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_resposta', models.DateTimeField(blank=True, null=True)),
                ('status_resposta', models.BooleanField(default=False)),
                ('aceite_usuario', models.CharField(choices=[('aceito', 'Aceito'), ('pendente', 'Pendente'), ('recusado', 'Recusado')], default='pendente', max_length=100)),
                ('aprovacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='tech_assets.approval')),
                ('movimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resp', to='tech_assets.movement')),
            ],
        ),
    ]
