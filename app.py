# app.py

from flask import Flask, render_template, request, jsonify
from webscout import PhindSearch

# Initialize Flask app
app = Flask(__name__)

# Function to generate resume section using Phind
def generate_resume_section(prompt):
    ph = PhindSearch()
    response = ph.ask(prompt)
    message = ph.get_message(response)
    return message

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to generate the resume
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')

    try:
        # Generate resume sections with clear prompts
        objective = generate_resume_section(
            f"Write a concise resume objective for a {role}. Keep it to about 20 words, focusing solely on the skills and aspirations relevant to this role. Avoid unnecessary phrases."
        )
        
        skills = generate_resume_section(
            f"List 10 to 20 key skills relevant for a {role}, separated by commas. Avoid introductory phrases. Example: skill1, skill2, skill3."
        )
        
        education = generate_resume_section(
            f"Create a brief education section for a {role}. Include degrees, institutions, and years of graduation. Do not add unnecessary explanations."
        )
        
        experience = generate_resume_section(
            f"Write a detailed professional experience section for a {role}. Include relevant job titles, companies, and responsibilities without unnecessary phrases."
        )

        # Create a response object
        resume = {
            'name': name,
            'email': email,
            'phone': phone,
            'objective': objective,
            'skills': skills,
            'education': education,
            'experience': experience
        }
        return jsonify(resume)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
