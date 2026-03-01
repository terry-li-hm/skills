---
name: openrouter
description: Check OpenRouter credit balance. Use when user says "openrouter credits", "or credits", "top up openrouter", or consilium returns 402.
user_invocable: true
---

# OpenRouter Credits

Check remaining OpenRouter credit balance.

## Triggers

- "openrouter credits"
- "or credits"
- "check openrouter"
- consilium returning 402

## Command

```bash
python3 -c "
import subprocess, json
key = subprocess.check_output(['security', 'find-generic-password', '-s', 'openrouter-api-key', '-w'], text=True).strip()
import urllib.request
req = urllib.request.Request('https://openrouter.ai/api/v1/credits', headers={'Authorization': f'Bearer {key}'})
data = json.loads(urllib.request.urlopen(req).read())['data']
total = data['total_credits']
used = data['total_usage']
remaining = total - used
print(f'Credits: \${remaining:.2f} remaining of \${total:.2f} total (\${used:.2f} used)')
if remaining < 5:
    print('⚠️  Low — top up at https://openrouter.ai/credits')
"
```

## Top-up

https://openrouter.ai/credits
