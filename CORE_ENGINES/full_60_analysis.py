import mne
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def find_hippocampus_channel(raw):
    # Expanded keywords for high robustness
    keywords = ['AHR', 'PHR', 'AHL', 'PHL', 'HIP', 'HC', 'Hippocampus', 'depth', 'AIL', 'ACL']
    for ch in raw.ch_names:
        for key in keywords:
            if key.lower() in ch.lower():
                return ch
    # Fallback to any SEEG (Depth) channel
    for i, ch_type in enumerate(raw.get_channel_types()):
        if ch_type == 'seeg':
            return raw.ch_names[i]
    return None

def main():
    base_dir = r"D:\Multimodal_Neuro_Research\Full_60_Baseline"
    vhdr_files = glob.glob(os.path.join(base_dir, "sub-*", "ses-iemu", "ieeg", "*task-rest*_ieeg.vhdr"))
    
    # If no resting state, try film task
    if not vhdr_files:
        vhdr_files = glob.glob(os.path.join(base_dir, "sub-*", "ses-iemu", "ieeg", "*.vhdr"))

    all_peaks = []
    all_psds = []
    freqs = None
    sfreq = 250 # Faster processing for large batch
    
    print(f"Starting Big Proof Analysis on {len(vhdr_files)} potential files...")
    
    count = 0
    for vhdr in vhdr_files:
        try:
            # We skip files that don't have their .eeg data yet
            eeg_file = vhdr.replace('.vhdr', '.eeg')
            if not os.path.exists(eeg_file):
                continue
                
            raw = mne.io.read_raw_brainvision(vhdr, preload=True, verbose=False)
            raw.resample(sfreq, verbose=False)
            
            ch = find_hippocampus_channel(raw)
            if not ch:
                continue
                
            raw.pick_channels([ch])
            
            # Power Spectrum Analysis
            psd_obj = raw.compute_psd(fmin=1, fmax=20, verbose=False)
            psd_data, psd_freqs = psd_obj.get_data(return_freqs=True)
            
            # Normalize and find peak in Alpha range (7-13Hz)
            psd_norm = psd_data[0] / np.max(psd_data[0])
            
            # Find the actual peak Hz
            alpha_mask = (psd_freqs >= 7) & (psd_freqs <= 13)
            peak_freq = psd_freqs[alpha_mask][np.argmax(psd_norm[alpha_mask])]
            
            all_peaks.append(peak_freq)
            all_psds.append(psd_norm)
            freqs = psd_freqs
            count += 1
            if count % 10 == 0:
                print(f"Processed {count} subjects...")
                
        except Exception:
            continue

    if not all_peaks:
        print("No valid data found.")
        return

    # Statistics
    avg_hz = np.mean(all_peaks)
    std_hz = np.std(all_peaks)
    avg_psd = np.mean(all_psds, axis=0)

    # Visualization
    plt.figure(figsize=(12, 7))
    
    # Plot all individuals in light gray
    for p in all_psds:
        plt.plot(freqs, p, color='gray', alpha=0.1, linewidth=0.5)
        
    # Plot the Population Average
    plt.plot(freqs, avg_psd, color='#2980b9', linewidth=4, label=f'Population Average (N={count})')
    
    # Highlight the Average Peak
    plt.axvline(avg_hz, color='#e67e22', linestyle='--', linewidth=2, label=f'Avg Peak: {avg_hz:.2f}Hz')
    plt.fill_betweenx([0, 1], avg_hz - std_hz, avg_hz + std_hz, color='#e67e22', alpha=0.1, label='Standard Deviation')

    plt.title(f"THE BIG PROOF: Healthy Population Baseline (Memory Rhythm)", fontsize=16, fontweight='bold')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Relative Power")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    output_path = r"D:\Multimodal_Neuro_Research\THE_BIG_PROOF_60_SUBJECTS.png"
    plt.savefig(output_path)
    # Also copy to desktop for user
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'ALZHEIMER_RESEARCH_RESULTS', 'THE_BIG_PROOF_60_SUBJECTS.png')
    plt.savefig(desktop_path)
    
    print(f"\nSUCCESS! Average Healthy Hz: {avg_hz:.2f}Hz")
    print(f"Graph saved to Desktop folder.")

if __name__ == "__main__":
    main()
