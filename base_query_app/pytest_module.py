import pytest
from query_app import app  # Import the Flask app from your main app file

# Define a fixture for setting up the Flask test client
@pytest.fixture
def client():
    # Using Flask's test client to simulate requests
    with app.test_client() as client:
        yield client

# Test POST request to "/query_base"
def test_query_base(client):
    payload = {
        "query": "What is the best movie from TFI?"
    }
    
    response = client.post('/query_base', json=payload)
    
    assert response.status_code == 200
    
    response_json = response.get_json()
    assert 'data' in response_json
    assert response_json['data'] == 'Your answer'
    

# Test POST request to "/insert_new_data" and check for "inserted successfully"
def test_insert_new_data(client):
    # Example payload for inserting new data

    payload = {
        "new_data": "Sample data"
    }
    
    # Simulate a POST request to /insert_new_data
    response = client.post('/insert_new_data', json=payload)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Get the response JSON
    response_json = response.get_json()
    
    # Check if the response contains the expected message
    assert 'message' in response_json
    assert response_json['message'] == 'File uploaded successfully'
