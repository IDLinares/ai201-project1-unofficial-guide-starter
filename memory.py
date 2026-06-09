def _extract_text(content) -> str:
    """Normalise a Gradio content field to a plain string.

    Gradio 5+ may pass content as a list of typed blocks:
    [{"type": "text", "text": "..."}] — extract and join the text parts.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            block["text"] for block in content
            if isinstance(block, dict) and "text" in block
        )
    return str(content)


def build_retrieval_query(query: str, history: list, n_turns: int = 2) -> str:
    """
    Prepend the last n_turns user messages from history to the current query
    so the retriever has more context for referential follow-ups like
    "tell me more" or "what about for kids?".

    The original query is always the final token so it remains the primary
    signal — prior turns are extra context, not a replacement.

    Handles Gradio's dict format: [{"role": "user", "content": "..."}, ...]
    """
    if not history:
        return query

    recent_user_turns = [
        _extract_text(turn["content"]) for turn in history
        if isinstance(turn, dict) and turn.get("role") == "user" and turn.get("content")
    ][-n_turns:]

    if not recent_user_turns:
        return query

    prior_context = " ".join(recent_user_turns)
    return f"{prior_context} {query}"


def format_history_for_llm(history: list) -> list[dict]:
    """
    Normalise Gradio history for the Groq messages array.

    Gradio 5+ passes history as [{"role": "user"|"assistant", "content": "..."}, ...]
    which is already in the correct format — return it directly.
    """
    return [
        {"role": turn["role"], "content": _extract_text(turn["content"])}
        for turn in history
        if isinstance(turn, dict) and turn.get("role") in ("user", "assistant")
        and turn.get("content")
    ]
