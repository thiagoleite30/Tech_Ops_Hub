from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

from apps.tech_assets.models import ConteudoTermo


@receiver(post_migrate)
def cria_grupos_iniciais(sender, **kwargs):
    grupos = ['Administradores', 'Aprovadores TI',
              'Suporte', 'TH', 'Basico', 'Move GPOS']

    for grupo in grupos:
        Group.objects.get_or_create(name=grupo)




@receiver(post_migrate)
def cria_primeira_versao_termo_emprestimo(sender, **kwargs):
    conteudo = f"""
    <p><strong>2. Objeto:</strong></p>
    <p>A EMPRESA concede ao USUÁRIO o empréstimo dos ATIVOS E/OU ACESSÓRIOS e/ou acessórios de tecnologia listados na tela deste termo, doravante denominados "ATIVOS E/OU ACESSÓRIOS".</p>
    </br>
    <p><strong>3. Condições de Uso:</strong></p>
    <ul>
        <li>Os ATIVOS E/OU ACESSÓRIOS emprestados deverão ser utilizados exclusivamente para fins profissionais, em atividades relacionadas às funções desempenhadas pelo USUÁRIO na EMPRESA.</li>
        <li>O USUÁRIO se compromete a zelar pelos ATIVOS E/OU ACESSÓRIOS, mantendo-os em boas condições de uso e conservação.</li>
        <li>Qualquer dano, perda ou roubo dos ATIVOS E/OU ACESSÓRIOS deverá ser comunicado imediatamente à EMPRESA. Em caso de negligência, o USUÁRIO poderá ser responsabilizado por arcar com os custos de reparo ou substituição dos ATIVOS E/OU ACESSÓRIOS.</li>
        <li>
            <strong>Obs.:</strong> Segundo a política operacional <strong>Instalação de Software - POL-093</strong>, “qualquer software que, por necessidade do serviço, necessite ser instalado, deve ser comunicado a GETI, que procederá a instalação caso constate a necessidade do mesmo”.
        </li>
    </ul>
    </br>
    <p><strong>4. Devolução:</strong></p>
     <p>No término do prazo de empréstimo, o USUÁRIO deverá devolver os ATIVOS E/OU ACESSÓRIOS à EMPRESA em perfeitas condições de uso, exceto pelo desgaste natural decorrente do tempo e do uso adequado.</li>
    </br>
    <p><strong>5. Política de Privacidade e Segurança:</strong></p>
    <p>O USUÁRIO se compromete a respeitar todas as políticas de privacidade e segurança da informação estabelecidas pela EMPRESA, abstendo-se de instalar softwares não autorizados ou utilizar os ATIVOS E/OU ACESSÓRIOS para atividades ilegais ou não relacionadas ao trabalho.</p>
    </br>
    <p><strong>6. Termo de Ciência:</strong></p>
    <p>Estou ciente de que, todos os valores de hardware e softwares referentes a depreciação, serão alocadas de acordo com a movimentação dos equipamentos entre áreas. Declaro, ainda, que na qualidade de fiel depositário do equipamento acima descrito, assumo a inteira responsabilidade pela guarda do mesmo e comprometo-me a devolvê-lo em perfeito estado de conservação, após o uso ou por ocasião do rompimento do vínculo empregatício ou rescisão do contrato de prestação de serviços com a AVIVA.</p>
    """

    ConteudoTermo.objects.get_or_create(tipo='emprestimo', conteudo=conteudo, publicar=True)

@receiver(post_migrate)
def cria_primeira_versao_termo_transferencia(sender, **kwargs):
    conteudo = f"""
    <p><strong>2. Confirmação de Recebimento:</strong></p>
    <p>O USUÁRIO confirma, por meio deste, o recebimento dos ativos transferidos e reconhece sua responsabilidade sobre
        o uso, manutenção e eventual devolução dos mesmos, conforme aplicável. Em caso de baixa, o USUÁRIO está ciente
        de que os ativos foram removidos do seu inventário e de suas responsabilidades.</p>
    </br>
    <p><strong>3. Assinatura e Validação:</strong></p>
    <p>Este termo é considerado válido a partir do aceite do USUÁRIO, que confirma ter recebido e compreendido todas as
        condições aqui estabelecidas. A assinatura também serve como comprovação da movimentação dos ativos e da
        aceitação das responsabilidades associadas.</p>
    """

    ConteudoTermo.objects.get_or_create(tipo='transferencia', conteudo=conteudo, publicar=True)    


@receiver(post_migrate)
def cria_primeira_versao_termo_baixa(sender, **kwargs):
    conteudo = f"""
    <p><strong>2. Confirmação de Recebimento:</strong></p>
    <p>O USUÁRIO confirma, por meio deste, o recebimento dos ativos transferidos e reconhece sua responsabilidade sobre
        o uso, manutenção e eventual devolução dos mesmos, conforme aplicável. Em caso de baixa, o USUÁRIO está ciente
        de que os ativos foram removidos do seu inventário e de suas responsabilidades.</p>
    </br>
    <p><strong>3. Assinatura e Validação:</strong></p>
    <p>Este termo é considerado válido a partir do aceite do USUÁRIO, que confirma ter recebido e compreendido todas as
        condições aqui estabelecidas. A assinatura também serve como comprovação da movimentação dos ativos e da
        aceitação das responsabilidades associadas.</p>
    """

    ConteudoTermo.objects.get_or_create(tipo='baixa', conteudo=conteudo, publicar=True)