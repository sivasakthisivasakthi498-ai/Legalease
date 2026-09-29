def sanitize_text(text: str | None) -> str:
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u00a0": " ",
    }
    result = "" if text is None else str(text)
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result.strip()

def format_txt(text: str | None) -> bytes:
    return sanitize_text(text).encode("utf-8")
