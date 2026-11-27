import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(8.5, 7.0), dpi=300)
ax.set_xlim(-3.6, 3.6)
ax.set_ylim(-3.6, 3.6)
ax.axis('off')

# Four overlapping circular patches
# Theme 1: Top (AI Computing Workloads) - Deep Blue
# Theme 2: Right (Data Center Infrastructure) - Emerald Green
# Theme 3: Bottom (India's Electricity Grid) - Warm Amber
# Theme 4: Left (Renewable Energy Integration) - Royal Purple

c1 = patches.Circle((0, 1.1), radius=1.65, facecolor='#3182CE', edgecolor='#1A365D', alpha=0.35, lw=2.5)
c2 = patches.Circle((1.15, 0), radius=1.65, facecolor='#38A169', edgecolor='#1C4532', alpha=0.35, lw=2.5)
c3 = patches.Circle((0, -1.1), radius=1.65, facecolor='#DD6B20', edgecolor='#7B341E', alpha=0.35, lw=2.5)
c4 = patches.Circle((-1.15, 0), radius=1.65, facecolor='#805AD5', edgecolor='#322659', alpha=0.35, lw=2.5)

ax.add_patch(c1)
ax.add_patch(c2)
ax.add_patch(c3)
ax.add_patch(c4)

# Labels for each theme
ax.text(0, 2.4, 'AI Computing\nWorkloads', ha='center', va='center', fontsize=12, fontweight='bold', color='#1A365D',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#EBF8FF', edgecolor='#3182CE', lw=1.5))

ax.text(2.45, 0, 'Data Center\nInfrastructure', ha='center', va='center', fontsize=12, fontweight='bold', color='#1C4532',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#F0FFF4', edgecolor='#38A169', lw=1.5))

ax.text(0, -2.4, "India's Electricity\nGrid Infrastructure", ha='center', va='center', fontsize=12, fontweight='bold', color='#7B341E',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFFAF0', edgecolor='#DD6B20', lw=1.5))

ax.text(-2.45, 0, 'Renewable Energy\nMatching and Integration', ha='center', va='center', fontsize=12, fontweight='bold', color='#322659',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FAF5FF', edgecolor='#805AD5', lw=1.5))

# Central Intersection Box (Highlighting the Gap)
target_box = patches.FancyBboxPatch((-1.35, -0.75), 2.7, 1.5, boxstyle='round,pad=0.2', 
                                    facecolor='#FEFCBF', edgecolor='#B7791F', lw=2.5, zorder=10)
ax.add_patch(target_box)

ax.text(0, 0.35, 'CORE DISSERTATION TARGET', ha='center', va='center', fontsize=11, fontweight='bold', color='#975A16', zorder=11)
ax.text(0, -0.05, 'Assessing Grid and RE Sustainability\nof India\'s AI Data Center Expansion', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#744210', zorder=11)
ax.text(0, -0.42, '(Only 33 Papers | Verified Academic Literature Void)', ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#975A16', zorder=11)

plt.title('Four-Theme Conceptual Intersection & Literature Gap Framework', fontsize=13.5, fontweight='bold', pad=15, color='#1A202C')
plt.tight_layout()
out_dir = r'c:\Users\rajch\Desktop\SEM 7\Dissertation\Data\BIBLIO\bibliometric_gap_analysis_files'
os.makedirs(out_dir, exist_ok=True)
out_img = os.path.join(out_dir, 'four_themes_intersection.png')
plt.savefig(out_img, dpi=300, bbox_inches='tight')
plt.close()
print('Successfully saved four_themes_intersection.png to:', out_img)
