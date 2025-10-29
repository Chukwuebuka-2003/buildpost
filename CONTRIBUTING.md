# Contributing to BuildPost

Thank you for your interest in contributing to BuildPost! This document provides guidelines and information for contributors.

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to help developers build in public.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Chukwuebuka-2003/buildpost/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Why this would be useful
   - Possible implementation approach

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- An OpenAI or Groq API key for testing

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/Chukwuebuka-2003/buildpost.git
cd buildpost

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=buildpost
```

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black buildpost/

# Lint code
flake8 buildpost/

# Type check
mypy buildpost/
```

## Project Structure

```
buildpost/
├── buildpost/
│   ├── core/           # Core functionality
│   │   ├── git_parser.py      # Git repository parsing
│   │   ├── ai_service.py      # LLM provider integration (OpenAI/Groq)
│   │   └── prompt_engine.py   # YAML template engine
│   ├── utils/          # Utilities
│   │   ├── config.py          # Configuration management
│   │   └── formatters.py      # Platform formatters
│   ├── templates/      # YAML templates
│   │   └── prompts.yaml       # Default prompts
│   └── cli.py          # CLI interface
├── tests/              # Test files
├── setup.py            # Package setup
└── requirements.txt    # Dependencies
```

## Adding New Features

### Adding a New Prompt Style

Edit `buildpost/templates/prompts.yaml`:

```yaml
prompts:
  your_new_style:
    name: "Your New Style"
    description: "Description of your style"
    system: |
      System prompt here...
    template: |
      User prompt template here...
      Commit: {commit_message}
      Files: {files_changed}
```

### Adding a New Platform

Edit `buildpost/templates/prompts.yaml`:

```yaml
platforms:
  your_platform:
    name: "Your Platform"
    max_length: 1000
    guidelines:
      - Guideline 1
      - Guideline 2
    default_hashtags:
      - "#hashtag1"
      - "#hashtag2"
```

Then add a formatter in `buildpost/utils/formatters.py`:

```python
@staticmethod
def format_for_your_platform(content, hashtags=None, max_length=1000):
    # Your formatting logic
    return formatted_content
```

### Adding New CLI Commands

Add commands to `buildpost/cli.py`:

```python
@cli.command()
@click.option('--your-option')
def your_command(your_option):
    """Your command description."""
    # Your command logic
    pass
```

## Commit Message Guidelines

We follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for GitHub Gists platform
fix: resolve API timeout error
docs: update installation instructions
refactor: simplify prompt rendering logic
```

## Pull Request Guidelines

### PR Title

Use conventional commit format:
```
feat: add dark mode support
```

### PR Description

Include:
1. What changes were made
2. Why these changes were needed
3. How to test the changes
4. Screenshots (if UI changes)
5. Related issues

### PR Checklist

Before submitting:
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No breaking changes (or clearly documented)

## Areas for Contribution

### High Priority

- [ ] Additional prompt templates
- [ ] More platform integrations
- [ ] Improved error handling
- [ ] Better test coverage
- [ ] Documentation improvements

### Feature Ideas

- [ ] Auto-posting to platforms
- [ ] Post scheduling
- [ ] Image generation from code
- [ ] Support for other LLM providers
- [ ] Analytics and tracking
- [ ] Browser extension
- [ ] VS Code extension

### Good First Issues

Look for issues tagged with `good-first-issue` on GitHub.

## Questions?

- Open a [Discussion](https://github.com/Chukwuebuka-2003/buildpost/discussions)
- Join our [Discord](https://discord.gg/buildpost) (coming soon)
- Email: hello@buildpost.dev

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to BuildPost!
