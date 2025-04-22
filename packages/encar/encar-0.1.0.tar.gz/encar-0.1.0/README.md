# Carapis Encar API Client (Python)

[![PyPI version](https://badge.fury.io/py/encar.svg)](https://badge.fury.io/py/encar)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Carapis Documentation](https://img.shields.io/badge/API%20Docs-Carapis.com-blue)](https://carapis.com/docs)
[![Carapis Catalog](https://img.shields.io/badge/Live%20Catalog-Carapis.com-green)](https://carapis.com/catalog)

Official Python client library from **Carapis.com** for interacting with the Carapis Encar v2 API (<https://api.carapis.com/>).

This client provides a straightforward way to access real-time Korean used vehicle data from Encar.com programmatically.

Explore a live catalog powered by this API: [Carapis Catalog](https://carapis.com/catalog)

## Installation

Install the client library using pip. Dependencies (`requests`, `pyyaml`) are automatically handled.

```bash
pip install encar
```

## Configuration

1.  **API Key**: The client requires a Carapis API key for full access. Get yours at [Carapis.com Pricing](https://carapis.com/pricing). Retrieve this key from a secure location, such as environment variables.

    *Without an API key, access is limited to the latest 1,000 vehicles (Free Tier).*

## Python Client Usage

Initialize the client and make API calls.

```python
import os
from encar import CarapisClient, CarapisClientError

# --- Initialization ---
# Retrieve the API key from environment variables (recommended)
API_KEY = os.getenv("CARAPIS_API_KEY")

# Ensure API_KEY is available before initializing
if not API_KEY:
    print("Error: CARAPIS_API_KEY environment variable not set. Exiting.")
    exit()

try:
    # Initialize client with the API key
    client = CarapisClient(api_key=API_KEY)
    print("Carapis Client initialized successfully.")

    # --- Proceed with API calls ---

except CarapisClientError as e:
    print(f"API Client Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

---

## API Method Examples

Below are examples for the main API methods provided by the client.

### List Vehicles

Retrieve a list of vehicles with various filtering options.

```python
try:
    print("\n--- Listing Vehicles ---")
    # Example: List 5 gasoline SUVs from 2021 onwards, under 50,000km, newest first
    vehicles = client.list_vehicles(
        limit=5,
        min_year=2021,
        fuel_type='gasoline',
        body_type='suv',
        max_mileage=50000,
        ordering='-created_at'
    )
    print("Vehicles Found:")
    if vehicles and vehicles.get('results'):
        for v in vehicles['results']:
             print(f"- ID: {v.get('vehicle_id')}, Model: {v.get('model_name', 'N/A')}, Year: {v.get('year')}, Price: {v.get('price')}")
    else:
        print("No vehicles found matching criteria or error occurred.")

except CarapisClientError as e:
    print(f"API Client Error listing vehicles: {e}")
```

### Get Vehicle Details

Retrieve detailed information for a specific vehicle by its ID.

```python
try:
    vehicle_id_to_get = 12345678 # Replace with a valid Vehicle ID
    print(f"\n--- Getting Vehicle Details (ID: {vehicle_id_to_get}) ---")
    vehicle_details = client.get_vehicle(vehicle_id=vehicle_id_to_get)
    print("Vehicle Details Received:")
    print(vehicle_details)

except CarapisClientError as e:
    print(f"API Client Error getting vehicle {vehicle_id_to_get}: {e}")
```

### List Manufacturers

Retrieve a list of vehicle manufacturers.

```python
try:
    print("\n--- Listing Manufacturers ---")
    # Example: List top 10 manufacturers from South Korea ('KR')
    manufacturers = client.list_manufacturers(country='KR', limit=10, ordering='name')
    print("Manufacturers Found:")
    if manufacturers and manufacturers.get('results'):
        for mfr in manufacturers['results']:
             print(f"- Code: {mfr.get('code')}, Name: {mfr.get('name')}")
    else:
        print("No manufacturers found or error occurred.")

except CarapisClientError as e:
    print(f"API Client Error listing manufacturers: {e}")
```

### Get Manufacturer Details

Retrieve details for a specific manufacturer by its code.

```python
try:
    manufacturer_code = '101' # Example: Hyundai
    print(f"\n--- Getting Manufacturer Details (Code: {manufacturer_code}) ---")
    manufacturer_info = client.get_manufacturer(code=manufacturer_code)
    print("Manufacturer Details Received:")
    print(manufacturer_info)

except CarapisClientError as e:
    print(f"API Client Error getting manufacturer {manufacturer_code}: {e}")
```

### List Model Groups

Retrieve a list of model groups, optionally filtered.

```python
try:
    manufacturer_code = '101' # Example: Hyundai
    print(f"\n--- Listing Model Groups (Manufacturer: {manufacturer_code}) ---")
    model_groups = client.list_model_groups(manufacturer=manufacturer_code, search='Avante', limit=5)
    print("Model Groups Found:")
    if model_groups and model_groups.get('results'):
        for mg in model_groups['results']:
             print(f"- Code: {mg.get('code')}, Name: {mg.get('name')}")
    else:
        print("No model groups found or error occurred.")

except CarapisClientError as e:
    print(f"API Client Error listing model groups: {e}")
```

### Get Model Group Details

Retrieve details for a specific model group by its code.

```python
try:
    model_group_code = '1101' # Example: Avante
    print(f"\n--- Getting Model Group Details (Code: {model_group_code}) ---")
    model_group_info = client.get_model_group(code=model_group_code)
    print("Model Group Details Received:")
    print(model_group_info)

except CarapisClientError as e:
    print(f"API Client Error getting model group {model_group_code}: {e}")
```

### List Models

Retrieve a list of specific vehicle models, optionally filtered.

```python
try:
    model_group_code = '1101' # Example: Avante
    print(f"\n--- Listing Models (Model Group: {model_group_code}) ---")
    models = client.list_models(model_group=model_group_code, search='CN7', limit=5)
    print("Models Found:")
    if models and models.get('results'):
        for mdl in models['results']:
             print(f"- Code: {mdl.get('code')}, Name: {mdl.get('name')}")
    else:
        print("No models found or error occurred.")

except CarapisClientError as e:
    print(f"API Client Error listing models: {e}")
```

### Get Model Details

Retrieve details for a specific vehicle model by its code.

```python
try:
    model_code = '21101' # Example: Specific Avante model
    print(f"\n--- Getting Model Details (Code: {model_code}) ---")
    model_info = client.get_model(code=model_code)
    print("Model Details Received:")
    print(model_info)

except CarapisClientError as e:
    print(f"API Client Error getting model {model_code}: {e}")
```

### Get Vehicle Enums

Retrieve possible enum values used in vehicle data (e.g., for `FuelType`, `Color`).

```python
try:
    print("\n--- Getting Vehicle Enums ---")
    enums = client.get_vehicle_enums()
    print("Available Enums Received:")
    if enums:
        print(f"- Fuel Types: {list(enums.get('FuelType', {}).keys())}")
        print(f"- Colors: {list(enums.get('Color', {}).keys())}")
        print(f"- Body Types: {list(enums.get('BodyType', {}).keys())}")
    else:
         print("Could not retrieve enums.")

except CarapisClientError as e:
    print(f"API Client Error getting enums: {e}")
```

### Get Vehicle Stats

Retrieve overall statistics about vehicles in the database.

```python
try:
    print("\n--- Getting Vehicle Stats ---")
    vehicle_stats = client.get_vehicle_stats()
    print("Vehicle Statistics Received:")
    print(vehicle_stats)

except CarapisClientError as e:
    print(f"API Client Error getting stats: {e}")
```

*(Note: Methods for Dealers and Diagnosis Centers like `list_dealers`, `get_dealer`, `list_diagnosis_centers`, `get_diagnosis_center` work similarly and are omitted here for brevity. Refer to the API documentation for details.)*

---

## Direct API Access & Documentation

Interact with the API directly using `curl` or other HTTP clients.

**Full API Documentation:** [https://carapis.com/docs](https://carapis.com/docs)

**Example `curl` Requests:**

*   **With API Key (Full Access):**
    ```bash
    curl -X 'GET' \
      'https://api.carapis.com/api/encar/v2/vehicles/?limit=5&min_year=2021' \
      -H 'accept: application/json' \
      -H 'Authorization: ApiKey YOUR_API_KEY_UUID'
    ```

*   **Without API Key (Free Tier - 1,000 Record Limit):**
    ```bash
    curl -X 'GET' \
      'https://api.carapis.com/api/encar/v2/vehicles/?limit=5' \
      -H 'accept: application/json'
    ```

See [Pricing Plans](https://carapis.com/pricing) for details on access tiers and features.

## Support & Contact

- Website: [https://carapis.com](https://carapis.com)
- Telegram: [t.me/markinmatrix](https://t.me/markinmatrix)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
