# README-frontend (Replit 전용)

## 실행
1. `.env.local`에 `VITE_API_BASE=http://127.0.0.1:8787` 설정
2. `npm i && npm run dev`

## 연결되는 엔드포인트(모의)
- `GET /v1/health`
- `POST /v1/auth/gate`
- `POST /v1/heartbeat`
- `GET /v1/events/nearby?hop=8`

## 수용 기준(AC)
- 계약 스키마 준수 (contracts/openapi.yaml, *.schema.json)
- GM 전용 UI는 권한일치 시에만 노출(미권한 시 미표시)
- 503(Npcap 미설치) 시 안내 모달 표시
