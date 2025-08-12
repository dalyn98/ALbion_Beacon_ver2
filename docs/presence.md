# Presence Heartbeat (Milestone 1)
- 간격: 120s (settings.json), 지터 허용 ±10s
- 자동 OFF: 10m 미수신 / 30m 정체 (문서 기준, 런타임 정책은 추후 서버 연동 시 반영)
- CLI: `python -m src.main heartbeat --once --nick <NICK> --node <NODE> --status active`
