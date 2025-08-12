# API Mock Server (Milestone 3)

내장 HTTP 서버(`http.server`)로 간단한 계약 검증용 목업을 제공합니다. **추가 의존성 없음.**

## 엔드포인트
- `POST /telemetry/heartbeat` → `{ "ok": true }`
- `GET  /auth/status?nick=...&gm=...` → `{ "state": "SELF_VERIFIED"|"GM_VERIFIED" }`
- `POST /guild/verify` (body: `{ "nick": "...", "gm": "..." }`) → `{ "gm": true|false }`
- `POST /location/state` (body: `{ "node_id": "...", ... }`) → `{ "ok": true }`

## 실행 (PowerShell)
```powershell
python -m src.api.mock_server --port 8787
# 새 터미널에서 테스트
curl -s -X POST http://127.0.0.1:8787/telemetry/heartbeat -H "Content-Type: application/json" -d "{\"v\":1,\"ts_ms\":0,\"app\":\"v0\",\"session_id\":\"s\",\"nick_id\":\"n\",\"node_id\":\"ASIA:x:portal\",\"status\":\"active\",\"hb_seq\":0}"
```
