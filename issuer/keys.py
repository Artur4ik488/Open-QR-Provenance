from jwcrypto import jwk
import json, os
from .settings import settings

def ensure_keys():
    """Создаёт dev‑ключ, если нет файла PRIVATE_JWK_PATH и PUBLIC_JWKS_PATH."""
    if not os.path.exists(settings.PRIVATE_JWK_PATH):
        key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
        key.update(kid=settings.KID)
        with open(settings.PRIVATE_JWK_PATH, 'w', encoding='utf-8') as f:
            f.write(key.export(private_key=True))
        pub = jwk.JWK.from_json(key.export(private_key=False))
        with open(settings.PUBLIC_JWKS_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps({"keys": [json.loads(pub.export())]}, ensure_ascii=False, indent=2))
    if not os.path.exists(settings.CRL_PATH):
        with open(settings.CRL_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps({"revoked": [], "revoked_kids": []}, ensure_ascii=False, indent=2))

def load_private_key() -> jwk.JWK:
    with open(settings.PRIVATE_JWK_PATH, 'r', encoding='utf-8') as f:
        return jwk.JWK.from_json(f.read())

def load_public_jwks() -> dict:
    with open(settings.PUBLIC_JWKS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_crl() -> dict:
    with open(settings.CRL_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
