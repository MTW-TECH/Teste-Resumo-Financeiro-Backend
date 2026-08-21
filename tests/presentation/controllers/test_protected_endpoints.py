from unittest.mock import Mock

import jwt

from app.domain.entities.company import Company
from app.domain.entities.financial_summary import FinancialSummary
from app.domain.entities.user import User
from tests.conftest import override_provider


def _auth_header(token: str = "valid-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_company_list_success(client, app, token_verifier_mock):
    use_case = Mock()
    use_case.execute.return_value = [
        Company(
            id=1,
            nome="Acme",
            cnpj="00.000.000/0001-00",
            uf="SP",
            cidade="Sao Paulo",
            ativo=True,
            regime_atual="Simples",
        )
    ]

    with override_provider(app.container, "get_company_list_use_case", use_case):
        response = client.get("/v1/company/list", headers=_auth_header())

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "nome": "Acme",
            "cnpj": "00.000.000/0001-00",
            "uf": "SP",
            "cidade": "Sao Paulo",
            "ativo": True,
            "regime_atual": "Simples",
        }
    ]
    use_case.execute.assert_called_once_with()
    token_verifier_mock.verify.assert_called_once_with("valid-token")


def test_company_list_missing_token_returns_401(client):
    response = client.get("/v1/company/list")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Missing bearer token"}


def test_company_list_invalid_token_returns_401(client, token_verifier_mock):
    token_verifier_mock.verify.side_effect = jwt.InvalidTokenError("bad token")

    response = client.get("/v1/company/list", headers=_auth_header("bad-token"))

    assert response.status_code == 401
    assert "Invalid token:" in response.get_json()["error"]


def test_financial_summary_success(client, app, token_verifier_mock):
    use_case = Mock()
    use_case.execute.return_value = FinancialSummary(
        receita="1000",
        custos="400",
        taxas="100",
        lucro_liquido="500",
        ebitda="550",
        lucro="500",
        lajida="550",
        montlyData=[{"mes": "2026-08", "receita": 1000, "custos": 400, "taxa": 100}],
    )

    with override_provider(app.container, "get_financial_summary_use_case", use_case):
        response = client.get("/v1/financial/financialSummary/", headers=_auth_header())

    assert response.status_code == 200
    assert response.get_json() == {
        "receita": "1000",
        "custos": "400",
        "taxas": "100",
        "lucro_liquido": "500",
        "ebitda": "550",
        "lucro": "500",
        "lajida": "550",
        "montlyData": [{"mes": "2026-08", "receita": 1000, "custos": 400, "taxa": 100}],
    }
    use_case.execute.assert_called_once_with()
    token_verifier_mock.verify.assert_called_once_with("valid-token")


def test_financial_summary_missing_token_returns_401(client):
    response = client.get("/v1/financial/financialSummary/")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Missing bearer token"}


def test_financial_summary_invalid_token_returns_401(client, token_verifier_mock):
    token_verifier_mock.verify.side_effect = jwt.InvalidTokenError("bad token")

    response = client.get("/v1/financial/financialSummary/", headers=_auth_header("bad-token"))

    assert response.status_code == 401
    assert "Invalid token:" in response.get_json()["error"]


def test_user_me_success(client, app, token_verifier_mock):
    use_case = Mock()
    use_case.execute.return_value = User(
        id=10,
        name="John Doe",
        email="john@example.com",
        role="admin",
        cognito_sub="cognito-sub-123",
    )

    with override_provider(app.container, "get_current_user_use_case", use_case):
        response = client.get("/v1/user/me", headers=_auth_header())

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 10,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "admin",
        "cognito_sub": "cognito-sub-123",
    }
    use_case.execute.assert_called_once_with(
        cognito_sub="cognito-sub-123",
        email="john@example.com",
        name="John Doe",
    )
    token_verifier_mock.verify.assert_called_once_with("valid-token")


def test_user_me_missing_token_returns_401(client):
    response = client.get("/v1/user/me")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Missing bearer token"}


def test_user_me_invalid_token_returns_401(client, token_verifier_mock):
    token_verifier_mock.verify.side_effect = jwt.InvalidTokenError("bad token")

    response = client.get("/v1/user/me", headers=_auth_header("bad-token"))

    assert response.status_code == 401
    assert "Invalid token:" in response.get_json()["error"]