# Dotfiles Sync

A Python daemon application that automatically synchronizes your dotfiles with a git repository.

## Features

- 🔄 Automatic git add, commit, and push operations
- ⏰ Configurable scheduling (default: once per day)
- 🎯 Custom dotfiles path support
- 🖥️ Background daemon mode
- 📝 Detailed logging

## Installation

```bash
pip install dotfiles-sync
```

Or from source:

```bash
git clone <repo-url>
cd dotfiles-sync
pip install -e .
```

## Usage

### Start the daemon

```bash
dotfiles-sync start --dot-file-path /path/to/your/dotfiles
```

### Schedule with custom interval

```bash
dotfiles-sync start --dot-file-path /path/to/your/dotfiles --interval-hours 6
```

### Stop the daemon

```bash
dotfiles-sync stop
```

### Check status

```bash
dotfiles-sync status
```

## Configuration

The app supports the following parameters:

- `--dot-file-path`: Path to your dotfiles directory (required)
- `--interval-hours`: Scheduling interval in hours (default: 24)
- `--commit-message`: Custom commit message template (default: "Auto-sync dotfiles")

## Examples

```bash
# Sync once per day (default)
dotfiles-sync start --dot-file-path ~/.dotfiles

# Sync every 6 hours
dotfiles-sync start --dot-file-path ~/.dotfiles --interval-hours 6

# Sync every hour
dotfiles-sync start --dot-file-path ~/.dotfiles --interval-hours 1
```

## Logging

Logs are saved to `~/.dotfiles-sync/logs/dotfiles-sync.log`

## Requirements

- Python 3.8+
- Git

