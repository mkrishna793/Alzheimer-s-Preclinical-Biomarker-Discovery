import mne
import matplotlib.pyplot as plt
import numpy as np
import os

def find_hippocampus_channel(raw):
    # Expanded keywords for different naming conventions
    keywords = ['AHR', 'PHR', 'AHL', 'PHL', 'HIP', 'HC', 'Hippocampus', 'depth']
    for ch in raw.ch_names:
        for key in keywords:
            if key.lower() in ch.lower():
                return ch
    # If no keywords, look for 'SEEG' types which are often hippocampus
    for i, ch_type in enumerate(raw.get_channel_types()):
        if ch_type == 'seeg':
            return raw.ch_names[i]
    return None

def main():
    # Final verified paths for the group baseline
    base_dir = r"D:\Multimodal_Neuro_Research\Group_Baseline_Clean"
    subjects = [
        r"D:\Multimodal_Neuro_Research\Subject_01_Clean\sub-01\ses-iemu\ieeg\sub-01_ses-iemu_task-rest_acq-clinical_run-1_ieeg.vhdr",
        os.path.join(base_dir, r"sub-02\ses-iemu\ieeg\sub-02_ses-iemu_task-film_acq-clinical_run-1_ieeg.vhdr"),
        os.path.join(base_dir, r"sub-03\ses-iemu\ieeg\sub-03_ses-iemu_task-film_acq-clinical_run-1_ieeg.vhdr"),
        os.path.join(base_dir, r"sub-05\ses-iemu\ieeg\sub-05_ses-iemu_task-film_acq-clinical_run-1_ieeg.vhdr"),
        os.path.join(base_dir, r"sub-06\ses-iemu\ieeg\sub-06_ses-iemu_task-film_acq-clinical_run-1_ieeg.vhdr")
    ]
    
    all_psds = []
    all_pulses = []
    freqs = None
    sfreq = 500
    
    print(f"Starting Average Scan for {len(subjects)} subjects...")
    
    for vhdr in subjects:
        try:
            if not os.path.exists(vhdr):
                print(f"File missing: {vhdr}")
                continue
                
            print(f"Analyzing {os.path.basename(vhdr)}...")
            raw = mne.io.read_raw_brainvision(vhdr, preload=True)
            raw.resample(sfreq)
            
            ch = find_hippocampus_channel(raw)
            if not ch:
                print(f"Skipping {vhdr}: No Hippocampus sensor found.")
                continue
            
            print(f"Using channel: {ch}")
            raw.pick_channels([ch])
            
            # Pulse extraction
            data = raw.get_data(start=0, stop=sfreq)[0]
            data = (data - np.mean(data)) / np.std(data)
            all_pulses.append(data)
            
            # PSD
            psd_obj = raw.compute_psd(fmin=1, fmax=40)
            psd_data, psd_freqs = psd_obj.get_data(return_freqs=True)
            psd_norm = psd_data[0] / np.max(psd_data[0])
            all_psds.append(psd_norm)
            freqs = psd_freqs
            
        except Exception as e:
            print(f"Error processing {vhdr}: {e}")

    if len(all_psds) < 2:
        print("Not enough subjects processed successfully.")
        return

    # Calculate Group Averages
    avg_pulse = np.mean(all_pulses, axis=0)
    avg_psd = np.mean(all_psds, axis=0)
    times = np.linspace(0, 1, sfreq)

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # Plot 1: The Average Pulse
    for p in all_pulses:
        ax1.plot(times, p, color='gray', alpha=0.15, linewidth=0.8)
    ax1.plot(times, avg_pulse, color='#d35400', linewidth=4, label='The Universal Pulse (Healthy Avg)')
    ax1.set_title("The 'Universal Memory Pulse' - Healthy Population Baseline", fontsize=16, fontweight='bold')
    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Normalized Strength")
    ax1.legend()
    ax1.grid(True, alpha=0.1)

    # Plot 2: Average Power Spectrum
    for p in all_psds:
        ax2.plot(freqs, p, color='gray', alpha=0.15, linewidth=0.8)
    ax2.plot(freqs, avg_psd, color='#8e44ad', linewidth=4, label='The Universal Spectrum (Healthy Avg)')
    ax2.axvspan(8, 12, color='orange', alpha=0.1, label='Alpha Standard (10Hz)')
    ax2.set_title("The 'Universal Memory Rhythm' - Healthy Population Baseline", fontsize=16, fontweight='bold')
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Relative Power")
    
    # Mark the average peak
    peak_idx = np.argmax(avg_psd[(freqs >= 1) & (freqs <= 15)])
    peak_freq = freqs[peak_idx]
    ax2.annotate(f'Avg Peak: {peak_freq:.1f}Hz', xy=(peak_freq, avg_psd[peak_idx]), 
                 xytext=(peak_freq+5, avg_psd[peak_idx]),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))

    ax2.legend()
    ax2.grid(True, alpha=0.1)

    plt.tight_layout()
    plt.savefig(r"D:\Multimodal_Neuro_Research\universal_healthy_baseline.png")
    print(f"Success! Universal Baseline Chart saved with {len(all_psds)} subjects.")

if __name__ == "__main__":
    main()
