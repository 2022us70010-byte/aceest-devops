from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store (based on the ACEest programs from the provided code)
programs = {
    "FL": {
        "name": "Fat Loss",
        "workout": "Mon: 5x5 Back Squat, Tue: EMOM 20min Assault Bike, Wed: Bench Press, Thu: Deadlifts",
        "diet": "Target: 2000 kcal | Breakfast: 3 Egg Whites + Oats | Lunch: Grilled Chicken + Rice",
        "calories": 2000
    },
    "MG": {
        "name": "Muscle Gain",
        "workout": "Mon: Squat 5x5, Tue: Bench 5x5, Wed: Deadlift 4x6, Thu: Front Squat 4x8",
        "diet": "Target: 3200 kcal | Breakfast: 4 Eggs + PB Oats | Lunch: Chicken Biryani",
        "calories": 3200
    },
    "BG": {
        "name": "Beginner",
        "workout": "Circuit: Air Squats, Ring Rows, Push-ups. Focus: Technique Mastery",
        "diet": "Balanced meals: Idli-Sambar, Rice-Dal. Protein: 120g/day",
        "calories": 2200
    }
}

clients = {}

@app.route('/')
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym API", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0"}), 200

@app.route('/programs', methods=['GET'])
def get_programs():
    return jsonify(programs)

@app.route('/programs/<program_id>', methods=['GET'])
def get_program(program_id):
    program = programs.get(program_id.upper())
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify(program)

@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(list(clients.values()))

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    name = data['name']
    program_id = data.get('program', 'BG').upper()
    
    if program_id not in programs:
        return jsonify({"error": "Invalid program"}), 400
    
    client = {
        "id": len(clients) + 1,
        "name": name,
        "program": program_id,
        "weight": data.get('weight', 0),
        "age": data.get('age', 0)
    }
    clients[name] = client
    return jsonify(client), 201

@app.route('/clients/<name>', methods=['GET'])
def get_client(name):
    client = clients.get(name)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client)

@app.route('/bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    weight = data.get('weight')
    height = data.get('height')
    
    if not weight or not height:
        return jsonify({"error": "Weight and height are required"}), 400
    
    bmi = round(weight / (height ** 2), 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return jsonify({"bmi": bmi, "category": category})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)