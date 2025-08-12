"""
Albion Beacon CLI — Consolidated (M1..M4)
Includes:
  - auth status|gate (IdentitySM, GM gating)
  - heartbeat (--once | --demo)
  - diagnose (Npcap soft detection)
  - roi validate|sample
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time
import uuid
import os
from typing import Optional, List, Dict, Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERSION_FILE = ROOT / "VERSION"
SETTINGS_FILE = ROOT / "settings.json"


def get_version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"


def load_settings() -> dict:
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[warn] settings.json 로드 실패: {e}")
        return {}


# ---- Identity State Machine ----
class RoleState:
    UNKNOWN = "UNKNOWN"
    SELF_VERIFIED = "SELF_VERIFIED"
    GM_VERIFIED = "GM_VERIFIED"


def _normalize_nick(nick: str) -> str:
    base = " ".join(nick.strip().split())
    return base.lower()


def _sha256_hex(data: str) -> str:
    import hashlib
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _masked_id(nick: str) -> str:
    salt = os.environ.get("AB_SALT", "dev-salt")
    return _sha256_hex(_normalize_nick(nick) + salt)


class IdentitySM:
    def __init__(self, threshold: float = 0.80):
        self.state = RoleState.UNKNOWN
        self.nick: Optional[str] = None
        self.threshold = threshold

    def update_self(self, nick: str, conf: float) -> None:
        if conf >= self.threshold:
            self.nick = nick
            self.state = RoleState.SELF_VERIFIED

    def update_gm(self, gm_name: str, conf: float) -> None:
        if self.state == RoleState.SELF_VERIFIED and self.nick is not None:
            if conf >= self.threshold and _normalize_nick(gm_name) == _normalize_nick(self.nick):
                self.state = RoleState.GM_VERIFIED


# ---- Presence Heartbeat (with demo presence transitions) ----
class PresenceState:
    ACTIVE = "active"
    IDLE = "idle"
    STUCK = "stuck"
    OFFLINE = "offline"
    OFF = "off"


class HeartbeatManager:
    def __init__(self, settings: dict, session_id: Optional[str] = None):
        hb = settings.get("heartbeat", {})
        self.interval = int(hb.get("interval_sec", 120))
        self.miss_off_min = int(hb.get("miss_off_min", 10))
        self.stuck_off_min = int(hb.get("stuck_off_min", 30))
        self.jitter_tol = int(hb.get("jitter_tolerance_sec", 10))
        self.session_id = session_id or str(uuid.uuid4())
        self.seq = 0
        self.presence_state = PresenceState.ACTIVE
        self._last_active_min = 0  # virtual minutes since start

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def build_payload(self, *, app: str, nick: str, node_id: str, status: str) -> dict:
        return {
            "v": 1,
            "ts_ms": self._now_ms(),
            "app": app,
            "session_id": self.session_id,
            "nick_id": _masked_id(nick),
            "node_id": node_id,
            "status": status,
            "hb_seq": self.seq,
        }

    def tick(self, *, app: str, nick: str, node_id: str, status: str) -> dict:
        payload = self.build_payload(app=app, nick=nick, node_id=node_id, status=status)
        self.seq += 1
        if status == PresenceState.ACTIVE:
            # reset inactivity counter and log transition if needed
            prev = self.presence_state
            self._last_active_min = 0
            if prev != PresenceState.ACTIVE:
                print(f"[presence] transition: {prev} -> active")
                self.presence_state = PresenceState.ACTIVE
        return payload

    # demo tick in "virtual minutes"
    def demo_advance_min(self, minutes: int = 1) -> None:
        self._last_active_min += minutes
        # 10m miss → offline
        if self._last_active_min >= self.miss_off_min and self.presence_state != PresenceState.OFFLINE:
            print(f"[presence] transition: {self.presence_state} -> offline (miss {self.miss_off_min}m)")
            self.presence_state = PresenceState.OFFLINE
        # 30m stuck → off
        if self._last_active_min >= self.stuck_off_min and self.presence_state != PresenceState.OFF:
            print(f"[presence] transition: {self.presence_state} -> off (stuck {self.stuck_off_min}m)")
            self.presence_state = PresenceState.OFF


# ---- ROI tools ----
REQUIRED_FIELDS = ["id", "label", "type", "x_pct", "y_pct", "w_pct", "h_pct", "locale"]


def _validate_roi_item(item: Dict[str, Any], i: int) -> List[str]:
    errs: List[str] = []
    for f in REQUIRED_FIELDS:
        if f not in item:
            errs.append(f"[{i}] missing field: {f}")
    if "type" in item and item.get("type") not in {"text", "box"}:
        errs.append(f"[{i}] invalid type: {item.get('type')} (allowed: text|box)")
    for fld in ["x_pct", "y_pct", "w_pct", "h_pct"]:
        v = item.get(fld)
        if not isinstance(v, (int, float)):
            errs.append(f"[{i}] {fld} must be number 0..100")
        else:
            if not (0.0 <= float(v) <= 100.0):
                errs.append(f"[{i}] {fld} out of range: {v}")
    loc = item.get("locale")
    if not isinstance(loc, list) or not all(isinstance(x, str) for x in loc):
        errs.append(f"[{i}] locale must be a string array")
    return errs


def roi_validate(path: pathlib.Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[error] JSON 로드 실패: {e}")
        return 2
    if not isinstance(data, list):
        print("[error] 최상위는 배열이어야 합니다.")
        return 2
    all_errs: List[str] = []
    for i, item in enumerate(data):
        all_errs.extend(_validate_roi_item(item, i))
    if all_errs:
        print("\n".join(all_errs))
        print(f"[fail] {len(all_errs)} error(s)")
        return 1
    print("[ok] ROI_LABELS 검증 통과")
    return 0


def roi_sample(out_path: pathlib.Path) -> int:
    sample = [
        {"id": "hud_nick", "label": "HUD Nickname", "type": "text", "x_pct": 42.0, "y_pct": 6.0, "w_pct": 16.0, "h_pct": 3.0, "locale": ["ko", "en"]},
        {"id": "char_card_nick_self", "label": "Character Card (Self)", "type": "text", "x_pct": 50.0, "y_pct": 50.0, "w_pct": 20.0, "h_pct": 3.0, "locale": ["ko", "en"]},
        {"id": "char_card_nick_other", "label": "Character Card (Other)", "type": "text", "x_pct": 50.0, "y_pct": 55.0, "w_pct": 20.0, "h_pct": 3.0, "locale": ["ko", "en"]},
        {"id": "guild_master_name", "label": "Guild Master Name", "type": "text", "x_pct": 48.0, "y_pct": 58.0, "w_pct": 24.0, "h_pct": 3.0, "locale": ["ko", "en"]},
    ]
    out_path.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] sample written: {out_path}")
    return 0


# ---- Commands ----
def cmd_auth(args: argparse.Namespace) -> int:
    sm = IdentitySM(threshold=0.80)
    if args.subcmd == "status":
        if not args.nick:
            print("[error] --nick 은 필수입니다.")
            return 2
        sm.update_self(args.nick, 1.0)
        if args.gm:
            sm.update_gm(args.gm, 1.0)
        print(f"state={sm.state}")
        print(f"nick_id={_masked_id(args.nick)}")
        return 0
    if args.subcmd == "gate":
        if not args.nick:
            print("[error] --nick 은 필수입니다.")
            return 2
        sm.update_self(args.nick, 1.0)
        if args.gm:
            sm.update_gm(args.gm, 1.0)
        out = {"state": sm.state, "render_gm_ui": sm.state == RoleState.GM_VERIFIED}
        print(json.dumps(out, ensure_ascii=False))
        return 0
    print("Usage: auth status|gate --nick <NICK> [--gm <GM_NAME>]")
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    settings = load_settings()
    app = get_version()
    nick = args.nick or "anonymous"
    node = args.node or "ASIA:unknown:portal_x"
    status = args.status or "active"
    hb = HeartbeatManager(settings=settings)

    if args.once:
        print(json.dumps(hb.tick(app=app, nick=nick, node_id=node, status=status), ensure_ascii=False))
        return 0

    if args.demo:
        print(f"[hb] DEMO mode: 1 sec == 1 min, miss_off={hb.miss_off_min}m, stuck_off={hb.stuck_off_min}m")
        try:
            while True:
                payload = hb.tick(app=app, nick=nick, node_id=node, status=status)
                print(json.dumps(payload, ensure_ascii=False))
                time.sleep(1)           # 1 sec per virtual minute
                hb.demo_advance_min(1)  # advance 1 minute
        except KeyboardInterrupt:
            print("\n[hb] demo stopped")
        return 0

    # normal mode (real interval)
    print(f"[hb] interval={hb.interval}s, jitter±{hb.jitter_tol}s, session_id={hb.session_id}")
    try:
        while True:
            payload = hb.tick(app=app, nick=nick, node_id=node, status=status)
            print(json.dumps(payload, ensure_ascii=False))
            time.sleep(hb.interval)
    except KeyboardInterrupt:
        print("\n[hb] stopped")
    return 0


def cmd_diagnose(args: argparse.Namespace) -> int:
    print(f"[Albion Beacon] Diagnose — version {get_version()}")
    # pcap module
    try:
        import pcap  # type: ignore
        print("pcap module: available")
    except Exception:
        print("pcap module: not found (OK for now)")
    # Npcap soft detection
    candidates = [
        r"C:\Windows\System32\Npcap\Packet.dll",
        r"C:\Windows\System32\Npcap",
        r"C:\Program Files\Npcap",
        r"C:\Program Files (x86)\Npcap",
    ]
    found = False
    for path in candidates:
        if pathlib.Path(path).exists():
            print(f"Npcap: found at {path}")
            found = True
            break
    if not found:
        print("Npcap: not found — please install from https://npcap.com/ (normal installer)")
    return 0


def cmd_roi(args: argparse.Namespace) -> int:
    if args.subcmd == "validate":
        path = pathlib.Path(args.file or "data/ROI_LABELS.json")
        return roi_validate(path)
    if args.subcmd == "sample":
        out = pathlib.Path(args.out or "data/ROI_LABELS.sample.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        return roi_sample(out)
    print("Usage: roi validate|sample [--file X | --out Y]")
    return 2


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ab", description="Albion Beacon CLI")
    sub = p.add_subparsers(dest="command")

    # auth
    p_auth = sub.add_parser("auth", help="인증/권한 상태 & UI 게이팅")
    sub_auth = p_auth.add_subparsers(dest="subcmd")
    p_auth_status = sub_auth.add_parser("status", help="현재 상태 보기")
    p_auth_status.add_argument("--nick", required=False)
    p_auth_status.add_argument("--gm", required=False)
    p_auth_gate = sub_auth.add_parser("gate", help="GM UI 렌더 가능 여부(JSON)")
    p_auth_gate.add_argument("--nick", required=False)
    p_auth_gate.add_argument("--gm", required=False)

    # heartbeat
    p_hb = sub.add_parser("heartbeat", help="하트비트 송신 + 상태 전이 로그")
    p_hb.add_argument("--nick", required=False, help="표시 닉네임(마스킹됨)")
    p_hb.add_argument("--node", required=False, help="node_id (예: ASIA:martlock:portal_n1)")
    p_hb.add_argument("--status", required=False, help="active/idle/stuck/offline/off")
    p_hb.add_argument("--once", action="store_true", help="1회 출력 후 종료")
    p_hb.add_argument("--demo", action="store_true", help="데모모드(1초=1분)")

    # diagnose
    p_diag = sub.add_parser("diagnose", help="환경 진단(Npcap 등)")

    # roi
    p_roi = sub.add_parser("roi", help="ROI Label Pack 도구")
    sub_roi = p_roi.add_subparsers(dest="subcmd")
    p_roi_val = sub_roi.add_parser("validate", help="ROI JSON 검증")
    p_roi_val.add_argument("--file", required=False, help="기본: data/ROI_LABELS.json")
    p_roi_smp = sub_roi.add_parser("sample", help="샘플 JSON 생성")
    p_roi_smp.add_argument("--out", required=False, help="기본: data/ROI_LABELS.sample.json")

    args = p.parse_args(argv)
    if args.command == "auth":
        return cmd_auth(args)
    if args.command == "heartbeat":
        return cmd_heartbeat(args)
    if args.command == "diagnose":
        return cmd_diagnose(args)
    if args.command == "roi":
        return cmd_roi(args)

    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
