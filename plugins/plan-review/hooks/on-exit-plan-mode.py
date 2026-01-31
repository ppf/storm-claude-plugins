#!/usr/bin/env python3
"""PreToolUse hook for ExitPlanMode - opens plan review playground."""

import json
import os
import subprocess
import sys
from glob import glob
from pathlib import Path


def find_latest_plan():
    """Find the most recently modified plan file."""
    plans_dir = Path.home() / ".claude" / "plans"
    if not plans_dir.exists():
        return None

    plan_files = list(plans_dir.glob("*.md"))
    if not plan_files:
        return None

    # Sort by modification time, newest first
    plan_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return plan_files[0]


def load_template():
    """Load the HTML template."""
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT', '')
    template_path = Path(plugin_root) / "templates" / "plan-review.html"

    if template_path.exists():
        return template_path.read_text()
    return None


def escape_js_string(s):
    """Escape a string for safe inclusion in JavaScript."""
    return (s
            .replace('\\', '\\\\')
            .replace('`', '\\`')
            .replace('$', '\\$'))


def main():
    try:
        # Read stdin (tool context)
        input_data = json.load(sys.stdin)

        # Find the latest plan file
        plan_path = find_latest_plan()
        if not plan_path:
            print(json.dumps({
                "systemMessage": "No plan file found in ~/.claude/plans/"
            }))
            sys.exit(0)

        # Read plan content
        plan_content = plan_path.read_text()
        plan_name = plan_path.stem  # filename without extension

        # Load template
        template = load_template()
        if not template:
            print(json.dumps({
                "systemMessage": "Plan review template not found"
            }))
            sys.exit(0)

        # Inject plan content into template
        html = template.replace('{{PLAN_NAME}}', plan_name)
        html = html.replace('{{PLAN_CONTENT}}', escape_js_string(plan_content))

        # Write to temp file
        temp_path = Path(f"/tmp/plan-review-{plan_name}.html")
        temp_path.write_text(html)

        # Open in browser
        subprocess.run(['open', str(temp_path)], check=False)

        # Return success message
        print(json.dumps({
            "systemMessage": f"Plan review playground opened for '{plan_name}'. "
                           f"Add your comments, then copy and paste them back here."
        }))

    except Exception as e:
        # On error, allow operation to proceed
        print(json.dumps({
            "systemMessage": f"Plan review hook error: {e}"
        }))

    sys.exit(0)


if __name__ == '__main__':
    main()
