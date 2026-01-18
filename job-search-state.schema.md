# Job Search State Schema

Shared state file that allows job search skills to build on each other. Located at `/Users/terry/notes/job-search-state.json`.

## Purpose

Instead of each skill operating in isolation, they can read from and write to this shared state:
- `/evaluate-job` → adds to `considering` or `passed`
- `/message --type=followup` → reads from `awaiting_response`
- `/weekly-reset` → summarizes from all sections, updates `metrics`
- `/tailor-resume` → can check if role is already in pipeline

## Schema

```json
{
  "pipeline": {
    "interviews_scheduled": [
      {
        "company": "Stripe",
        "role": "Staff ML Engineer",
        "date": "2026-01-25",
        "stage": "technical",
        "contact": "Jane Doe",
        "notes": "Focus on system design"
      }
    ],
    "awaiting_response": [
      {
        "company": "Plaid",
        "role": "ML Lead",
        "applied_date": "2026-01-10",
        "last_contact": "2026-01-10",
        "days_waiting": 8
      }
    ],
    "recently_applied": [
      {
        "company": "Monzo",
        "role": "Head of Data Science",
        "applied_date": "2026-01-17",
        "source": "LinkedIn",
        "referral": null
      }
    ],
    "considering": [
      {
        "company": "Revolut",
        "role": "ML Platform Lead",
        "url": "https://linkedin.com/jobs/...",
        "fit_score": "APPLY",
        "notes": "Good tech stack match"
      }
    ],
    "passed": [
      {
        "company": "HSBC",
        "role": "Data Scientist",
        "reason": "Too junior",
        "date": "2026-01-15"
      }
    ]
  },

  "networking": {
    "active_conversations": [
      {
        "name": "John Smith",
        "company": "Stripe",
        "relationship": "former colleague",
        "last_contact": "2026-01-12",
        "status": "waiting for intro"
      }
    ],
    "pending_followups": [
      {
        "name": "Jane Doe",
        "type": "application",
        "last_contact": "2026-01-08",
        "recommended_action": "send follow-up"
      }
    ],
    "scheduled_calls": [
      {
        "name": "Bob Lee",
        "date": "2026-01-20",
        "purpose": "informational",
        "company": "Anthropic"
      }
    ]
  },

  "weekly_goals": {
    "applications_target": 5,
    "networking_calls_target": 2,
    "last_reset": "2026-01-12"
  },

  "metrics": {
    "total_applications": 15,
    "total_interviews": 3,
    "response_rate": 0.20,
    "weeks_active": 2
  }
}
```

## Usage in Skills

### Reading state
```python
import json
with open('/Users/terry/notes/job-search-state.json') as f:
    state = json.load(f)

# Get roles awaiting response
awaiting = state['pipeline']['awaiting_response']
```

### Writing state
```python
# Add new application
state['pipeline']['recently_applied'].append({
    "company": "New Corp",
    "role": "ML Lead",
    "applied_date": "2026-01-18",
    "source": "referral"
})

with open('/Users/terry/notes/job-search-state.json', 'w') as f:
    json.dump(state, f, indent=2)
```

## Maintenance

- `/weekly-reset` should recalculate `metrics` and move stale items
- Items in `recently_applied` older than 2 weeks → `awaiting_response`
- Items in `awaiting_response` older than 4 weeks → consider `passed` (likely ghosted)
