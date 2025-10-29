# Quick Start Guide

Get started with BuildPost in under 2 minutes!

## 1. Installation

```bash
pip install buildpost
```

## 2. Choose a Provider & Get an API Key

BuildPost works with three LLM providers:

| Provider | Why use it? | Where to get a key |
|----------|-------------|--------------------|
| `openai` (default) | Wide model selection (GPT-4o mini, GPT-4o) | [OpenAI dashboard](https://platform.openai.com/api-keys) |
| `groq` | Super-fast Qwen3/LLaMA inference | [Groq console](https://console.groq.com/keys) |

Sign up with your chosen provider and copy the API key.

## 3. Configure BuildPost

```bash
buildpost config set-key YOUR_API_KEY_HERE           # saves key for the active provider (OpenAI by default)
# Optional: switch providers or models
buildpost config set-provider openai --model gpt-4o-mini
buildpost config set-key --provider openai sk-XXXX
```

## 4. Generate Your First Post

Navigate to any git repository and run:

```bash
buildpost
```

That's it! Your post is generated and copied to your clipboard.

## Common Use Cases

### Tweet about your latest work
```bash
buildpost
```

### Professional LinkedIn post
```bash
buildpost --style professional --platform linkedin
```

### Technical blog post starter
```bash
buildpost --style technical --platform devto
```

### Post about a specific commit
```bash
buildpost --commit abc123
```

### Customize your prompts
```bash
buildpost prompts edit
```

## Next Steps

- Run `buildpost --help` to see all options
- Run `buildpost prompts list` to see available styles
- Edit `~/.buildpost/config.yaml` to set defaults
- Edit `~/.buildpost/prompts.yaml` to customize prompts

## Examples

### Example Output (Casual Twitter)

**Input:** `fix: resolve authentication timeout in user sessions`

**Output:**
```
Just fixed a timeout bug in our auth system! ⏱️

Users were getting logged out unexpectedly. Turned out to be
a session expiry issue. All sorted now!

#BugFix #BuildInPublic
```

### Example Output (Professional LinkedIn)

**Input:** `feat: implement Redis caching for API responses`

**Output:**
```
Implemented a Redis caching layer for our API, resulting in
significant performance improvements.

Key achievements:
• 65% reduction in average response time
• Decreased database load by 40%
• Improved scalability for concurrent requests

The caching strategy uses smart invalidation based on data
mutation events, ensuring users always see fresh data while
benefiting from improved performance.

What caching strategies have worked well in your projects?

#BackendDevelopment #Performance #Redis
```

## Troubleshooting

**No API key error?**
```bash
buildpost config set-key YOUR_API_KEY
# or set an environment variable:
# export OPENAI_API_KEY=... or GROQ_API_KEY=...
```

**Not a git repository error?**
```bash
cd your-git-repo
buildpost
```

**Want to customize prompts?**
```bash
buildpost prompts edit
```

---

Happy building in public!
