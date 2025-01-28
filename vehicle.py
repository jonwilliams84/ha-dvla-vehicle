"""Modified VehicleLookupSystem for Home Assistant."""
import sqlite3
import json
from datetime import datetime
import logging
from typing import Optional, Dict, Any
import requests

class VehicleLookupSystem:
    """Modified version of VehicleLookupSystem for Home Assistant integration."""
    
    def __init__(self, db_path: str, api_key: str):
        """Initialize the system."""
        self.db_path = db_path
        self.api_key = api_key
        self.api_url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
        self.setup_database()

    def setup_database(self):
        """Initialize the database with required tables."""
        sqlite3.register_adapter(datetime, lambda x: x.isoformat())
        sqlite3.register_converter('TIMESTAMP', lambda x: datetime.fromisoformat(x.decode()))
    
        with sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cur = conn.cursor()
            
            # Create vehicle data table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    registration TEXT PRIMARY KEY,
                    data_json TEXT,
                    last_updated TIMESTAMP
                )
            ''')
            
            conn.commit()

    def fetch_vehicle_data(self, registration: str) -> Optional[Dict[str, Any]]:
        """Fetch vehicle data from API."""
        registration = registration.strip().upper()
        
        try:
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                "registrationNumber": registration
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            return None

        except Exception as e:
            logging.getLogger(__name__).error(f"API call failed: {str(e)}")
            return None
