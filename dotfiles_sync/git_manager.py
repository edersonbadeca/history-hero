"""
Git Manager - Handles git operations for dotfiles
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GitManager:
    """Manages git operations for dotfiles repository"""

    def __init__(self, repo_path: str):
        """
        Initialize GitManager

        Args:
            repo_path: Path to the dotfiles repository
        """
        self.repo_path = Path(repo_path).expanduser()

        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")

        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def add_all(self) -> bool:
        """
        Add all changes to staging area

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "add", "."],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                logger.info(f"Successfully staged changes in {self.repo_path}")
                return True
            else:
                logger.error(f"Failed to stage changes: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error during git add: {str(e)}")
            return False

    def commit(self, message: str) -> bool:
        """
        Commit staged changes

        Args:
            message: Commit message

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Return code 1 can mean no changes to commit (not an error)
            if result.returncode == 0:
                logger.info(f"Successfully committed: {message}")
                return True
            elif result.returncode == 1 and "nothing to commit" in result.stdout:
                logger.info("No changes to commit")
                return True
            else:
                logger.error(f"Failed to commit: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error during git commit: {str(e)}")
            return False

    def push(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Push commits to remote repository

        Args:
            remote: Remote repository name (default: origin)
            branch: Branch name (default: current branch)

        Returns:
            True if successful, False otherwise
        """
        try:
            if branch:
                cmd = ["git", "push", remote, branch]
            else:
                cmd = ["git", "push", remote]

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                logger.info(f"Successfully pushed to {remote}")
                return True
            else:
                logger.error(f"Failed to push: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error during git push: {str(e)}")
            return False

    def sync(self, commit_message: str = "Auto-sync dotfiles") -> bool:
        """
        Perform full sync: add, commit, and push

        Args:
            commit_message: Message for the commit

        Returns:
            True if all operations successful, False otherwise
        """
        logger.info(f"Starting dotfiles sync for {self.repo_path}")

        if not self.add_all():
            logger.warning("Failed to stage changes, skipping commit and push")
            return False

        if not self.commit(commit_message):
            logger.warning("Failed to commit, skipping push")
            return False

        if not self.push():
            logger.warning("Failed to push")
            return False

        logger.info("Dotfiles sync completed successfully")
        return True

