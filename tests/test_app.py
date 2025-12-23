import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from CI/CD Lab!' in response.data

def test_health(client):
    """Test the health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'

def test_get_data(client):
    """Test the data endpoint"""
    response = client.get('/api/data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'data' in json_data
    assert json_data['count'] == 5