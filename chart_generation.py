import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Set style for professional-looking charts
plt.style.use('default')
sns.set_palette("husl")

# Read the comprehensive dataset
df = pd.read_csv('remote_work_comprehensive_data.csv')

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

# 1. US Industries Chart
print("Generating US Industries chart...")
fig1, ax1 = plt.subplots(figsize=(12, 8))
us_data = df[df['region'] == 'US'].sort_values('value', ascending=True)
simplified_names = [industry_names.get(industry, industry) for industry in us_data['industry']]

bars1 = ax1.barh(range(len(us_data)), us_data['value'], color='#2E86AB', alpha=0.8)
ax1.set_yticks(range(len(us_data)))
ax1.set_yticklabels(simplified_names, fontsize=14)
ax1.set_xlabel('Percentage Points Increase', fontsize=16)
plt.suptitle('US Industries: Remote Work Growth (2019-2022)', fontweight='bold', fontsize=20, y=0.95)
ax1.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(us_data['value']):
    ax1.text(v - 0.5, i, f'{v:.1f}pp', va='center', ha='right', fontsize=14, fontweight='bold', color='white')

plt.subplots_adjust(top=0.96)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("us_industries_chart.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Global Industries Chart
print("Generating Global Industries chart...")
fig2, ax2 = plt.subplots(figsize=(12, 8))
global_data = df[df['region'] == 'Global'].sort_values('value', ascending=True)
bars2 = ax2.barh(range(len(global_data)), global_data['value'], color='#F4A261', alpha=0.8)
ax2.set_yticks(range(len(global_data)))
ax2.set_yticklabels(global_data['industry'], fontsize=14)
ax2.set_xlabel('Growth Rate (%)', fontsize=16)
plt.suptitle('Global Industries: Notable Industries for Remote Job Growth (2024-2025)', fontweight='bold', fontsize=20, y=0.95)
ax2.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(global_data['value']):
    ax2.text(v - 1, i, f'{v:.1f}%', va='center', ha='right', fontsize=14, fontweight='bold', color='white')

plt.subplots_adjust(top=0.96)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("global_industries_chart.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Top Growth Sectors Summary Chart
print("Generating Top Growth Sectors summary chart...")
fig3, ax3 = plt.subplots(figsize=(16, 10))

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

bars3 = ax3.barh(range(len(summary_df)), summary_df['value'], color=colors_summary, height=0.7, alpha=0.8)
ax3.set_yticks(range(len(summary_df)))
ax3.set_yticklabels(summary_df['sector'], fontsize=14)
ax3.set_xlabel('Growth Rate (% or pp)', fontsize=16)
plt.suptitle('Top Remote Work Growth Sectors Worldwide', fontweight='bold', fontsize=22, y=0.95)
ax3.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(summary_df['value']):
    ax3.text(v - 1, i, f'{v:.1f}', va='center', ha='right', fontsize=13, fontweight='bold', color='white')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=category) for category, color in category_colors.items()]
ax3.legend(handles=legend_elements, loc='lower right', fontsize=14, frameon=True, fancybox=True, shadow=True)

plt.subplots_adjust(top=0.96)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("top_growth_sectors_chart.png", dpi=300, bbox_inches='tight')
plt.close()

# 4. World Map
print("Generating World Map...")
fig4, ax4 = plt.subplots(figsize=(16, 10), subplot_kw={'projection': ccrs.PlateCarree()})

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

# Set global extent
ax4.set_global()

# Plot circles for each country with data
for i, country_data in enumerate(all_countries_data):
    country = country_data['country']
    if country in country_coords:
        lon, lat = country_coords[country]
        value = country_data['value']
        unit = country_data['unit']
        
        # Size based on value (scaled appropriately) - larger circles for higher values
        if unit == 'pp':
            size = max(300, min(3000, value * 40))
        else:  # percentage
            size = max(300, min(3000, value * 35))
        
        # Color based on type
        if country_data['type'] == 'Regional Growth':
            color = '#A23B72'
        elif country_data['type'] == 'Industry Average':
            color = '#2E86AB'
        else:  # Policy Survey
            color = '#F18F01'
        
        # Plot the circle
        circle = ax4.scatter(lon, lat, s=size, c=color, alpha=0.8, edgecolors='black', 
                           linewidth=2, zorder=5, transform=ccrs.PlateCarree())
        
        # Add country label - larger text for better readability
        if value > 50:  # Large values
            fontsize = 16
            offset = -15
        else:
            fontsize = 14
            offset = -12
            
        ax4.text(lon, lat + offset, f"{country}\n{value:.1f}{unit}", ha='center', va='top', 
                fontsize=fontsize, fontweight='bold', transform=ccrs.PlateCarree(),
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.95, edgecolor='black', linewidth=2))

plt.suptitle('Global Remote Work Growth\n(2023-2024)', fontweight='bold', fontsize=22, y=0.95)

# Add a legend with larger text
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#A23B72', markersize=15, label='Regional Growth (pp)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E86AB', markersize=15, label='US Industry Avg (pp)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F18F01', markersize=15, label='Asia Policy Survey (%)')
]
ax4.legend(handles=legend_elements, loc='lower left', fontsize=16, frameon=True, fancybox=True, framealpha=0.9)

plt.subplots_adjust(top=0.97)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("world_map_chart.png", dpi=300, bbox_inches='tight')
plt.close()

print("All four charts generated successfully!")
print("Generated files:")
print("- us_industries_chart.png")
print("- global_industries_chart.png") 
print("- top_growth_sectors_chart.png")
print("- world_map_chart.png")
