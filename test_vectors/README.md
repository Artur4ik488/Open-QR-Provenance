# Test Vectors

1) Start issuer:
```bash
cd issuer
cp .env.example .env
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

2) Issue a token:
```bash
curl -X POST http://localhost:8000/api/issue   -H "Content-Type: application/json"   -d '{"url":"https://pay.example.org","purpose":"parking-payment"}'
```

3) Copy `token` into `sample_token_ok.txt` and test it in the verifier.
