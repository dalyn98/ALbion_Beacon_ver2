# ALbion_Beacon_ver2 — 협업 핸드북

## 문서 자동화 원칙
- 계약은 `contracts/`가 원본(Single Source of Truth)입니다.
- `docs/`는 스크립트로 재생성되어 항상 최신 계약을 반영합니다.

## 디렉터리 규약
- `contracts/`: OpenAPI, JSON Schema
- `docs/`: 사람이 읽는 가이드/핸드북/릴리즈 노트
- `scripts/`: 동기화/버전/검증 스크립트 (PowerShell 우선)
- `.github/`: PR/이슈 템플릿, CI 워크플로우

## 작업 브랜치
- main: 안정 릴리즈
- dev: 통합 개발
- feat/ui-<slug>: Replit UI 작업
- feat/api-<slug>: 백엔드 계약/엔드포인트 작업

## 커밋/PR
- 커밋: `feat(ui): ...`, `fix(api): ...`, `docs: ...`
- PR 체크: 빌드/테스트 통과, 계약 준수, 스크린샷 1장 첨부

## Replit 환경 변수
- VITE_API_BASE=http://127.0.0.1:8787
