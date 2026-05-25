import hashlib
import os

CACHE_DIR = "cache"

# create cache folder automatically
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def generate_hash(text):

    return hashlib.md5(
        text.encode()
    ).hexdigest()

def get_cached_response(text):

    file_hash = generate_hash(text)

    cache_file = os.path.join(
        CACHE_DIR,
        f"{file_hash}.txt"
    )

    if os.path.exists(cache_file):

        with open(
            cache_file,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    return None

def save_response_to_cache(
    text,
    response
):

    file_hash = generate_hash(text)

    cache_file = os.path.join(
        CACHE_DIR,
        f"{file_hash}.txt"
    )

    with open(
        cache_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(response)