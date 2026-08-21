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

## Execução

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

## Documentação Swagger (pública)

- UI: `http://localhost:5000/v1/docs/`
- OpenAPI JSON: `http://localhost:5000/v1/docs/openapi.json`

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
