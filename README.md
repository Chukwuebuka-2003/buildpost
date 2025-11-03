# BuildPost

> Turn your git commits into engaging social media posts using AI

Free CLI tool that transforms your git commits into social media content. Perfect for developers who want to build in public but struggle with content creation.

## Features

- **AI-Powered**: Works with OpenAI, Groq or OpenRouter LLMs
- **Multiple Styles**: Casual, professional, technical, learning-focused, and more
- **Platform-Optimized**: Twitter, LinkedIn, Dev.to, and generic formats
- **YAML Templates**: Fully customizable prompt templates
- **Zero Config**: Works out of the box with sensible defaults
- **Flexible Providers**: Choose the LLM provider that fits your workflow and budget

## Quick Start

### Installation

```bash
pip install buildpost
```

### Setup

1. Pick your LLM provider:
   - `openai`: GPT-4o mini (default) or any compatible Chat Completions model
   - `groq`: Lightning-fast Qwen3 and Llama-family models
<<<<<<< HEAD
=======
   - `openrouter`: GPT-4o mini (default) or any compatible Chat Completions model
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

2. Grab an API key:
   - OpenAI: [OpenAI dashboard](https://platform.openai.com/api-keys)
   - Groq: [Groq console](https://console.groq.com/keys)
<<<<<<< HEAD
=======
   - OpenRouter: [OpenRouter keys](https://openrouter.ai/settings/keys)
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

3. Configure BuildPost:

```bash
buildpost config set-key YOUR_API_KEY           # saves key for the active provider (OpenAI by default)
# Optional: switch providers or customise the default model
buildpost config set-provider groq --model qwen/qwen3-32b
buildpost config set-key --provider groq gsk-XXXX
```

Prefer environment variables?

```bash
<<<<<<< HEAD
export OPENAI_API_KEY=your_key    # or GROQ_API_KEY=...
=======
export OPENAI_API_KEY=your_key    # or GROQ_API_KEY=... # or OPENROUTER_API_KEY=...
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
```

### Usage

Generate a post from your latest commit:

```bash
buildpost
```

That's it! The post will be generated and copied to your clipboard.

## Advanced Usage

### Specify a Commit

```bash
# Use a specific commit
buildpost --commit abc123

# Use a commit range (summarizes multiple commits)
buildpost --range HEAD~5..HEAD
```

### Choose a Style

```bash
# Available styles: casual, professional, technical, thread_starter, achievement, learning
buildpost --style professional
```

### Target a Platform

```bash
# Available platforms: twitter, linkedin, devto, generic
buildpost --platform linkedin
```

### Combine Options

```bash
buildpost --commit abc123 --style technical --platform devto --no-hashtags
```

## Configuration

### View Configuration

```bash
buildpost config show
```

### Set Default Style and Platform

Edit `~/.buildpost/config.yaml`:

```yaml
defaults:
  prompt_style: casual
  platform: twitter
  include_hashtags: true
  copy_to_clipboard: true
```

### Customize Prompts

BuildPost uses YAML templates for prompts. Edit them:

```bash
buildpost prompts edit
```

Or manually edit `~/.buildpost/prompts.yaml`.

## Available Commands

### Main Commands

```bash
buildpost                    # Generate post from latest commit
buildpost --commit <hash>    # Generate from specific commit
buildpost --range <range>    # Generate from commit range
buildpost --style <style>    # Use specific prompt style
buildpost --platform <name>  # Format for specific platform
buildpost --provider groq    # Use Groq for this run
buildpost --no-hashtags      # Exclude hashtags
buildpost --no-copy          # Don't copy to clipboard
```

### Configuration Commands

```bash
buildpost config show        # Show current configuration
buildpost config set-key     # Set API key for the current provider
buildpost config set-key --provider groq gsk-...    # Store key for Groq
buildpost config set-provider openai --model gpt-4o-mini
buildpost config reset       # Reset to defaults
buildpost config init        # Initialize configuration
```

### Prompt Commands

```bash
buildpost prompts list       # List available prompts
buildpost prompts edit       # Edit prompts in your editor
```

### Platform Commands

```bash
buildpost platforms list     # List available platforms
```

### Other Commands

```bash
buildpost version            # Show version
buildpost --help             # Show help
```

## Prompt Styles

### Casual (Default)
Perfect for Twitter and personal brands. Conversational, friendly, uses emojis.

**Example:**
```
Just squashed a tricky auth bug! 🐛

Spent the morning debugging the login flow and finally tracked it down.
Feels good to ship a fix!

#100DaysOfCode #BuildInPublic
```

### Professional
Ideal for LinkedIn. Polished, achievement-focused, no emojis.

**Example:**
```
Improved API performance by implementing a Redis caching layer.

Key improvements:
• 60% reduction in average response time
• Decreased database load
• Better user experience during peak traffic

What caching strategies have worked well for your team?

#SoftwareEngineering #Performance
```

### Technical
Great for Dev.to and Hashnode. Detailed, educational, technical.

**Example:**
```
Migrated our user API from REST to GraphQL

Why we made the switch:
- Reduced over-fetching (clients request only needed fields)
- Single endpoint vs. multiple REST routes
- Better type safety with GraphQL schemas

The refactor took about a week but the DX improvement is worth it.

#GraphQL #APIDesign
```

### Thread Starter
Opens a Twitter thread. Hook-focused and intriguing.

### Achievement
Celebrate milestones and wins. Great for any platform.

### Learning
Share what you learned. Perfect for building in public.

## Platforms

### Twitter/X
- Max 280 characters
- 2-3 hashtags
- Punchy and concise

### LinkedIn
- Up to 3000 characters
- Professional tone
- 2-4 paragraphs
- Ends with a question

### Dev.to / Hashnode
- Technical and detailed
- Educational focus
- Can include code concepts

### Generic
- Balanced format
- Works across platforms
- Moderate length

## Customization

### Creating Custom Prompts

Edit `~/.buildpost/prompts.yaml`:

```yaml
prompts:
  my_custom_style:
    name: "My Custom Style"
    description: "A custom prompt for my needs"
    system: |
      You are a developer with a unique voice...

    template: |
      Based on this commit, create a post:

      Commit: {commit_message}
      Files: {files_changed}

      Make it awesome!
```

Use it:

```bash
buildpost --style my_custom_style
```

### Template Variables

Available variables in templates:

- `{commit_hash}` - Full commit hash
- `{short_hash}` - Short commit hash (7 chars)
- `{commit_message}` - Commit message
- `{author}` - Commit author
- `{date}` - Commit date
- `{files_changed}` - List of changed files
- `{diff_summary}` - Summary of changes
- `{insertions}` - Lines added
- `{deletions}` - Lines deleted
- `{files_count}` - Number of files changed

## Examples

### Example 1: Quick Tweet

```bash
$ buildpost
```

```
Just implemented dark mode for the settings page! 🌙

Added theme switching with React Context and CSS variables.
The toggle feels so smooth!

#ReactJS #WebDev
```

### Example 2: LinkedIn Post

```bash
$ buildpost --style professional --platform linkedin
```

```
Implemented a comprehensive caching strategy for our API layer.

This optimization resulted in:
• 65% faster average response times
• 40% reduction in database queries
• Improved scalability for concurrent users

The implementation uses Redis for distributed caching with a
smart invalidation strategy based on data mutation events.

What performance optimization techniques have had the biggest
impact in your projects?

#BackendDevelopment #APIDesign #Performance
```

### Example 3: Technical Blog Post

```bash
$ buildpost --commit abc123 --style technical --platform devto
```

```
Refactored our authentication system to use JWT instead of sessions

Why we made the change:
- Stateless authentication (no server-side session storage)
- Better scalability across multiple servers
- Simpler mobile app integration
- Industry standard with broad library support

The migration was done in phases:
1. Implemented JWT generation alongside existing sessions
2. Migrated frontend to use JWT tokens
3. Deprecated session-based auth after monitoring period

Key learnings: Always implement both systems in parallel during
migration to allow easy rollback.

#Authentication #JWT #BackendDevelopment
```

## Troubleshooting

### "No API key found"

Make sure you’ve saved a key for the provider you’re using:

```bash
buildpost config set-provider openai
buildpost config set-key --provider openai sk-...   # OpenAI key

buildpost config set-provider groq
buildpost config set-key --provider groq gsk-...    # Groq key
<<<<<<< HEAD
=======

buildpost config set-provider openrouter
buildpost config set-key --provider openrouter sk-or-v1-...    # OpenRouter key
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
```

Environment variable names:

<<<<<<< HEAD
| Provider | Environment variable | Notes |
|----------|----------------------|-------|
| `openai` | `OPENAI_API_KEY`     | Works with GPT-4o mini, GPT-4o, GPT-3.5 |
| `groq`   | `GROQ_API_KEY`       | Supports Qwen & Llama models |
=======
|   Provider   | Environment variable | Notes |
|--------------|----------------------|-------|
| `openai`     | `OPENAI_API_KEY`     | Works with GPT-4o mini, GPT-4o, GPT-3.5 |
| `groq`       | `GROQ_API_KEY`       | Supports Qwen & Llama models |
| `openrouter` | `OPENROUTER_API_KEY` | Supports GPT-4o mini, Llama, Grok models |
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

Set it before running BuildPost:

```bash
export GROQ_API_KEY=gsk-...
```

### "Not a git repository"

Run BuildPost from within a git repository:

```bash
cd your-git-repo
buildpost
```

### "Invalid commit reference"

Make sure the commit hash exists:

```bash
git log --oneline  # See available commits
buildpost --commit <hash>
```

### Generated post is too long

Try a different platform or style:

```bash
buildpost --platform twitter  # Shorter format
buildpost --style casual       # Usually more concise
```

### API rate limits

Each provider enforces its own rate/usage limits. If you hit them:
- OpenAI: check account limits or switch to a lighter model (gpt-4o-mini, gpt-3.5)
- Groq: review quota in the Groq console or pick a smaller model
<<<<<<< HEAD
=======
- OpenRouter: check credits available and usage limits for the API key
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
- Reduce how frequently you generate posts

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Chukwuebuka-2003/buildpost.git
cd buildpost

# Install in development mode
pip install -e .

# Run from source
python -m buildpost.cli
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Issues: [GitHub Issues](https://github.com/Chukwuebuka-2003/buildpost/issues)
- Twitter: [@ebukagaus](https://x.com/ebukagaus)

## Acknowledgments

<<<<<<< HEAD
- LLM support provided by [OpenAI](https://openai.com/) and [Groq](https://groq.com/)
=======
- LLM support provided by [OpenAI](https://openai.com/) and [Groq](https://groq.com/) and [OpenRouter](https://openrouter.ai)
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
- Powered by [GitPython](https://gitpython.readthedocs.io/)
- CLI built with [Click](https://click.palletsprojects.com/)

---

# Example image of what i did

<img width="1359" height="339" alt="image" src="https://github.com/user-attachments/assets/1e7a2191-6b1b-40cd-bef0-f01c29a31abb" />

