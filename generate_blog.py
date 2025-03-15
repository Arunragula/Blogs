import requests
import datetime
import yaml
import os
import json
from pathlib import Path

# Load API key from config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
GEMINI_API_KEY = config["gemini_api_key"]

# API endpoint
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# Ensure posts directory exists
os.makedirs("posts", exist_ok=True)

def generate_blog():
    today = datetime.date.today().strftime("%Y-%m-%d")
    title = f"AI Trends and Innovations: {today} Update"
    prompt = f"Write a 500-word blog titled '{title}' about the latest AI trends in a professional tone. Include 5 sections with headers."

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise error if request fails
        result = response.json()

        # Extract generated text
        blog_content = result["candidates"][0]["content"]["parts"][0]["text"]

        filename = f"posts/blog_{today}.md"

        # Format as markdown with frontmatter
        formatted_content = f"""---
title: "{title}"
date: {today}
---

{blog_content}
"""

        # Save the blog
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_content)

        print(f"✅ Blog saved: {filename}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        return None
    except KeyError as e:
        print(f"❌ Unexpected API Response: {e}")
        return None

if __name__ == "__main__":
    generate_blog()
