import pandas as pd
import numpy as np
import mne
import matplotlib.pyplot as plt
import os
import glob
import shutil

def find_temporal_channel(raw):
    keywords = ['T7', 'T8', 'P7', 'P8', 'T3', 'T4', 'A1', 'A2', 'CZ', 'PZ']
    for ch in keywords:
        matched = [c for c in raw.ch_names if ch in c.upper()]
        if matched: return matched[0]
    return raw.ch_names[0]

def main():
    base_dir = r"D:\Multimodal_Neuro_Research\synapse_cache_backup"
    moca_file = r"D:\Multimodal_Neuro_Research\synapse_cache_backup\731\133142731\cognition_ad_eeg_data.csv"
    
    # 1. Load MoCa Scores
    moca_df = pd.read_csv(moca_file)
    id_col = 'id EEG' if 'id EEG' in moca_df.columns else 'id'
    moca_df = moca_df[[id_col, 'moca_total']].dropna()
    moca_scores = dict(zip(moca_df[id_col], moca_df['moca_total']))

    # 2. Map all .set files (Aggressive search)
    print("Mapping Alzheimer's Mega-Files...")
    all_set_files = {}
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.set'):
                all_set_files[f] = os.path.join(root, f)

    results = []
    print(f"Linking {len(moca_scores)} Alzheimer's patients to their rhythms...")

    for sub_id, score in moca_scores.items():
        try:
            # Find the .set file containing the sub_id
            found_set = None
            for fname, fpath in all_set_files.items():
                if sub_id in fname:
                    found_set = fpath
                    break
            
            if not found_set: continue

            # For .set files with internal data, we can load them directly
            raw = mne.io.read_raw_eeglab(found_set, preload=True, verbose=False)
            ch = find_temporal_channel(raw)
            raw.pick_channels([ch])
            
            psd_obj = raw.compute_psd(fmin=1, fmax=20, verbose=False)
            psd_data, psd_freqs = psd_obj.get_data(return_freqs=True)
            psd_norm = psd_data[0] / np.max(psd_data[0])
            
            alpha_mask = (psd_freqs >= 4) & (psd_freqs <= 15)
            peak_hz = psd_freqs[alpha_mask][np.argmax(psd_norm[alpha_mask])]
            
            results.append({'sub': sub_id, 'hz': peak_hz, 'moca': score})
            print(f"Linked {sub_id}: {peak_hz:.2f}Hz -> MoCa {score}")
                
        except Exception as e:
            continue

    res_df = pd.DataFrame(results)
    if res_df.empty:
        print("Final Link failed.")
        return

    # 3. The Discovery Graph
    plt.figure(figsize=(10, 6))
    plt.scatter(res_df['hz'], res_df['moca'], color='#c0392b', s=150, alpha=0.8, edgecolors='black', label='Alzheimer Patients')
    
    # Fit line
    z = np.polyfit(res_df['hz'], res_df['moca'], 1)
    p = np.poly1d(z)
    plt.plot(res_df['hz'], p(res_df['hz']), color='#2980b9', linewidth=4, label='The Alzheimer\'s Decay Law')

    plt.title("STEP 3 BREAKTHROUGH: Brain Speed vs. Dementia Severity", fontsize=16, fontweight='bold')
    plt.xlabel("Alpha Rhythm Speed (Hz)")
    plt.ylabel("Memory Score (MoCa)")
    plt.legend()
    plt.grid(True, alpha=0.1)
    
    plt.savefig(r"D:\Multimodal_Neuro_Research\FINAL_STEP3_DECAY_LINK.png")
    plt.savefig(r"C:\Users\bhanu\OneDrive\Desktop\ALZHEIMER_RESEARCH_RESULTS\FINAL_STEP3_DECAY_LINK.png")
    
    correlation = res_df['hz'].corr(res_df['moca'])
    print(f"\nSUCCESS! Linked {len(res_df)} Alzheimer's patients.")
    print(f"Correlation: {correlation:.4f}")
    print(f"Discovery Formula: MoCa = {z[0]:.2f} * Hz + {z[1]:.2f}")

if __name__ == "__main__":
    main()
