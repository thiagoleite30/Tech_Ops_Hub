# Tech Ops Hub

Django Version: 5.1

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.aviva.com.br/thiago.leite/tech-ops-hub.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.aviva.com.br/thiago.leite/tech-ops-hub/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Tech Ops Hub

## Descrição do projeto
Tech Ops Hub é um conjunto de microaplicações destinadas a facilitar as operações do departamento de TI. Ele centraliza a gestão de ativos, usuários e processos, integrando diferentes ferramentas e fluxos para otimizar a gestão e a movimentação de dispositivos de TI.

### Funcionalidades

1. Tech Assets:

    - Gerencia o ciclo de vida de ativos de TI, como notebooks, monitores, celulares, e outros dispositivos.

    - Permite a geração de movimentações, incluindo:

        - Empréstimos: Cadastrar e acompanhar ativos emprestados.
        - Baixas: Registrar a retirada ou o descarte de ativos.
        - Transferências: Gerir a mudança de ativos entre departamentos ou usuários.


2. Tech Persons:

    - Integra dados de associados à plataforma para vinculação com usuários.
    - Gera informações relevantes para documentações de movimentações, como as requisições de empréstimo e transferência.
    - Facilita a gestão de perfis e informações de usuários vinculados aos ativos.


3. Move GPOS:

    - Apresenta um formulário de requisição de movimentação de dispositivos GPOS (terminais de pagamento).
    - O usuário pode solicitar a movimentação dos dispositivos para novos locais.
    - Integra-se com o Power Automate para execução automatizada do fluxo de movimentação.
    - Permite o acompanhamento de solicitações em tempo real.


## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Instalação
Para instalar e executar o projeto localmente, siga os passos abaixo:

### Pré-requisitos
    - Python 3.10 >
    - Django 5.1
    - PostgresSQL (recomendado) 

### Passos para Instalação

#### Clone o repositório

`git clone https://github.com/seu-usuario/tech-ops-hub.git`

#### Acesse o diretório do projeto:

`cd tech-ops-hub`

#### Crie e ative um ambiente virtual:

`python -m venv venv`

`source venv/bin/activate  # Para sistemas Unix`

`venv\Scripts\activate  # Para Windows`

#### Instale as dependências:

`pip install -r requirements.txt`

#### Configure o banco de dados no arquivo settings.py.

#### Aplique as migrações:

`python manage.py migrate`

#### Inicie o servidor de desenvolvimento:

`python manage.py runserver`


## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
