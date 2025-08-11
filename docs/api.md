# API Contract v0.1 (Draft — 문서 단계)

## Endpoints
- POST /telemetry/heartbeat
- GET  /auth/status
- POST /guild/verify
- POST /location/state

## 공통
- JSON, UTF-8
- 오류: 400(스키마), 401/403(권한), 429(레이트), 500(서버)

## heartbeat (예시 페이로드 필드)
- v, ts_ms, app, session_id, nick_id(masked), node_id, status, hb_seq, sig?
