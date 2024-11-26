# Documentação de Execução Local e Deploy Produtivo

Este documento descreve os passos necessários para executar o projeto em ambiente local com **FastAPI** e **PostgreSQL**, bem como como fazer o deploy do projeto na **Azure** utilizando **CLI** e **VSCode**. **Docker** não será utilizado para deploy.

## 1. Executar o Projeto Localmente com FastAPI e PostgreSQL

### Pré-requisitos

Antes de rodar o projeto localmente, verifique se as seguintes ferramentas estão instaladas:

- **Python** (versão 3.8 ou superior)
- **PostgreSQL** (instalação local)
- **pip** para gerenciar pacotes Python
- **Alembic** para migrações do banco de dados

### Passo 1: Criar e Ativar o Ambiente Virtual

Antes de instalar as dependências, é necessário criar e ativar o ambiente virtual.

1. **Navegar até o Diretório do Projeto**:

   Antes de criar o ambiente virtual, certifique-se de estar no diretório correto do projeto. Use o comando:
   
   `cd .\desafio03-04\`

2. **Criar o Ambiente Virtual** (caso não tenha feito isso anteriormente):

   - Se estiver utilizando **venv** (pip):
     
     Execute o comando para criar o ambiente virtual:
     
     `python -m venv .venv`

3. **Ativar o Ambiente Virtual**:

   - **Windows**:
     
     Execute o comando:
     
     `.venv\Scripts\activate`

   - **macOS/Linux**:
     
     Execute o comando:
     
     `source .venv/bin/activate`

### Passo 2: Instalar as Dependências

Após ativar o ambiente virtual, instale as dependências do projeto utilizando o gerenciador de pacotes Python (pip):

- Para instalar as dependências, execute:

  `pip install -r requirements.txt`

### Passo 3: Configurar o Banco de Dados PostgreSQL

1. **Instalar o PostgreSQL**:
   
   Caso o PostgreSQL não esteja instalado, faça o download e siga as instruções no [site oficial](https://www.postgresql.org/download/).

2. **Configurar o Banco de Dados**:

   - Crie um banco de dados para o projeto.
   - Configure as variáveis de ambiente para o banco de dados, como **DB_HOST**, **DB_NAME**, **DB_USER**, **DB_PASSWORD**.

3. **Ajustar o `DATABASE_URL` no arquivo `.env`**:

   Dependendo de onde você está rodando o projeto (local ou Docker), é necessário ajustar a variável `DATABASE_URL` no arquivo `.env`.

   - Se estiver rodando localmente, altere o valor para:

     DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@localhost:5432/<nome-do-banco>

   - Se estiver rodando no Docker, altere o valor para:

     DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@db:5432/<nome-do-banco>

   Além disso, ainda no .env, você deve configurar as variáveis de ambiente do `docker-compose.yml` para o PostgreSQL:

   environment:
     - POSTGRES_USER=<usuario>
     - POSTGRES_PASSWORD=<senha>
     - POSTGRES_DB=<nome-do-banco> 

   Isso garantirá que a conexão ao banco de dados no Docker seja feita corretamente, utilizando o serviço `db` como o host do banco de dados.

### Passo 4: Rodar as Migrações do Banco de Dados

No ambiente local, antes de rodar a aplicação, é necessário aplicar as migrações manualmente. Utilize o Alembic para isso.

- Para rodar as migrações manualmente, execute:

  `alembic upgrade head`

Este comando aplicará as migrações necessárias para o banco de dados, atualizando-o para a versão mais recente.

### Passo 5: Rodar o Projeto Localmente

Com as dependências instaladas, as migrações aplicadas e o banco de dados configurado, você pode rodar o projeto localmente com FastAPI:

- Para rodar o servidor localmente, execute:

  `uvicorn app.main:app --reload`

Isso iniciará o servidor FastAPI, geralmente acessível em `http://localhost:8000/docs/`.

---

## 2. Executar o projeto em Docker

### Pré-requisitos

Antes de rodar o projeto em Docker, certifique-se de que as seguintes ferramentas estão instaladas:

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (se necessário)

### Passo 1: Construir as Imagens Docker

No diretório raiz do projeto, construa a imagem Docker usando o comando:

`docker-compose build`

Isso irá construir as imagens Docker conforme definidas no arquivo `docker-compose.yml`.

### Passo 2: Rodar o Projeto com Docker Compose

Com as imagens construídas, você pode iniciar o ambiente com Docker Compose:

`docker-compose up`

Para rodar os containers em segundo plano (modo "detached"), use a opção `-d`:

`docker-compose up -d`

Este comando irá inicializar a aplicação e o banco de dados (PostgreSQL) conforme configurado no `docker-compose.yml`. No caso do ambiente Docker, o comando `docker-compose` já está configurado para rodar as migrações automaticamente.

## Solução para Problemas de Formato de Linha (CRLF para LF)

Quando scripts ou arquivos são criados ou editados em sistemas Windows, eles podem ser salvos com o formato de linha CRLF (`\r\n`), que não é reconhecido corretamente em ambientes Linux, como os utilizados nos containers Docker. Isso pode causar erros como:

`/usr/bin/env: ‘bash\r’: No such file or directory`

Para evitar esses problemas, siga as instruções abaixo para garantir que os arquivos estejam no formato correto (**LF**).

### Identificar e Corrigir o Problema

1. **Identifique o arquivo problemático.**
   O pode ocorrer no script `wait-for-it.sh`.

2. **Converta o arquivo para o formato LF.**

   #### 2.1 Usando `dos2unix`
   Se você tiver acesso a um ambiente Linux/Unix (ou WSL):
   1. Navegue até o diretório onde o arquivo está localizado.
   2. Execute o comando:
      `dos2unix nome_do_arquivo.sh`

   #### 2.2 Usando Visual Studio Code
   1. Abra o arquivo no **VS Code**.
   2. No canto inferior direito, clique onde está escrito `CRLF`.
   3. Selecione a opção `LF`.
   4. Salve o arquivo.

3. **Reconstrua o ambiente Docker.**
   Para garantir que as alterações sejam aplicadas, reconstrua os containers:
   `docker-compose down`
   `docker-compose up --build`

### **Uso do `wait-for-it` no Ambiente Docker**

O `wait-for-it` é utilizado para garantir que o serviço do banco de dados PostgreSQL esteja totalmente disponível antes da aplicação FastAPI ser iniciada. Isso é necessário porque, em ambientes Docker, a ordem de inicialização dos containers não é garantida, e o serviço de banco de dados pode não estar pronto para aceitar conexões no momento em que a aplicação tenta acessá-lo. Ao usar o `wait-for-it`, o processo de inicialização da aplicação é automaticamente adiado até que o banco de dados esteja totalmente operacional, evitando falhas de conexão e melhorando a confiabilidade do deploy. Essa abordagem facilita o gerenciamento da ordem de execução dos serviços no Docker e assegura que a comunicação entre a aplicação e o banco de dados ocorra sem problemas de sincronização.

### Passo 3: Acessar o Banco de Dados

Para acessar o banco de dados PostgreSQL em execução no Docker:

1. **Identifique o nome do container**: Utilize o comando `docker ps` para listar os containers ativos.

2. **Acessar o container do PostgreSQL**: Use o comando `docker exec -it <nome_do_container> bash`.

3. **Acessar o PostgreSQL dentro do container**: Após acessar o container, use o comando `psql -U postgres -d postgres` para acessar o banco de dados PostgreSQL.

4. **Executar Consultas SQL**: Para verificar que o banco de dados já contém dados, execute a seguinte consulta SQL para visualizar os registros da tabela `users`:

   `SELECT * FROM users LIMIT 10;`

   Isso irá retornar os primeiros 10 registros da tabela `users`, caso existam dados pré-populados no banco.

### Passo 4: Parar os Containers

Para parar os containers, use o comando:

`docker-compose down`

Isso irá parar e remover todos os containers, redes e volumes definidos no `docker-compose.yml`.

### Passo 5: Limpar Containers e Volumes (Opcional)

Se você deseja remover os containers e volumes, use:

`docker-compose down -v`

Isso irá limpar os containers e volumes de dados, útil para resetar o banco de dados.

---

## 3. Deploy do Projeto na Azure via CLI

### Pré-requisitos

- **Conta na Azure**: Certifique-se de que você possui uma conta na Azure.
- **Azure CLI**: Acesse [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) e siga as instruções de instalação.
- **Git**: Se ainda não tiver o Git instalado, instale-o [aqui](https://git-scm.com/).

### Passo 1: Fazer Login no Azure

Antes de realizar qualquer operação, é necessário fazer login na Azure usando a CLI:

Execute o comando para login:

`az login`

Isso abrirá uma janela para inserir suas credenciais da Azure.

### Passo 2: Criar um Grupo de Recursos

Se você ainda não tem um grupo de recursos, crie um com o comando:

`az group create --name shipay-app --location eastus`

### Passo 3: Criar o App Service na Azure

Crie um **App Service** para o deploy da aplicação:

`az webapp up --name shipay --resource-group shipay-app --runtime "PYTHON|3.8" --sku B1`

Isso criará um App Service na Azure, configurado para rodar uma aplicação Python.

### Passo 4: Configurar Variáveis de Ambiente

É necessário configurar as variáveis de ambiente para o banco de dados e outras configurações necessárias. Você pode fazer isso diretamente no portal da Azure ou via CLI.

Para adicionar a variável de ambiente no App Service:

`az webapp config appsettings set --name shipay --resource-group shipay-app --settings DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@<HOST_AZURE>:5432/<nome-do-banco>`

### Passo 5: Deploy da Aplicação

Com tudo configurado, você pode realizar o deploy da aplicação utilizando o **Git**. Faça um push da aplicação para o repositório remoto (ou crie um repositório se necessário).

No repositório da sua aplicação, adicione o remote do App Service da Azure:

`git remote add azure https://<USERNAME>@shipay.scm.azurewebsites.net:443/shipay.git`

Agora, envie a aplicação para a Azure com o comando:

`git push azure master`

### Passo 6: Acessar a Aplicação na Azure

Após o deploy ser realizado com sucesso, você pode acessar a aplicação via URL pública fornecida pela Azure, que será algo como:

`https://shipay.azurewebsites.net`

---

## 4. Cobertura de Testes Unitários e de Integração com pytest e TestClient

**Atenção:** Antes de rodar os testes, verifique se a configuração do banco de dados no arquivo `.env` está apontando para o banco de dados local (**localhost**). Caso esteja configurado para o banco do Docker, atualize a variável `DATABASE_URL` para o seguinte valor:

`DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@localhost:5432/<nome-do-banco>`

Certifique-se de que o banco de dados local esteja em funcionamento antes de executar os testes.

---

O projeto utiliza **pytest** e **TestClient** para garantir a qualidade do código por meio de testes automatizados. Para rodar os testes:

1. **Rodar os testes**:

   Para rodar todos os testes do projeto, execute o seguinte comando:

   `pytest`

2. **Verificar a cobertura dos testes**:

   Para verificar a cobertura de testes, execute o seguinte comando:

   `pytest --cov=app`

   Este comando executará os testes e, ao final, mostrará um relatório de cobertura, indicando quais partes do código foram cobertas pelos testes.

3. **Se o diretório não for identificado**:

   Caso você receba um erro informando que o diretório ou módulo não foi encontrado (por exemplo, `ModuleNotFoundError: No module named 'app'`), você pode rodar os testes através do script `run_tests.py`, que ajusta automaticamente o caminho do Python. Execute o seguinte comando:

   `python run_tests.py`

   Isso garantirá que o caminho do projeto seja configurado corretamente antes da execução dos testes.

---

## 5. Teste de Carga com Locust

Para testar a performance e a escalabilidade do sistema, o projeto utiliza a ferramenta **Locust** para realizar testes de carga, simulando múltiplos usuários interagindo com os endpoints do sistema.

### Passos para rodar os testes de carga com Locust:

1. **Rodar o teste de carga**:

   Para rodar o teste de carga com Locust, execute o seguinte comando na raiz do projeto:

   `locust -f app\tests\load\locustfile.py -H http://localhost:8000`

   Onde `locustfile.py` é o arquivo que contém a definição das tarefas e os testes a serem executados pelos usuários simulados.

2. **Configuração do ambiente Locust**:

   Após rodar o comando, o Locust estará disponível na interface web, geralmente em:

   `http://localhost:8089`

   Na interface web, você poderá configurar:
   - **Número de usuários simulados** (quantos usuários você quer que o Locust simule)
   - **Taxa de spawn** (quantos usuários por segundo serão criados)

   Clique em "Start Swarming" para iniciar o teste de carga.

3. **Tarefas Simuladas**:

   O arquivo `locustfile.py` contém as definições das tarefas que os usuários irão executar. No exemplo, temos tarefas como:
   
   - **Obter role por ID**: Envia uma solicitação GET para um endpoint simulando a obtenção de uma role por ID.
   - **Criar usuário**: Envia uma solicitação POST para o endpoint de criação de usuário.

   Essas tarefas são associadas a prioridades e podem incluir verificações de status e manipulação de respostas.

4. **Analisando os Resultados**:

   Após iniciar o teste, a interface web do Locust mostrará diversas métricas em tempo real, como:
   - **Tempo de resposta médio**
   - **Taxa de sucesso e falhas**
   - **Número de requisições por segundo**
   - **Percentis de tempo de resposta** (p. ex., 95% das requisições retornaram em X segundos)

   Essas métricas são úteis para avaliar o desempenho do sistema sob carga e identificar possíveis gargalos ou falhas.

---

## 6. Configuração do Pipeline de Integração Contínua (CI) com GitHub Actions

O projeto utiliza **GitHub Actions** para configurar um pipeline de integração contínua (CI), garantindo que os testes sejam executados automaticamente a cada alteração no código. Abaixo estão os detalhes da configuração do pipeline:

1. **Configuração Geral**:
   O pipeline é acionado em dois cenários:
   - Push no branch `main`.
   - Abertura de pull requests direcionados ao branch `main`.

2. **Ambiente de Execução**:
   - O pipeline é executado em um ambiente Ubuntu (`ubuntu-latest`).
   - Utiliza Python 3.12 como versão padrão.
   - Configura um serviço PostgreSQL (versão 15) para ser utilizado nos testes.

3. **Configuração do Banco de Dados**:
   - O serviço PostgreSQL é configurado com as seguintes credenciais:
     - **Usuário**: `test_user`
     - **Senha**: `test_password`
     - **Banco de Dados**: `test_db`
   - O serviço utiliza as configurações de saúde (`pg_isready`) para garantir que o banco esteja pronto antes da execução dos testes.

4. **Passos do Pipeline**:
   O pipeline realiza as seguintes etapas:
   - **Checkout do Código**:
     Faz o download do código do repositório utilizando a ação `actions/checkout@v3`.
   - **Configuração do Ambiente Python**:
     Configura o Python 3.12 no ambiente utilizando `actions/setup-python@v4`.
   - **Instalação de Dependências**:
     Atualiza o `pip` e instala as dependências definidas no arquivo `requirements.txt`.
   - **Configuração de Variáveis de Ambiente**:
     Exporta a variável `DATABASE_URL`, necessária para que os testes se conectem ao banco PostgreSQL.
   - **Aguardando Inicialização do Banco de Dados**:
     Usa o comando `pg_isready` para garantir que o banco esteja pronto antes de prosseguir.
   - **Execução de Testes**:
     Executa o script `run_tests.py`, utilizando a variável de ambiente `DATABASE_URL`.

---

### Aviso Importante para Ambiente de Desenvolvimento:

- **Em ambiente de desenvolvimento (localhost ou Docker)**, a URL do banco de dados deve ser configurada corretamente no arquivo `.env`, dependendo de onde o ambiente está sendo executado.

  - **Para execução local (localhost)**, a URL do banco deve ser configurada como:

    `DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@localhost:5432/<nome-do-banco>`

  - **Para execução em Docker**, a URL do banco deve ser configurada como:

    `DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@db:5432/<nome-do-banco>`

  Isso assegura que os testes de banco de dados e as consultas realizadas no ambiente de desenvolvimento funcionem corretamente, seja localmente ou dentro de um contêiner Docker.
