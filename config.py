import os
from dataclasses import dataclass

@dataclass
class Config:
    # Sentinel Hub credentials (get from https://apps.sentinel-hub.com/)
    SENTINEL_HUB_CLIENT_ID: str = os.getenv('SH_CLIENT_ID', '')
    SENTINEL_HUB_CLIENT_SECRET: str = os.getenv('SH_CLIENT_SECRET', '')
    
    # Google Earth Engine (requires authentication)
    USE_GOOGLE_EARTH_ENGINE: bool = False
    
    # Default analysis parameters
    DEFAULT_CLOUD_COVERAGE: int = 20
    NDVI_STRESS_THRESHOLD: float = 0.20
    BASELINE_YEARS: int = 3
    
    # Assam districts for testing
    TEST_REGIONS = {
        'Kamrup': {'lat': 26.1445, 'lon': 91.7362},
        'Nagaon': {'lat': 26.3479, 'lon': 92.6881}
    }

# Create instance
config = Config()
