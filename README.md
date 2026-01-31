# Storm Plugins

Custom Claude Code plugins marketplace.

## Plugins

### plan-review

Interactive plan review playground with line-by-line commenting.

**Features:**
- Automatically opens in browser when `ExitPlanMode` is called
- Click any line to add comments
- Clipboard-based feedback injection back into Claude
- Dark theme, monospace font for code

## Installation

Add this marketplace to Claude Code:

```bash
# The marketplace will be added when you install a plugin from it
claude plugins install plan-review --marketplace https://github.com/YOUR_USERNAME/storm-plugins
```

Or manually add to `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "storm-plugins": {
    "source": {
      "source": "github",
      "repo": "YOUR_USERNAME/storm-plugins"
    }
  }
}
```
