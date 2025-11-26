
from google.genai import types

def dump_event_texts(events, label="DEBUG_EVENTS"):
    print(f"\n[{label}] Dumping event texts:")
    for i, e in enumerate(events):
        content = getattr(e, "content", None)
        if not content:
            continue

        parts = getattr(content, "parts", [])
        for j, part in enumerate(parts):
            text = getattr(part, "text", None)
            if text:
                print(f"\n--- event #{i} part #{j} ---")
                print(text[:1500])  # truncamos para no spamear
