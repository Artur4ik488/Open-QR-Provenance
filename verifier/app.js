async function fetchJWKS(issuer) {
  const url = new URL('/.well-known/jwks.json', issuer).toString();
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('JWKS fetch failed');
  return res.json();
}

async function fetchCRL(issuer) {
  const url = new URL('/.well-known/oqrp/crl.json', issuer).toString();
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('CRL fetch failed');
  return res.json();
}

function b64urlToUint8(b64url) {
  b64url = b64url.replace(/-/g, '+').replace(/_/g, '/');
  const pad = b64url.length % 4 ? 4 - (b64url.length % 4) : 0;
  return Uint8Array.from(atob(b64url + '='.repeat(pad)), c => c.charCodeAt(0));
}

async function importEd25519KeyFromJWK(jwk) {
  return crypto.subtle.importKey(
    'jwk', jwk, { name: 'Ed25519', namedCurve: 'Ed25519' }, true, ['verify']
  );
}

function parseJWS(compact) {
  const parts = compact.split('.');
  if (parts.length !== 3) throw new Error('Bad JWS format');
  const [h, p, s] = parts;
  const header = JSON.parse(new TextDecoder().decode(b64urlToUint8(h)));
  const payload = JSON.parse(new TextDecoder().decode(b64urlToUint8(p)));
  const signature = b64urlToUint8(s);
  const signingInput = new TextEncoder().encode(`${h}.${p}`);
  return { header, payload, signature, signingInput };
}

async function verifyJWS(jwks, jws) {
  if (jws.header.alg !== 'EdDSA') throw new Error('Unsupported alg');
  const key = (jwks.keys || []).find(k => k.kid === jws.header.kid);
  if (!key) throw new Error('Key not found');
  const cryptoKey = await importEd25519KeyFromJWK(key);
  const ok = await crypto.subtle.verify('Ed25519', cryptoKey, jws.signature, jws.signingInput);
  return ok;
}

function show(el, cls, msg) { el.className = cls; el.textContent = msg; }
function domain(u){ try { return new URL(u).hostname; } catch { return ''; } }

async function verifyToken(compact, issuerBase){
  const jws = parseJWS(compact);
  const now = Math.floor(Date.now()/1000);
  if (jws.payload.exp <= now) throw new Error('Token expired');
  const base = issuerBase || jws.payload.iss;
  const [jwks, crl] = await Promise.all([fetchJWKS(base), fetchCRL(base)]);
  const ok = await verifyJWS(jwks, jws);
  if (!ok) throw new Error('Signature invalid');
  const revoked = (crl.revoked || []);
  if (jws.payload.nonce && revoked.includes(jws.payload.nonce)) throw new Error('Revoked (nonce)');
  if (jws.header.kid && (crl.revoked_kids||[]).includes(jws.header.kid)) throw new Error('Revoked (key)');
  const expected = domain(jws.payload.url);
  if (!expected) throw new Error('Bad url');
  return { payload: jws.payload, expectedDomain: expected };
}

async function main(){
  const tokenEl = document.getElementById('token');
  const issuerEl = document.getElementById('issuer');
  const resultEl = document.getElementById('result');
  document.getElementById('verify').addEventListener('click', async () => {
    try {
      const { payload, expectedDomain } = await verifyToken(tokenEl.value.trim(), issuerEl.value.trim());
      show(resultEl, 'ok', `OK ✔ purpose=${payload.purpose} url=${payload.url} (exp ${payload.exp})`);
    } catch (e) {
      show(resultEl, 'bad', 'NOT VALID ✖ ' + e.message);
    }
  });
}
main();
