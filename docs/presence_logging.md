# Presence State Transition Logging (Milestone 3)

## 개요
- 상태: active → idle → stuck → offline → off
- 규칙(문서 기준): 미수신 10분 → offline, 정체 30분 → off
- **데모 모드**: 1초 = 1분으로 간주하여 빠르게 상태 전이 로그 확인

## 사용 예 (PowerShell)
```powershell
# 1회 출력
python -m src.main heartbeat --once --nick "Hyunwoo" --node "ASIA:martlock:portal_n1" --status active

# 데모 모드(1초=1분): 5초 동안 active 유지 후 CTRL+C
python -m src.main heartbeat --nick "Hyunwoo" --node "ASIA:martlock:portal_n1" --status active --demo
```
