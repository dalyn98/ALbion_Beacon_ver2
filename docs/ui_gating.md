# UI Gating Interface (GM-only UI Render Policy)

- Rule: GM UI is **not rendered** unless state==GM_VERIFIED.
- CLI helper (for frontend contract):
  ```powershell
  python -m src.main auth gate --nick "YourNick" --gm "GuildMasterName"
  ```
- Output (JSON):
  ```json
  {
    "state": "SELF_VERIFIED",
    "render_gm_ui": false
  }
  ```
- States: UNKNOWN → SELF_VERIFIED → GM_VERIFIED
