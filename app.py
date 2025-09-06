from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)  # Allow React app to communicate with Flask

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
    },
    "cough": {
        "recommended_drugs": ["Dextromethorphan", "Guaifenesin"],
        "dosage": "10ml syrup every 4 hours",
        "side_effects": ["Drowsiness", "Dry mouth"],
        "interactions": ["Avoid with MAO inhibitors"]
    },
    "cold": {
        "recommended_drugs": ["Paracetamol", "Phenylephrine"],
        "dosage": "1 tablet every 6 hours",
        "side_effects": ["Nasal dryness", "Insomnia"],
        "interactions": ["Avoid with antidepressants"]
    },
    "nausea": {
        "recommended_drugs": ["Ondansetron", "Domperidone"],
        "dosage": "1 tablet before meals",
        "side_effects": ["Headache", "Constipation"],
        "interactions": ["Avoid with QT-prolonging drugs"]
    },
    "vomiting": {
        "recommended_drugs": ["Metoclopramide", "Ondansetron"],
        "dosage": "1 tablet every 8 hours",
        "side_effects": ["Fatigue", "Restlessness"],
        "interactions": ["Avoid with antipsychotics"]
    },
    "diarrhea": {
        "recommended_drugs": ["Loperamide", "ORS"],
        "dosage": "2 capsules after first loose stool",
        "side_effects": ["Constipation", "Cramps"],
        "interactions": ["Avoid with antibiotics"]
    },
    "constipation": {
        "recommended_drugs": ["Lactulose", "Psyllium"],
        "dosage": "1–2 tablespoons daily",
        "side_effects": ["Bloating", "Gas"],
        "interactions": ["Avoid with antacids"]
    },
    "sore throat": {
        "recommended_drugs": ["Lozenges", "Paracetamol"],
        "dosage": "1 lozenge every 3 hours",
        "side_effects": ["Numbness", "Dry throat"],
        "interactions": ["None significant"]
    },
    "fatigue": {
        "recommended_drugs": ["Vitamin B12", "Iron supplements"],
        "dosage": "As prescribed daily",
        "side_effects": ["Nausea", "Stomach upset"],
        "interactions": ["Avoid with calcium supplements"]
    },
    "dizziness": {
        "recommended_drugs": ["Meclizine", "Betahistine"],
        "dosage": "1 tablet twice daily",
        "side_effects": ["Drowsiness", "Dry mouth"],
        "interactions": ["Avoid with alcohol"]
    },
    "insomnia": {
        "recommended_drugs": ["Melatonin", "Diphenhydramine"],
        "dosage": "1 tablet before bedtime",
        "side_effects": ["Next-day drowsiness"],
        "interactions": ["Avoid with sedatives"]
    },
    "anxiety": {
        "recommended_drugs": ["Diazepam", "Buspirone"],
        "dosage": "As prescribed",
        "side_effects": ["Drowsiness", "Dependence"],
        "interactions": ["Avoid with alcohol"]
    },
    "depression": {
        "recommended_drugs": ["Sertraline", "Fluoxetine"],
        "dosage": "1 tablet daily",
        "side_effects": ["Weight gain", "Sexual dysfunction"],
        "interactions": ["Avoid with MAO inhibitors"]
    },
    "high blood pressure": {
        "recommended_drugs": ["Amlodipine", "Lisinopril"],
        "dosage": "1 tablet daily",
        "side_effects": ["Dizziness", "Swelling"],
        "interactions": ["Avoid with NSAIDs"]
    },
    "diabetes": {
        "recommended_drugs": ["Metformin", "Insulin"],
        "dosage": "As prescribed",
        "side_effects": ["Low blood sugar", "GI upset"],
        "interactions": ["Avoid with alcohol"]
    },
    "asthma": {
        "recommended_drugs": ["Salbutamol", "Fluticasone"],
        "dosage": "2 puffs as needed",
        "side_effects": ["Tremors", "Increased heart rate"],
        "interactions": ["Avoid with beta blockers"]
    },
    "acne": {
        "recommended_drugs": ["Benzoyl peroxide", "Clindamycin"],
        "dosage": "Apply twice daily",
        "side_effects": ["Skin irritation", "Dryness"],
        "interactions": ["Avoid with other topical treatments"]
    },
    "back pain": {
        "recommended_drugs": ["Ibuprofen", "Naproxen"],
        "dosage": "1 tablet every 8 hours",
        "side_effects": ["Stomach upset", "Drowsiness"],
        "interactions": ["Avoid with blood thinners"]
    },
    "muscle pain": {
        "recommended_drugs": ["Paracetamol", "Diclofenac"],
        "dosage": "1 tablet every 6–8 hours",
        "side_effects": ["Heartburn", "Drowsiness"],
        "interactions": ["Avoid with alcohol"]
    },
    "skin rash": {
        "recommended_drugs": ["Hydrocortisone cream", "Antihistamines"],
        "dosage": "Apply twice daily",
        "side_effects": ["Skin thinning", "Burning sensation"],
        "interactions": ["Avoid with strong steroids"]
    },
    "heartburn": {
        "recommended_drugs": ["Omeprazole", "Ranitidine"],
        "dosage": "1 tablet before meals",
        "side_effects": ["Headache", "Constipation"],
        "interactions": ["Avoid with antifungals"]
    }
}

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

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
