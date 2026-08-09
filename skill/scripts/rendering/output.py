"""Terminal output formatting for magic circle diagrams."""


def format_output(text, width=None):
    """Centre-pad each line of *text* to *width* columns.

    If *width* is ``None``, the text is returned unchanged.
    """
    if width is None:
        return text
    lines = text.splitlines()
    padded = []
    for line in lines:
        stripped = line.rstrip()
        pad = max(0, (width - len(stripped)) // 2)
        padded.append(" " * pad + stripped)
    return "\n".join(padded)
