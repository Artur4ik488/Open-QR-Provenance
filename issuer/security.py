import time, json, base64, os
from jwcrypto import jws
from .settings import settings
from .keys import load_private_key

B64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=")

HEADER = {"alg": "EdDSA", "typ": "OQRP", "kid": settings.KID}

def issue_token(url: str, purpose: str, ttl: int | None = None) -> tuple[str, int]:
    iat = int(time.time())
    exp = iat + (ttl or settings.TOKEN_TTL_SECONDS)
    payload = {
        "iss": settings.ISSUER_BASE_URL,
        "iat": iat,
        "exp": exp,
        "purpose": purpose,
        "url": url,
        "nonce": B64(os.urandom(8)).decode(),
    }
    payload_b = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()

    j = jws.JWS(payload_b)
    priv = load_private_key()
    j.add_signature(priv, alg="EdDSA", protected=json.dumps(HEADER))
    token = j.serialize(compact=True)
    return token, exp
