#!/usr/bin/env python3

import logging
import os

from ..git_query import find_git_root
from ..rules import get_applicable_rules_content

__all__ = [
    "user_prompt",
]


async def user_prompt(user_text: str, chat_id: str | None = None) -> str:
    """Store the user's verbatim prompt text for later use.

    This function processes the user's prompt and applies any relevant cursor rules.

    Args:
        user_text: The user's original prompt verbatim
        chat_id: The unique ID of the current chat session

    Returns:
        A message with any applicable cursor rules
    """
    logging.info(f"Received user prompt for chat ID {chat_id}: {user_text}")

    # Get the current working directory to find repo root
    cwd = os.getcwd()
    repo_root = find_git_root(cwd)

    result = "User prompt received"

    # If we're in a git repo, look for applicable rules
    if repo_root:
        # Add applicable rules (no file path for UserPrompt)
        result += get_applicable_rules_content(repo_root)

    return result
