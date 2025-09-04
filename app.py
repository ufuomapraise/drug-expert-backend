from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This lets your React app talk to Flask without errors

drug_knowledge_base = {
    "headache": {
        "recommended_drugs": ["Paracetamol", "Ibuprofen"],
        "dosage": "1 tablet every 6 hours after food",
        "side_effects": ["Nausea", "Dizziness"],
        "interactions": ["Avoid with alcohol"]
    },
    "fever": {
        "recommended_drugs": ["Paracetamol", "Aspirin"],
        "dosage": "1 tablet every 4–6 hours",
        "side_effects": ["Stomach upset"],
        "interactions": ["Avoid with blood thinners"]
    },
    "allergy": {
        "recommended_drugs": ["Loratadine", "Cetirizine"],
        "dosage": "1 tablet daily",
        "side_effects": ["Drowsiness"],
        "interactions": ["Avoid mixing with alcohol"]
    }
}

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/api/get_drug_info', methods=['POST'])
def get_drug_info():
    data = request.json
    symptom = data.get('symptom', '').lower()
    
    if symptom in drug_knowledge_base:
        return jsonify({
            "status": "success",
            "data": drug_knowledge_base[symptom]
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Symptom not found in the knowledge base."
        }), 404

if __name__ == '__main__':
    app.run(debug=True)
