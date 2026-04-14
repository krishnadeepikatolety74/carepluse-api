## 🎥 Demo Video
[Watch Demo](https://drive.google.com/file/d/12stVDUj99xz2wcCNZBfPX7A-cDu9MCxK/view?usp=drivesdk)
# carepluse-api
A RESTful API for managing patient records with real-time emergency prediction based on vital signs.
code:
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
patients = []
patient_id = 1

# ------------------ CRUD APIs ------------------

# Create Patient
@app.route('/patients', methods=['POST'])
def create_patient():
    global patient_id
    data = request.json

    data['id'] = patient_id
    patients.append(data)
    patient_id += 1

    return jsonify({"message": "Patient added", "patient": data})


# Get All Patients
@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify(patients)


# Update Patient
@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.json

    for patient in patients:
        if patient['id'] == id:
            patient.update(data)
            return jsonify({"message": "Patient updated", "patient": patient})

    return jsonify({"message": "Patient not found"}), 404


# Delete Patient
@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    global patients
    patients = [p for p in patients if p['id'] != id]

    return jsonify({"message": "Patient deleted"})


# ------------------ Prediction API ------------------

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    heart_rate = data.get('heart_rate')
    bp = data.get('blood_pressure')
    temperature = data.get('temperature')

    # Simple rule-based logic
    if heart_rate > 100 or bp > 140 or temperature > 38:
        result = "EMERGENCY"
    else:
        result = "STABLE"

    return jsonify({"prediction": result})


# ------------------ Run Server ------------------

if __name__ == '__main__':
    app.run(debug=True)
