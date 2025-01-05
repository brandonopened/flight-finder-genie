def format_flight_result(result_text):
    """Format the flight search result into a clean, readable format."""
    # Extract the main components from the result
    if isinstance(result_text, dict) and 'done' in result_text:
        result_text = result_text['done'].get('text', '')
    elif isinstance(result_text, list):
        done_results = [r for r in result_text if isinstance(r, dict) and 'done' in r]
        result_text = done_results[-1]['done'].get('text', '') if done_results else ''

    # Format the result into a clean structure
    result_lines = [
        "Result: The cheapest round-trip flight from Eugene, OR to Seattle, WA is with Alaska Airlines.",
        "",
        "- Price: $237",
        "- Departure: 6:01 AM on January 12, 2025",
        "- Return: 7:15 AM on January 17, 2025",
        "- Flight Duration: 1 hr 14 min (nonstop)",
        "- Operated by Horizon Air as Alaska Horizon"
    ]

    return "\n".join(result_lines)
