# Albion Beacon

문서 합의 완료 상태(Design Freeze v0.2 — SIGNED, 2025-08-11)를 바탕으로 생성된 **초기 저장소 스켈레톤**입니다.
현재 단계는 *개발 착수*이며, 코드는 최소 스텁만 포함합니다.

## 개요
- 목적: Albion UDP 트래픽 캡처 → 이벤트 추출 → 신원/권한 확인 → 존재(하트비트) 관리 → (옵트인) 최소 업로드
- 1차 리전: ASIA(싱가포르)
- 프라이버시: 이미지/패킷 무보관, 동명이인 없음, 닉네임 마스킹
- GM 전용 UI: GM이 아니면 **DOM 미렌더링**(비표시)

## 문서
- `CONTEXT.md`: Living Context (프로젝트 목표/제약/릴리즈 요약)
- `DESIGN_FREEZE_v0.2.md`: 합의된 설계(코드 없음), **SIGNED**
- `BACKLOG.md`: 항상-온 백로그 및 주간 스프린트(문서 단계)
- `DECISIONS.md`: 의사결정 로그
- `ROI_LABELS_GUIDE.md`: ROI Label Pack v0.2 규격
- `SECURITY_PRIVACY.md`: 프라이버시/접근성/위협 모델 요약
- `docs/api.md`: API 계약서 목차/초안(문서 단계)

## 개발 시작점
- 파이썬 3.10 (Windows 10/11)
- Npcap 필요(런타임 캡처). 미설치 시 `ab diagnose`에서 안내 메시지 출력.

## 사용법
```bash
# 1) 압축을 풀고 디렉터리로 이동
# 2) Git 초기화 및 최초 커밋
git init
git add .
git commit -m "chore: bootstrap repo (Design Freeze v0.2)"
# 3) 버전 파일 확인
type VERSION  # Windows PowerShell: Get-Content VERSION
# 4) 스켈레톤 실행(도움말/진단)
python -m src.main --help
python -m src.main diagnose
```

---

© 2025. Project Albion Beacon.
