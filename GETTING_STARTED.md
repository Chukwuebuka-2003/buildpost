# Getting Started with BuildPost

Welcome to BuildPost! This guide will have you generating social media posts from your git commits in under 2 minutes.

## Prerequisites

- Python 3.8 or higher
- Git (any version)
- A git repository to test with
- An API key from one of the supported LLM providers:
  - OpenAI (default)
  - Groq

## Step 1: Pick a Provider & Get an API Key

| Provider | Why choose it? | Signup link | Default model |
|----------|----------------|-------------|---------------|
| `openai` (default) | Access to GPT-4o mini and GPT-4o | [OpenAI dashboard](https://platform.openai.com/api-keys) | `gpt-4o-mini` |
| `groq` | Ultra-fast Qwen3 & LLaMA | [Groq console](https://console.groq.com/keys) | `qwen/qwen3-32b` |

Create an API key with your chosen provider and keep it handy.

## Step 2: Install BuildPost

### Option A: From PyPI (Recommended when published)

```bash
pip install buildpost
```

### Option B: From Source (Current)

```bash
# Clone the repository
git clone https://github.com/Chukwuebuka-2003/buildpost.git
cd buildpost

# Install in development mode
pip install -e .
```

## Step 3: Configure Your API Key

### Method 1: Using the CLI (Recommended)

```bash
buildpost config set-key YOUR_API_KEY_HERE          # saves key for the active provider (OpenAI by default)
buildpost config set-provider groq --model qwen/qwen3-32b
buildpost config set-key --provider groq gsk-XXXX
```

This stores your keys securely in `~/.buildpost/config.yaml`. You can keep multiple providers on file and switch between them.

### Method 2: Environment Variable

Add to your `.bashrc`, `.zshrc`, or `.bash_profile`:

```bash
export OPENAI_API_KEY=your_api_key_here   # or GROQ_API_KEY=...
```

### Method 3: Per-Command

```bash
buildpost --provider groq --api-key gsk_xxxx
```

## Step 4: Generate Your First Post

Navigate to any git repository:

```bash
cd your-git-project
```

Run BuildPost:

```bash
buildpost                       # Uses configured provider (OpenAI by default)
buildpost --provider groq       # Temporarily override the provider
```

That's it! Your post is:
- Displayed in your terminal
- Automatically copied to your clipboard
- Ready to paste into social media

## Understanding the Output

When you run `buildpost`, you'll see:

```
Commit: abc1234
Message: feat: add user authentication
Files: 3 changed

============================================================
┌─────────────────────────────────────────────────────────┐
│ Generated Post (twitter | casual)                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Just shipped user authentication! 🔐                    │
│                                                          │
│ Added login/signup with JWT tokens. Security is         │
│ looking good!                                            │
│                                                          │
│ #WebDev #BuildInPublic                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
============================================================

Characters: 145/280

✓ Copied to clipboard!
```

Now just paste it into Twitter/X!

## Customizing Your Posts

### Choose a Different Style

```bash
buildpost --style professional  # For LinkedIn
buildpost --style technical     # For Dev.to
buildpost --style learning      # For sharing lessons
```

**Available styles:**
- `casual` (default) - Friendly, conversational, with emojis
- `professional` - Polished, achievement-focused
- `technical` - Educational, detailed
- `thread_starter` - Hook for Twitter threads
- `achievement` - Celebrate wins
- `learning` - Share what you learned

### Target a Specific Platform

```bash
buildpost --platform linkedin   # Longer, professional format
buildpost --platform devto      # Technical blog format
buildpost --platform twitter    # Short and punchy (default)
```

**Available platforms:**
- `twitter` (default) - 280 character limit
- `linkedin` - 3000 character limit
- `devto` - 1000 character limit, technical
- `generic` - 500 character limit, balanced

### Use a Specific Commit

```bash
buildpost --commit abc1234
```

### Combine Options

```bash
buildpost --commit abc1234 --style professional --platform linkedin
```

### Exclude Hashtags

```bash
buildpost --no-hashtags
```

### Preview Without Copying

```bash
buildpost --no-copy
```

## Viewing Available Options

### List All Prompt Styles

```bash
buildpost prompts list
```

Output:
```
Available Prompt Templates
┌──────────────────┬────────────────────────┬─────────────────────┐
│ Name             │ Display Name           │ Description         │
├──────────────────┼────────────────────────┼─────────────────────┤
│ casual           │ Casual & Friendly      │ Perfect for Twitter │
│ professional     │ Professional           │ Ideal for LinkedIn  │
│ technical        │ Technical & Education  │ Great for Dev.to    │
└──────────────────┴────────────────────────┴─────────────────────┘
```

### List All Platforms

```bash
buildpost platforms list
```

### Show Your Configuration

```bash
buildpost config show
```

## Customizing Prompts

BuildPost uses YAML templates that you can customize!

### Edit Prompts

```bash
buildpost prompts edit
```

This opens `~/.buildpost/prompts.yaml` in your default editor.

### Prompt Template Structure

```yaml
prompts:
  my_custom_style:
    name: "My Custom Style"
    description: "Posts in my unique voice"
    system: |
      You are a developer with a unique perspective...

    template: |
      Create a post about this commit:

      Commit: {commit_message}
      Files: {files_changed}

      Make it awesome!
```

### Available Template Variables

Use these in your templates:
- `{commit_message}` - The commit message
- `{commit_hash}` - Full hash
- `{short_hash}` - Short hash (7 chars)
- `{author}` - Commit author
- `{date}` - Commit date
- `{files_changed}` - List of changed files
- `{diff_summary}` - Summary of changes
- `{insertions}` - Lines added
- `{deletions}` - Lines deleted
- `{files_count}` - Number of files

## Setting Defaults

Edit `~/.buildpost/config.yaml`:

```yaml
defaults:
  prompt_style: casual        # Your favorite style
  platform: twitter           # Your main platform
  include_hashtags: true      # Add hashtags?
  copy_to_clipboard: true     # Auto-copy?

generation:
  temperature: 0.7            # AI creativity (0.0-1.0)
  max_tokens: 500             # Response length
```

## Common Workflows

### Daily Build-in-Public Workflow

```bash
# After making a commit
git add .
git commit -m "feat: add cool feature"

# Generate and post
buildpost
# → Paste into Twitter

# Want LinkedIn too?
buildpost --platform linkedin
# → Paste into LinkedIn
```

### End-of-Week Summary

```bash
# Generate from last week's commits
git log --oneline --since="1 week ago"
# Pick your favorite commit

buildpost --commit abc1234 --style achievement
```

### Technical Blog Posts

```bash
buildpost --style technical --platform devto --no-copy
# Review, edit if needed
# Then copy the version you like
```

### Multiple Platforms

```bash
# Generate for each platform
buildpost --platform twitter    # Copy, paste to Twitter
buildpost --platform linkedin   # Copy, paste to LinkedIn
buildpost --platform devto      # Copy, paste to Dev.to
```

## Tips for Better Posts

### 1. Write Good Commit Messages

Better commit messages = better posts!

**Good:**
```
feat: implement Redis caching for API responses

Added Redis caching layer to reduce database load and
improve response times by ~60%.
```

**Not as good:**
```
update stuff
```

### 2. Choose the Right Style

- Building in public? → `casual` or `learning`
- Job hunting? → `professional` or `achievement`
- Teaching? → `technical` or `learning`
- Starting a thread? → `thread_starter`

### 3. Customize for Your Voice

Edit the prompts to match how you actually write:
```bash
buildpost prompts edit
```

### 4. Review Before Posting

The generated post is a starting point. Feel free to:
- Edit for your voice
- Add personal touches
- Adjust hashtags
- Combine multiple versions

### 5. Be Consistent

Set defaults so you don't have to think:
```bash
buildpost config show
# Edit ~/.buildpost/config.yaml
```

## Troubleshooting

### "No API key found"

**Solution:**
```bash
buildpost config set-key YOUR_API_KEY
```

### "Not a git repository"

**Solution:** Run BuildPost from inside a git repository:
```bash
cd your-project
buildpost
```

### "Invalid commit reference"

**Solution:** Check the commit exists:
```bash
git log --oneline
buildpost --commit abc1234
```

### Post is too long

**Solutions:**
1. Try a different platform: `buildpost --platform twitter`
2. Try a different style: `buildpost --style casual`
3. Edit the generated post before posting

### API Rate Limits

Each provider has usage limits. If you hit them:
- OpenAI: check account usage or switch to a lighter model
- Groq: review your quota in the Groq console or choose a smaller model
- Reduce generation frequency if possible

### Can't copy to clipboard

**On Linux:** Install xclip or xsel:
```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

### Permission errors on config

**Solution:** Check file permissions:
```bash
ls -la ~/.buildpost/
chmod 644 ~/.buildpost/config.yaml
```

## Getting Help

### Command Help

```bash
buildpost --help                # General help
buildpost config --help         # Config commands
buildpost prompts --help        # Prompt commands
```

### Version Info

```bash
buildpost version
```

### Documentation

- Full README: `README.md`
- Quick start: `QUICKSTART.md`
- Examples: `examples/demo.md`
- Contributing: `CONTRIBUTING.md`
- Roadmap: `ROADMAP.md`

### Community Support

- GitHub Issues: [Report bugs](https://github.com/Chukwuebuka-2003/buildpost/issues)
- Discussions: [Ask questions](https://github.com/Chukwuebuka-2003/buildpost/discussions)
- Twitter: [@ebukagaus](https://x.com/ebukagaus)

## Next Steps

Now that you're set up:

1. ✅ Generate your first post
2. ✅ Try different styles and platforms
3. ✅ Customize prompts to match your voice
4. ✅ Set your default preferences
5. ✅ Start building in public!

## Example: First 5 Minutes

```bash
# Install
pip install buildpost

# Configure
buildpost config set-key AIza...

# Go to a project
cd ~/projects/my-app

# Generate a post
buildpost
# → ✓ Copied to clipboard!

# Try LinkedIn version
buildpost --platform linkedin
# → ✓ Copied to clipboard!

# List all styles
buildpost prompts list

# Try technical style
buildpost --style technical --platform devto

# Make it yours
buildpost prompts edit
```

---

## You're Ready! 🚀

You now know everything you need to start using BuildPost effectively.

**Remember:**
- Good commits → good posts
- Customize prompts for your voice
- Different styles for different audiences
- Review and edit before posting

**Happy building in public!**

Share your journey, inspire others, and grow your developer brand with BuildPost.

---

Questions? Check the [README](README.md) or open an [issue](https://github.com/Chukwuebuka-2003/buildpost/issues).
