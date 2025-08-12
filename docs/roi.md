# ROI Label Pack v0.2 — Template & Validation (Milestone 4)

## 템플릿 파일
- `data/ROI_LABELS.template.json` (필수 4개 라벨)
  - 필드: id, label, type, x_pct, y_pct, w_pct, h_pct, locale[], tbd
  - 좌표는 0.0–100.0 (%), 현재는 0.0 placeholder + `"tbd": true`

## 로케일 키워드
- `data/locale_keywords.json` (ko/en)
  - `gm`: 길드마스터 텍스트 후보
  - `nick_labels`, `hud`: 닉네임/HUD 관련 표기 후보

## CLI — 검증/샘플 생성
```powershell
# 검증 (파일 경로 지정, 기본: data/ROI_LABELS.json)
python -m src.main roi validate --file data/ROI_LABELS.template.json

# 샘플 생성(초기 템플릿 사본)
python -m src.main roi sample --out data/ROI_LABELS.sample.json
```
