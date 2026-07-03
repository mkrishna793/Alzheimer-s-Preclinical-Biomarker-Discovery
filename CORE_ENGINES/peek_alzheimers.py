import mne
import os

def main():
    set_path = r"D:\Multimodal_Neuro_Research\synapse_cache_backup\100\133033100\s6_sub-100040_rs_eeg.set"
    
    print(f"Peeking into Alzheimer's subject: {os.path.basename(set_path)}")
    
    try:
        # Load the header only to see channels
        raw = mne.io.read_raw_eeglab(set_path, preload=False)
        print(f"Success! Found {len(raw.ch_names)} channels.")
        print(f"First 50 channels: {raw.ch_names[:50]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
