import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for professional-looking charts
plt.style.use('default')
sns.set_palette("husl")

# Read the comprehensive dataset
df = pd.read_csv('remote_work_comprehensive_data.csv')

# Create a figure with subplots - larger size for better spacing
fig = plt.figure(figsize=(24, 16))

# Use GridSpec for better control over subplot positioning - 2x2 grid
from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1], width_ratios=[1, 1])

# 1. US Industries - Top Remote Work Growth (2019-2022) - Top Left
ax1 = fig.add_subplot(gs[0, 0])
us_data = df[df['region'] == 'US'].sort_values('value', ascending=True)

# Simplify industry names for better readability
industry_names = {
    'Tech & IT': 'Tech & IT',
    'Publishing': 'Publishing',
    'Data Processing': 'Data Processing',
    'Insurance Carriers': 'Insurance',
    'Securities & Futures': 'Securities',
    'Funds & Trusts': 'Financial Funds',
    'Management Companies': 'Management',
    'Federal Reserve Banks': 'Banking',
    'Broadcasting & Telecom': 'Telecom',
    'Professional Services': 'Prof. Services'
}

simplified_names = [industry_names.get(industry, industry) for industry in us_data['industry']]

bars1 = ax1.barh(range(len(us_data)), us_data['value'], color='#2E86AB')
ax1.set_yticks(range(len(us_data)))
ax1.set_yticklabels(simplified_names, fontsize=12)
ax1.set_xlabel('Percentage Points Increase', fontsize=12)
ax1.set_title('US Industries: Remote Work Growth\n(2019-2022)', fontweight='bold', fontsize=14)
ax1.grid(axis='x', alpha=0.3)

# Add value labels on bars close to end, avoiding borders
for i, v in enumerate(us_data['value']):
    ax1.text(v - 0.5, i, f'{v:.1f}pp', va='center', ha='right', fontsize=12, fontweight='bold')

# 2. Global Industries - Remote Job Growth (2024-2025) - Top Right
ax2 = fig.add_subplot(gs[0, 1])
global_data = df[df['region'] == 'Global'].sort_values('value', ascending=True)
bars2 = ax2.barh(range(len(global_data)), global_data['value'], color='#F4A261')
ax2.set_yticks(range(len(global_data)))
ax2.set_yticklabels(global_data['industry'], fontsize=12)
ax2.set_xlabel('Growth Rate (%)', fontsize=12)
ax2.set_title('Global Industries: Remote Job Growth\n(2024-2025)', fontweight='bold', fontsize=14)
ax2.grid(axis='x', alpha=0.3)

# Add value labels on bars close to end, avoiding borders
for i, v in enumerate(global_data['value']):
    ax2.text(v - 1, i, f'{v:.1f}%', va='center', ha='right', fontsize=12, fontweight='bold')

# 3. Summary Chart - Top Growth Sectors - Bottom Left
ax3 = fig.add_subplot(gs[1, 0])
# Combine top performers from different categories
top_sectors = []

# Top 5 US industries with simplified names
us_top = df[df['region'] == 'US'].nlargest(5, 'value')
for _, row in us_top.iterrows():
    simplified_name = industry_names.get(row['industry'], row['industry'])
    top_sectors.append({'sector': f"{simplified_name} (US)", 'value': row['value'], 'category': 'US Industries'})

# Global industries
global_top = df[df['region'] == 'Global']
for _, row in global_top.iterrows():
    top_sectors.append({'sector': f"{row['industry']} (Global)", 'value': row['value'], 'category': 'Global Growth'})

# All regional/country data (All Industries)
regional_all = df[df['industry'] == 'All Industries'].copy()
for _, row in regional_all.iterrows():
    if row['country'] not in ['Global']:
        # Determine category based on region
        if row['region'] == 'Asia':
            category = 'Asia Policy'
        else:
            category = 'Regional'
        top_sectors.append({'sector': f"All Industries ({row['country']})", 'value': row['value'], 'category': category})

summary_df = pd.DataFrame(top_sectors)
summary_df = summary_df.sort_values('value', ascending=True)

# Create color map for categories
category_colors = {'US Industries': '#2E86AB', 'Global Growth': '#F4A261', 'Regional': '#A23B72', 'Asia Policy': '#C73E1D'}
colors_summary = [category_colors[cat] for cat in summary_df['category']]

bars3 = ax3.barh(range(len(summary_df)), summary_df['value'], color=colors_summary, height=0.7)
ax3.set_yticks(range(len(summary_df)))
ax3.set_yticklabels(summary_df['sector'], fontsize=15)
ax3.set_xlabel('Growth Rate (% or pp)', fontsize=15)
ax3.set_title('Top Remote Work Growth Sectors Worldwide', fontweight='bold', fontsize=18, pad=20)
ax3.grid(axis='x', alpha=0.3)

# Add value labels on bars close to end, avoiding borders
for i, v in enumerate(summary_df['value']):
    ax3.text(v - 1, i, f'{v:.1f}', va='center', ha='right', fontsize=13, fontweight='bold')

# Add legend for summary chart with better spacing
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=category) for category, color in category_colors.items()]
ax3.legend(handles=legend_elements, loc='lower right', fontsize=13, frameon=True, fancybox=True, shadow=True)

# 4. World Map - Regional Remote Work Growth - Bottom Right
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ax4 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree())

# Get all countries with remote work data from our dataset
all_countries_data = []

# Regional data (All Industries) - get ALL countries with All Industries data
regional_data = df[df['industry'] == 'All Industries'].copy()
for _, row in regional_data.iterrows():
    if row['country'] not in ['Global']:
        # Skip individual EU countries, use EU as whole
        if row['country'] in ['Sweden', 'Ireland']:
            continue
            
        # Determine the type based on region
        if row['region'] == 'Asia':
            data_type = 'Policy Survey'
            unit = '%'
        else:
            data_type = 'Regional Growth'
            unit = 'pp'
            
        all_countries_data.append({
            'country': row['country'],
            'value': row['value'],
            'type': data_type,
            'unit': unit
        })

# US data (take average of top industries)
us_avg = df[df['region'] == 'US']['value'].mean()
all_countries_data.append({
    'country': 'United States',
    'value': us_avg,
    'type': 'Industry Average',
    'unit': 'pp'
})

# Asia data is now handled above in the All Industries section

# Define coordinates for all countries
country_coords = {
    'Colombia': (-74.0, 4.6),
    'European Union': (10.0, 54.0),  # Central Europe
    'Argentina': (-64.0, -34.0),
    'United States': (-98.0, 39.5),
    'Singapore': (103.8, 1.3),
    'Japan': (138.2, 36.2),
    'China': (104.2, 35.9)
}

# Add map features
ax4.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax4.add_feature(cfeature.BORDERS, linewidth=0.3)
ax4.add_feature(cfeature.LAND, color='lightgray', alpha=0.5)
ax4.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
ax4.add_feature(cfeature.LAKES, color='lightblue', alpha=0.3)

# Set global extent with tighter bounds to fill more space
ax4.set_global()
ax4.set_aspect('auto')  # Allow map to fill available space better

# Plot circles for each country with data
for i, country_data in enumerate(all_countries_data):
    country = country_data['country']
    if country in country_coords:
        lon, lat = country_coords[country]
        value = country_data['value']
        unit = country_data['unit']
        
        # Size based on value (scaled appropriately) - larger circles for higher values
        if unit == 'pp':
            size = max(200, min(2000, value * 30))
        else:  # percentage
            size = max(200, min(2000, value * 25))
        
        # Color based on type
        if country_data['type'] == 'Regional Growth':
            color = '#A23B72'
        elif country_data['type'] == 'Industry Average':
            color = '#2E86AB'
        else:  # Policy Survey
            color = '#F18F01'
        
        # Plot the circle
        circle = ax4.scatter(lon, lat, s=size, c=color, alpha=0.8, edgecolors='black', 
                           linewidth=1.5, zorder=5, transform=ccrs.PlateCarree())
        
        # Add country label - larger text for better readability
        if value > 50:  # Large values
            fontsize = 12
            offset = -12
        else:
            fontsize = 11
            offset = -10
            
        ax4.text(lon, lat + offset, f"{country}\n{value:.1f}{unit}", ha='center', va='top', 
                fontsize=fontsize, fontweight='bold', transform=ccrs.PlateCarree(),
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.95, edgecolor='black', linewidth=1.5))

ax4.set_title('Global Remote Work Growth\n(Various Metrics & Time Periods)', fontweight='bold', fontsize=14)

# Add a simple legend with larger text
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#A23B72', markersize=12, label='Regional Growth (pp)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E86AB', markersize=12, label='US Industry Avg (pp)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F18F01', markersize=12, label='Asia Policy Survey (%)')
]
ax4.legend(handles=legend_elements, loc='lower left', fontsize=12, frameon=True, fancybox=True, framealpha=0.9)

# Overall title with more space
fig.suptitle('Remote Work Industry Migration: Global Trends & Sector Analysis', 
             fontsize=24, fontweight='bold', y=0.95)

# Add subtitle with more space
fig.text(0.5, 0.91, 'Which sectors are going remote and regional differences in remote work adoption', 
         ha='center', fontsize=17, style='italic')

plt.tight_layout()
gs.update(top=0.87, hspace=0.3, wspace=0.25, bottom=0.08, left=0.08, right=0.95)

# Save the comprehensive visualization
plt.savefig("remote_work_clean_analysis.png", dpi=300, bbox_inches='tight')
print("Clean remote work analysis saved as 'remote_work_clean_analysis.png'")

plt.show()