import requests
import datetime
import yaml
import os

# Load API key from config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
GEMINI_API_KEY = config["gemini_api_key"]

# API endpoint
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# Ensure posts directory exists
os.makedirs("posts", exist_ok=True)

def generate_blog():
    prompt = "Write a 500-word blog on the latest AI trends in a professional tone."

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

        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"posts/blog_{today}.md"

        # Save the blog
        with open(filename, "w", encoding="utf-8") as file:
            file.write(blog_content)

        print(f"✅ Blog saved: {filename}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
    except KeyError:
        print(f"❌ Unexpected API Response: {result}")

if __name__ == "__main__":
    generate_blog()
