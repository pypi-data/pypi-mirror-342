import pickle
import requests
from pathlib import Path
import os

def build_library_cache():
    """Build and save cache of top Python libraries from PyPI."""
    URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json"
    
    try:
        r = requests.get(URL)
        r.raise_for_status()  # Raise an exception for HTTP errors
        data = r.json()
        
        # Extract library names from the data
        libs = [pkg["project"] for pkg in data["rows"]]
        
        # Define cache directory relative to the script location
        # This ensures it works when installed as a package
        cache_dir = Path(__file__).parent.parent.parent / "cache"
        os.makedirs(cache_dir, exist_ok=True)
        
        # Save the library list to the cache file
        with open(cache_dir / "libraries.pkl", "wb") as f:
            pickle.dump(libs, f)
        
        return True
    except Exception as e:
        print(f"Error building library cache: {e}")
        return False

if __name__ == "__main__":
    # This allows the script to be run directly
    success = build_library_cache()
    if success:
        print("Library cache built successfully!")
    else:
        print("Failed to build library cache.")