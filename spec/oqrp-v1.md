# OQRP v1 — Signed, Time-Bound QR Tokens (draft)

## Token
- Format: Compact JWS (JOSE), `alg: EdDSA`, `typ: OQRP`.
- Header: `{ alg: "EdDSA", typ: "OQRP", kid: <key-id> }`
- Payload:
  - `iss`: issuer base URL (JWKS at `/.well-known/jwks.json`)
  - `iat`: issued-at (epoch seconds)
  - `exp`: expiry (short TTL)
  - `purpose`: e.g., `parking-payment`, `donation`
  - `url`: expected destination URL/domain
  - `nonce`: base64url random 8 bytes

## Verification
1. parse JWS; 2. fetch JWKS; 3. verify Ed25519; 4. check `exp > now`; 5. policy checks (domain/purpose).

## Revocation (CRL)
`/.well-known/oqrp/crl.json`:
```json
{ "revoked": ["<nonce1>","<nonce2>"], "revoked_kids": ["dev-key-1"] }
```

## Privacy
Offline verification by default (only JWKS/CRL fetched; can be cached).
