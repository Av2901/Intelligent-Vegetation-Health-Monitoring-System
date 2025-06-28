import numpy as np
from scipy import ndimage
import pandas as pd

class NDVIProcessor:
    def __init__(self):
        self.ndvi_classes = {
            'water_barren': (-1.0, 0.1),
            'sparse_vegetation': (0.1, 0.3),
            'moderate_vegetation': (0.3, 0.6),
            'healthy_vegetation': (0.6, 0.9)
        }
    
    def calculate_ndvi(self, red_band, nir_band, mask_clouds=True):
        """Calculate NDVI with cloud masking"""
        # Convert to float for calculation
        red = red_band.astype(np.float32)
        nir = nir_band.astype(np.float32)
        
        # Avoid division by zero
        denominator = nir + red
        denominator = np.where(denominator == 0, 0.0001, denominator)
        
        # Calculate NDVI
        ndvi = (nir - red) / denominator
        
        # Apply realistic bounds
        ndvi = np.clip(ndvi, -1, 1)
        
        return ndvi
    
    def classify_vegetation(self, ndvi_array):
        """Classify vegetation health based on NDVI"""
        classification = np.zeros_like(ndvi_array, dtype=int)
        
        for i, (class_name, (min_val, max_val)) in enumerate(self.ndvi_classes.items()):
            mask = (ndvi_array >= min_val) & (ndvi_array < max_val)
            classification[mask] = i + 1
        
        return classification
    
    def calculate_statistics(self, ndvi_array):
        """Calculate NDVI statistics for a region"""
        valid_ndvi = ndvi_array[~np.isnan(ndvi_array)]
        
        if len(valid_ndvi) == 0:
            return None
        
        return {
            'mean': float(np.mean(valid_ndvi)),
            'median': float(np.median(valid_ndvi)),
            'std': float(np.std(valid_ndvi)),
            'min': float(np.min(valid_ndvi)),
            'max': float(np.max(valid_ndvi)),
            'percentile_25': float(np.percentile(valid_ndvi, 25)),
            'percentile_75': float(np.percentile(valid_ndvi, 75))
        }
    
    def detect_stress_areas(self, current_ndvi, baseline_ndvi, threshold=0.2):
        """Detect areas with significant NDVI decline"""
        # Calculate relative change
        change = (current_ndvi - baseline_ndvi) / np.abs(baseline_ndvi)
        change = np.where(np.abs(baseline_ndvi) < 0.1, 0, change)
        
        # Identify stress areas
        stress_mask = change < -threshold
        
        # Calculate stress severity
        stress_severity = np.abs(change) * stress_mask
        
        return {
            'stress_mask': stress_mask,
            'stress_severity': stress_severity,
            'stress_percentage': float(np.sum(stress_mask) / stress_mask.size * 100)
        }
