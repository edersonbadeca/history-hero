# History Hero - Dotfiles Sync Daemon
<p align="center">
<img src="./assets/logo.png" alt="history hero logo" width="459" height="310"/>
</p>
A Python daemon application that automatically synchronizes your dotfiles with a git repository.

## Features

- 🔄 Automatic git add, commit, and push operations
- ⏰ Configurable scheduling (default: once per day)
- 🎯 Custom dotfiles path support
- 🖥️ Background daemon mode
- 📝 Detailed logging

## Installation

### Quick Install (Curl)

```bash
curl -sSL https://raw.githubusercontent.com/edersonbadeca/history-hero/main/install.sh | bash
```

### Using pip

```bash
pip install dotfiles-sync
```

Or from source:

```bash
git clone https://github.com/edersonbadeca/history-hero.git
cd history-hero
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
- A Git repository initialized in your dotfiles directory
- Python 3.8+
- Git

