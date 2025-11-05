from flask import Flask, jsonify, render_template, request
import requests
import json
import math

app = Flask(__name__)

API_BASE_URL = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = "test"

def clean_nan_values(obj):
    """Recursively replace NaN, Infinity values with None for JSON serialization"""
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj

# Note: Sandbox token only works for Belmont North
SUBURBS = [
    'Belmont North'  # Only this suburb works with sandbox token
]

PROPERTY_TYPES = ['unit', 'house', 'townhouse']

@app.route('/')
def index():
    return render_template('index.html', suburbs=SUBURBS, property_types=PROPERTY_TYPES)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/api/properties')
def get_properties():
    suburb = request.args.get('suburb', 'Belmont North')
    property_type = request.args.get('property_type', 'unit')
    
    # Use the exact format from the working curl command
    url = "https://www.microburbs.com.au/report_generator/api/suburb/properties"
    
    headers = {
        "Authorization": "Bearer test",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    params = {
        "suburb": suburb,
        "property_type": property_type
    }
    
    try:
        print(f"\n=== API Request ===")
        print(f"URL: {url}")
        print(f"Params: {params}")
        print(f"Headers: {headers}")
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text (first 500 chars): {response.text[:500]}")
        
        if response.status_code == 401:
            print("API returned 401 - Unauthorized")
            return jsonify({"error": "Unauthorized - check API token", "results": []})
        
        response.raise_for_status()
        
        # Try to parse JSON
        try:
            data = response.json()
        except ValueError as json_err:
            print(f"JSON Parse Error: {json_err}")
            print(f"Response content type: {response.headers.get('content-type')}")
            return jsonify({"error": "API returned invalid JSON response", "results": []})
        
        # Clean NaN values from the data
        data = clean_nan_values(data)
        
        print(f"Success! Received {len(data.get('results', []))} properties")
        return jsonify(data)
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return jsonify({"error": f"API Error: {str(e)}", "results": []}), 200
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return jsonify({"error": f"Connection Error: {str(e)}", "results": []}), 200
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": f"Unexpected Error: {str(e)}", "results": []}), 200

@app.route('/api/suburb/<endpoint>')
def get_suburb_data(endpoint):
    suburb = request.args.get('suburb', 'Belmont North')
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/suburb/{endpoint}"
        response = requests.get(url, headers=headers, params={"suburb": suburb}, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/api/property/<endpoint>')
def get_property_data(endpoint):
    # Get query parameters
    params = dict(request.args)
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/property/{endpoint}"
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/api/avm')
def get_avm():
    property_id = request.args.get('id', '')
    
    if not property_id:
        return jsonify({"error": "Property ID is required"})
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/avm"
        response = requests.get(url, headers=headers, params={"id": property_id}, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/api/cma')
def get_cma():
    property_id = request.args.get('id', '')
    
    if not property_id:
        return jsonify({"error": "Property ID is required"})
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/cma"
        response = requests.get(url, headers=headers, params={"id": property_id}, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

if __name__ == '__main__':
    app.run(debug=True)

