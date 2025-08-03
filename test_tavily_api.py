import requests
import time
import pytest
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.tavily.com/search"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def send_request(payload, custom_headers=None):
    start_time = time.time()
    h = custom_headers if custom_headers else headers
    response = requests.post(BASE_URL, headers=h, json=payload)
    end_time = time.time()
    latency = end_time - start_time
    return response , latency

# --- TC01: Valid query with all required parameters ---
def test_valid_query_basic():
    payload = {
        "query": "Artificial Intelligence",
        "include_answer": True,
        "include_images": False,
        "search_depth": "basic"
    }
    response , latency = send_request(payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    print(f"Latency: {latency:.2f}s")

# --- TC02: Valid query with advanced search_depth ---
def test_valid_query_advanced():
    payload = {
        "query": "AI",
        "search_depth": "advanced"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC03: Valid query with auto_parameters enabled ---
def test_valid_query_auto_parameters():
    payload = {
        "query": "AI",
        "auto_parameters": True
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC04: Valid query with topic set to "news" ---
def test_valid_query_topic_news():
    payload = {
        "query": "AI",
        "topic": "news"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC05 & TC06: Valid query with edge max_results ---
@pytest.mark.parametrize("max_results", [1, 20])
def test_valid_query_max_results_edge(max_results):
    payload = {
        "query": "AI",
        "max_results": max_results
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= max_results
    print(f"Latency: {latancy:.2f}s")

# --- TC07: Valid query with chunks_per_source=3 (advanced) ---
def test_valid_query_chunks_per_source():
    payload = {
        "query": "AI",
        "search_depth": "advanced",
        "chunks_per_source": 3
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC08: Valid query with time_range ---
def test_valid_query_time_range():
    payload = {
        "query": "AI",
        "time_range": "week"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC09: Valid query with start_date and end_date ---
def test_valid_query_date_range():
    payload = {
        "query": "AI",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC10: Valid query with include_raw_content ---
def test_valid_query_include_raw_content():
    payload = {
        "query": "AI",
        "include_raw_content": True
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC11: Valid query with include_favicon ---
def test_valid_query_include_favicon():
    payload = {
        "query": "AI",
        "include_favicon": True
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC12: Valid query with include_domains ---
def test_valid_query_include_domains():
    payload = {
        "query": "AI",
        "include_domains": ["bbc.com"]
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC13: Valid query with exclude_domains ---
def test_valid_query_exclude_domains():
    payload = {
        "query": "AI",
        "exclude_domains": ["cnn.com"]
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC14: Valid query with country ---
def test_valid_query_country():
    payload = {
        "query": "AI",
        "country": "india"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC15: Valid query with special characters ---
def test_valid_query_special_characters():
    payload = {
        "query": "!@#$%^&*()",
        "include_answer": True
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    print(f"Latency: {latancy:.2f}s")

# --- TC16: Very short query ---
def test_edge_very_short_query():
    payload = {
        "query": "a"
    }
    response , latancy  = send_request(payload)
    assert response.status_code in [200, 400] 
    print(f"Latency: {latancy:.2f}s") 

# --- TC17: Very long query ---
def test_edge_very_long_query():
    payload = {
        "query": "a" * 2000
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 400
    print(f"Latency: {latancy:.2f}s")

# --- TC18: Missing query parameter ---
def test_negative_missing_query():
    payload = {
        "include_answer": True
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 422
    print(f"Latency: {latancy:.2f}s")

# --- TC19: Missing API key ---
def test_negative_missing_api_key():
    payload = {
        "query": "AI"
    }
    # Remove Authorization header
    response , latency = send_request(payload, custom_headers={"Content-Type": "application/json"})
    assert response.status_code in [400, 401]
    print(f"Latency: {latency:.2f}s")

# --- TC20: Invalid API key ---
def test_negative_invalid_api_key():
    payload = {
        "query": "AI"
    }
    bad_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer invalid-key"
    }
    response , latency = send_request(payload, custom_headers=bad_headers)
    assert response.status_code == 401
    print(f"Latency: {latency:.2f}s")

# --- TC21: Invalid parameter type (include_images as string) ---
def test_negative_invalid_param_type():
    payload = {
        "query": "AI",
        "include_images": "yes"
    }
    response , latancy  = send_request(payload)
    assert response.status_code in [200, 400]
    print(f"Latency: {latancy:.2f}s")

# --- TC22: Invalid value for search_depth ---
def test_negative_invalid_search_depth():
    payload = {
        "query": "AI",
        "search_depth": "invalid"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 400
    print(f"Latency: {latancy:.2f}s")

# --- TC23: Invalid value for topic ---
def test_negative_invalid_topic():
    payload = {
        "query": "AI",
        "topic": "invalid"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 400
    print(f"Latency: {latancy:.2f}s")

# --- TC24: Invalid value for country ---
def test_negative_invalid_country():
    payload = {
        "query": "AI",
        "country": "invalid"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 400
    print(f"Latency: {latancy:.2f}s")

# --- TC25 & TC26: Invalid value for max_results ---
@pytest.mark.parametrize("max_results", [-1, 21])
def test_negative_invalid_max_results(max_results):
    payload = {
        "query": "AI",
        "max_results": max_results
    }
    response , latancy  = send_request(payload)
    assert response.status_code in [400, 200]  
    print(f"Latency: {latancy:.2f}s")

# # --- TC27 & TC28: Invalid value for chunks_per_source ---
@pytest.mark.parametrize("chunks_per_source", [0, 4])
def test_negative_invalid_chunks_per_source(chunks_per_source):
    payload = {
        "query": "AI",
        "search_depth": "advanced",
        "chunks_per_source": chunks_per_source
    }
    response , latancy  = send_request(payload)
    assert response.status_code in[200,422]
    print(f"Latency: {latancy:.2f}s")
    

# --- TC29 & TC30: Invalid date format ---
@pytest.mark.parametrize("date_field, date_value", [
    ("start_date", "01-01-2025"),
    ("end_date", "01-31-2025")
])
def test_negative_invalid_date_format(date_field, date_value):
    payload = {
        "query": "AI",
        date_field: date_value
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 400
    print(f"Latency: {latancy:.2f}s")
    

# --- TC31: Response structure check ---
def test_response_structure():
    payload = {
        "query": "AI"
    }
    response , latancy  = send_request(payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert "response_time" in data
    assert isinstance(data["response_time"], (float, int, str))
    print(f"Latency: {latancy:.2f}s")
    

# --- TC32: Latency metric check ---
def test_latency_metric():
    
    payload = {
        "query": "AI"
    }
    response , latency  = send_request(payload)
    assert latency >= 0
    print(f"Latency: {latency:.2f}s")
    