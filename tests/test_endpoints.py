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

def test_contact_submission_and_resolution(client):
    """Verify contact form submission, DB persistence, admin visibility, and inquiry resolution."""
    from algo.db import get_db

    # 1. Submit contact inquiry
    res = client.post('/contact', data={
        'full_name': 'Test Querier',
        'email': 'querier@example.com',
        'phone': '1234567890',
        'subject': 'Inquiry about SIH Project',
        'message': 'Can alumni mentor multiple teams?'
    }, follow_redirects=True)
    assert res.status_code == 200

    # 2. Check persistence in PostgreSQL
    with client.application.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, status FROM contacts WHERE email = 'querier@example.com' ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        assert row is not None
        query_id, status = row
        assert status == 'pending'
        cur.close()

    # 3. Log in as admin
    login_res = client.post('/login', data={
        'email': 'admin@alumnigo.test',
        'password': 'admin123'
    }, follow_redirects=True)
    assert login_res.status_code == 200

    # 4. Verify inquiry appears on Admin Dashboard
    dash_res = client.get('/admin_dashboard')
    assert dash_res.status_code == 200
    assert b"Contact Us Inquiries" in dash_res.data
    assert b"Inquiry about SIH Project" in dash_res.data

    # 5. Resolve the inquiry via Admin action
    resolve_res = client.post(f'/admin/contact/{query_id}/resolve', data={
        'resolution_notes': 'Verified and addressed via email.'
    }, follow_redirects=True)
    assert resolve_res.status_code == 200

    # 6. Verify status updated to 'resolved' in PostgreSQL
    with client.application.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT status, resolution_notes FROM contacts WHERE id = %s", (query_id,))
        resolved_status, notes = cur.fetchone()
        assert resolved_status == 'resolved'
        assert notes == 'Verified and addressed via email.'
        cur.close()

def test_admin_dashboard_auth_guards(client):
    """Verify that unauthenticated and non-admin users cannot access admin dashboard."""
    # 1. Unauthenticated request must redirect to login
    unauth_res = client.get('/admin_dashboard')
    assert unauth_res.status_code == 302
    assert '/auth/login' in unauth_res.headers.get('Location', '')

    # 2. Student login must be forbidden from admin dashboard and redirected to user_dashboard
    client.post('/login', data={
        'email': 'student@alumnigo.test',
        'password': 'student123'
    }, follow_redirects=True)
    student_res = client.get('/admin_dashboard')
    assert student_res.status_code == 302
    assert '/user_dashboard' in student_res.headers.get('Location', '')

def test_chat_api_endpoints(client):
    """Verify online status and user search endpoints for chat."""
    # 1. Login as student
    client.post('/login', data={
        'email': 'student@alumnigo.test',
        'password': 'student123'
    }, follow_redirects=True)

    # 2. Test /api/online_status
    online_res = client.get('/api/online_status')
    assert online_res.status_code == 200
    data = online_res.get_json()
    assert 'online_users' in data
    assert isinstance(data['online_users'], list)

    # 3. Test /api/search_users
    search_res = client.get('/api/search_users?q=Alumni')
    assert search_res.status_code == 200
    search_data = search_res.get_json()
    assert 'users' in search_data
    assert isinstance(search_data['users'], list)


