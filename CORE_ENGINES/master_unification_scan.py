import pandas as pd
import numpy as np
import mne
import matplotlib.pyplot as plt
import seaborn as sns
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
    synapse_dir = r"D:\Multimodal_Neuro_Research\synapse_cache_backup"
    healthy_dir = r"D:\Multimodal_Neuro_Research\Full_60_Baseline"
    temp_dir = r"D:\Multimodal_Neuro_Research\Temp_Stitch"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    results_file = r"D:\Multimodal_Neuro_Research\MASTER_POPULATION_DATA.csv"
    
    print("Mapping 28GB of Human Brain Data...")
    all_set = []
    for root, dirs, files in os.walk(synapse_dir):
        for f in files:
            if f.endswith('.set'): all_set.append(os.path.join(root, f))
    all_vhdr = glob.glob(os.path.join(healthy_dir, "sub-*", "ses-iemu", "ieeg", "*.vhdr"))

    results = []
    
    # 1. Healthy Subjects
    print(f"Precision Scanning {len(all_vhdr)} Healthy Subjects...")
    for vhdr in all_vhdr:
        try:
            raw = mne.io.read_raw_brainvision(vhdr, preload=True, verbose=False)
            ch = find_temporal_channel(raw)
            raw.pick_channels([ch])
            psd = raw.compute_psd(fmin=1, fmax=20, verbose=False)
            data, freqs = psd.get_data(return_freqs=True)
            
            # ALPHA MASK (4-15Hz)
            mask = (freqs >= 4) & (freqs <= 15)
            peak_hz = freqs[mask][np.argmax(data[0][mask])]
            
            results.append({'group': 'Healthy', 'hz': peak_hz})
        except: continue

    # 2. Alzheimer's/Dementia
    print(f"Precision Scanning {len(all_set)} Dementia Patients...")
    for set_path in all_set:
        try:
            has_internal = os.path.getsize(set_path) > 1000000
            if not has_internal:
                fdt_path = set_path.replace('.set', '.fdt')
                if not os.path.exists(fdt_path): continue
            
            raw = mne.io.read_raw_eeglab(set_path, preload=True, verbose=False)
            ch = find_temporal_channel(raw)
            raw.pick_channels([ch])
            psd = raw.compute_psd(fmin=1, fmax=20, verbose=False)
            data, freqs = psd.get_data(return_freqs=True)
            
            mask = (freqs >= 4) & (freqs <= 15)
            peak_hz = freqs[mask][np.argmax(data[0][mask])]
            
            group = 'Alzheimers' if 'sub-300' in os.path.basename(set_path) else 'Other_Dementia'
            results.append({'group': group, 'hz': peak_hz})
        except: continue

    df = pd.DataFrame(results)
    df.to_csv(results_file, index=False)

    # 3. Master Graph
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="darkgrid")
    
    # KDE
    sns.kdeplot(data=df[df['group']=='Healthy'], x='hz', fill=True, color='#2ecc71', label='Healthy Baseline (Avg)', linewidth=4, alpha=0.4)
    sns.kdeplot(data=df[df['group']=='Alzheimers'], x='hz', fill=True, color='#e74c3c', label='Alzheimer Population (Avg)', linewidth=4, alpha=0.4)
    
    # Stats
    h_mean = df[df['group']=='Healthy']['hz'].mean()
    a_mean = df[df['group']=='Alzheimers']['hz'].mean()
    
    plt.axvline(h_mean, color='#27ae60', linestyle='--', linewidth=3)
    plt.axvline(a_mean, color='#c0392b', linestyle='--', linewidth=3)

    plt.text(h_mean+0.2, 0.5, f"Healthy: {h_mean:.2f}Hz", color='#27ae60', fontweight='bold')
    plt.text(a_mean-1.5, 0.5, f"AD: {a_mean:.2f}Hz", color='#c0392b', fontweight='bold')

    plt.title(f"THE FINAL POPULATION PROOF (N={len(df)})", fontsize=18, fontweight='bold')
    plt.xlabel("Brain Speed (Hz)", fontsize=14)
    plt.ylabel("Population Density", fontsize=14)
    plt.xlim(4, 15)
    plt.legend(fontsize=12)
    
    plt.savefig(r"D:\Multimodal_Neuro_Research\TOTAL_POPULATION_PROOF.png")
    plt.savefig(r"C:\Users\bhanu\OneDrive\Desktop\ALZHEIMER_RESEARCH_RESULTS\TOTAL_POPULATION_PROOF.png")
    
    print(f"\nTOTAL PRECISION COMPLETE!")
    print(f"Total Subjects: {len(df)}")
    print(df.groupby('group')['hz'].mean())

if __name__ == "__main__":
    main()
