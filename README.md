# OQRP — Open QR Provenance

Open standard + offline verifier for **signed, time‑bound QR codes** protecting people from offline QR swaps (quishing).

## Why
URL filters don't prove provenance. OQRP proves **who issued the QR** and **whether it's still valid** — privately, offline, <300ms.

## Architecture
- **Issuer (FastAPI)** → JWS (Ed25519), JWKS, CRL
- **Verifier (PWA)** → offline verify, CRL, domain/purpose policies
- **Spec + Test vectors**

## Quick start
```bash
cd issuer && cp .env.example .env && pip install -r requirements.txt
uvicorn app:app --reload --port 8000
# open verifier/index.html (e.g. via: python -m http.server 8080)
```

## Security model
Ed25519, short TTL, CRL (nonce/key), offline-first.

## License
Apache-2.0
