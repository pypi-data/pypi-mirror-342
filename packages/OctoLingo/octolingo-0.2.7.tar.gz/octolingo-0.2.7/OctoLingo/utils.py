import re
import hashlib
from functools import wraps

def split_text_into_chunks(text, max_chunk_size=4900):
    """Split the text into chunks, ensuring sentences are not broken."""
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split by sentence boundaries
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def cache_translation(func):
    """Decorator to cache translations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        text = args[1]  # Assuming text is the second argument
        dest_language = args[2]  # Assuming dest_language is the third argument
        cache_key = hashlib.md5(f"{text}_{dest_language}".encode('utf-8')).hexdigest()

        # Check cache
        if cache_key in wrapper.cache:
            return wrapper.cache[cache_key]

        # Call the function and cache the result
        result = func(*args, **kwargs)
        wrapper.cache[cache_key] = result
        return result

    wrapper.cache = {}  # Initialize cache
    return wrapper