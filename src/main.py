"""Albion Beacon CLI (skeleton) — development kickoff.
This module intentionally contains only minimal runtime to avoid heavy deps.
"""
from __future__ import annotations
import argparse
import pathlib

VERSION_FILE = pathlib.Path(__file__).resolve().parents[2] / "VERSION"

def get_version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"

def cmd_diagnose() -> int:
    print("[Albion Beacon] Development skeleton")
    print(f"Version: {get_version()}")
    # Npcap/pcap check (soft)
    try:
        import pcap  # type: ignore  # may not exist
        print("pcap module: available")
    except Exception:
        print("pcap module: not found (this is OK for now).")
        print("Npcap가 설치되어 있지 않다면, 설치 후 재시도하세요.")
    return 0

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ab", description="Albion Beacon (skeleton)")
    parser.add_argument("command", nargs="?", default="help", help="help | diagnose")
    args = parser.parse_args(argv)

    if args.command == "diagnose":
        return cmd_diagnose()
    print("Usage: ab diagnose")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
