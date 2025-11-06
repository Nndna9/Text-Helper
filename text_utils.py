from datetime import datetime

def to_upper(text):
    return text.upper()

def to_lower(text):
    return text.lower()

def strip_text(text):
    return text.strip()

def replace_text(text, old, new):
    return text.replace(old, new)

def count_substring(text, sub):
    return text.count(sub)

def get_stats(text):
    lines = text.splitlines()
    line_count = len(lines)
    word_count = len(text.split())
    char_count = len(text)
    return line_count, word_count, char_count

def add_timestamp(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{text}\n\nProcessed on: {timestamp}"
