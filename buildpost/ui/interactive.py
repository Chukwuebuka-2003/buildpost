"""Interactive TUI for selecting commits and generating changelogs."""

import sys
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt, Confirm

from buildpost.core.git_parser import GitParser, CommitInfo
from buildpost.core.ai_service import AIService
from buildpost.core.prompt_engine import PromptEngine
from buildpost.utils.config import Config


class CommitItem:
    """A selectable commit item for the TUI."""

    def __init__(self, commit: CommitInfo, selected: bool = False):
        self.commit = commit
        self.selected = selected

    def toggle(self):
        self.selected = not self.selected

    @property
    def short_display(self) -> str:
        date = self.commit.date.split(" ")[0]
        return f"{date} {self.commit.short_hash} {self.commit.message[:40]}"

    @property
    def detail_display(self) -> str:
        date = self.commit.date.split(" ")[0]
        files = len(self.commit.files_changed)
        ins = self.commit.insertions
        del_ = self.commit.deletions
        delta = f"+{ins}/-{del_}" if ins or del_ else ""
        return f"{date} | {self.commit.short_hash} | {self.commit.message[:50]} | {files} files | {delta}"


class InteractiveSelector:
    """
    Interactive TUI for commit selection with arrow key navigation.
    """

    def __init__(
        self,
        commits: List[CommitInfo],
        ai_service: AIService,
        prompt_engine: PromptEngine,
    ):
        self.commits = commits
        self.items = [CommitItem(c) for c in commits]
        self.ai_service = ai_service
        self.prompt_engine = prompt_engine
        self.console = Console()
        self.cursor = 0
        self.filter_since: Optional[str] = None
        self.filter_until: Optional[str] = None
        self.selected_style = "daily_changelog"
        self.selected_platform = "twitter"

    def _get_filtered_items(self) -> List[CommitItem]:
        """Get items filtered by date range."""
        if not self.filter_since and not self.filter_until:
            return self.items
        filtered = []
        for item in self.items:
            commit_date = datetime.strptime(
                item.commit.date.split(" ")[0], "%Y-%m-%d"
            )
            if self.filter_since:
                since_date = datetime.strptime(self.filter_since, "%Y-%m-%d")
                if commit_date < since_date:
                    continue
            if self.filter_until:
                until_date = datetime.strptime(self.filter_until, "%Y-%m-%d")
                if commit_date > until_date:
                    continue
            filtered.append(item)
        return filtered

    def _get_selected_items(self) -> List[CommitItem]:
        """Get selected items."""
        return [item for item in self._get_filtered_items() if item.selected]

    def _render_header(self) -> Panel:
        """Render the header panel."""
        selected_count = len(self._get_selected_items())
        filter_info = ""
        if self.filter_since or self.filter_until:
            filter_info = f" | Filter: {self.filter_since or '*'} to {self.filter_until or '*'}"
        header_text = Text.assemble(
            ("BuildPost Commit Selector", "bold cyan"),
            (f"\nSelected: {selected_count} commits{filter_info}", "dim"),
        )
        return Panel(header_text, border_style="cyan")

    def _render_commit_list(self) -> Table:
        """Render the commit list table."""
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Sel", width=4, justify="center")
        table.add_column("Date", width=12)
        table.add_column("Hash", width=8, style="yellow")
        table.add_column("Message", width=40)
        table.add_column("Files", width=6, justify="right")
        table.add_column("+/-", width=10, justify="right")

        filtered = self._get_filtered_items()
        for i, item in enumerate(filtered):
            marker = "[*]" if item.selected else "[ ]"
            marker_style = "green" if item.selected else "dim"
            cursor_marker = ">>" if i == self.cursor else "  "
            cursor_style = "bold white on blue" if i == self.cursor else ""

            date = item.commit.date.split(" ")[0]
            msg = item.commit.message[:38] + "..." if len(item.commit.message) > 38 else item.commit.message
            files = str(len(item.commit.files_changed))
            delta = f"+{item.commit.insertions}/-{item.commit.deletions}"

            row = [
                Text(f"{marker} {cursor_marker}", style=cursor_style if cursor_style else marker_style),
                Text(date, style=cursor_style if cursor_style else ""),
                Text(item.commit.short_hash, style=cursor_style if cursor_style else "yellow"),
                Text(msg, style=cursor_style if cursor_style else ""),
                Text(files, style=cursor_style if cursor_style else "", justify="right"),
                Text(delta, style=cursor_style if cursor_style else "green"),
            ]
            table.add_row(*row)

        return table

    def _render_footer(self) -> Panel:
        """Render the footer with controls."""
        footer_text = Text.assemble(
            ("[Space]", "bold"),
            " Select  ",
            ("[Enter]", "bold"),
            " Confirm  ",
            ("[d]", "bold"),
            " Date filter  ",
            ("[s]", "bold"),
            " Style  ",
            ("[p]", "bold"),
            " Platform  ",
            ("[q]", "bold"),
            " Quit",
        )
        return Panel(footer_text, border_style="cyan")

    def _render_style_panel(self) -> Panel:
        """Render style selection panel."""
        daily_selected = "[*]" if self.selected_style == "daily_changelog" else "[ ]"
        weekly_selected = "[*]" if self.selected_style == "weekly_changelog" else "[ ]"

        content = Text.assemble(
            f"{daily_selected} Daily Changelog (concise, ~150 words)\n",
            f"{weekly_selected} Weekly Changelog (detailed, ~350 words)",
        )
        return Panel(content, title="[bold]Select Style[/bold]", border_style="green")

    def _render_platform_panel(self) -> Panel:
        """Render platform selection panel."""
        twitter_sel = "[*]" if self.selected_platform == "twitter" else "[ ]"
        linkedin_sel = "[*]" if self.selected_platform == "linkedin" else "[ ]"
        devto_sel = "[*]" if self.selected_platform == "devto" else "[ ]"
        generic_sel = "[*]" if self.selected_platform == "generic" else "[ ]"

        content = Text.assemble(
            f"{twitter_sel} Twitter/X\n",
            f"{linkedin_sel} LinkedIn\n",
            f"{devto_sel} Dev.to\n",
            f"{generic_sel} Generic",
        )
        return Panel(content, title="[bold]Select Platform[/bold]", border_style="green")

    def _set_date_filter(self):
        """Set date filter interactively."""
        self.console.print("\n[bold]Date Filter[/bold]")
        since = Prompt.ask("Since (YYYY-MM-DD, empty for no filter)", default="")
        until = Prompt.ask("Until (YYYY-MM-DD, empty for no filter)", default="")

        self.filter_since = since if since else None
        self.filter_until = until if until else None

    def _set_style(self):
        """Set style interactively."""
        self.console.print("\n[bold]Select Style[/bold]")
        self.console.print("[1] Daily Changelog (concise)")
        self.console.print("[2] Weekly Changelog (detailed)")

        choice = Prompt.ask("Choice", choices=["1", "2"], default="1")
        self.selected_style = "daily_changelog" if choice == "1" else "weekly_changelog"

    def _set_platform(self):
        """Set platform interactively."""
        self.console.print("\n[bold]Select Platform[/bold]")
        self.console.print("[1] Twitter/X")
        self.console.print("[2] LinkedIn")
        self.console.print("[3] Dev.to")
        self.console.print("[4] Generic")

        choice = Prompt.ask("Choice", choices=["1", "2", "3", "4"], default="1")
        platforms = ["twitter", "linkedin", "devto", "generic"]
        self.selected_platform = platforms[int(choice) - 1]

    def _build_changelog_context(self, selected_commits: List[CommitInfo]) -> dict:
        """Build context for changelog generation."""
        commit_lines = []
        unique_files = set()
        total_insertions = 0
        total_deletions = 0

        for commit in selected_commits:
            date = commit.date.split(" ")[0]
            file_count = len(commit.files_changed)
            unique_files.update(commit.files_changed)
            total_insertions += commit.insertions
            total_deletions += commit.deletions

            delta_parts = []
            if commit.insertions:
                delta_parts.append(f"+{commit.insertions}")
            if commit.deletions:
                delta_parts.append(f"-{commit.deletions}")
            delta = " ".join(delta_parts) if delta_parts else "0"

            commit_lines.append(
                f"- {date} {commit.short_hash} {commit.message} ({file_count} files, {delta})"
            )

        if selected_commits:
            newest = selected_commits[0].date.split(" ")[0]
            oldest = selected_commits[-1].date.split(" ")[0]
            date_range = f"{oldest} to {newest}"
        else:
            date_range = "No commits selected"

        return {
            "date_range": date_range,
            "range_spec": "selected commits",
            "commit_count": len(selected_commits),
            "unique_files_count": len(unique_files),
            "total_insertions": total_insertions,
            "total_deletions": total_deletions,
            "commits_list": "\n".join(commit_lines) if commit_lines else "No commits.",
        }

    def _generate_preview(self, selected_commits: List[CommitInfo]) -> str:
        """Generate AI preview of the changelog."""
        if not selected_commits:
            return "No commits selected."

        context = self._build_changelog_context(selected_commits)

        try:
            rendered_prompt = self.prompt_engine.render_prompt(self.selected_style, context)
        except KeyError:
            fallback_system = (
                "You are a senior software engineer writing changelogs."
            )
            fallback_template = (
                "Create a changelog from the following commit data.\n\n"
                "Date Range: {date_range}\n"
                "Total Commits: {commit_count}\n"
                "Unique Files: {unique_files_count}\n"
                "Total Changes: +{total_insertions}/-{total_deletions}\n\n"
                "Commits:\n{commits_list}\n\n"
                "Write a concise changelog."
            )
            rendered_prompt = {
                "system": fallback_system,
                "user": fallback_template.format(**context),
            }

        try:
            generated = self.ai_service.generate_post(
                system_prompt=rendered_prompt["system"],
                user_prompt=rendered_prompt["user"],
                max_tokens=800,
                temperature=0.7,
            )
            return generated
        except Exception as e:
            return f"Error generating preview: {e}"

    def _show_preview_screen(self, selected_commits: List[CommitInfo]) -> Optional[str]:
        """Show preview screen and return result."""
        self.console.clear()
        self.console.print("[bold cyan]Generating preview...[/bold cyan]\n")

        preview = self._generate_preview(selected_commits)

        self.console.print(Panel(preview, title="[bold green]Preview[/bold green]", border_style="green"))
        self.console.print()

        self.console.print("[bold]Options:[/bold]")
        self.console.print("[1] Copy to clipboard")
        self.console.print("[2] Write to file")
        self.console.print("[3] Return to selection")
        self.console.print("[4] Exit")

        choice = Prompt.ask("Choice", choices=["1", "2", "3", "4"], default="1")

        if choice == "1":
            try:
                import pyperclip
                pyperclip.copy(preview)
                self.console.print("[green]✓ Copied to clipboard![/green]")
                return preview
            except Exception:
                self.console.print("[yellow]Could not copy to clipboard[/yellow]")
                return preview
        elif choice == "2":
            output_path = Prompt.ask("Output file path")
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(preview)
                self.console.print(f"[green]✓ Written to {output_path}[/green]")
                return preview
            except Exception as e:
                self.console.print(f"[red]Error writing file: {e}[/red]")
                return preview
        elif choice == "3":
            return None
        else:
            sys.exit(0)

    def run(self):
        """Run the interactive selector."""
        try:
            import readchar
        except ImportError:
            self.console.print("[yellow]Installing readchar...[/yellow]")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "readchar"])
            import readchar

        self.console.print("[bold cyan]BuildPost Commit Selector[/bold cyan]")
        self.console.print("Use arrow keys to navigate, Space to select, Enter to confirm\n")

        while True:
            filtered = self._get_filtered_items()
            if self.cursor >= len(filtered):
                self.cursor = max(0, len(filtered) - 1)

            self.console.clear()
            self.console.print(self._render_header())
            self.console.print(self._render_commit_list())
            self.console.print()
            self.console.print(self._render_style_panel())
            self.console.print()
            self.console.print(self._render_platform_panel())
            self.console.print()
            self.console.print(self._render_footer())

            key = readchar.readkey()

            if key == readchar.key.UP:
                self.cursor = max(0, self.cursor - 1)
            elif key == readchar.key.DOWN:
                self.cursor = min(len(filtered) - 1, self.cursor + 1)
            elif key == " ":
                if filtered:
                    filtered[self.cursor].toggle()
            elif key == readchar.key.ENTER:
                selected = self._get_selected_items()
                if not selected:
                    self.console.print("[yellow]No commits selected. Press any key to continue...[/yellow]")
                    readchar.readkey()
                    continue
                result = self._show_preview_screen([item.commit for item in selected])
                if result:
                    break
            elif key.lower() == "d":
                self._set_date_filter()
            elif key.lower() == "s":
                self._set_style()
            elif key.lower() == "p":
                self._set_platform()
            elif key.lower() == "q":
                self.console.print("\n[yellow]Exiting...[/yellow]")
                sys.exit(0)


def run_interactive(config: Config):
    """Run the interactive commit selector."""
    try:
        git_parser = GitParser()
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    console = Console()
    console.print("[bold cyan]Loading commits...[/bold cyan]")

    since_date = datetime.now(timezone.utc) - timedelta(days=7)
    since = since_date.strftime("%Y-%m-%d")
    commits = git_parser.get_commits_by_date(since=since)
    commits = commits[:50]

    if not commits:
        console.print("[yellow]No commits found.[/yellow]")
        sys.exit(0)

    provider = config.get_provider()
    api_key = config.get_api_key(provider)
    if not api_key:
        provider_info = AIService.get_provider_info(provider)
        console.print(
            f"[bold red]Error:[/bold red] No API key found for {provider_info.get('display_name', provider)}.\n"
            f"Set it with: buildpost config set-key --provider {provider} YOUR_API_KEY"
        )
        sys.exit(1)

    ai_service = AIService(
        provider=provider,
        api_key=api_key,
        model=config.get_model(provider),
    )
    prompt_engine = PromptEngine(prompts_file=str(config.get_prompts_file()))

    selector = InteractiveSelector(commits, ai_service, prompt_engine)
    selector.run()