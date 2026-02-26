#!/usr/bin/env python3
import json
from pathlib import Path

session_path = Path.home() / "Library/Application Support/Code/User/workspaceStorage/0020fb2bdf5bf60f539cb28bff6f68bb/chatSessions/15ea4da1-2f5d-4cd1-b38e-63f58a5c3103.json"

with open(session_path) as f:
    d = json.load(f)

reqs = d.get('requests', [])
print(f"Total messages: {len(reqs)}")
print()

# Find job tracker related messages
for i, r in enumerate(reqs):
    msg = r.get('message', {})
    if isinstance(msg, dict):
        text = msg.get('text', '')
    else:
        text = str(msg)
    
    resp = r.get('response', [])
    resp_text = str(resp)
    
    if 'job-tracker-collab' in text.lower() or 'job-tracker-collab' in resp_text.lower():
        print(f"=== Message {i+1} ===")
        print(f"User: {text[:500]}")
        print("---")

print("\n\nChecking for 'JOB_TRACKER' mentions...")
for i, r in enumerate(reqs):
    msg = r.get('message', {})
    if isinstance(msg, dict):
        text = msg.get('text', '')
    else:
        text = str(msg)
    
    if 'JOB_TRACKER' in text or 'job tracker' in text.lower():
        print(f"=== Message {i+1} ===")
        print(f"User: {text[:500]}")
        print("---")
