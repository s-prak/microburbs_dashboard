# Microburbs Property Dashboard

A modern, interactive web application that showcases property listings from the Microburbs API using Python/Flask backend and vanilla JavaScript frontend.

## Features

- 🏘️ **Browse Properties**: View detailed property listings across multiple NSW suburbs
- 🔍 **Smart Search**: Real-time search filtering by address, area name, or description
- 📊 **Live Statistics**: Dynamic analytics showing total properties and average bedrooms/bathrooms
- 🎨 **Modern UI**: Clean, responsive design with gradient backgrounds and smooth animations
- ⚡ **Fast Performance**: Vanilla JavaScript for lightweight, snappy interactions

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Styling**: Pure CSS with modern gradients and animations
- **API**: Microburbs API

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Install required Python packages:
```bash
pip install flask requests
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## How It Works

1. **Flask Backend**: Serves the HTML template and proxies API requests to Microburbs API
2. **Vanilla JS Frontend**: Handles all UI interactions, filtering, and dynamic rendering
3. **Real-time Filtering**: Client-side search provides instant results without additional API calls
4. **Dynamic Data**: Suburb and property type dropdowns trigger new API requests

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────────┐
│   Browser   │─────▶│    Flask     │─────▶│ Microburbs API   │
│  (Vanilla)  │◀─────│ (Python 3)   │◀─────│ (External)       │
└─────────────┘      └──────────────┘      └──────────────────┘
```

## Project Structure

```
.
├── app.py                 # Flask application with API endpoints
├── templates/
│   └── index.html        # Single-page application with embedded CSS/JS
└── README.md             # This file
```

## Features Breakdown

### Interactive Controls
- **Suburb Selector**: Choose from 9 NSW suburbs
- **Property Type Filter**: Switch between units, houses, and townhouses
- **Search Bar**: Real-time text search across properties

### Statistics Dashboard
- Total number of properties
- Average bedrooms across listings
- Average bathrooms across listings

### Property Cards
Each card displays:
- Property area name
- Building size badge
- Full address
- Number of bedrooms and bathrooms
- Property description (truncated)

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Adaptive grid layout
- Touch-friendly controls

## Available Suburbs

**Note:** The sandbox API token only works with specific demo data:
- **Belmont North** (Properties endpoint works)
- For other suburbs, you'll need a full API key from Microburbs

## Property Types

- Unit
- House
- Townhouse

## API Endpoints

### `GET /`
Returns the main dashboard HTML page

### `GET /api/properties?suburb=<name>&property_type=<type>`
Fetches property data from Microburbs API

**Parameters:**
- `suburb` (optional): Suburb name (default: "Belmont North")
- `property_type` (optional): Property type (default: "unit")

**Response:** JSON object with property listings

## Development

The application uses Flask's debug mode by default. Changes to `app.py` will auto-reload the server. For frontend changes (HTML/CSS/JS in `templates/index.html`), simply refresh your browser.

## Future Enhancements

- Add property detail modal/page
- Implement map view with location markers
- Add price filtering when available from API
- Export property data to CSV
- Add pagination for large result sets
- Implement caching to reduce API calls
