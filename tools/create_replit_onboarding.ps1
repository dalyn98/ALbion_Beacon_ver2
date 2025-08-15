# 파일: tools/create_replit_onboarding.ps1
param(
  [string]$DocPath = "docs/REPLIT_ONBOARDING.md"
)

# 폴더 준비
New-Item -ItemType Directory -Path "docs" -ErrorAction SilentlyContinue | Out-Null

# 중요: 여기서부터 Here-String 시작. 시작표식 @' 과 종료표식 '@ 는 반드시 줄 맨 앞(컬럼1)!
$Content = @'
# ALbion_Beacon_ver2 — Replit 온보딩 & 협업 가이드

**버전:** 2025-08-13
**작성자:** Hyunwoo Kim (프로젝트 오너)
**역할 분담:**
- **Hyunwoo(오너)**: 기능 우선순위 결정, 요구사항 전달, 릴리즈 승인
- **[설계 담당]**: 설계·품질·계약 관리, GitHub→Replit 동기화
- **Replit 팀**: 실행·프리뷰 제공, UI 검증, 데모 운영

## 1. 프로젝트 개요
- 로컬(Npcap) 에이전트 → API(백엔드) → 웹 대시보드(프론트)
- 주요 기능: Heartbeat / Gate / ROI Validate
- Replit에서는 **실데이터 금지**, Synthetic 데이터만 사용

## 2. 협업 방식
- **GitHub = 단일 사실 원천(SoT)**, Replit은 미러/실행 전용(웹 IDE 편집 금지)
- 계약 파일: `CONTRACT/api.schema.v0.2.json`, `CONTRACT/ui.rules.v0.2.md`, `CONTRACT/contract.lock.json`
- 서버 메타: `GET /__meta` → VERSION & 계약 해시 노출

## 3. UI 규칙(핵심)
- GM 전용 버튼은 **DOM 렌더링 자체 금지**(disabled 금지)
- 권한 없음 알림 토스트 금지

## 4. API 계약 (v0.2 예시)
POST /api/heartbeat
{
  "nick": "Hyunwoo",
  "region": "ASIA-SG",
  "ts": 1723500000.123,
  "demo": true
}

GET /api/gate?nick=Hyunwoo&guild_master=true
{
  "ok": true,
  "gm": true
}

## 5. 작업 흐름
GitHub 변경 → CI 통과 → Replit 미러 → `/__meta` 해시 일치 확인 → 프리뷰 URL 공유

## 6. 요청/피드백 템플릿
[요청 유형] 기능 추가 / UI 수정 / 버그
[설명] 무엇을, 왜, 어떻게
[기대 동작] 시나리오
[관련 API/계약] 파일/엔드포인트
[완료 목표일] YYYY-MM-DD

## 7. 첫 요청(프로젝트 시작 시)
- Backend:
  - POST /api/heartbeat (api.schema.v0.2.json)
  - GET  /api/gate      (ui.rules.v0.2.md)
  - GET  /__meta        (VERSION, 해시)
- Frontend: GM 버튼 DOM 미표시
- 데이터: Synthetic heartbeat 5초 간격 → 대시보드 표시
- 결과물: 프리뷰 URL + 스크린샷/영상 + 변경 요약
- 검증: `/__meta` 해시 == `CONTRACT/contract.lock.json`

<!-- AUTO-SECTION:CHANGELOG START -->
_자동 생성 영역 — commit 시 갱신됨_
<!-- AUTO-SECTION:CHANGELOG END -->
'@

# 저장 (UTF8)
Set-Content -Path $DocPath -Value $Content -Encoding UTF8

Write-Host "[ok] $DocPath 생성 완료"
