from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

API_BASE_URL = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = "test"

# Note: Sandbox token only works for Belmont North
SUBURBS = [
    'Belmont North'  # Only this suburb works with sandbox token
]

PROPERTY_TYPES = ['unit', 'house', 'townhouse']

@app.route('/')
def index():
    return render_template('index.html', suburbs=SUBURBS, property_types=PROPERTY_TYPES)

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
        
        if response.status_code == 401:
            print("API returned 401 - Unauthorized")
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg, "results": []})
        
        response.raise_for_status()
        data = response.json()
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
    address = request.args.get('address', '')
    
    if not address:
        return jsonify({"error": "Address is required"})
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/avm"
        response = requests.get(url, headers=headers, params={"address": address}, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/api/cma')
def get_cma():
    address = request.args.get('address', '')
    
    if not address:
        return jsonify({"error": "Address is required"})
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{API_BASE_URL}/cma"
        response = requests.get(url, headers=headers, params={"address": address}, timeout=10)
        
        if response.status_code == 401:
            error_msg = response.json().get('error', 'Unauthorized') if response.text else 'Unauthorized'
            return jsonify({"error": error_msg})
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 200

if __name__ == '__main__':
    app.run(debug=True)

