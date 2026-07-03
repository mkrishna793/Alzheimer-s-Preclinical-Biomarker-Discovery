import mne
import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    # UPDATED PATH to the clean binary data
    vhdr_path = r"D:\Multimodal_Neuro_Research\Subject_01_Clean\sub-01\ses-iemu\ieeg\sub-01_ses-iemu_task-rest_acq-clinical_run-1_ieeg.vhdr"
    
    print(f"Loading REAL iEEG data from: {vhdr_path}")
    
    try:
        # Load the data
        raw = mne.io.read_raw_brainvision(vhdr_path, preload=True)
        
        # Target AHR1 (Anterior Hippocampus Right)
        target_channel = 'AHR1'
        
        if target_channel not in raw.ch_names:
            # Sometimes names have extra spaces or prefixes
            matched = [c for c in raw.ch_names if target_channel in c]
            if matched:
                target_channel = matched[0]
            else:
                print(f"Error: {target_channel} not found. Available: {raw.ch_names[:10]}")
                return

        print(f"Success! Extracting rhythm for {target_channel}...")
        
        # Select the channel
        raw.pick_channels([target_channel])
        
        # Plotting
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 1. Raw signal
        data, times = raw.get_data(start=0, stop=int(raw.info['sfreq']*3), return_times=True)
        ax1.plot(times, data[0] * 1e6, color='#2ecc71', linewidth=1)
        ax1.set_title(f"The 'Brain Pulse' (Raw Signal) - Healthy Hippocampus", fontsize=15, fontweight='bold')
        ax1.set_ylabel("Microvolts (uV)")
        ax1.set_xlabel("Time (seconds)")
        ax1.grid(True, alpha=0.3)
        
        # 2. Power Spectrum
        print("Calculating the Power Spectrum (The Rhythms)...")
        psd = raw.compute_psd(fmin=1, fmax=40)
        psds, freqs = psd.get_data(return_freqs=True)
        
        # Log scale for power is often clearer
        ax2.fill_between(freqs, psds[0], color='#3498db', alpha=0.3)
        ax2.plot(freqs, psds[0], color='#2980b9', linewidth=2.5)
        ax2.set_title("The 'Music' Chart (Power Spectrum) - Healthy Baseline", fontsize=15, fontweight='bold')
        ax2.set_ylabel("Power")
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_xlim(1, 40)
        
        # Annotate peaks
        # Let's find the max in the Alpha range
        alpha_mask = (freqs >= 8) & (freqs <= 12)
        if any(alpha_mask):
            peak_freq = freqs[alpha_mask][np.argmax(psds[0][alpha_mask])]
            ax2.annotate(f'Alpha Peak: {peak_freq:.1f}Hz', xy=(peak_freq, psds[0][freqs == peak_freq][0]), 
                         xytext=(peak_freq+2, psds[0][freqs == peak_freq][0]*1.2),
                         arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
        
        ax2.axvspan(4, 8, color='green', alpha=0.1, label='Theta (Memory)')
        ax2.axvspan(8, 12, color='orange', alpha=0.1, label='Alpha (Idle)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        output_path = r"D:\Multimodal_Neuro_Research\healthy_rhythm_FINAL.png"
        plt.savefig(output_path)
        print(f"Discovery Complete! Graph saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
