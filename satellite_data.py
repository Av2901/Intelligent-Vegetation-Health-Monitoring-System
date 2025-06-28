import numpy as np
import requests
from datetime import datetime, timedelta
# Remove the sentinelhub imports for now since they might not be installed
# from sentinelhub import SHConfig, BBox, CRS, DataCollection, SentinelHubRequest, MimeType
# import rasterio
from config import config

class SatelliteDataProcessor:
    def __init__(self):
        self.demo_mode = True  # Force demo mode for now
        print("Running in demo mode - using synthetic satellite data")
        
    def create_bbox(self, lat, lon, buffer_km=5):
        """Create bounding box around coordinates"""
        # Approximate conversion: 1 degree ≈ 111 km
        buffer_deg = buffer_km / 111.0
        
        return {
            'min_lon': lon - buffer_deg,
            'min_lat': lat - buffer_deg,
            'max_lon': lon + buffer_deg,
            'max_lat': lat + buffer_deg
        }
    
    def fetch_sentinel2_data(self, bbox, start_date, end_date):
        """Fetch Sentinel-2 data for specified region and time"""
        return self._generate_demo_data()
    
    def _generate_demo_data(self):
        """Generate synthetic satellite data for testing"""
        # Create realistic synthetic data
        size = (256, 256, 3)  # Smaller size for faster processing
        
        # Generate base patterns
        x, y = np.meshgrid(np.linspace(0, 10, 256), np.linspace(0, 10, 256))
        
        # Red band (B04) - typically lower for vegetation
        red = 1000 + 500 * np.sin(x) * np.cos(y) + np.random.normal(0, 100, (256, 256))
        red = np.clip(red, 0, 4000).astype(np.uint16)
        
        # NIR band (B08) - typically higher for vegetation
        nir = 3000 + 1000 * np.sin(x + 1) * np.cos(y + 1) + np.random.normal(0, 200, (256, 256))
        nir = np.clip(nir, 0, 8000).astype(np.uint16)
        
        # Scene classification (simplified)
        scl = np.ones((256, 256), dtype=np.uint16) * 4  # Vegetation class
        
        return np.stack([red, nir, scl], axis=2)
