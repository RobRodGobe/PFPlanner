def sanitize_number(value):
    if value is None or value == "":
        return None
    try:
        cleaned = (
            str(value)
            .replace(",", "")
            .replace("$", "")
            .replace("%", "")
            .strip()
        )
        return float(cleaned)
    except ValueError:
        return None
