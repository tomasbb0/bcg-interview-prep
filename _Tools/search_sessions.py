import json

with open('/Users/tomasbatalha/Documents/VS Code Projects/Advisory & Planning/Tomas_Batalha_Future_Plan/.chat-sessions/42ce5f61-8e60-4c88-8a10-b964a09ee934.json', 'r') as f:
    data = json.load(f)

# Search for any file creation with .py extension
for i, req in enumerate(data.get('requests', [])):
    for resp in req.get('response', []):
        kind = resp.get('kind')
        if kind == 'toolInvocationSerialized':
            val = resp.get('value', {})
            if isinstance(val, dict):
                tool_name = val.get('toolName', '')
                invocation = val.get('invocation', {})
                params = invocation.get('parameters', {})
                
                # Check for create_file with .py
                filepath = str(params.get('filePath', ''))
                content = str(params.get('content', ''))
                command = str(params.get('command', ''))
                
                if '.py' in filepath or ('python' in command.lower() and len(command) > 100):
                    print(f'=== Message {i+1} ===')
                    print(f'Tool: {tool_name}')
                    print(f'FilePath: {filepath}')
                    print(f'Content/Command: {content or command}')
                    print()
                    print('=' * 60)
