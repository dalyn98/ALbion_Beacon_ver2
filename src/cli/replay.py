"""Offline replay CLI (stub)."""
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(description="Replay PCAP (stub)")
    parser.add_argument("--pcap", help="pcapng file path")
    parser.parse_args(argv)
    print("Replay mode: not implemented in skeleton.")

if __name__ == "__main__":
    main()
