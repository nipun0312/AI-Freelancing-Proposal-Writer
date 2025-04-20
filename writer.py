# writer.py

import requests
import os
from dotenv import load_dotenv

# ✅ Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_proposal_with_groq(service_type, client_description, experience_level):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # ✅ Prompt to generate proposal
    prompt = f"""
    Write a professional Fiverr/Upwork proposal for the following gig:

    ✦ Service: {service_type}
    ✦ Client Request: {client_description}
    ✦ My Experience Level: {experience_level}

    Write it in a convincing and friendly tone. Start with a greeting, talk briefly about your experience, show understanding of the client's needs, and end with a strong call to action.
    """

    data = {
        "model": "llama3-70b-8192",  # ✅ Updated model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\n🔄 Status Code: {response.status_code}")
        print("🔍 Raw Response:\n", response.text)

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"❌ Error: {str(e)}"


# === CLI Interface ===
if __name__ == "__main__":
    print("🚀 AI Freelancing Proposal Writer (Groq + .env)")
    service = input("Enter your service (e.g., Logo Design, Web Scraping): ")
    client_needs = input("Describe what the client wants: ")
    exp = input("Your experience level (e.g., Beginner, 3 years): ")

    proposal = generate_proposal_with_groq(service, client_needs, exp)
    print("\n📄 Generated Proposal:\n")
    print(proposal)
