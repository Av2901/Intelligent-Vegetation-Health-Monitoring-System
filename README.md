

# 🌱 Intelligent Vegetation Health Monitoring System

An **AI-powered satellite imagery analysis system** that monitors crop health and detects vegetation stress in agricultural regions using **Sentinel-2 data** and **NDVI calculations**.

---

## 🚀 Key Features

* 🛰️ **Real-time Satellite Analysis** – Processes Sentinel-2 imagery for vegetation health assessment
* 📊 **NDVI Time Series Analysis** – Compares current vegetation health against historical baselines
* ⚠️ **Automated Stress Detection** – Flags areas with significant vegetation decline (>20% deviation)
* 🗺️ **Interactive Dashboard** – Web-based interface with maps, charts, and visualizations
* 📋 **Plain-Language Reports** – Generates actionable insights for agricultural stakeholders
* 🌍 **Multi-Region Support** – Covers 35+ districts across northeastern India
* 📱 **Export Capabilities** – Download reports as text, JSON, or PDF formats

---

## 🚀 Quick Start

### ✅ Prerequisites

* Python 3.8 or higher
* Internet connection for satellite data access
* Modern web browser

### 📦 Installation

```bash
git clone https://github.com/yourusername/vegetation-health-monitor.git
cd vegetation-health-monitor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

### 🌐 Sentinel Hub API Setup

For real satellite data (optional — demo data included):

1. Sign up at [Sentinel Hub](https://www.sentinel-hub.com)
2. Create a configuration and obtain your credentials
3. Create a `.env` file:

```text
SH_CLIENT_ID=your_client_id_here  
SH_CLIENT_SECRET=your_client_secret_here
```

---

