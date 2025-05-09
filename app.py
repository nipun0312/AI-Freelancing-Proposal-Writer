from flask import Flask, render_template, request
import os
import requests
import html
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

def generate_proposal_with_groq(project_name, project_details, experience_level):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Write a professional Fiverr/Upwork proposal for the following project:

    ✦ Project Name: {project_name}
    ✦ Project Details: {project_details}
    ✦ My Experience Level: {experience_level}

    Write it in a convincing and friendly tone. Start with a greeting, talk briefly about your experience, show understanding of the client's needs, and end with a strong call to action. Use bullet points if needed.
    """

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        result = response.json()
        raw_text = result['choices'][0]['message']['content']
        return html.escape(raw_text).replace("\n", "<br>")
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    proposal = ""
    if request.method == "POST":
        project_name = request.form["project_name"]
        project_details = request.form["project_details"]
        experience = request.form["experience"]
        proposal = generate_proposal_with_groq(project_name, project_details, experience)
    return render_template("index.html", proposal=proposal)

if __name__ == "__main__":
    app.run(debug=True)
