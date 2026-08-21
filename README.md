# Financial Flask API 

Uma API REST em Flask construída com Clean Architecture (camadas de Domain, Application, Presentation e Infrastructure) e injeção de dependência via [`dependency-injector`](https://python-dependency-injector.ets-labs.org/).

## Estrutura do projeto

```
app/
  domain/            # Entidades e interfaces de repositório (sem dependências de framework)
    entities/
    repositories/
  application/        # Casos de uso orquestrando a lógica de domínio
    use_cases/
  infrastructure/      # Implementações concretas de repositório e container de DI
    repositories/
    containers.py
  presentation/        # Blueprints/controllers Flask (camada HTTP)
    controllers/
config.py
run.py
```

## Endpoints

| Método | Path                              | Descrição                    |
|--------|------------------------------------|-------------------------------|
| GET    | `/v1/financial/financialSummary/`  | Retorna um resumo financeiro  |
| GET    | `/v1/company/list`                 | Retorna a lista de empresas   |
| GET    | `/v1/user/me`                      | Retorna o usuário atual       |
| GET    | `/v1/user/<int:user_id>`           | Retorna um usuário por id     |

> Observação: o endpoint de usuário usa `/v1/user/<id>` (ex.: `/v1/user/1`), pois um id deve ser informado para identificar qual usuário buscar.

## Configuração

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Configuração das variáveis de ambiente

É necessário preencher o arquivo `.env` antes de iniciar a aplicação. Use o arquivo `.env.example` como base:

```bash
cp .env.example .env
```

As principais variáveis utilizadas pela aplicação são:

- `API_VERSION`: define a versão da API e o prefixo utilizado nas rotas. Para usar a versão atual do projeto, mantenha `API_VERSION=v1`. Nesse caso, os endpoints e a documentação Swagger estarão disponíveis sob o prefixo `/v1`, como em `/v1/company/list` e `/v1/docs/`. Ao alterar esse valor, o prefixo das rotas também será alterado.
- `COGNITO_USER_POOL_ID`: identifica o User Pool do Amazon Cognito usado para validar os tokens JWT dos endpoints protegidos. Informe o ID do User Pool correspondente ao ambiente, por exemplo:
- `DOCKERHUB_IMAGE`: informa a imagem da API publicada no Docker Hub, usada pelo ambiente de homologação. Substitua o valor de exemplo pelo nome real da imagem e sua tag.

```env
API_VERSION=v1
COGNITO_USER_POOL_ID=seu_user_pool_id
DOCKERHUB_IMAGE=seu-usuario/financial-flask-api:latest
```

O valor de `COGNITO_USER_POOL_ID` deve ser utilizado junto com a região configurada em `COGNITO_REGION`. Sem um User Pool válido, a autenticação dos endpoints protegidos não funcionará. Reinicie os containers após modificar o arquivo `.env`.

## Execução

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

## Execução com Docker Compose

O arquivo `docker-compose.yml` contém a configuração compartilhada entre os ambientes. Cada estágio possui um arquivo de override que herda essa configuração:

- `docker-compose.dev.yaml`: desenvolvimento, API na porta `5000`.
- `docker-compose.hml.yml`: homologação, API na porta `5001`.
- `docker-compose.prod.yml`: produção, API na porta `5002`.

Certifique-se de que o arquivo `.env` está configurado na raiz do projeto. Para iniciar o ambiente de desenvolvimento, construir a imagem e iniciar a API junto com o banco de dados PostgreSQL, execute:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yaml up --build
```

O ambiente de homologação utiliza a imagem definida em `DOCKERHUB_IMAGE` e não realiza o build local. Para iniciar o ambiente de homologação localmente em primeiro plano:

```bash
docker compose -f docker-compose.yml -f docker-compose.hml.yml up
```

Para iniciar o ambiente de produção em segundo plano:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

A API estará disponível em `http://localhost:5000` no desenvolvimento, `http://localhost:5001` em homologação e `http://localhost:5002` em produção. Para acompanhar os logs do ambiente de desenvolvimento:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yaml logs -f api
```

Para parar e remover os serviços de um ambiente, use os mesmos arquivos informados na inicialização. Exemplo para desenvolvimento:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yaml down
```

## Migrações do banco de dados com Alembic

O projeto utiliza o Alembic para criar e atualizar a estrutura do banco de dados. Depois de iniciar os serviços com o Docker Compose, entre no container da aplicação:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yaml exec api sh
```

Dentro do container, execute a migração até a versão mais recente:

```bash
alembic upgrade head
```

Esse comando cria as tabelas necessárias no banco de dados. Execute-o antes de utilizar os endpoints da API. Para sair do container, use `exit`.

## Documentação Swagger (pública)

Com a aplicação em execução, acesse a documentação pelo navegador:

- Interface Swagger UI: [http://localhost:5000/v1/docs/](http://localhost:5000/v1/docs/)
- Especificação OpenAPI em JSON: [http://localhost:5000/v1/docs/openapi.json](http://localhost:5000/v1/docs/openapi.json)

Na Swagger UI, é possível visualizar os endpoints e executar requisições diretamente. A especificação JSON pode ser usada por ferramentas compatíveis com OpenAPI.

As rotas de documentação são públicas e não são protegidas por JWT. Os endpoints de negócio continuam exigindo um token bearer.

## Testes

Use Docker para executar os testes em um ambiente consistente.

Inicie o serviço de banco de dados:

```bash
docker compose up -d db
```

Execute apenas os testes dos endpoints (`/company/list`, `/financial/financialSummary/`, `/user/me`):

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q tests/presentation/controllers/test_protected_endpoints.py"
```

Execute os testes dos endpoints com cobertura:

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q --cov=app --cov-report=term-missing tests/presentation/controllers/test_protected_endpoints.py"
```

Execute toda a suíte de testes com cobertura:

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q --cov=app --cov-report=term-missing"
```

## Exemplos de requisições

```bash
curl http://localhost:5000/v1/financial/financialSummary/
curl http://localhost:5000/v1/company/list
curl http://localhost:5000/v1/user/1
```
