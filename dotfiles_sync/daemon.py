"""
Daemon Manager - Handles daemon lifecycle and scheduling
"""

import schedule
import time
import threading
import logging
import atexit
from pathlib import Path
from typing import Optional
from datetime import datetime

from .git_manager import GitManager

logger = logging.getLogger(__name__)


class DotfilesSyncDaemon:
    """Daemon that schedules and runs dotfiles synchronization"""

    def __init__(
        self,
        dot_file_path: str,
        interval_hours: int = 24,
        commit_message: str = "Auto-sync dotfiles",
    ):
        """
        Initialize the daemon

        Args:
            dot_file_path: Path to dotfiles repository
            interval_hours: Schedule interval in hours (default: 24)
            commit_message: Commit message template
        """
        self.dot_file_path = dot_file_path
        self.interval_hours = interval_hours
        self.commit_message = commit_message
        self.git_manager = GitManager(dot_file_path)
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.pid_file = Path.home() / ".dotfiles-sync" / "daemon.pid"
        self.log_file = Path.home() / ".dotfiles-sync" / "logs" / "dotfiles-sync.log"

        # Create necessary directories
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """Configure logging"""
        logger = logging.getLogger("dotfiles_sync")
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _schedule_task(self):
        """Schedule the sync task"""
        schedule.every(self.interval_hours).hours.do(self._sync_task)
        logger.info(
            f"Scheduled dotfiles sync every {self.interval_hours} hour(s)"
        )

    def _sync_task(self):
        """Execute the sync task"""
        logger.info(f"[{datetime.now().isoformat()}] Running scheduled sync...")
        try:
            success = self.git_manager.sync(self.commit_message)
            if success:
                logger.info("Sync completed successfully")
            else:
                logger.warning("Sync completed with warnings")
        except Exception as e:
            logger.error(f"Sync failed with error: {str(e)}")

    def _run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Scheduler started")
        self._schedule_task()

        # Also run on startup
        self._sync_task()

        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def _write_pid(self):
        """Write PID to file"""
        import os

        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))
        logger.info(f"PID file written: {self.pid_file}")

    def _cleanup(self):
        """Cleanup resources"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                logger.info("PID file removed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def start(self):
        """Start the daemon"""
        if self.running:
            logger.warning("Daemon is already running")
            return False

        logger.info("Starting Dotfiles Sync Daemon")
        logger.info(f"Repository path: {self.dot_file_path}")
        logger.info(f"Interval: {self.interval_hours} hour(s)")

        self.running = True
        self._write_pid()
        atexit.register(self._cleanup)

        self.thread = threading.Thread(target=self._run_scheduler, daemon=False)
        self.thread.start()

        logger.info("Daemon started successfully")
        return True

    def stop(self):
        """Stop the daemon"""
        if not self.running:
            logger.warning("Daemon is not running")
            return False

        logger.info("Stopping daemon...")
        self.running = False

        if self.thread:
            self.thread.join(timeout=5)

        logger.info("Daemon stopped")
        return True

    def is_running(self) -> bool:
        """Check if daemon is running"""
        if not self.pid_file.exists():
            return False

        try:
            import os
            import signal

            with open(self.pid_file, "r") as f:
                pid = int(f.read().strip())

            # Send signal 0 to check if process exists
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError, FileNotFoundError):
            return False

    def wait(self):
        """Wait for daemon thread to finish"""
        if self.thread:
            self.thread.join()

