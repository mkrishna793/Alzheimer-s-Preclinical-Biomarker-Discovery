import mne
import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    # 1. Load Healthy Baseline (Subject 01)
    healthy_vhdr = r"D:\Multimodal_Neuro_Research\Subject_01_Clean\sub-01\ses-iemu\ieeg\sub-01_ses-iemu_task-rest_acq-clinical_run-1_ieeg.vhdr"
    raw_h = mne.io.read_raw_brainvision(healthy_vhdr, preload=True)
    raw_h.pick_channels(['AHR1']) # Hippocampus
    psd_h = raw_h.compute_psd(fmin=1, fmax=20)
    data_h, freqs_h = psd_h.get_data(return_freqs=True)
    psd_h_norm = data_h[0] / np.max(data_h[0])

    # 2. Load Alzheimer's Subject (Subject 100037)
    ad_set = r"D:\Multimodal_Neuro_Research\Comparison_Study\s6_sub-100037_rs_eeg.set"
    raw_ad = mne.io.read_raw_eeglab(ad_set, preload=True)
    
    # In scalp EEG, T7/T8 or P7/P8 are closest to the Temporal lobe/Hippocampus
    # Let's find what channels we have
    print(f"AD Subject Channels: {raw_ad.ch_names[:20]}")
    
    # We'll pick a temporal channel like 'T7' or the first available temporal
    target_ad = None
    for ch in ['T7', 'T8', 'P7', 'P8', 'T3', 'T4']:
        if ch in raw_ad.ch_names:
            target_ad = ch
            break
    
    if not target_ad:
        target_ad = raw_ad.ch_names[0] # Fallback
        
    print(f"Using AD channel: {target_ad}")
    raw_ad.pick_channels([target_ad])
    psd_ad = raw_ad.compute_psd(fmin=1, fmax=20)
    data_ad, freqs_ad = psd_ad.get_data(return_freqs=True)
    psd_ad_norm = data_ad[0] / np.max(data_ad[0])

    # 3. Visualization: Side-by-Side Comparison
    plt.figure(figsize=(12, 6))
    
    # Plot Healthy
    plt.plot(freqs_h, psd_h_norm, color='#2ecc71', linewidth=3, label='Healthy Baseline (10Hz Target)')
    
    # Plot Alzheimer's
    plt.plot(freqs_ad, psd_ad_norm, color='#e74c3c', linewidth=3, linestyle='--', label=f'Alzheimer\'s Patient ({target_ad})')
    
    # Highlight the shift zone
    plt.axvspan(8, 12, color='orange', alpha=0.1, label='Healthy Alpha Zone')
    plt.axvspan(4, 8, color='red', alpha=0.05, label='Disease Slowing Zone')

    plt.title("THE BREAKTHROUGH: Healthy vs. Alzheimer's Brain Rhythms", fontsize=16, fontweight='bold')
    plt.xlabel("Frequency (Speed in Hz)")
    plt.ylabel("Normalized Power")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    # Save comparison
    output_path = r"D:\Multimodal_Neuro_Research\final_comparison_discovery.png"
    plt.savefig(output_path)
    print(f"Comparison Complete! Graph saved to: {output_path}")

if __name__ == "__main__":
    main()
