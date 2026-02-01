# Storm Plugins

Custom Claude Code plugins marketplace.

## Plugins

### plan-review

Interactive plan review with line-by-line commenting. Supports both **browser playground** and **terminal TUI** modes.

**Features:**
- 🎯 **Auto-launches** when `ExitPlanMode` is called
- 💻 **Two modes**:
  - **Browser**: Web-based playground with click-to-comment
  - **TUI**: Terminal interface with keyboard-driven workflow ([tui-ccplan-review](https://github.com/ppf/tui-ccplan-review))
- 🔄 **Smart fallback**: TUI → Browser if not in tmux
- 📋 **Clipboard integration**: Copy feedback back to Claude
- ⌨️ **TUI features**: Section navigation, approve/reject, auto-save, theme support
- ⚙️ **Configurable**: Switch modes via `~/.claude/settings.json`

**TUI Mode Setup:**
```json
{
  "planReview": {
    "mode": "tui",
    "tuiCommand": "ccplan-review-latest"
  }
}
```

See [plan-review/README.md](plugins/plan-review/README.md) for complete documentation.

## Installation

Add this marketplace to Claude Code:

```bash
# The marketplace will be added when you install a plugin from it
claude plugins install plan-review --marketplace https://github.com/ppf/storm-claude-plugins
```

Or manually add to `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "storm-plugins": {
    "source": {
      "source": "github",
      "repo": "ppf/storm-claude-plugins"
    }
  }
}
```
