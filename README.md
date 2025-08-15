# ALbion_Beacon_ver2

<<<<<<< HEAD

## Milestone 1 (Presence & Identity) — 2025-08-11
- Presence Heartbeat(120s/±10s), auto OFF(10m/30m) 스켈레톤
- Identity State Machine: UNKNOWN → SELF_VERIFIED → GM_VERIFIED
- CLI: `ab heartbeat` / `ab auth status`
=======
## 로컬 실행(프런트)
- `.env.local`에 `VITE_API_BASE=http://127.0.0.1:8787`

## 동기화 규칙
1) `contracts/` 수정 (단일 진실 소스)
2) `scripts/sync-docs.ps1` 실행 → `docs/` 갱신
3) 코드/프런트 반영 → PR

## 릴리즈
- `scripts/bump-version.ps1 -NewVersion vX.Y.Z`
>>>>>>> 9b20f32 (chore(scaffold): contracts/docs/scripts/CI for Replit sync)
