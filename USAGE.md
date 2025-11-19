# Dotfiles Sync Configuration

This package can be installed and used to manage your dotfiles repository automatically.

## Quick Start

1. Install the package:
```bash
pip install -e .
```

2. Start the daemon:
```bash
dotfiles-sync start --dot-file-path ~/dot-files
```

3. Check status:
```bash
dotfiles-sync status
```

4. Stop the daemon:
```bash
dotfiles-sync stop
```

## Advanced Usage

### Custom sync interval
```bash
dotfiles-sync start --dot-file-path ~/dot-files --interval-hours 6
```

### Manual sync
```bash
dotfiles-sync sync --dot-file-path ~/dot-files
```

### View logs
```bash
tail -f ~/.dotfiles-sync/logs/dotfiles-sync.log
```

