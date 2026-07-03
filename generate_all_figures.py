"""Generate ALL publication figures for the 25-30 page research paper."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, mannwhitneyu
import os

OUT = r"D:\NEURO_BRIDGE_RESEARCH\PAPER_FIGURES"
os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(r"D:\NEURO_BRIDGE_RESEARCH\DISCOVERY_VAULT\MASTER_POPULATION_DATA.csv")
healthy = df[df['group']=='Healthy']['hz']
alzheimers = df[df['group']=='Alzheimers']['hz']
other = df[df['group']=='Other_Dementia']['hz']

# ---- FIG 1: Population Bar Chart ----
fig, ax = plt.subplots(figsize=(10, 5))
groups = ['Healthy Controls\n(N=107)', 'Alzheimer\'s Disease\n(N=35)', 'Other Dementia\n(N=19)']
counts = [len(healthy), len(alzheimers), len(other)]
colors = ['#27ae60', '#c0392b', '#f39c12']
bars = ax.bar(groups, counts, color=colors, edgecolor='black', linewidth=1.2, width=0.55)
for bar, c in zip(bars, counts):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, str(c), ha='center', fontsize=18, fontweight='bold')
ax.set_ylabel('Number of Subjects', fontsize=14)
ax.set_title('Figure 1: Study Population Distribution (N = 161)', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(counts)+15); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig1_population.png'), dpi=300); plt.close()
print("Fig 1 done")

# ---- FIG 2: KDE Distribution ----
fig, ax = plt.subplots(figsize=(12, 6))
sns.kdeplot(healthy, fill=True, color='#27ae60', alpha=0.4, linewidth=3, label=f'Healthy (n={len(healthy)}, μ={healthy.mean():.2f} Hz)', ax=ax)
sns.kdeplot(alzheimers, fill=True, color='#c0392b', alpha=0.4, linewidth=3, label=f'AD (n={len(alzheimers)}, μ={alzheimers.mean():.2f} Hz)', ax=ax)
sns.kdeplot(other, fill=True, color='#f39c12', alpha=0.3, linewidth=2, linestyle='--', label=f'Other Dementia (n={len(other)}, μ={other.mean():.2f} Hz)', ax=ax)
ax.axvline(healthy.mean(), color='#1e8449', linestyle='--', linewidth=2)
ax.axvline(alzheimers.mean(), color='#922b21', linestyle='--', linewidth=2)
ax.set_xlabel('Peak Frequency (Hz)', fontsize=14); ax.set_ylabel('Probability Density', fontsize=14)
ax.set_title('Figure 2: Population-Level Peak Frequency Distribution', fontsize=16, fontweight='bold')
ax.set_xlim(2, 16); ax.legend(fontsize=11)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig2_kde_distribution.png'), dpi=300); plt.close()
print("Fig 2 done")

# ---- FIG 3: Box + Strip Plot ----
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = df[df['group'].isin(['Healthy','Alzheimers'])].copy()
plot_df['group'] = plot_df['group'].replace({'Healthy':'Healthy Controls','Alzheimers':'Alzheimer\'s Disease'})
palette = {'Healthy Controls':'#27ae60','Alzheimer\'s Disease':'#c0392b'}
sns.boxplot(data=plot_df, x='group', y='hz', hue='group', palette=palette, width=0.5, ax=ax, linewidth=2, legend=False)
sns.stripplot(data=plot_df, x='group', y='hz', color='black', alpha=0.4, size=5, jitter=True, ax=ax)
ax.set_xlabel(''); ax.set_ylabel('Peak Frequency (Hz)', fontsize=14)
ax.set_title('Figure 3: Healthy vs. Alzheimer\'s — Individual Subject Comparison', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig3_boxplot.png'), dpi=300); plt.close()
print("Fig 3 done")

# ---- FIG 4: Histogram + Gaussian ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
mu_h, std_h = norm.fit(healthy); mu_a, std_a = norm.fit(alzheimers)
x = np.linspace(2, 16, 200)
axes[0].hist(healthy, bins=15, color='#27ae60', alpha=0.6, edgecolor='black', density=True)
axes[0].plot(x, norm.pdf(x, mu_h, std_h), color='#1e8449', linewidth=3)
axes[0].set_title(f'Healthy Controls\nμ={mu_h:.2f} Hz, σ={std_h:.2f}', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Peak Frequency (Hz)'); axes[0].set_ylabel('Density'); axes[0].set_xlim(2,16)
axes[1].hist(alzheimers, bins=12, color='#c0392b', alpha=0.6, edgecolor='black', density=True)
axes[1].plot(x, norm.pdf(x, mu_a, std_a), color='#922b21', linewidth=3)
axes[1].set_title(f'Alzheimer\'s Disease\nμ={mu_a:.2f} Hz, σ={std_a:.2f}', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Peak Frequency (Hz)'); axes[1].set_xlim(2,16)
fig.suptitle('Figure 4: Frequency Distribution with Gaussian Fit', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig4_histogram.png'), dpi=300, bbox_inches='tight'); plt.close()
print("Fig 4 done")

# ---- FIG 5: Stats Table ----
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.axis('off')
stats = []
for gn, gl in [('Healthy','Healthy Controls'),('Alzheimers','Alzheimer\'s Disease'),('Other_Dementia','Other Dementia')]:
    g = df[df['group']==gn]['hz']
    stats.append([gl, len(g), f'{g.mean():.2f}', f'{g.median():.2f}', f'{g.std():.2f}', f'{g.min():.2f}', f'{g.max():.2f}'])
cols = ['Group','N','Mean (Hz)','Median (Hz)','SD (Hz)','Min (Hz)','Max (Hz)']
table = ax.table(cellText=stats, colLabels=cols, loc='center', cellLoc='center')
table.auto_set_font_size(False); table.set_fontsize(11); table.scale(1.2, 1.8)
for j in range(len(cols)):
    table[0,j].set_facecolor('#2c3e50'); table[0,j].set_text_props(color='white', fontweight='bold')
for i,c in enumerate(['#d5f5e3','#fadbd8','#fdebd0']):
    for j in range(len(cols)): table[i+1,j].set_facecolor(c)
ax.set_title('Table 1: Descriptive Statistics of Peak Frequency', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig5_table.png'), dpi=300, bbox_inches='tight'); plt.close()
print("Fig 5 done")

# ---- FIG 6: Pipeline ----
fig, ax = plt.subplots(figsize=(14, 4))
ax.axis('off')
steps = [('STEP 1\nData\nAcquisition','28.3 GB\n222 Subjects','#3498db'),
         ('STEP 2\nHealthy\nBaseline','9.87 Hz\nN=53','#27ae60'),
         ('STEP 3\nDisease\nMapping','8.35 Hz\nN=35','#c0392b'),
         ('STEP 4\nCognitive\nLink','MoCa ↔ Hz','#8e44ad'),
         ('STEP 5\nAI Model\n(Future)','Digital Twin','#f39c12')]
for i,(t,d,c) in enumerate(steps):
    x = 0.05 + i*0.19
    rect = plt.Rectangle((x,0.15),0.16,0.7, facecolor=c, edgecolor='black', linewidth=2, alpha=0.85, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x+0.08,0.6,t,ha='center',va='center',fontsize=10,fontweight='bold',color='white',transform=ax.transAxes)
    ax.text(x+0.08,0.3,d,ha='center',va='center',fontsize=9,color='white',transform=ax.transAxes)
    if i < len(steps)-1:
        ax.annotate('',xy=(x+0.18,0.5),xytext=(x+0.16,0.5),arrowprops=dict(arrowstyle='->',color='#2c3e50',lw=3),transform=ax.transAxes)
ax.set_title('Figure 6: Research Pipeline Overview', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig6_pipeline.png'), dpi=300, bbox_inches='tight'); plt.close()
print("Fig 6 done")

# ---- FIG 7: MoCa Correlation ----
moca_data = [('sub-30001',7.0,22),('sub-30002',8.0,18),('sub-30004',8.75,22),('sub-30008',7.75,19),
             ('sub-30009',8.25,21),('sub-30011',8.50,20),('sub-30012',8.75,14),('sub-30013',8.50,20),
             ('sub-30015',7.75,14),('sub-30017',8.50,20),('sub-30018',8.25,21),('sub-30020',6.50,17),
             ('sub-30022',7.75,11),('sub-30026',7.75,18),('sub-30029',8.50,20),('sub-30031',8.75,20),
             ('sub-30003',9.00,10),('sub-30006',4.00,17),('sub-30016',4.25,15),('sub-30021',6.00,14),
             ('sub-30023',7.75,18),('sub-30019',9.00,16),('sub-30024',9.50,18),('sub-30025',11.00,20),
             ('sub-30027',8.50,15),('sub-30028',10.50,19),('sub-30033',7.75,15),('sub-30035',8.00,17),
             ('sub-30034',7.25,21)]
mdf = pd.DataFrame(moca_data, columns=['sub','hz','moca'])
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(mdf['hz'], mdf['moca'], color='#c0392b', s=120, alpha=0.7, edgecolors='black', zorder=5)
z = np.polyfit(mdf['hz'], mdf['moca'], 1); p = np.poly1d(z)
xline = np.linspace(3, 12, 100)
ax.plot(xline, p(xline), color='#2980b9', linewidth=3, label=f'Trend (slope={z[0]:.2f})')
corr = mdf['hz'].corr(mdf['moca'])
ax.set_xlabel('Peak Frequency (Hz)', fontsize=14); ax.set_ylabel('MoCa Score', fontsize=14)
ax.set_title(f'Figure 7: Brain Rhythm vs. Cognitive Score (r = {corr:.3f})', fontsize=15, fontweight='bold')
ax.legend(fontsize=12); ax.grid(True, alpha=0.15)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig7_moca_correlation.png'), dpi=300); plt.close()
print("Fig 7 done")

# ---- FIG 8: Violin Plot ----
fig, ax = plt.subplots(figsize=(10,6))
vdf = df.copy()
vdf['group'] = vdf['group'].replace({'Healthy':'Healthy\nControls','Alzheimers':'Alzheimer\'s\nDisease','Other_Dementia':'Other\nDementia'})
palette2 = {'Healthy\nControls':'#27ae60','Alzheimer\'s\nDisease':'#c0392b','Other\nDementia':'#f39c12'}
sns.violinplot(data=vdf, x='group', y='hz', hue='group', palette=palette2, inner='quartile', linewidth=2, ax=ax, legend=False)
ax.set_xlabel(''); ax.set_ylabel('Peak Frequency (Hz)', fontsize=14)
ax.set_title('Figure 8: Frequency Distribution by Group (Violin Plot)', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig8_violin.png'), dpi=300); plt.close()
print("Fig 8 done")

# ---- FIG 9: Future Roadmap ----
fig, ax = plt.subplots(figsize=(12, 5))
ax.axis('off')
phases = [('Phase 1\n(COMPLETED)','Data Collection\n& Baseline\nEstablishment','#27ae60',True),
          ('Phase 2\n(COMPLETED)','Disease Mapping\n& Cognitive\nCorrelation','#2980b9',True),
          ('Phase 3\n(NEXT)','AI Diagnostic\nModel\nDevelopment','#8e44ad',False),
          ('Phase 4\n(FUTURE)','Clinical\nHospital\nValidation','#e67e22',False),
          ('Phase 5\n(VISION)','Global\nDeployment\n& Screening','#c0392b',False)]
for i,(t,d,c,done) in enumerate(phases):
    x = 0.03 + i*0.19
    style = '-' if done else '--'
    rect = plt.Rectangle((x,0.15),0.17,0.7, facecolor=c if done else 'white', edgecolor=c, linewidth=3, linestyle=style, alpha=0.85 if done else 0.3, transform=ax.transAxes)
    ax.add_patch(rect)
    tcol = 'white' if done else '#2c3e50'
    ax.text(x+0.085,0.62,t,ha='center',va='center',fontsize=9,fontweight='bold',color=tcol,transform=ax.transAxes)
    ax.text(x+0.085,0.35,d,ha='center',va='center',fontsize=8,color=tcol,transform=ax.transAxes)
    if i < len(phases)-1:
        ax.annotate('',xy=(x+0.2,0.5),xytext=(x+0.17,0.5),arrowprops=dict(arrowstyle='->',color='#2c3e50',lw=2),transform=ax.transAxes)
ax.set_title('Figure 9: Project Neuro-Bridge — Development Roadmap', fontsize=15, fontweight='bold', pad=20)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig9_roadmap.png'), dpi=300, bbox_inches='tight'); plt.close()
print("Fig 9 done")

# ---- FIG 10: AI Architecture ----
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
# Input
rect1 = plt.Rectangle((0.02,0.6),0.18,0.3, facecolor='#3498db', edgecolor='black', lw=2, transform=ax.transAxes)
ax.add_patch(rect1); ax.text(0.11,0.75,'INPUT\nRaw EEG\nRecording',ha='center',va='center',fontsize=10,fontweight='bold',color='white',transform=ax.transAxes)
ax.annotate('',xy=(0.23,0.75),xytext=(0.20,0.75),arrowprops=dict(arrowstyle='->',color='black',lw=2),transform=ax.transAxes)
# Feature extraction
rect2 = plt.Rectangle((0.23,0.55),0.22,0.4, facecolor='#2ecc71', edgecolor='black', lw=2, transform=ax.transAxes)
ax.add_patch(rect2); ax.text(0.34,0.82,'FEATURE EXTRACTOR',ha='center',va='center',fontsize=10,fontweight='bold',color='white',transform=ax.transAxes)
feats = '• Peak Frequency\n• Alpha/Theta Power\n• Theta/Alpha Ratio\n• Spectral Entropy'
ax.text(0.34,0.68,feats,ha='center',va='center',fontsize=8,color='white',transform=ax.transAxes)
ax.annotate('',xy=(0.48,0.75),xytext=(0.45,0.75),arrowprops=dict(arrowstyle='->',color='black',lw=2),transform=ax.transAxes)
# ML Model
rect3 = plt.Rectangle((0.48,0.55),0.22,0.4, facecolor='#8e44ad', edgecolor='black', lw=2, transform=ax.transAxes)
ax.add_patch(rect3); ax.text(0.59,0.82,'ML CLASSIFIER',ha='center',va='center',fontsize=10,fontweight='bold',color='white',transform=ax.transAxes)
ax.text(0.59,0.68,'Random Forest\nGradient Boosting\nSVM Ensemble',ha='center',va='center',fontsize=8,color='white',transform=ax.transAxes)
ax.annotate('',xy=(0.73,0.75),xytext=(0.70,0.75),arrowprops=dict(arrowstyle='->',color='black',lw=2),transform=ax.transAxes)
# Output
rect4 = plt.Rectangle((0.73,0.55),0.24,0.4, facecolor='#e74c3c', edgecolor='black', lw=2, transform=ax.transAxes)
ax.add_patch(rect4); ax.text(0.85,0.82,'DIAGNOSTIC OUTPUT',ha='center',va='center',fontsize=10,fontweight='bold',color='white',transform=ax.transAxes)
ax.text(0.85,0.68,'• Risk Score (0-100%)\n• Classification\n• Predicted MoCa\n• Biomarker Report',ha='center',va='center',fontsize=8,color='white',transform=ax.transAxes)
# Database
rect5 = plt.Rectangle((0.35,0.05),0.30,0.3, facecolor='#f39c12', edgecolor='black', lw=2, transform=ax.transAxes)
ax.add_patch(rect5); ax.text(0.50,0.20,'REFERENCE DATABASE\n161 Subjects | 28.3 GB\nHealthy Baseline: 9.87 Hz',ha='center',va='center',fontsize=9,fontweight='bold',color='white',transform=ax.transAxes)
ax.annotate('',xy=(0.50,0.55),xytext=(0.50,0.35),arrowprops=dict(arrowstyle='->',color='black',lw=2),transform=ax.transAxes)
ax.set_title('Figure 10: Proposed AI Diagnostic Engine Architecture', fontsize=15, fontweight='bold', pad=10)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig10_ai_architecture.png'), dpi=300, bbox_inches='tight'); plt.close()
print("Fig 10 done")

print("\nAll 10 figures generated!")
