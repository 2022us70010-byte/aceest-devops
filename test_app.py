import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ─── HOME ────────────────────────────────────────────────────────────────────

def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_has_welcome_message(client):
    response = client.get('/')
    data = response.get_json()
    assert "message" in data
    assert data["status"] == "running"

# ─── HEALTH ──────────────────────────────────────────────────────────────────

def test_health_returns_200(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_health_status_is_healthy(client):
    response = client.get('/health')
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "version" in data

# ─── PROGRAMS ────────────────────────────────────────────────────────────────

def test_get_all_programs(client):
    response = client.get('/programs')
    assert response.status_code == 200
    data = response.get_json()
    assert "FL" in data
    assert "MG" in data
    assert "BG" in data

def test_get_valid_program(client):
    response = client.get('/programs/FL')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fat Loss"
    assert "workout" in data
    assert "calories" in data

def test_get_program_mg(client):
    response = client.get('/programs/MG')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Muscle Gain"
    assert data["calories"] == 3200

def test_get_program_bg(client):
    response = client.get('/programs/BG')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Beginner"
    assert data["calories"] == 2200

def test_get_program_lowercase(client):
    response = client.get('/programs/fl')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fat Loss"

def test_get_invalid_program_returns_404(client):
    response = client.get('/programs/INVALID')
    assert response.status_code == 404

def test_get_invalid_program_has_error_key(client):
    response = client.get('/programs/XX')
    data = response.get_json()
    assert "error" in data

# ─── CLIENTS ─────────────────────────────────────────────────────────────────

def test_get_all_clients_returns_200(client):
    response = client.get('/clients')
    assert response.status_code == 200

def test_get_all_clients_returns_list(client):
    response = client.get('/clients')
    data = response.get_json()
    assert isinstance(data, list)

def test_add_client_success(client):
    payload = {"name": "Arjun", "program": "MG", "weight": 75, "age": 25}
    response = client.post('/clients', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Arjun"
    assert data["program"] == "MG"

def test_add_client_default_program_is_bg(client):
    payload = {"name": "DefaultUser", "weight": 60, "age": 20}
    response = client.post('/clients', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["program"] == "BG"

def test_add_client_has_id(client):
    payload = {"name": "IdUser", "program": "FL"}
    response = client.post('/clients', json=payload)
    data = response.get_json()
    assert "id" in data

def test_add_client_without_name_returns_400(client):
    response = client.post('/clients', json={"program": "FL"})
    assert response.status_code == 400

def test_add_client_empty_body_returns_400(client):
    response = client.post('/clients', json={})
    assert response.status_code == 400

def test_add_client_invalid_program_returns_400(client):
    response = client.post('/clients', json={"name": "Test", "program": "INVALID"})
    assert response.status_code == 400

def test_add_client_invalid_program_has_error_key(client):
    response = client.post('/clients', json={"name": "Test", "program": "ZZ"})
    data = response.get_json()
    assert "error" in data

def test_get_existing_client(client):
    client.post('/clients', json={"name": "Priya", "program": "FL"})
    response = client.get('/clients/Priya')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Priya"

def test_get_nonexistent_client_returns_404(client):
    response = client.get('/clients/NonExistentPerson')
    assert response.status_code == 404

def test_get_nonexistent_client_has_error_key(client):
    response = client.get('/clients/Ghost')
    data = response.get_json()
    assert "error" in data

# ─── BMI ─────────────────────────────────────────────────────────────────────

def test_bmi_calculation_normal(client):
    response = client.post('/bmi', json={"weight": 70, "height": 1.75})
    assert response.status_code == 200
    data = response.get_json()
    assert data["bmi"] == 22.86
    assert data["category"] == "Normal"

def test_bmi_calculation_obese(client):
    response = client.post('/bmi', json={"weight": 100, "height": 1.60})
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Obese"

def test_bmi_underweight(client):
    response = client.post('/bmi', json={"weight": 45, "height": 1.75})
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Underweight"

def test_bmi_overweight(client):
    response = client.post('/bmi', json={"weight": 90, "height": 1.75})
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Overweight"

def test_bmi_missing_fields_returns_400(client):
    response = client.post('/bmi', json={"weight": 70})
    assert response.status_code == 400

def test_bmi_missing_weight_returns_400(client):
    response = client.post('/bmi', json={"height": 1.75})
    assert response.status_code == 400

def test_bmi_has_bmi_key(client):
    response = client.post('/bmi', json={"weight": 70, "height": 1.75})
    data = response.get_json()
    assert "bmi" in data
    assert "category" in data