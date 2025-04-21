import pickle
from pathlib import Path

def load_libraries():
    import os
    from pathlib import Path
    
    # Define the cache path
    cache_dir = Path(__file__).parent.parent / "cache"
    LIB_CACHE = cache_dir / "libraries.pkl"
    
    # Check if cache exists
    if not os.path.exists(LIB_CACHE):
        print("Building library cache for first use...")
        # Make sure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        # Import and run the build cache function
        from thereispythonlibraryforthis.scripts.build_cache import build_library_cache
        build_library_cache()
        print("Cache built successfully!")
    
    # Now load the cache as before
    with open(LIB_CACHE, "rb") as f:
        return pickle.load(f)