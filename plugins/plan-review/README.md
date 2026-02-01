# Plan Review Plugin

Interactive plan review with line-by-line commenting. Supports both browser-based playground and terminal TUI modes.

## Features

- 🎯 **Auto-launches** on plan mode exit
- 💬 **Two modes**: Browser playground or Terminal TUI
- 🔄 **Smart fallback**: TUI → Browser if not in tmux
- ⚙️ **Configurable**: Easy mode switching via settings

## Installation

The plugin is automatically installed from the storm-plugins marketplace.

### Optional: TUI Mode Setup

For terminal-based plan reviews (recommended for tmux users):

**1. Install TUI tool:**
```bash
git clone https://github.com/ppf/tui-ccplan-review.git
cd tui-ccplan-review
python -m venv venv
source venv/bin/activate
pip install -e .
```

**2. Add to PATH:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$PATH:/path/to/tui-ccplan-review/bin"
```

**3. Configure tmux (optional but recommended):**
```bash
# Add to ~/.tmux.conf
bind-key P display-popup -E -w 90% -h 90% \
  "/path/to/tui-ccplan-review/bin/ccplan-review-latest"
```

**4. Enable TUI mode in Claude settings:**
```json
{
  "planReview": {
    "mode": "tui",
    "tuiCommand": "ccplan-review-latest"
  }
}
```

Add to `~/.claude/settings.json` (global) or `.claude/settings.json` (per-project).

## Usage

### Automatic (On Plan Exit)

When you exit plan mode in Claude Code, the hook automatically:

**TUI Mode (in tmux):**
- Launches TUI in 90% popup
- Navigate with `n/p`, comment with `c`, approve/reject with `a/r`
- Generate summary with `s` (auto-copied to clipboard)
- Paste summary back to Claude

**Browser Mode:**
- Opens browser playground
- Add comments inline
- Copy summary back to Claude

### Manual Launch

**TUI:**
```bash
# Review specific plan
ccplan-review ~/.claude/plans/my-plan.md

# Review latest plan
ccplan-review-latest
```

**Browser:**
- Open `.html` file from `/tmp/plan-review-*.html`

## Configuration

### Mode Selection

Add to `~/.claude/settings.json`:

```json
{
  "planReview": {
    "mode": "tui",              // "tui" or "browser"
    "tuiCommand": "ccplan-review-latest"  // TUI command to run
  }
}
```

### Switch Modes

**Use TUI (terminal-based):**
```bash
jq '.planReview.mode = "tui"' ~/.claude/settings.json | sponge ~/.claude/settings.json
```

**Use Browser (web-based):**
```bash
jq '.planReview.mode = "browser"' ~/.claude/settings.json | sponge ~/.claude/settings.json
```

## TUI Mode Features

When using TUI mode, you get:

- 🔢 **Line numbers** with current line indicator
- 📍 **Section navigation** (n/p) with auto-scroll
- 💬 **Inline comments** - add, edit, delete (multiple per line)
- ✅ **Approve/reject sections** with reasons
- 📋 **Summary generation** - auto-copy to clipboard
- 🔄 **Auto-save** - review state persists
- 🎨 **Theme support** - dracula, monokai, nord, etc.
- ⌨️ **Keyboard-driven** workflow

## How It Works

### Hook Flow

```
Exit Plan Mode (ExitPlanMode tool called)
  ↓
on-exit-plan-mode.py hook runs
  ↓
Read ~/.claude/settings.json
  ↓
Check planReview.mode
  ├─ "tui" → Check if in tmux
  │   ├─ In tmux → Launch TUI popup ✅
  │   └─ Not in tmux → Fallback to browser
  └─ "browser" → Open browser playground
```

### Settings Locations

Hook checks in order:
1. `.claude/settings.json` (project-local)
2. `~/.claude/settings.json` (global)
3. Default: `browser` mode

## Troubleshooting

### TUI not launching in tmux

**Check:**
1. Is TUI installed? `which ccplan-review-latest`
2. Is PATH set? `echo $PATH | grep tui-ccplan-review`
3. Is tmux running? `echo $TMUX`
4. Is mode set? `jq '.planReview.mode' ~/.claude/settings.json`

**Fix:**
```bash
# Reinstall TUI
cd /path/to/tui-ccplan-review
source venv/bin/activate
pip install -e .

# Verify
ccplan-review-latest --version
```

### Falls back to browser every time

**Reason:** Not in tmux session or TUI command not found

**Fix:**
- Start tmux: `tmux`
- Ensure TUI installed and in PATH
- Check settings: `jq '.planReview' ~/.claude/settings.json`

### Browser mode not working

**Check template exists:**
```bash
ls ~/.claude/plugins/marketplaces/storm-plugins/plugins/plan-review/templates/plan-review.html
```

## Files

```
plan-review/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── hooks/
│   ├── hooks.json               # Hook registration
│   ├── on-exit-plan-mode.py     # Main hook (launches review)
│   └── on-user-prompt.py        # User prompt hook
├── templates/
│   └── plan-review.html         # Browser playground template
└── README.md                    # This file
```

## Development

### Hook Modification

Edit `hooks/on-exit-plan-mode.py` to customize behavior.

**Key functions:**
- `get_review_mode()` - Read settings
- `launch_tui_review()` - Launch TUI in tmux
- `launch_browser_review()` - Open browser
- `is_in_tmux()` - Detect tmux

### Template Modification

Edit `templates/plan-review.html` for browser playground UI.

## Links

- **TUI Tool**: https://github.com/ppf/tui-ccplan-review
- **Storm Plugins**: https://github.com/ppf/storm-claude-plugins

## License

MIT
