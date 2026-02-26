#!/usr/bin/env python3
"""Export job-tracker-collab related chat messages"""
import json
from pathlib import Path
from datetime import datetime

session_path = Path.home() / "Library/Application Support/Code/User/workspaceStorage/0020fb2bdf5bf60f539cb28bff6f68bb/chatSessions/15ea4da1-2f5d-4cd1-b38e-63f58a5c3103.json"
output_path = Path("/Users/tomasbatalha/Projects/Planning and Advisory/job-tracker-collab/CHAT_HISTORY/job-tracker-collab-development.md")

with open(session_path) as f:
    d = json.load(f)

reqs = d.get('requests', [])

# Messages 658-671 are the core job-tracker-collab development
# But let's get all related messages (658-693 covers the full development)
job_tracker_messages = []
for i, r in enumerate(reqs):
    msg = r.get('message', {})
    if isinstance(msg, dict):
        text = msg.get('text', '')
    else:
        text = str(msg)
    
    resp = r.get('response', [])
    
    # Check if this message is related to job tracker
    combined = text.lower() + str(resp).lower()
    if any(kw in combined for kw in ['job-tracker', 'job tracker', 'collaborative doc', 'firebase', 'job_tracker', 'apply link', 'referral linkedin', 'anthropic top', 'business development rep']):
        job_tracker_messages.append((i+1, text, resp))

print(f"Found {len(job_tracker_messages)} job-tracker related messages")

with open(output_path, 'w') as f:
    f.write("# Job Tracker Collab - Development Chat History\n\n")
    f.write("**Source:** VS Code Chat Session\n")
    f.write("**Original Session:** Converting a folder to a workspace in VS Code\n")
    f.write(f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Messages:** {len(job_tracker_messages)} related to job tracker development\n\n")
    f.write("---\n\n")
    
    for msg_num, user_text, response in job_tracker_messages:
        f.write(f"## Message {msg_num}\n\n")
        f.write(f"**User:**\n{user_text}\n\n")
        
        if response:
            f.write("**Assistant:**\n")
            if isinstance(response, list):
                for item in response:
                    if isinstance(item, dict):
                        content = item.get('value', item.get('content', ''))
                        if content and len(content) > 50:
                            # Truncate very long responses
                            if len(content) > 3000:
                                content = content[:3000] + "\n\n[... response truncated ...]"
                            f.write(f"{content}\n\n")
            elif isinstance(response, dict):
                content = response.get('value', response.get('content', ''))
                if content:
                    if len(content) > 3000:
                        content = content[:3000] + "\n\n[... response truncated ...]"
                    f.write(f"{content}\n\n")
        
        f.write("---\n\n")

print(f"✅ Exported to: {output_path}")
