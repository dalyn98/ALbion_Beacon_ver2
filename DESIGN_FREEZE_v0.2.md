# Design Freeze Package (No Code) v0.2 — SIGNED (2025-08-11)

본 문서는 **코드/명령 없이** 합의 가능한 설계 산출물만을 포함합니다. 모든 항목에 대한 **사전 합의 완료**.

## 1. 범위 & 목표
- UDP 캡처 → 이벤트 추출 → 신원/권한 → 존재(하트비트) → (옵트인) 업로드 파이프라인.

## 2. 기능 요구사항 (FR-01~10)
- FR-01: 본인 닉네임 식별로 SELF_VERIFIED.
- FR-02: 길드마스터=본인 닉 매칭 시 GM_VERIFIED.
- FR-03: GM 전용 UI 비표시(렌더 금지) 규칙.
- FR-04: 온라인 캡처 + pcap 리플레이 지원.
- FR-05: 영역/파티 규모 등 도메인 시그널 추출.
- FR-06: 하트비트 120s, 10m 미수신/30m 정체 시 자동 OFF.
- FR-07: 업로드는 옵트인, 최소 다이제스트만.
- FR-08: 맵=그래프, 노드 차수≤4, Hop≤8.
- FR-09: 리전 분리, 1차 ASIA@Singapore.
- FR-10: 설정 검증 + PII 마스킹.

## 3. 비기능 요구사항 (NFR-01~07)
- NFR-01 성능: 리플레이 5k/min, drop<1% 목표.
- NFR-02 안정성: 오류 격리/레이트 제한 로그.
- NFR-03 프라이버시: 닉네임 마스킹, 무보관.
- NFR-04 보안: 전송 무결성(서명 옵션), 서버 저장 기본 비활성.
- NFR-05 국제화: ko/en 우선, 확장 가능.
- NFR-06 운용성: Npcap 미설치 안내, 설정 오류 메시지.
- NFR-07 유지보수성: 모듈 경계·인터페이스 문서화.

## 4. 아키텍처 개요
Capture Agent, Parser, Signal Extractor, Identity&Role(OCR/API), Presence, UI Gatekeeping, Config, Telemetry(옵트인).

## 5. 데이터 흐름
캡처/리플레이 → 파싱 → 시그널 → 신원/권한 → 하트비트/업로드 → UI 게이팅.

## 6. 인터페이스 요약
- 하트비트 핵심 필드: v, ts_ms, app, session_id, nick_id(masked), node_id, status, hb_seq, sig?.
- 상태머신: UNKNOWN → SELF_VERIFIED → GM_VERIFIED.

## 7. ROI Label Pack v0.2 규격
- 좌표계: 0–100% (x,y,w,h). 소수 1자리 권장.
- 라벨: hud_nick, char_card_nick_self, char_card_nick_other, guild_master_name.
- 로케일: ko/en 우선.

## 8. 보안·프라이버시(위협 모델 요약)
위조 업로드/권한 오판/PII 노출/리플레이 오용 → 서명옵션·임계값·마스킹·로컬용 한정 등 대응.

## 9. 테스트·수용 기준
FR/NFR 기준 시나리오, 성능 지표, 마스킹 로그 샘플, GM UI 비표시 체크리스트.

## 10. 릴리즈·버전 정책
버전 증가 → 변경 기록 → 드래프트 릴리즈. 실제 명령은 개발 단계에서 실행.

## 11. 결정 사항(기본안 채택)
- OCR: 로컬 엔진, 플러그형.
- 임계값 τ=0.80.
- 닉 정규화: Unicode NFKC → trim → 내부 다중 공백 축약 → 소문자 비교(표시는 원형 보존).
- 로케일 확장: ko,en → jp → zh.
- 보관 정책: 서버 저장 없음. 로컬 디버그(옵트인) 24h 순환.
- node_id: REGION:ZONE:PORTAL_ID (slug).
- 최소 해상도: 1280×720 (권장 1920×1080).
- 하트비트 지터: ±10s.
- 오류 언어: ko 우선, en 폴백.
- 접근성: 대비 ≥4.5:1, 색각 안전, 텍스트 ≥12pt.

**Sign‑off:** 2025-08-11 KST — User(Hyunwoo Kim) 승인 / Assistant 기록.
