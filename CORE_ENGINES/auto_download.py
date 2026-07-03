import synapseclient
import os
import shutil

token = "eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyIsImRvd25sb2FkIiwibW9kaWZ5Il0sIm9pZGNfY2xhaW1zIjp7fX0sInRva2VuX3R5cGUiOiJQRVJTT05BTF9BQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwczovL3JlcG8tcHJvZC5wcm9kLnNhZ2ViYXNlLm9yZy9hdXRoL3YxIiwiYXVkIjoiMCIsIm5iZiI6MTc3NzU0ODYwMCwiaWF0IjoxNzc3NTQ4NjAwLCJqdGkiOiIzNjYzMiIsInN1YiI6IjM1ODc1ODUifQ.DCV_kDhalmiOOdkWSQwbg2SdXuzci2T5vv6-lkcsBi5GVdevgznU6qqkPkFdoWANzvO3dFiIGCYmnOpq4RvjWTZeBJo56BdbYwEmgWaP_r6vDzNjBt9hzkoCDAFo9hvoMyRwLCJ3uQ8MiqRCGJttXaXflU00Gw3mYbFL6HcyndaZkd6IQclC7Vaj_08niebBSSYxVSlMXcYCodvwwvIFEw-dz6tSGvI_UgiZ0w-Iyb-YFz9FIIl3ejysqXcjj38zSRmd4QRWboF3zlSqsxdfjBZNHvVGYBAaPB8XiwJCR7I1Oa1O_SsyFvnh7HCBT7EVdwxXy39F3zCjQqWh3hfMbA"

def main():
    # Permanently set the cache directory to the D drive
    cache_dir = r"D:\Multimodal_Neuro_Research\synapse_cache"
    os.makedirs(cache_dir, exist_ok=True)
    
    # Setting the environment variable BEFORE initializing Synapse is the key
    os.environ["SYNAPSE_CACHE_DIR"] = cache_dir
    
    print(f"Starting Synapse automated download...")
    print(f"Cache location: {cache_dir}")
    
    try:
        # Initialize Synapse (it will now use SYNAPSE_CACHE_DIR)
        syn = synapseclient.Synapse()
        syn.login(authToken=token)
        print("Login successful! Continuing your download...")
        
        # This will resume the download directly into the D-drive cache
        downloaded_files = syn.get_download_list()
        
        print(f"\nAll files have been successfully synced to your D-drive!")
        print(f"Total files in download list: {len(downloaded_files)}")
        
    except Exception as e:
        print(f"Error during download: {e}")

if __name__ == "__main__":
    main()
