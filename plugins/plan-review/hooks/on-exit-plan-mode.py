#!/usr/bin/env python3
"""PreToolUse hook for ExitPlanMode - opens plan review playground."""

import json
import os
import subprocess
import sys
from pathlib import Path


def get_plans_directory():
    """Get plans directory from Claude settings, with fallbacks."""
    cwd = Path.cwd()

    # Try to read from project's .claude/settings.json first
    project_settings = cwd / ".claude" / "settings.json"
    if project_settings.exists():
        try:
            settings = json.loads(project_settings.read_text())
            if "plansDirectory" in settings:
                plans_dir = settings["plansDirectory"]
                # Handle relative paths (starting with ./)
                if plans_dir.startswith("./"):
                    return cwd / plans_dir[2:]
                elif plans_dir.startswith("~/"):
                    return Path.home() / plans_dir[2:]
                else:
                    return Path(plans_dir)
        except Exception:
            pass

    # Try global settings
    global_settings = Path.home() / ".claude" / "settings.json"
    if global_settings.exists():
        try:
            settings = json.loads(global_settings.read_text())
            if "plansDirectory" in settings:
                plans_dir = settings["plansDirectory"]
                if plans_dir.startswith("./"):
                    return cwd / plans_dir[2:]
                elif plans_dir.startswith("~/"):
                    return Path.home() / plans_dir[2:]
                else:
                    return Path(plans_dir)
        except Exception:
            pass

    # Fallback: check common locations
    project_plans = cwd / ".claude" / "plans"
    if project_plans.exists():
        return project_plans

    home_plans = Path.home() / ".claude" / "plans"
    return home_plans


def find_latest_plan():
    """Find the most recently modified plan file."""
    plans_dir = get_plans_directory()

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
            plans_dir = get_plans_directory()
            print(json.dumps({
                "systemMessage": f"No plan file found in {plans_dir}"
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
