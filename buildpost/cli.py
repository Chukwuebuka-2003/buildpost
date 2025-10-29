"""Command-line interface for BuildPost."""

import sys
import click
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from buildpost.core.git_parser import GitParser, InvalidGitRepositoryError
from buildpost.core.ai_service import AIService
from buildpost.core.prompt_engine import PromptEngine
from buildpost.utils.config import Config
from buildpost.utils.formatters import format_post

console = Console()


@click.group(invoke_without_command=True)
@click.option("--commit", "-c", help="Specific commit hash to use")
@click.option("--range", "-r", help="Commit range (e.g., HEAD~5..HEAD)")
@click.option("--style", "-s", help="Prompt style (casual, professional, etc.)")
@click.option("--platform", "-p", help="Target platform (twitter, linkedin, etc.)")
@click.option("--no-hashtags", is_flag=True, help="Exclude hashtags")
@click.option("--no-copy", is_flag=True, help="Do not copy to clipboard")
@click.option("--api-key", help="LLM API key (overrides config)")
@click.option(
    "--provider",
    type=click.Choice(AIService.supported_providers()),
    help="LLM provider to use (openai, groq)",
)
@click.pass_context
def cli(ctx, commit, range, style, platform, no_hashtags, no_copy, api_key, provider):
    """BuildPost - Turn your git commits into social media posts using AI."""
    # If a subcommand is being called, don't run the main logic
    if ctx.invoked_subcommand is not None:
        return

    try:
        # Load configuration
        config = Config()
        active_provider = provider or config.get_provider()

        if active_provider not in AIService.supported_providers():
            console.print(
                f"[bold red]Error:[/bold red] Unsupported provider '{active_provider}'. "
                f"Supported providers: {', '.join(AIService.supported_providers())}"
            )
            sys.exit(1)

        # Get API key
        if not api_key:
            api_key = config.get_api_key(active_provider)

        if not api_key:
            provider_info = AIService.get_provider_info(active_provider)
            env_var = provider_info.get("env_var", "API_KEY")
            signup_url = provider_info.get("signup_url")
            display_name = provider_info.get("display_name", active_provider)

            console.print(
                f"[bold red]Error:[/bold red] No API key found for {display_name}.\n"
            )
            if signup_url:
                console.print(f"Get your API key at: {signup_url}\n")
            console.print(
                "Then set it using one of these methods:\n"
                f"  1. buildpost config set-key --provider {active_provider} YOUR_API_KEY\n"
                f"  2. export {env_var}=YOUR_API_KEY\n"
                "  3. buildpost --api-key YOUR_API_KEY"
            )
            sys.exit(1)

        # Initialize services
        git_parser = GitParser()
        ai_service = AIService(
            provider=active_provider,
            api_key=api_key,
            model=config.get_model(active_provider),
        )
        prompt_engine = PromptEngine(prompts_file=str(config.get_prompts_file()))

        # Get commit info
        if range:
            console.print(
                "[yellow]Note:[/yellow] Range mode will summarize multiple commits.\n"
            )
            commits = git_parser.get_commit_range(range)
            if not commits:
                console.print("[bold red]Error:[/bold red] No commits found in range.")
                sys.exit(1)
            # Use the first commit for now (future: summarize all)
            commit_info = commits[0]
        elif commit:
            commit_info = git_parser.get_commit(commit)
        else:
            commit_info = git_parser.get_latest_commit()

        # Show commit info
        console.print(f"\n[bold]Commit:[/bold] {commit_info.short_hash}")
        console.print(f"[bold]Message:[/bold] {commit_info.message}")
        console.print(f"[bold]Files:[/bold] {len(commit_info.files_changed)} changed\n")

        # Get style and platform
        prompt_style = style or config.get_default_prompt()
        target_platform = platform or config.get_default_platform()

        # Render prompt
        try:
            rendered_prompt = prompt_engine.render_prompt(
                prompt_style, commit_info.to_dict()
            )
        except KeyError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            console.print("\nAvailable prompts:")
            for p in prompt_engine.list_prompts():
                console.print(f"  • {p['name']}: {p['description']}")
            sys.exit(1)

        # Generate post
        with console.status("[bold green]Generating post with AI...", spinner="dots"):
            try:
                generated_content = ai_service.generate_post(
                    system_prompt=rendered_prompt["system"],
                    user_prompt=rendered_prompt["user"],
                    temperature=config.get_temperature(),
                    max_tokens=config.get_max_tokens(),
                )
            except Exception as e:
                console.print(f"[bold red]Error generating post:[/bold red] {e}")
                sys.exit(1)

        # Get platform config and hashtags
        try:
            platform_config = prompt_engine.get_platform(target_platform)
            hashtags = None

            if not no_hashtags and config.should_include_hashtags():
                hashtags = prompt_engine.get_platform_hashtags(target_platform)
                max_tags = prompt_engine.get_max_hashtags()
                hashtags = hashtags[:max_tags] if hashtags else None

        except KeyError:
            console.print(
                f"[yellow]Warning:[/yellow] Unknown platform '{target_platform}', using generic format."
            )
            platform_config = {"max_length": 500}
            hashtags = None

        # Format post
        formatted_post = format_post(
            generated_content, target_platform, platform_config, hashtags
        )

        # Display the post
        console.print("\n" + "=" * 60)
        console.print(
            Panel(
                formatted_post,
                title=f"[bold green]Generated Post[/bold green] ({target_platform} | {prompt_style})",
                border_style="green",
            )
        )
        console.print("=" * 60 + "\n")

        # Show character count
        char_count = len(formatted_post)
        max_length = platform_config.get("max_length", 500)
        count_color = "green" if char_count <= max_length else "red"
        console.print(
            f"[{count_color}]Characters: {char_count}/{max_length}[/{count_color}]\n"
        )

        # Copy to clipboard
        if not no_copy and config.should_copy_to_clipboard():
            try:
                pyperclip.copy(formatted_post)
                console.print("[bold green]✓[/bold green] Copied to clipboard!")
            except Exception:
                console.print("[yellow]Could not copy to clipboard[/yellow]")

    except InvalidGitRepositoryError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)


@cli.group()
def config():
    """Manage BuildPost configuration."""
    pass


@config.command("show")
def config_show():
    """Show current configuration."""
    cfg = Config()
    console.print("\n[bold]Current Configuration:[/bold]\n")
    console.print(cfg.show())


@config.command("set-key")
@click.argument("api_key")
@click.option(
    "--provider",
    "-p",
    type=click.Choice(AIService.supported_providers()),
    help="LLM provider to associate with this key",
)
def config_set_key(api_key, provider):
    """Set an API key for the selected LLM provider."""
    cfg = Config()
    target_provider = provider or cfg.get_provider()

    if not AIService.validate_api_key(api_key, target_provider):
        console.print(
            "[bold yellow]Warning:[/bold yellow] API key format looks unusual for "
            f"provider '{target_provider}'."
        )

    cfg.set_api_key(api_key, provider=target_provider)
    provider_name = AIService.get_provider_info(target_provider).get(
        "display_name", target_provider
    )
    console.print(f"[bold green]✓[/bold green] API key saved for {provider_name}!")


@config.command("set-provider")
@click.argument("provider", type=click.Choice(AIService.supported_providers()))
@click.option("--model", help="Optional default model name to use for this provider")
def config_set_provider(provider, model):
    """Switch the active LLM provider."""
    cfg = Config()
    cfg.set_provider(provider)
    if model:
        cfg.set_model(provider, model)
    provider_name = AIService.get_provider_info(provider).get("display_name", provider)
    console.print(
        f"[bold green]✓[/bold green] Active provider set to {provider_name} ({provider})."
    )
    if model:
        console.print(f"[green]-[/green] Default model updated to '{model}'.")

    if not cfg.get_api_key(provider):
        info = AIService.get_provider_info(provider)
        env_var = info.get("env_var", "API_KEY")
        console.print(
            f"[yellow]Reminder:[/yellow] Configure an API key for {provider_name}:\n"
            f"  buildpost config set-key --provider {provider} YOUR_API_KEY\n"
            f"  or set {env_var}=YOUR_API_KEY"
        )


@config.command("reset")
def config_reset():
    """Reset configuration to defaults."""
    cfg = Config()
    cfg.reset()
    console.print("[bold green]✓[/bold green] Configuration reset to defaults!")


@config.command("init")
def config_init():
    """Initialize BuildPost configuration."""
    cfg = Config()
    cfg.init_prompts_file()
    console.print("[bold green]✓[/bold green] Configuration initialized!")
    console.print(f"Config directory: {cfg.config_dir}")
    console.print(f"Prompts file: {cfg.prompts_file}")


@cli.group()
def prompts():
    """Manage prompt templates."""
    pass


@prompts.command("list")
def prompts_list():
    """List available prompt templates."""
    cfg = Config()
    prompt_engine = PromptEngine(prompts_file=str(cfg.get_prompts_file()))

    table = Table(title="Available Prompt Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Description")

    for prompt in prompt_engine.list_prompts():
        table.add_row(prompt["name"], prompt["display_name"], prompt["description"])

    console.print("\n")
    console.print(table)
    console.print("\n")


@prompts.command("edit")
def prompts_edit():
    """Open prompts file in default editor."""
    import os
    import subprocess

    cfg = Config()
    prompts_file = cfg.get_prompts_file()

    editor = os.getenv("EDITOR", "nano")

    try:
        subprocess.run([editor, str(prompts_file)])
        console.print("[bold green]✓[/bold green] Prompts file edited!")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Could not open editor: {e}")
        console.print(f"Edit manually: {prompts_file}")


@cli.group()
def platforms():
    """Manage platform configurations."""
    pass


@platforms.command("list")
def platforms_list():
    """List available platforms."""
    cfg = Config()
    prompt_engine = PromptEngine(prompts_file=str(cfg.get_prompts_file()))

    table = Table(title="Available Platforms")
    table.add_column("Name", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Max Length", style="yellow")

    for platform in prompt_engine.list_platforms():
        table.add_row(
            platform["name"], platform["display_name"], str(platform["max_length"])
        )

    console.print("\n")
    console.print(table)
    console.print("\n")


@cli.command()
def version():
    """Show BuildPost version."""
    console.print("[bold]BuildPost[/bold] v0.1.1")
    console.print("Turn your git commits into social media posts using AI")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
