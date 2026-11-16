"""Evaluate archived conversation coverage for private scientific-event review.

Input data must remain private. The public repository contains only this parser
and synthetic tests. Never publish extracted message text or identifiers.
"""
from __future__ import annotations

import json
from pathlib import Path


def conversations_from_shards(paths):
    out = {}
    for path in paths:
        for convo in json.loads(Path(path).read_text(encoding="utf-8")):
            cid = convo.get("id") or convo.get("conversation_id")
            if cid in out:
                raise ValueError("Duplicate conversation ID across shards")
            out[cid] = convo
    return out


def message_text(message):
    if not isinstance(message, dict):
        return ""
    parts = message.get("content", {}).get("parts", [])
    return "\n".join(str(part) for part in parts if isinstance(part, str))


def ancestor_with_role(mapping, anchor_id, role="assistant"):
    """Find closest ancestor of a given role along the anchor's parent chain."""
    anchor = mapping.get(anchor_id)
    if not anchor:
        return None, None
    parent_id = anchor.get("parent")
    seen = {anchor_id}
    while parent_id is not None and parent_id not in seen:
        seen.add(parent_id)
        node = mapping.get(parent_id)
        if node is None:
            return None, None
        message = node.get("message") or {}
        if message.get("author", {}).get("role") == role:
            return parent_id, message
        parent_id = node.get("parent")
    return None, None


def context_status(conversations, conversation_id, anchor_id):
    convo = conversations.get(conversation_id)
    if convo is None:
        return "conversation_unavailable"
    mapping = convo.get("mapping") or {}
    node = mapping.get(anchor_id)
    if node is None:
        return "anchor_unavailable"
    user_msg = node.get("message") or {}
    if user_msg.get("author", {}).get("role") != "user":
        return "anchor_not_user"
    if not message_text(user_msg).strip():
        return "anchor_text_unavailable"
    _, assistant = ancestor_with_role(mapping, anchor_id)
    if assistant is None:
        return "no_preceding_assistant"
    if not message_text(assistant).strip():
        return "preceding_assistant_text_unavailable"
    return "user_and_preceding_assistant_recovered"


def match_source_text(user_text, archived_text):
    """Exact text correspondence; conservative rather than fuzzy matching."""
    return isinstance(user_text, str) and user_text == archived_text
