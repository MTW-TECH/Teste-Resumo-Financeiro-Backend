import jwt
from jwt import PyJWKClient


class CognitoTokenVerifier:

    def __init__(self, user_pool_id: str, region: str) -> None:
        self._issuer = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        self._jwk_client = PyJWKClient(f"{self._issuer}/.well-known/jwks.json")

    def verify(self, token: str) -> dict:
        signing_key = self._jwk_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=self._issuer,
            options={"verify_aud": False},
        )
        if claims.get("token_use") != "id":
            raise jwt.InvalidTokenError("Token is not a Cognito ID token")
        return claims
