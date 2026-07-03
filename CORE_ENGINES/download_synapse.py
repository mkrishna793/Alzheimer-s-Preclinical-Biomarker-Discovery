import synapseclient
import os
import getpass

def main():
    print("=== SYNAPSE DATA DOWNLOADER ===")
    print("This script downloads all files you have added to your Synapse Download List.")
    
    # Get auth token securely
    auth_token = getpass.getpass("Please paste your Synapse Personal Access Token: ")
    
    try:
        # Initialize and login
        syn = synapseclient.Synapse()
        syn.login(authToken=auth_token)
        print("\nLogin successful!")
        
        # Get the download list
        print("Fetching your download list...")
        dl_list_file_entities = syn.get_download_list()
        
        if not dl_list_file_entities:
            print("Your Synapse download list is empty.")
            return
            
        print(f"Found files in download list. Starting download to {os.getcwd()}...")
        
        # Download the files
        # The download_list returns a list of file entities, we download them one by one or in batch
        # syn.download_from_download_list actually exists but let's use the simplest reliable method:
        manifest = syn.download_from_download_list(path=os.getcwd())
        
        print("\nDownload complete! Files saved to:", os.getcwd())
        
    except Exception as e:
        print("\nError during Synapse download:")
        print(str(e))

if __name__ == "__main__":
    main()
