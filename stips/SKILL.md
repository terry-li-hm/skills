---
name: stips
description: Check OpenRouter credits and usage. Use when user says "stips", "openrouter credits", "or credits", or consilium returns 402.
user_invocable: true
---

# stips

OpenRouter CLI — credits, usage, key management.

`~/code/stips` · [crates.io](https://crates.io/crates/stips) · [github](https://github.com/terry-li-hm/stips)

## Commands

```bash
stips                  # credit balance (default)
stips credits          # same
stips usage            # daily / weekly / monthly spend
stips key open         # open openrouter.ai/keys in browser
stips key save <key>   # save API key to macOS keychain
```

## Keychain

Key stored under service `openrouter-api-key`, account `openrouter`.

## Low balance

Exits 1 + warns when remaining < $5. Top up at https://openrouter.ai/credits.
