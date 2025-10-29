"""Git repository parser for extracting commit information."""

import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from git import Repo, Commit, InvalidGitRepositoryError, BadName


@dataclass
class CommitInfo:
    """Structured information about a git commit."""

    hash: str
    short_hash: str
    message: str
    author: str
    date: str
    files_changed: List[str]
    diff_summary: str
    insertions: int
    deletions: int

    def to_dict(self) -> Dict:
        """Convert to dictionary for template rendering."""
        return {
            'commit_hash': self.hash,
            'short_hash': self.short_hash,
            'commit_message': self.message,
            'author': self.author,
            'date': self.date,
            'files_changed': ', '.join(self.files_changed) if self.files_changed else 'No files',
            'diff_summary': self.diff_summary,
            'insertions': self.insertions,
            'deletions': self.deletions,
            'files_count': len(self.files_changed),
        }


class GitParser:
    """Parse git repository and extract commit information."""

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize GitParser.

        Args:
            repo_path: Path to git repository. If None, uses current directory.

        Raises:
            InvalidGitRepositoryError: If path is not a git repository.
        """
        self.repo_path = repo_path or os.getcwd()
        try:
            self.repo = Repo(self.repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            raise InvalidGitRepositoryError(
                f"'{self.repo_path}' is not a git repository. "
                "Please run this command from within a git repository."
            )

    def get_latest_commit(self) -> CommitInfo:
        """
        Get the latest commit from the current branch.

        Returns:
            CommitInfo object with commit details.
        """
        commit = self.repo.head.commit
        return self._parse_commit(commit)

    def get_commit(self, commit_ref: str) -> CommitInfo:
        """
        Get a specific commit by reference (hash, tag, branch).

        Args:
            commit_ref: Git reference (commit hash, branch name, tag, etc.)

        Returns:
            CommitInfo object with commit details.

        Raises:
            BadName: If commit reference is invalid.
        """
        try:
            commit = self.repo.commit(commit_ref)
            return self._parse_commit(commit)
        except BadName:
            raise BadName(
                f"Invalid commit reference: '{commit_ref}'. "
                "Please provide a valid commit hash, branch, or tag."
            )

    def get_commit_range(self, rev_range: str) -> List[CommitInfo]:
        """
        Get multiple commits from a range.

        Args:
            rev_range: Git revision range (e.g., 'HEAD~5..HEAD', 'main..feature')

        Returns:
            List of CommitInfo objects.
        """
        commits = list(self.repo.iter_commits(rev_range))
        return [self._parse_commit(commit) for commit in commits]

    def _parse_commit(self, commit: Commit) -> CommitInfo:
        """
        Parse a git Commit object into CommitInfo.

        Args:
            commit: GitPython Commit object

        Returns:
            CommitInfo with parsed data
        """
        # Get commit basic info
        commit_hash = commit.hexsha
        short_hash = commit.hexsha[:7]
        message = commit.message.strip()
        author = f"{commit.author.name} <{commit.author.email}>"
        date = commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Get changed files
        files_changed = []
        insertions = 0
        deletions = 0

        # Get diff stats
        if commit.parents:
            # Compare with parent commit
            parent = commit.parents[0]
            diffs = parent.diff(commit)

            for diff in diffs:
                if diff.a_path:
                    files_changed.append(diff.a_path)
                elif diff.b_path:
                    files_changed.append(diff.b_path)

            # Get stats
            stats = commit.stats.total
            insertions = stats.get('insertions', 0)
            deletions = stats.get('deletions', 0)
        else:
            # Initial commit - get all files
            files_changed = list(commit.stats.files.keys())
            stats = commit.stats.total
            insertions = stats.get('insertions', 0)
            deletions = stats.get('deletions', 0)

        # Create diff summary
        diff_summary = self._create_diff_summary(
            files_changed, insertions, deletions
        )

        return CommitInfo(
            hash=commit_hash,
            short_hash=short_hash,
            message=message,
            author=author,
            date=date,
            files_changed=files_changed,
            diff_summary=diff_summary,
            insertions=insertions,
            deletions=deletions,
        )

    def _create_diff_summary(
        self,
        files: List[str],
        insertions: int,
        deletions: int
    ) -> str:
        """
        Create a human-readable summary of changes.

        Args:
            files: List of changed file paths
            insertions: Number of lines added
            deletions: Number of lines deleted

        Returns:
            Summary string
        """
        file_count = len(files)

        # Categorize files by extension
        file_types = {}
        for file_path in files:
            ext = os.path.splitext(file_path)[1] or 'no extension'
            file_types[ext] = file_types.get(ext, 0) + 1

        # Build summary
        parts = []

        # File count
        parts.append(f"{file_count} file{'s' if file_count != 1 else ''} changed")

        # File types (top 3)
        if file_types:
            top_types = sorted(
                file_types.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            type_str = ', '.join([f"{ext} ({count})" for ext, count in top_types])
            parts.append(f"types: {type_str}")

        # Lines changed
        if insertions or deletions:
            changes = []
            if insertions:
                changes.append(f"+{insertions}")
            if deletions:
                changes.append(f"-{deletions}")
            parts.append(' '.join(changes))

        return ' | '.join(parts)

    def is_repo_clean(self) -> bool:
        """Check if repository has uncommitted changes."""
        return not self.repo.is_dirty()

    def get_current_branch(self) -> str:
        """Get current branch name."""
        return self.repo.active_branch.name
