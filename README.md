# ⏳ TimeLock Vault

> [TimeLock Vault](https://t.rt0.me/)

Server-side time-lock file encryption. Files are sealed with AES-256-GCM.
The decryption key lives on the server and is **released only after the unlock date**.

---

## Quickstart

### curl

```bash
# encrypt — default 1month
curl -T file.txt t.rt0.me/en -o file.txt.tlp

# encrypt — custom duration
curl -T file.txt t.rt0.me/en/1year -o file.txt.tlp

# decrypt
curl -T file.txt.tlp t.rt0.me/de -o file.txt
```

### CLI

```bash
python enc.py file.txt                                    # 1month default
python enc.py file.txt 1year
python enc.py file.txt 2weeks --server https://domain.com

python dec.py file.txt.tlp
python dec.py file.txt.tlp --server https://domain.com
```

---

## Available Durations

★ Default when no duration specified

| Token     | Duration    |
|-----------|-------------|
| `1h`      | 1 hour      |
| `2h`      | 2 hours     |
| `6h`      | 6 hours     |
| `12h`     | 12 hours    |
| `1d`      | 1 day       |
| `3d`      | 3 days      |
| `1week`   | 1 week      |
| `2weeks`  | 2 weeks     |
| `1month`  | 30 days ★   |
| `3months` | 90 days     |
| `6months` | 180 days    |
| `1year`   | 365 days    |

---

## API Reference

### `PUT /en[/<duration>]`

Encrypt a file and store its key in the vault.

**Request:**
- Body: raw file bytes
- Header `X-Filename`: original filename (optional)

**Response:** `.tlp` file (JSON blob)

**Response headers:**
- `X-Unlock-At`: unix timestamp
- `X-Unlock-ISO`: ISO 8601 datetime
- `X-Duration`: duration token used

---

### `PUT /de`

Attempt to decrypt a `.tlp` file.

**Request:**
- Body: `.tlp` file bytes

**Responses:**

| Code  | Meaning                                  |
|-------|------------------------------------------|
| `200` | Decrypted — body is original file bytes  |
| `423` | Locked — body is JSON countdown          |
| `400` | Malformed `.tlp` file                    |
| `403` | Integrity check failed (tampered file)   |
| `404` | Key not found (server reset?)            |

**423 JSON body:**
```json
{
  "error": "🔒 Locked",
  "message": "This file unlocks in 47d 3h 22m",
  "unlock_at": 1798761600,
  "unlock_iso": "2027-01-01T00:00:00+00:00",
  "remaining_seconds": 4079340,
  "remaining_human": "47d 3h 22m"
}
```

### `GET /health`

**Responses:**
```json
{
  "ok": true,
  "ts": 1710000000
}
```

---

## .tlp File Format

```json
{
  "v": 1,
  "id": "key_id_on_server",
  "unlock_at": 1798761600,
  "unlock_iso": "2027-01-01T00:00:00+00:00",
  "original": "secret.pdf",
  "nonce": "<base64 AES-GCM nonce>",
  "ct": "<base64 ciphertext>",
  "_sig": "<32-char integrity hash>"
}
```

The `.tlp` file contains **only the ciphertext** and a key reference ID.
The actual AES-256 key lives only on the server.

---


## Deploy

### 1. Clone & configure

```bash
cp .env.example .env
# edit .env — set DOMAIN
```

### 2. Point your DNS

```
example.com  →  your server IP
```

### 3. Run

```bash
docker compose up -d
```

Routes:

```
GET  /              → main UI (Jinja template)
GET  /health        → {"ok": true, "ts": ...}

PUT  /en            → encrypt (default: 1month)
PUT  /en/1year      → encrypt with duration
PUT  /en/file.txt   → encrypt (curl -T auto filename)
PUT  /en/1year/f.txt→ encrypt (duration + filename)

PUT  /de            → decrypt
PUT  /de/file.tlp   → decrypt (curl -T auto filename)
```

---

## Security Notes

- Keys are stored in SQLite on the server — back it up, don't delete `vault.db` before files unlock.
- `SERVER_SECRET` signs all `.tlp` files — set it once, never change it.
- The server sees plaintext briefly during encryption (in memory, over HTTPS).
- For maximum security, self-host so you control the key vault entirely.