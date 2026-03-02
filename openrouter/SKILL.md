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
stips          # credits (default)
stips usage    # daily/weekly/monthly spend
stips key open # open openrouter.ai/keys in browser
stips key save <key>  # save new key to keychain
```

## Top-up

https://openrouter.ai/credits

## See also

`/stips` — dedicated skill with full command reference.
