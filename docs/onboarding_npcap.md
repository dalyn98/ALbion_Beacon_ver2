# Onboarding: Npcap Detection & Guidance

- We attempt a soft detection:
  1) Try importing `pcap` module (may not exist).
  2) Look for common Npcap files/folders:
     - C:\Windows\System32\Npcap\Packet.dll
     - C:\Program Files\Npcap
- If missing, we print friendly guidance to install Npcap.

> Note: This is only a user guidance check, not a strict dependency at this milestone.
