import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))

from algo import create_app

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "DEBUG": False,
        "SECRET_KEY": "test-secret"
    })
    with app.test_client() as client:
        yield client

def test_public_pages(client):
    """Verify that public routes render with 200 OK."""
    for path in ['/', '/about', '/contact', '/login', '/register']:
        res = client.get(path)
        assert res.status_code == 200, f"Path {path} returned status {res.status_code}"

def test_login_flow_and_dashboard(client):
    """Test authentication and session access for test student."""
    # Attempt login with seeded user
    res = client.post('/login', data={
        'email': 'student@alumnigo.test',
        'password': 'student123'
    }, follow_redirects=True)
    assert res.status_code == 200

    # Access user dashboard with session
    dashboard_res = client.get('/dashboard')
    assert dashboard_res.status_code in [200, 302]

def test_channels_api(client):
    """Verify channel endpoints."""
    # Login as student
    client.post('/login', data={
        'email': 'student@alumnigo.test',
        'password': 'student123'
    }, follow_redirects=True)

    res = client.get('/channels')
    assert res.status_code == 200

def test_connect_networking_directory(client):
    """Verify alumni directory page."""
    client.post('/login', data={
        'email': 'student@alumnigo.test',
        'password': 'student123'
    }, follow_redirects=True)

    res = client.get('/connect')
    assert res.status_code == 200
