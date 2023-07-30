import requests
import uuid
import sys

from flask import redirect, render_template, session

def get_image():
    """Get a random coffee image from the ☕ Coffee API https://coffee.alexflipnote.dev/, GITHUB: https://github.com/AlexFlipnote/CoffeeAPI"""
    # Prepare API request
    url = (
        f"https://coffee.alexflipnote.dev/random.json"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        image_json = response.json()
        image = image_json["file"]

        return image
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

