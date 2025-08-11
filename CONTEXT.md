# CONTEXT — Living Context (All‑in‑One)

**Version:** 2025-08-11  
**Timezone:** Asia/Seoul (UTC+9)

## Goals
- Albion UDP 트래픽 캡처 → 지역/파티 규모 등 핵심 이벤트 자동 추출
- (선택) 실시간 위치 공유, 맵 기반 근접 매칭 보조
- 쉬운 UX: 인터페이스 자동 감지, Npcap 미설치 시 안내, 원클릭 실행

## Constraints / Rules
- 리전: ASIA 우선(싱가포르)
- 프라이버시: 이미지/패킷 무보관, 동명이인 없음
- 맵=그래프(차수≤4), 도메인=도시 포털, Hop≤8
- 위치 공유: 토글 ON/OFF, 하트비트 120s, 10분 미수신/30분 정체 시 자동 OFF
- 인증: HUD 닉 + 본인 정보창 OCR + API 대조, GM=길드 정보창의 ‘길드마스터’로 자동 인증
- GM 전용 UI: 비표시(렌더 자체 미수행)

## Build & Release
- OS: Windows 10/11, Python 3.10, Npcap 필요
- 패키징: PyInstaller (AlbionBeacon.spec)
- 버전: VERSION 파일 수동 증가, 릴리즈는 Draft/Pre-release
- 워크플로: Lint/Health 활성, CI/Release 수동(보류)

## Next Actions(요약)
- ROI 라벨 팩 v0.2 퍼센트 좌표 채움
- 하트비트 및 자동 OFF 로직
- GM 전용 버튼 미표시 분기
- OCR 인증은 보류(정확도 검증 후)

## Quick Commands (문서 단계에 한함)
- 버전 올리기:  echo vX.Y.Z > VERSION && git add VERSION && git commit -m "chore: bump vX.Y.Z"
- 태그:         git tag -a vX.Y.Z -m "Release vX.Y.Z (draft)"
- 빌드:         pyinstaller --clean AlbionBeacon.spec
- 드래프트 릴리즈(gh): gh release create vX.Y.Z --draft --notes "changes..."
