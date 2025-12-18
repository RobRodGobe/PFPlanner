from Backend.services.sanitize import sanitize_number

def test_sanitize_commas():
    assert sanitize_number("1,234") == 1234

def test_sanitize_dollar():
    assert sanitize_number("$5,000") == 5000

def test_invalid():
    assert sanitize_number("abc") is None
