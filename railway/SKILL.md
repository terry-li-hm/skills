---
description: Manage Railway deployments - check status, view logs, redeploy services
user_invocable: true
---

# Railway CLI Skill

Manage Railway deployments from the terminal.

## Setup (once per session)

If not linked, run from the project directory:
```bash
railway link
railway service link <service-id>
```

## Common Operations

### Check Status
```bash
railway status
```

### View Logs
```bash
# Runtime logs
railway logs | tail -50

# Build logs
railway logs --build | tail -50
```

### Redeploy
```bash
railway redeploy -y
```

### Get Domain
```bash
railway domain
```

### Health Check
After getting domain, test the health endpoint:
```bash
curl -s <domain>/health
```

## Projects Reference

| Project | Service | Directory |
|---------|---------|-----------|
| adverse-media-agent | backend | ~/adverse-media-agent/backend |

## Troubleshooting

- **403 on upload**: Check billing/permissions
- **No service found**: Run `railway service link <id>`
- **TTY errors**: Use `-y` flag for confirmations
- **Build fails**: Check `railway logs --build` for errors
