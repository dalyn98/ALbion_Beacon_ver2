"""
Albion Beacon CLI — Milestone 3
Adds:
  - Presence state-transition logging (demo mode: 1 sec == 1 min)
  - Fix: HeartbeatManager.tick passes correct node_id
"""
from __future__ import annotations
import argparse, json, pathlib, time, uuid, os
from typing import Optional

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

# ---- Presence Heartbeat ----
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
        # presence bookkeeping: treat 'active' as activity
        if status == PresenceState.ACTIVE:
            self._last_active_min = 0
            if self.presence_state != PresenceState.ACTIVE:
                print(f'[presence] transition: {self.presence_state} -> active')
                self.presence_state = PresenceState.ACTIVE
        return payload

    # demo tick in "virtual minutes"
    def demo_advance_min(self, minutes: int = 1) -> None:
        self._last_active_min += minutes
        # 10m miss → offline
        if self._last_active_min >= self.miss_off_min and self.presence_state != PresenceState.OFFLINE:
            print(f'[presence] transition: {self.presence_state} -> offline (miss {self.miss_off_min}m)')
            self.presence_state = PresenceState.OFFLINE
        # 30m stuck → off
        if self._last_active_min >= self.stuck_off_min and self.presence_state != PresenceState.OFF:
            print(f'[presence] transition: {self.presence_state} -> off (stuck {self.stuck_off_min}m)')
            self.presence_state = PresenceState.OFF

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

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ab", description="Albion Beacon CLI")
    sub = p.add_subparsers(dest="command")

    p_auth = sub.add_parser("auth", help="인증/권한 상태 & UI 게이팅")
    sub_auth = p_auth.add_subparsers(dest="subcmd")
    p_auth_status = sub_auth.add_parser("status", help="현재 상태 보기")
    p_auth_status.add_argument("--nick", required=False)
    p_auth_status.add_argument("--gm", required=False)
    p_auth_gate = sub_auth.add_parser("gate", help="GM UI 렌더 가능 여부(JSON)")
    p_auth_gate.add_argument("--nick", required=False)
    p_auth_gate.add_argument("--gm", required=False)

    p_hb = sub.add_parser("heartbeat", help="하트비트 송신 + 상태 전이 로그")
    p_hb.add_argument("--nick", required=False, help="표시 닉네임(마스킹됨)")
    p_hb.add_argument("--node", required=False, help="node_id (예: ASIA:martlock:portal_n1)")
    p_hb.add_argument("--status", required=False, help="active/idle/stuck/offline/off")
    p_hb.add_argument("--once", action="store_true", help="1회 출력 후 종료")
    p_hb.add_argument("--demo", action="store_true", help="데모모드(1초=1분)")

    p_diag = sub.add_parser("diagnose", help="환경 진단(Npcap 등)")

    args = p.parse_args(argv)
    if args.command == "auth":
        return cmd_auth(args)
    if args.command == "heartbeat":
        return cmd_heartbeat(args)
    if args.command == "diagnose":
        return cmd_diagnose(args)

    p.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
