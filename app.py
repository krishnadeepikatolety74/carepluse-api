from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------------------ MODEL ------------------
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(200))

# ------------------ CREATE DB ------------------
with app.app_context():
    db.create_all()

# ------------------ CREATE ------------------
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient = Patient(name=data['name'], age=data['age'], disease=data['disease'])
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": "Patient added"})

# ------------------ READ ------------------
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "disease": p.disease
        })
    return jsonify(result)

# ------------------ UPDATE ------------------
@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get(id)
    data = request.json
    patient.name = data['name']
    patient.age = data['age']
    patient.disease = data['disease']
    db.session.commit()
    return jsonify({"message": "Updated"})

# ------------------ DELETE ------------------
@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Deleted"})

# ------------------ PREDICTION ------------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    heart_rate = data['heart_rate']
    bp = data['blood_pressure']
    oxygen = data['oxygen_level']

    if heart_rate > 120 or bp > 180 or oxygen < 90:
        return jsonify({"status": "EMERGENCY"})
    else:
        return jsonify({"status": "STABLE"})

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)