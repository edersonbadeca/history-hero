"""
CLI - Command line interface for the dotfiles sync daemon
"""

import click
import logging
import sys
from pathlib import Path

from .daemon import DotfilesSyncDaemon

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dotfiles_sync")


@click.group()
def main():
    """Dotfiles Sync - Automatic dotfiles synchronization daemon"""
    pass


@main.command()
@click.option(
    "--dot-file-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to your dotfiles repository",
)
@click.option(
    "--interval-hours",
    default=24,
    type=int,
    help="Scheduling interval in hours (default: 24)",
)
@click.option(
    "--commit-message",
    default="Auto-sync dotfiles",
    help="Commit message template (default: 'Auto-sync dotfiles')",
)
def start(dot_file_path: str, interval_hours: int, commit_message: str):
    """Start the dotfiles sync daemon"""
    try:
        daemon = DotfilesSyncDaemon(
            dot_file_path=dot_file_path,
            interval_hours=interval_hours,
            commit_message=commit_message,
        )

        if not daemon.start():
            click.echo("Failed to start daemon", err=True)
            sys.exit(1)

        click.echo("✓ Daemon started successfully")
        click.echo(f"  Path: {dot_file_path}")
        click.echo(f"  Interval: {interval_hours} hour(s)")
        click.echo(f"  Logs: {daemon.log_file}")

        # Keep the daemon running
        daemon.wait()

    except ValueError as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n✓ Daemon stopped by user")
        sys.exit(0)
    except Exception as e:
        click.echo(f"✗ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
def stop():
    """Stop the dotfiles sync daemon"""
    pid_file = Path.home() / ".dotfiles-sync" / "daemon.pid"

    if not pid_file.exists():
        click.echo("✗ Daemon is not running", err=True)
        sys.exit(1)

    try:
        import os
        import signal

        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        os.kill(pid, signal.SIGTERM)
        click.echo("✓ Stop signal sent to daemon")
    except ProcessLookupError:
        click.echo("✗ Daemon process not found", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
def status():
    """Check daemon status"""
    pid_file = Path.home() / ".dotfiles-sync" / "daemon.pid"
    log_file = Path.home() / ".dotfiles-sync" / "logs" / "dotfiles-sync.log"

    if pid_file.exists():
        try:
            import os
            import signal

            with open(pid_file, "r") as f:
                pid = int(f.read().strip())

            os.kill(pid, 0)
            click.echo(f"✓ Daemon is running (PID: {pid})")
        except ProcessLookupError:
            click.echo("✗ Daemon is not running (stale PID file)")
            pid_file.unlink()
            sys.exit(1)
    else:
        click.echo("✗ Daemon is not running")
        sys.exit(1)

    if log_file.exists():
        click.echo(f"  Logs: {log_file}")
        click.echo("\n  Latest log entries:")
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in lines[-5:]:
                click.echo(f"    {line.rstrip()}")


@main.command()
@click.option(
    "--dot-file-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to your dotfiles repository",
)
@click.option(
    "--commit-message",
    default="Manual sync - dotfiles",
    help="Commit message for manual sync",
)
def sync(dot_file_path: str, commit_message: str):
    """Manually run a one-time sync"""
    try:
        from .git_manager import GitManager

        git_manager = GitManager(dot_file_path)
        click.echo("Running manual sync...")

        if git_manager.sync(commit_message):
            click.echo("✓ Sync completed successfully")
        else:
            click.echo("✗ Sync completed with warnings", err=True)
            sys.exit(1)

    except ValueError as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

