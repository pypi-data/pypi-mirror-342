"""
Helper functions for Telegram Bot API.
"""

import re
from typing import Dict, List, Optional, Union, Any

def escape_markdown(text: str, version: int = 1) -> str:
    """
    Escape Markdown special characters.
    
    Args:
        text: Text to escape
        version: Markdown version (1 or 2)
    
    Returns:
        Escaped text
    """
    if version == 1:
        escape_chars = r'_*`['
    else:
        escape_chars = r'_*[]()~`>#+-=|{}.!'
    
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def escape_html(text: str) -> str:
    """
    Escape HTML special characters.
    
    Args:
        text: Text to escape
    
    Returns:
        Escaped text
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def extract_command(text: str) -> Optional[str]:
    """
    Extract command from text.
    
    Args:
        text: Text to extract command from
    
    Returns:
        Command without prefix, or None if no command is found
    """
    if not text:
        return None
    
    # Match /command or /command@bot_username
    match = re.match(r'^/([a-zA-Z0-9_]+)(?:@[a-zA-Z0-9_]+)?', text)
    
    if match:
        return match.group(1)
    
    return None

def extract_args(text: str) -> str:
    """
    Extract arguments from text.
    
    Args:
        text: Text to extract arguments from
    
    Returns:
        Arguments after the command
    """
    if not text:
        return ''
    
    # Match /command or /command@bot_username
    match = re.match(r'^/[a-zA-Z0-9_]+(?:@[a-zA-Z0-9_]+)?(?:\s+(.*))?$', text)
    
    if match and match.group(1):
        return match.group(1)
    
    return ''

def split_message(text: str, max_length: int = 4096) -> List[str]:
    """
    Split a message into multiple messages if it exceeds the maximum length.
    
    Args:
        text: Text to split
        max_length: Maximum length of each message
    
    Returns:
        List of message parts
    """
    if len(text) <= max_length:
        return [text]
    
    parts = []
    
    for i in range(0, len(text), max_length):
        parts.append(text[i:i + max_length])
    
    return parts
