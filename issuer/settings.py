from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    ISSUER_BASE_URL: str = os.getenv("ISSUER_BASE_URL", "http://localhost:8000")
    TOKEN_TTL_SECONDS: int = int(os.getenv("TOKEN_TTL_SECONDS", "600"))
    KID: str = os.getenv("KID", "dev-key-1")
    PRIVATE_JWK_PATH: str = os.getenv("PRIVATE_JWK_PATH", "./private_ed25519.jwk.json")
    PUBLIC_JWKS_PATH: str = os.getenv("PUBLIC_JWKS_PATH", "./public_jwks.json")
    CRL_PATH: str = os.getenv("CRL_PATH", "./crl.json")

settings = Settings()
