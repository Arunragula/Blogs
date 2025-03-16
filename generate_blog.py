import requests
import datetime
import yaml
import os
import sys
import json
import random
from pathlib import Path

# Load API key from environment variable (preferred) or config.yaml as fallback
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    try:
        with open("config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
            GEMINI_API_KEY = config.get("gemini_api_key")
            if not GEMINI_API_KEY:
                raise ValueError("No API key found in config.yaml")
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# API endpoint
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# Ensure posts directory exists
os.makedirs("posts", exist_ok=True)
os.makedirs("images", exist_ok=True)

# Define topic categories with specific subtopics
TOPIC_CATEGORIES = {
    "AI & Machine Learning": [
        "Generative AI trends",
        "Machine learning advancements",
        "AI in healthcare",
        "Ethical AI development",
        "Computer vision breakthroughs"
    ],
    "Technology": [
        "Quantum computing developments",
        "Web3 and blockchain technology",
        "Cybersecurity trends",
        "IoT innovations",
        "Cloud computing advancements"
    ],
    "Finance & Business": [
        "Cryptocurrency market analysis",
        "Fintech innovations",
        "Investment strategies",
        "Global economic trends",
        "Sustainable finance"
    ],
    "Science & Innovation": [
        "Space exploration news",
        "Biotechnology breakthroughs",
        "Renewable energy advancements",
        "Nanotechnology applications",
        "Climate technology innovations"
    ]
}

def generate_svg_image(topic):
    """Generate a simple SVG image related to the blog topic"""
    # Define SVG templates for different categories
    svg_templates = {
        "AI & Machine Learning": """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
            <rect width="800" height="400" fill="#f0f8ff"/>
            <circle cx="400" cy="200" r="150" fill="#4a86e8" opacity="0.7"/>
            <circle cx="300" cy="180" r="80" fill="#6aa84f" opacity="0.7"/>
            <circle cx="500" cy="180" r="80" fill="#e06666" opacity="0.7"/>
            <circle cx="400" cy="280" r="80" fill="#f1c232" opacity="0.7"/>
            <text x="400" y="40" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">AI & Machine Learning</text>
            <text x="400" y="375" font-family="Arial" font-size="18" text-anchor="middle" fill="#333">{subtitle}</text>
        </svg>""",
        
        "Technology": """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
            <rect width="800" height="400" fill="#e6f2ff"/>
            <rect x="200" y="100" width="400" height="200" rx="20" fill="#a2c4c9" opacity="0.7"/>
            <circle cx="300" cy="150" r="30" fill="#6fa8dc"/>
            <circle cx="500" cy="150" r="30" fill="#6fa8dc"/>
            <rect x="350" y="220" width="100" height="40" rx="10" fill="#6fa8dc"/>
            <text x="400" y="40" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">Technology</text>
            <text x="400" y="375" font-family="Arial" font-size="18" text-anchor="middle" fill="#333">{subtitle}</text>
        </svg>""",
        
        "Finance & Business": """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
            <rect width="800" height="400" fill="#f9f9f9"/>
            <rect x="250" y="150" width="50" height="150" fill="#76a5af"/>
            <rect x="350" y="100" width="50" height="200" fill="#6fa8dc"/>
            <rect x="450" y="180" width="50" height="120" fill="#8e7cc3"/>
            <rect x="550" y="80" width="50" height="220" fill="#93c47d"/>
            <line x1="200" y1="300" x2="650" y2="300" stroke="#333" stroke-width="2"/>
            <text x="400" y="40" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">Finance & Business</text>
            <text x="400" y="375" font-family="Arial" font-size="18" text-anchor="middle" fill="#333">{subtitle}</text>
        </svg>""",
        
        "Science & Innovation": """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
            <rect width="800" height="400" fill="#f5f5f5"/>
            <circle cx="400" cy="200" r="120" fill="#d5a6bd" opacity="0.5"/>
            <path d="M400,80 L400,320 M280,200 L520,200 M330,130 L470,270 M330,270 L470,130" stroke="#333" stroke-width="2"/>
            <circle cx="400" cy="200" r="40" fill="#9fc5e8"/>
            <text x="400" y="40" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">Science & Innovation</text>
            <text x="400" y="375" font-family="Arial" font-size="18" text-anchor="middle" fill="#333">{subtitle}</text>
        </svg>"""
    }
    
    # Select the right template based on category
    for category, subtopics in TOPIC_CATEGORIES.items():
        if topic in subtopics:
            template = svg_templates[category]
            return template.format(subtitle=topic)
    
    # Default template if no match found
    return svg_templates["Technology"].format(subtitle="Technology Innovation")

def generate_blog():
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Randomly select a category
    category = random.choice(list(TOPIC_CATEGORIES.keys()))
    
    # Select a subtopic from the category
    subtopic = random.choice(TOPIC_CATEGORIES[category])
    
    # Create a title based on the topic
    title = f"{subtopic}: {today} Update"
    
    # Create prompt for content generation
    prompt = f"""Write a professional blog post titled '{title}' about {subtopic}. 
    Include 5 sections with clear headers.
    Each section should be 1-2 paragraphs in length.
    End with a brief conclusion or outlook for the future.
    Total length should be around 700-800 words.
    Use a professional but engaging tone appropriate for a tech/finance/AI blog."""

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {"Content-Type": "application/json"}

    try:
        print(f"🔍 Generating blog about: {subtopic} (Category: {category})")
        response = requests.post(API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()  # Raise error if request fails
        result = response.json()

        # Extract generated text
        blog_content = result["candidates"][0]["content"]["parts"][0]["text"]

        # Generate SVG image
        svg_content = generate_svg_image(subtopic)
        image_filename = f"images/image_{today.replace('-', '')}.svg"
        
        # Save the SVG image
        with open(image_filename, "w", encoding="utf-8") as img_file:
            img_file.write(svg_content)
        
        print(f"✅ Generated image: {image_filename}")
        
        filename = f"posts/blog_{today}.md"
        
        # Format blog content as markdown
        formatted_content = f"""---
title: "{title}"
date: {today}
category: "{category}"
topic: "{subtopic}"
image: "../{image_filename}"
---

# {title}

![{subtopic}](../{image_filename})

{blog_content}

---
*This blog post was automatically generated on {today}. Topics are selected randomly across technology, finance, AI, and science domains.*
"""

        # Save the blog
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_content)

        print(f"✅ Blog saved: {filename}")
        return filename, category, subtopic

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Text: {e.response.text}")
        return None, None, None
    except KeyError as e:
        print(f"❌ Unexpected API Response: {e}")
        return None, None, None

if __name__ == "__main__":
    generate_blog()
