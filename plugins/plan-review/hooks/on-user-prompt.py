#!/usr/bin/env python3
"""UserPromptSubmit hook - detects plan review comments in clipboard."""

import json
import re
import subprocess
import sys


def get_clipboard():
    """Read clipboard content using pbpaste (macOS)."""
    try:
        result = subprocess.run(
            ['pbpaste'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout
    except Exception:
        return ""


def main():
    try:
        # Read stdin (not used, but required)
        json.load(sys.stdin)

        # Get clipboard content
        clipboard = get_clipboard()

        # Check for plan review marker
        marker_match = re.search(r'<!-- PLAN-REVIEW:([^>]+) -->', clipboard)

        if not marker_match:
            # No marker found, exit silently
            print(json.dumps({}))
            sys.exit(0)

        plan_name = marker_match.group(1)

        # Extract the comments (everything after the marker)
        comments = clipboard[marker_match.end():].strip()

        if not comments:
            print(json.dumps({}))
            sys.exit(0)

        # Inject as system message
        print(json.dumps({
            "systemMessage": f"[Plan Review Feedback for '{plan_name}']\n\n{comments}"
        }))

    except Exception as e:
        # On error, allow operation to proceed
        print(json.dumps({
            "systemMessage": f"Plan review clipboard hook error: {e}"
        }))

    sys.exit(0)


if __name__ == '__main__':
    main()
