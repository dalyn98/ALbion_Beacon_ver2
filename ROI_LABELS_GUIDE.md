# ROI_LABELS_GUIDE v0.2

## 좌표계
- 좌상단 원점, 퍼센트 좌표(x_pct, y_pct, w_pct, h_pct) — 0.0–100.0
- 소수 1자리 권장(예: 42.3)

## 스키마(예시)
```json
{
  "id": "guild_master_name",
  "label": "Guild Master Name",
  "type": "text",
  "x_pct": 42.0,
  "y_pct": 51.2,
  "w_pct": 16.0,
  "h_pct": 3.2,
  "locale": ["ko","en"]
}
```

## 필수 라벨
- hud_nick
- char_card_nick_self
- char_card_nick_other
- guild_master_name
