"""
Generate Publication-Quality Figures for Project Neuro-Bridge Research Paper
Author: Mohan Krishna
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import os

OUT = r"D:\NEURO_BRIDGE_RESEARCH\PAPER_FIGURES"
os.makedirs(OUT, exist_ok=True)

# Load master data
df = pd.read_csv(r"D:\NEURO_BRIDGE_RESEARCH\DISCOVERY_VAULT\MASTER_POPULATION_DATA.csv")

# ============================================================
# FIGURE 1: Study Design Flowchart (as a structured bar chart)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
groups = ['Healthy Controls\n(ds003688)', 'Alzheimer\'s Disease\n(BrainLat/Synapse)', 'Other Dementia\n(BrainLat/Synapse)']
counts = [
    len(df[df['group']=='Healthy']),
    len(df[df['group']=='Alzheimers']),
    len(df[df['group']=='Other_Dementia'])
]
colors = ['#27ae60', '#c0392b', '#f39c12']
bars = ax.bar(groups, counts, color=colors, edgecolor='black', linewidth=1.2, width=0.6)
for bar, c in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(c),
            ha='center', fontsize=16, fontweight='bold')
ax.set_ylabel('Number of Subjects', fontsize=14)
ax.set_title('Figure 1: Study Population Distribution (N = 161)', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(counts) + 15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig1_population.png'), dpi=300)
plt.close()
print("Figure 1 saved.")

# ============================================================
# FIGURE 2: Alpha Peak Frequency Distribution (KDE)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
sns.set_theme(style="whitegrid")

healthy = df[df['group']=='Healthy']['hz']
alzheimers = df[df['group']=='Alzheimers']['hz']
other = df[df['group']=='Other_Dementia']['hz']

sns.kdeplot(healthy, fill=True, color='#27ae60', alpha=0.4, linewidth=3, label=f'Healthy (n={len(healthy)}, μ={healthy.mean():.2f} Hz)', ax=ax)
sns.kdeplot(alzheimers, fill=True, color='#c0392b', alpha=0.4, linewidth=3, label=f'AD (n={len(alzheimers)}, μ={alzheimers.mean():.2f} Hz)', ax=ax)
sns.kdeplot(other, fill=True, color='#f39c12', alpha=0.3, linewidth=2, linestyle='--', label=f'Other Dementia (n={len(other)}, μ={other.mean():.2f} Hz)', ax=ax)

ax.axvline(healthy.mean(), color='#1e8449', linestyle='--', linewidth=2)
ax.axvline(alzheimers.mean(), color='#922b21', linestyle='--', linewidth=2)

ax.set_xlabel('Peak Frequency (Hz)', fontsize=14)
ax.set_ylabel('Probability Density', fontsize=14)
ax.set_title('Figure 2: Population-Level Peak Frequency Distribution', fontsize=16, fontweight='bold')
ax.set_xlim(2, 16)
ax.legend(fontsize=11, loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig2_kde_distribution.png'), dpi=300)
plt.close()
print("Figure 2 saved.")

# ============================================================
# FIGURE 3: Box + Strip Plot Comparison
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = df[df['group'].isin(['Healthy', 'Alzheimers'])].copy()
plot_df['group'] = plot_df['group'].replace({'Healthy': 'Healthy Controls', 'Alzheimers': 'Alzheimer\'s Disease'})

palette = {'Healthy Controls': '#27ae60', 'Alzheimer\'s Disease': '#c0392b'}
sns.boxplot(data=plot_df, x='group', y='hz', palette=palette, width=0.5, ax=ax, linewidth=2)
sns.stripplot(data=plot_df, x='group', y='hz', color='black', alpha=0.4, size=5, jitter=True, ax=ax)

ax.set_xlabel('')
ax.set_ylabel('Peak Frequency (Hz)', fontsize=14)
ax.set_title('Figure 3: Healthy vs. Alzheimer\'s — Individual Subject Comparison', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Stats annotation
h_mean = healthy.mean()
a_mean = alzheimers.mean()
delta = h_mean - a_mean
ax.annotate(f'Δ = {abs(delta):.2f} Hz shift', xy=(0.5, max(plot_df['hz'])-1),
            fontsize=14, fontweight='bold', color='#2c3e50', ha='center')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig3_boxplot_comparison.png'), dpi=300)
plt.close()
print("Figure 3 saved.")

# ============================================================
# FIGURE 4: Histogram with Gaussian Fit
# ============================================================
from scipy.stats import norm

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Healthy
axes[0].hist(healthy, bins=15, color='#27ae60', alpha=0.6, edgecolor='black', density=True, label='Healthy')
mu_h, std_h = norm.fit(healthy)
x = np.linspace(2, 14, 200)
axes[0].plot(x, norm.pdf(x, mu_h, std_h), color='#1e8449', linewidth=3)
axes[0].set_title(f'Healthy Controls\nμ = {mu_h:.2f} Hz, σ = {std_h:.2f}', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Peak Frequency (Hz)', fontsize=12)
axes[0].set_ylabel('Density', fontsize=12)
axes[0].set_xlim(2, 16)

# Alzheimer's
axes[1].hist(alzheimers, bins=12, color='#c0392b', alpha=0.6, edgecolor='black', density=True, label='AD')
mu_a, std_a = norm.fit(alzheimers)
axes[1].plot(x, norm.pdf(x, mu_a, std_a), color='#922b21', linewidth=3)
axes[1].set_title(f'Alzheimer\'s Disease\nμ = {mu_a:.2f} Hz, σ = {std_a:.2f}', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Peak Frequency (Hz)', fontsize=12)
axes[1].set_xlim(2, 16)

fig.suptitle('Figure 4: Frequency Distribution with Gaussian Fit', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig4_histogram_gaussian.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

# ============================================================
# FIGURE 5: Summary Statistics Table (as image)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('off')

stats_data = []
for grp_name, grp_label in [('Healthy', 'Healthy Controls'), ('Alzheimers', 'Alzheimer\'s Disease'), ('Other_Dementia', 'Other Dementia')]:
    g = df[df['group']==grp_name]['hz']
    stats_data.append([grp_label, len(g), f'{g.mean():.2f}', f'{g.median():.2f}', f'{g.std():.2f}', f'{g.min():.2f}', f'{g.max():.2f}'])

col_labels = ['Group', 'N', 'Mean (Hz)', 'Median (Hz)', 'SD (Hz)', 'Min (Hz)', 'Max (Hz)']
table = ax.table(cellText=stats_data, colLabels=col_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.8)

# Color the header
for j in range(len(col_labels)):
    table[0, j].set_facecolor('#2c3e50')
    table[0, j].set_text_props(color='white', fontweight='bold')

# Color rows
row_colors = ['#d5f5e3', '#fadbd8', '#fdebd0']
for i in range(3):
    for j in range(len(col_labels)):
        table[i+1, j].set_facecolor(row_colors[i])

ax.set_title('Table 1: Descriptive Statistics of Peak Frequency by Group', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig5_statistics_table.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 5 (Table) saved.")

# ============================================================
# FIGURE 6: Research Pipeline Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(14, 4))
ax.axis('off')

steps = [
    ('STEP 1\nData Acquisition', '28.3 GB\n222 Subjects', '#3498db'),
    ('STEP 2\nHealthy Baseline', '9.87 Hz\nN = 53 (iEEG)', '#27ae60'),
    ('STEP 3\nDisease Mapping', '8.50 Hz (AD)\nN = 35 (EEG)', '#c0392b'),
    ('STEP 4\nCognitive Link', 'MoCa ↔ Hz\nCorrelation', '#8e44ad'),
    ('STEP 5\nPredictive Model', 'Digital Twin\n(Next Phase)', '#f39c12'),
]

for i, (title, desc, color) in enumerate(steps):
    x = 0.08 + i * 0.19
    rect = plt.Rectangle((x, 0.2), 0.15, 0.6, facecolor=color, edgecolor='black', linewidth=2, alpha=0.85, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x + 0.075, 0.62, title, ha='center', va='center', fontsize=10, fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(x + 0.075, 0.35, desc, ha='center', va='center', fontsize=9, color='white', transform=ax.transAxes)
    if i < len(steps) - 1:
        ax.annotate('', xy=(x + 0.17, 0.5), xytext=(x + 0.15, 0.5),
                    arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=3),
                    transform=ax.transAxes)

ax.set_title('Figure 6: Research Pipeline Overview', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig6_pipeline.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

print("\nAll 6 publication-quality figures generated successfully!")
print(f"Saved to: {OUT}")
