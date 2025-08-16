from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .keys import ensure_keys, load_public_jwks, load_crl
from .models import IssueRequest, IssueResponse
from .security import issue_token

app = FastAPI(title="OQRP Issuer")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])

ensure_keys()

@app.get("/.well-known/jwks.json")
def jwks():
    return load_public_jwks()

@app.get("/.well-known/oqrp/crl.json")
def crl():
    return load_crl()

@app.post("/api/issue", response_model=IssueResponse)
async def api_issue(req: IssueRequest):
    token, exp = issue_token(url=str(req.url), purpose=req.purpose, ttl=req.ttl_seconds)
    return {"token": token, "expires_at": exp}

@app.get("/")
def root():
    return {"ok": True, "issuer": settings.ISSUER_BASE_URL}
