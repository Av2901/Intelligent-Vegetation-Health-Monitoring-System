import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from analysis_engine import VegetationAnalyzer
from config import config

# Page configuration
st.set_page_config(
    page_title="Vegetation Health Monitor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize analyzer
@st.cache_resource
def load_analyzer():
    return VegetationAnalyzer()

analyzer = load_analyzer()

# Main application
def main():
    st.title("🌱 Intelligent Vegetation Health Monitoring System")
    st.markdown("Monitor crop health using Sentinel-2 satellite imagery and NDVI analysis")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Region selection
        region_type = st.selectbox(
            "Select Region Type",
            ["Predefined Districts", "Custom Coordinates"]
        )
        
        if region_type == "Predefined Districts":
            district = st.selectbox(
                "Select District",
                list(config.TEST_REGIONS.keys())
            )
            coordinates = config.TEST_REGIONS[district]
            lat, lon = coordinates['lat'], coordinates['lon']
            region_name = f"{district} District, Assam"
        else:
            lat = st.number_input("Latitude", value=26.1445, format="%.4f")
            lon = st.number_input("Longitude", value=91.7362, format="%.4f")
            region_name = f"Custom Location ({lat:.3f}, {lon:.3f})"
        
        # Analysis button
        if st.button("🔍 Analyze Region", type="primary"):
            st.session_state.analysis_requested = True
            st.session_state.analysis_coords = (lat, lon, region_name)
    
    # Main content
    if hasattr(st.session_state, 'analysis_requested') and st.session_state.analysis_requested:
        lat, lon, region_name = st.session_state.analysis_coords
        
        with st.spinner(f"Analyzing {region_name}..."):
            results = analyzer.analyze_region(lat, lon, region_name)
        
        if 'error' in results:
            st.error(f"Analysis failed: {results['error']}")
        else:
            display_results(results)
    else:
        display_welcome_screen()

def display_welcome_screen():
    """Display welcome screen with instructions"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Welcome to the Vegetation Health Monitor
        
        This system uses Sentinel-2 satellite imagery to monitor crop health and detect stress in agricultural regions.
        
        **How to use:**
        1. Select a region from the sidebar
        2. Click "Analyze Region" to start analysis
        3. View results including NDVI maps, trends, and recommendations
        
        **Features:**
        - 🛰️ Real-time satellite data analysis
        - 📊 NDVI trend comparison
        - ⚠️ Automated stress detection
        - 📋 Plain-language reports
        
        **Note:** Currently running with synthetic demo data for testing.
        """)

def display_results(results):
    """Display analysis results"""
    st.success(f"✅ Analysis completed for {results['region_name']}")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ NDVI Map", "📈 Statistics", "📋 Report"])
    
    with tab1:
        display_overview(results)
    
    with tab2:
        display_ndvi_map(results)
    
    with tab3:
        display_statistics(results)
    
    with tab4:
        display_report(results)

def display_overview(results):
    """Display overview metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    current_stats = results['current_stats']
    baseline_stats = results['baseline_stats']
    stress_analysis = results['stress_analysis']
    
    with col1:
        st.metric(
            "Current NDVI",
            f"{current_stats['mean']:.3f}",
            f"{((current_stats['mean'] - baseline_stats['mean']) / baseline_stats['mean'] * 100):+.1f}%"
        )
    
    with col2:
        st.metric(
            "Baseline NDVI",
            f"{baseline_stats['mean']:.3f}"
        )
    
    with col3:
        st.metric(
            "Stress Coverage",
            f"{stress_analysis['stress_percentage']:.1f}%"
        )
    
    with col4:
        health_status = "🟢 Healthy" if stress_analysis['stress_percentage'] < 15 else "🟡 Moderate" if stress_analysis['stress_percentage'] < 30 else "🔴 High Stress"
        st.metric("Health Status", health_status)

def display_ndvi_map(results):
    """Display NDVI visualization map"""
    st.subheader("🗺️ NDVI Visualization")
    
    lat, lon = results['coordinates']['lat'], results['coordinates']['lon']
    
    # Create map
    m = folium.Map(location=[lat, lon], zoom_start=12)
    
    # Add marker for analysis center
    folium.Marker(
        [lat, lon],
        popup=f"Analysis Center: {results['region_name']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add NDVI overlay (simplified visualization)
    current_ndvi = np.array(results['current_ndvi'])
    
    # Create color overlay based on NDVI values
    bounds = [[lat-0.05, lon-0.05], [lat+0.05, lon+0.05]]
    
    folium.Rectangle(
        bounds=bounds,
        color='green',
        fill=True,
        fillOpacity=0.3,
        popup="NDVI Analysis Area"
    ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)

def display_statistics(results):
    """Display detailed statistics"""
    st.subheader("📈 NDVI Statistics Comparison")
    
    current_stats = results['current_stats']
    baseline_stats = results['baseline_stats']
    
    # Create comparison chart
    metrics = ['mean', 'median', 'std', 'percentile_25', 'percentile_75']
    current_values = [current_stats[metric] for metric in metrics]
    baseline_values = [baseline_stats[metric] for metric in metrics]
    
    fig = go.Figure(data=[
        go.Bar(name='Current Period', x=metrics, y=current_values),
        go.Bar(name='Baseline Period', x=metrics, y=baseline_values)
    ])
    
    fig.update_layout(
        title="NDVI Statistics Comparison",
        xaxis_title="Metric",
        yaxis_title="NDVI Value",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics table
    st.subheader("Detailed Statistics")
    stats_df = pd.DataFrame({
        'Metric': metrics,
        'Current': current_values,
        'Baseline': baseline_values,
        'Change (%)': [((c-b)/b*100) for c, b in zip(current_values, baseline_values)]
    })
    
    st.dataframe(stats_df, use_container_width=True)

def display_report(results):
    """Display analysis report"""
    st.subheader("📋 Analysis Report")
    
    # Display the generated report
    st.text_area(
        "Automated Analysis Report",
        results['report'],
        height=300,
        disabled=True
    )
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download Report as Text"):
            st.download_button(
                label="Download",
                data=results['report'],
                file_name=f"vegetation_report_{results['region_name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📊 Download Data as JSON"):
            import json
            json_data = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="Download",
                data=json_data,
                file_name=f"vegetation_data_{results['region_name'].replace(' ', '_')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
