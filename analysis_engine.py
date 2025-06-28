import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from satellite_data import SatelliteDataProcessor
from ndvi_processor import NDVIProcessor

class VegetationAnalyzer:
    def __init__(self):
        self.satellite_processor = SatelliteDataProcessor()
        self.ndvi_processor = NDVIProcessor()
        
    def analyze_region(self, lat, lon, region_name="Unknown"):
        """Complete analysis pipeline for a region"""
        print(f"Analyzing region: {region_name} at {lat}, {lon}")
        
        # Create bounding box
        bbox = self.satellite_processor.create_bbox(lat, lon, buffer_km=10)
        
        # Define time periods
        current_end = datetime.now()
        current_start = current_end - timedelta(days=30)
        baseline_end = datetime(current_end.year - 1, current_end.month, current_end.day)
        baseline_start = baseline_end - timedelta(days=30)
        
        # Fetch satellite data
        print("Fetching current satellite data...")
        current_data = self.satellite_processor.fetch_sentinel2_data(
            bbox, current_start, current_end
        )
        
        print("Fetching baseline satellite data...")
        baseline_data = self.satellite_processor.fetch_sentinel2_data(
            bbox, baseline_start, baseline_end
        )
        
        if current_data is None or baseline_data is None:
            return {"error": "Could not fetch satellite data"}
        
        # Calculate NDVI
        print("Calculating NDVI...")
        current_ndvi = self.ndvi_processor.calculate_ndvi(
            current_data[:,:,0], current_data[:,:,1]
        )
        baseline_ndvi = self.ndvi_processor.calculate_ndvi(
            baseline_data[:,:,0], baseline_data[:,:,1]
        )
        
        # Analyze for stress
        print("Detecting stress areas...")
        stress_analysis = self.ndvi_processor.detect_stress_areas(
            current_ndvi, baseline_ndvi
        )
        
        # Calculate statistics
        current_stats = self.ndvi_processor.calculate_statistics(current_ndvi)
        baseline_stats = self.ndvi_processor.calculate_statistics(baseline_ndvi)
        
        # Generate report
        report = self._generate_analysis_report(
            region_name, current_stats, baseline_stats, stress_analysis
        )
        
        return {
            'region_name': region_name,
            'coordinates': {'lat': lat, 'lon': lon},
            'analysis_date': current_end.isoformat(),
            'current_ndvi': current_ndvi.tolist(),
            'baseline_ndvi': baseline_ndvi.tolist(),
            'current_stats': current_stats,
            'baseline_stats': baseline_stats,
            'stress_analysis': stress_analysis,
            'report': report
        }
    
    def _generate_analysis_report(self, region_name, current_stats, baseline_stats, stress_analysis):
        """Generate plain language analysis report"""
        if not current_stats or not baseline_stats:
            return "Unable to generate report due to insufficient data."
        
        current_mean = current_stats['mean']
        baseline_mean = baseline_stats['mean']
        change_pct = ((current_mean - baseline_mean) / baseline_mean) * 100
        
        stress_pct = stress_analysis['stress_percentage']
        
        report = f"Vegetation Health Analysis for {region_name}:\n\n"
        
        if change_pct < -20:
            report += f"⚠️ ALERT: Significant vegetation stress detected. "
            report += f"Current NDVI ({current_mean:.3f}) is {abs(change_pct):.1f}% lower than baseline ({baseline_mean:.3f}). "
        elif change_pct < -10:
            report += f"⚡ CAUTION: Moderate vegetation decline observed. "
            report += f"Current NDVI is {abs(change_pct):.1f}% below normal levels. "
        else:
            report += f"✅ NORMAL: Vegetation health appears stable. "
            report += f"Current NDVI ({current_mean:.3f}) shows {change_pct:+.1f}% change from baseline. "
        
        report += f"\n\nStress Coverage: {stress_pct:.1f}% of analyzed area shows stress indicators.\n"
        
        if stress_pct > 30:
            report += "\n🚨 RECOMMENDATION: Immediate field assessment recommended. Consider emergency agricultural interventions."
        elif stress_pct > 15:
            report += "\n📋 RECOMMENDATION: Monitor closely and prepare contingency measures."
        else:
            report += "\n✓ RECOMMENDATION: Continue routine monitoring."
        
        return report
