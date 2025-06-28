import subprocess
import sys

def main():
    print("🌱 Starting Vegetation Health Monitoring System...")
    print("📡 Loading satellite data processors...")
    print("🗺️ Initializing dashboard...")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    main()

