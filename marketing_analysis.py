"""
Marketing Analytics Dashboard
===============================
MBA Project | Marketing + Finance Dual Specialization
Author: [Your Name]
Description: End-to-end marketing analytics using RFM segmentation,
             sales trend analysis, and product performance insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# STYLE CONFIGURATION
# ─────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.facecolor': '#F8F9FA',
    'axes.facecolor': '#F8F9FA',
})

COLORS = {
    'primary': '#2563EB',
    'secondary': '#7C3AED',
    'accent': '#059669',
    'warning': '#D97706',
    'danger': '#DC2626',
    'light': '#E5E7EB',
    'dark': '#1F2937',
}

SEGMENT_COLORS = {
    'Champions':        '#059669',
    'Loyal Customers':  '#2563EB',
    'Potential':        '#7C3AED',
    'At Risk':          '#D97706',
    'Lost Customers':   '#DC2626',
}

# ─────────────────────────────────────────
# 1. GENERATE REALISTIC SYNTHETIC DATASET
# ─────────────────────────────────────────
np.random.seed(42)

def generate_ecommerce_data(n=2000):
    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2024, 6, 30)
    date_range = (end_date - start_date).days

    categories = {
        'Electronics':   {'avg_price': 350, 'std': 150, 'weight': 0.25},
        'Clothing':      {'avg_price': 75,  'std': 30,  'weight': 0.30},
        'Home & Garden': {'avg_price': 120, 'std': 50,  'weight': 0.20},
        'Sports':        {'avg_price': 95,  'std': 40,  'weight': 0.15},
        'Beauty':        {'avg_price': 55,  'std': 20,  'weight': 0.10},
    }

    channels = ['Organic Search', 'Paid Ads', 'Email Campaign', 'Social Media', 'Direct']
    cat_names    = list(categories.keys())
    cat_weights  = [categories[c]['weight'] for c in cat_names]

    customer_ids = [f'C{str(i).zfill(4)}' for i in range(1, 501)]
    customer_loyalty = {cid: np.random.choice(['low','medium','high'], p=[0.4,0.4,0.2])
                        for cid in customer_ids}

    records = []
    for _ in range(n):
        cid      = np.random.choice(customer_ids)
        loyalty  = customer_loyalty[cid]
        freq_map = {'low': 1, 'medium': 3, 'high': 8}
        cat      = np.random.choice(cat_names, p=cat_weights)
        info     = categories[cat]

        base_price = info['avg_price']
        price      = max(5, np.random.normal(base_price, info['std']))

        # Seasonal boost (Q4 + summer)
        rand_days = np.random.randint(0, date_range)
        order_date = start_date + timedelta(days=rand_days)
        month = order_date.month
        seasonal = 1.3 if month in [11, 12] else (1.1 if month in [6, 7, 8] else 1.0)
        price *= seasonal

        qty     = np.random.randint(1, freq_map[loyalty] + 2)
        channel = np.random.choice(channels, p=[0.30, 0.25, 0.20, 0.15, 0.10])

        records.append({
            'CustomerID':  cid,
            'OrderDate':   order_date,
            'Category':    cat,
            'Quantity':    qty,
            'UnitPrice':   round(price, 2),
            'Revenue':     round(price * qty, 2),
            'Channel':     channel,
            'Loyalty':     loyalty,
        })

    df = pd.DataFrame(records).sort_values('OrderDate').reset_index(drop=True)
    df['OrderID'] = [f'ORD{str(i).zfill(5)}' for i in range(1, len(df)+1)]
    return df

print("📦 Generating e-commerce dataset...")
df = generate_ecommerce_data(2000)
df.to_csv('/home/claude/marketing-analytics/data/ecommerce_data.csv', index=False)
print(f"   ✅ {len(df)} transactions | {df['CustomerID'].nunique()} customers\n")


# ─────────────────────────────────────────
# 2. RFM ANALYSIS & CUSTOMER SEGMENTATION
# ─────────────────────────────────────────
print("📊 Running RFM Analysis...")

snapshot_date = df['OrderDate'].max() + timedelta(days=1)

rfm = df.groupby('CustomerID').agg(
    Recency   = ('OrderDate',  lambda x: (snapshot_date - x.max()).days),
    Frequency = ('OrderID',    'count'),
    Monetary  = ('Revenue',    'sum'),
).reset_index()

# Score 1–4 (higher = better)
rfm['R_Score'] = pd.qcut(rfm['Recency'],   q=4, labels=[4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1,2,3,4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'],  q=4, labels=[1,2,3,4]).astype(int)
rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

def segment(row):
    s = row['RFM_Score']
    if s >= 10:   return 'Champions'
    elif s >= 8:  return 'Loyal Customers'
    elif s >= 6:  return 'Potential'
    elif s >= 4:  return 'At Risk'
    else:         return 'Lost Customers'

rfm['Segment'] = rfm.apply(segment, axis=1)
print(f"   ✅ Segments: {rfm['Segment'].value_counts().to_dict()}\n")


# ─────────────────────────────────────────
# 3. SALES TREND ANALYSIS
# ─────────────────────────────────────────
df['Month']   = df['OrderDate'].dt.to_period('M')
df['Quarter'] = df['OrderDate'].dt.to_period('Q')

monthly = df.groupby('Month').agg(
    Revenue = ('Revenue','sum'),
    Orders  = ('OrderID','count'),
).reset_index()
monthly['Month_dt'] = monthly['Month'].dt.to_timestamp()

cat_revenue = df.groupby('Category')['Revenue'].sum().sort_values(ascending=True)
channel_rev = df.groupby('Channel')['Revenue'].sum().sort_values(ascending=False)


# ─────────────────────────────────────────
# 4. BUILD DASHBOARD (3×2 grid)
# ─────────────────────────────────────────
print("🎨 Building dashboard...")

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor('#F0F4FF')

# Header
fig.text(0.5, 0.97, 'MARKETING ANALYTICS DASHBOARD',
         ha='center', va='top', fontsize=22, fontweight='bold', color=COLORS['dark'])
fig.text(0.5, 0.94, 'E-Commerce Customer Intelligence & Sales Performance Report — Jan 2023 to Jun 2024',
         ha='center', va='top', fontsize=11, color='#6B7280')

# ── KPI STRIP ──────────────────────────────────────────────────────────────
ax_kpi = fig.add_axes([0.03, 0.87, 0.94, 0.05])
ax_kpi.set_xlim(0, 4); ax_kpi.set_ylim(0, 1); ax_kpi.axis('off')

kpis = [
    ('Total Revenue', f"₹{df['Revenue'].sum()/1e5:.1f}L"),
    ('Total Orders',  f"{len(df):,}"),
    ('Unique Customers', f"{df['CustomerID'].nunique()}"),
    ('Avg Order Value',  f"₹{df['Revenue'].mean():.0f}"),
]
for i, (label, val) in enumerate(kpis):
    x = i + 0.5
    ax_kpi.add_patch(mpatches.FancyBboxPatch((i+0.05, 0.05), 0.88, 0.88,
        boxstyle='round,pad=0.02', fc='white', ec=COLORS['primary'], lw=1.5))
    ax_kpi.text(x, 0.70, val,   ha='center', va='center', fontsize=16, fontweight='bold', color=COLORS['primary'])
    ax_kpi.text(x, 0.25, label, ha='center', va='center', fontsize=9,  color='#6B7280')

# ── CHART AREA ─────────────────────────────────────────────────────────────
axes_positions = [
    [0.03, 0.49, 0.44, 0.34],   # top-left:  monthly trend
    [0.53, 0.49, 0.44, 0.34],   # top-right: RFM segments
    [0.03, 0.08, 0.27, 0.34],   # bot-left:  category revenue
    [0.36, 0.08, 0.27, 0.34],   # bot-mid:   channel mix
    [0.67, 0.08, 0.30, 0.34],   # bot-right: RFM scatter
]

# 1. Monthly Revenue Trend
ax1 = fig.add_axes(axes_positions[0])
ax1.set_facecolor('#F8F9FA')
ax1.fill_between(monthly['Month_dt'], monthly['Revenue'], alpha=0.15, color=COLORS['primary'])
ax1.plot(monthly['Month_dt'], monthly['Revenue'], color=COLORS['primary'], lw=2.5, marker='o', ms=5)
ax1.set_title('Monthly Revenue Trend', pad=10)
ax1.set_ylabel('Revenue (₹)', color='#6B7280', fontsize=9)
ax1.tick_params(axis='x', rotation=30, labelsize=8)
ax1.tick_params(axis='y', labelsize=8)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))

# 2. Customer Segments (donut)
ax2 = fig.add_axes(axes_positions[1])
ax2.set_facecolor('#F8F9FA')
seg_counts = rfm['Segment'].value_counts()
seg_colors = [SEGMENT_COLORS[s] for s in seg_counts.index]
wedges, texts, autotexts = ax2.pie(
    seg_counts.values, labels=seg_counts.index, colors=seg_colors,
    autopct='%1.1f%%', pctdistance=0.82, startangle=90,
    wedgeprops={'width': 0.5, 'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 9}
)
for at in autotexts:
    at.set_fontsize(8); at.set_color('white'); at.set_fontweight('bold')
ax2.set_title('Customer Segmentation (RFM)', pad=10)

# 3. Category Revenue (horizontal bar)
ax3 = fig.add_axes(axes_positions[2])
ax3.set_facecolor('#F8F9FA')
bars = ax3.barh(cat_revenue.index, cat_revenue.values,
                color=[COLORS['primary'], COLORS['secondary'], COLORS['accent'],
                       COLORS['warning'], COLORS['danger']], height=0.6)
ax3.set_title('Revenue by Category', pad=10)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
ax3.tick_params(labelsize=8)
for bar, val in zip(bars, cat_revenue.values):
    ax3.text(val + 500, bar.get_y() + bar.get_height()/2,
             f'₹{val/1000:.0f}K', va='center', fontsize=7, color=COLORS['dark'])

# 4. Channel Mix (bar)
ax4 = fig.add_axes(axes_positions[3])
ax4.set_facecolor('#F8F9FA')
ch_colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning'], COLORS['danger']]
ax4.bar(range(len(channel_rev)), channel_rev.values, color=ch_colors, width=0.6)
ax4.set_xticks(range(len(channel_rev)))
ax4.set_xticklabels([c.replace(' ', '\n') for c in channel_rev.index], fontsize=7)
ax4.set_title('Revenue by Channel', pad=10)
ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
ax4.tick_params(axis='y', labelsize=8)

# 5. RFM Scatter (Recency vs Monetary, colored by segment)
ax5 = fig.add_axes(axes_positions[4])
ax5.set_facecolor('#F8F9FA')
for seg, grp in rfm.groupby('Segment'):
    ax5.scatter(grp['Recency'], grp['Monetary'],
                color=SEGMENT_COLORS[seg], alpha=0.5, s=20, label=seg)
ax5.set_title('RFM: Recency vs Spend', pad=10)
ax5.set_xlabel('Recency (days)', fontsize=8, color='#6B7280')
ax5.set_ylabel('Total Spend (₹)', fontsize=8, color='#6B7280')
ax5.tick_params(labelsize=7)
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
legend_patches = [mpatches.Patch(color=SEGMENT_COLORS[s], label=s) for s in SEGMENT_COLORS]
ax5.legend(handles=legend_patches, fontsize=6, loc='upper right', framealpha=0.7)

# Footer
fig.text(0.5, 0.02, 'MBA Marketing Analytics Project  •  Data: Synthetic E-Commerce Dataset  •  Tools: Python, Pandas, Matplotlib',
         ha='center', fontsize=8, color='#9CA3AF')

plt.savefig('/home/claude/marketing-analytics/outputs/marketing_dashboard.png',
            dpi=150, bbox_inches='tight', facecolor='#F0F4FF')
print("   ✅ Dashboard saved!\n")


# ─────────────────────────────────────────
# 5. BUSINESS INSIGHTS SUMMARY
# ─────────────────────────────────────────
print("=" * 55)
print("       📈 KEY BUSINESS INSIGHTS")
print("=" * 55)

total_rev  = df['Revenue'].sum()
top_cat    = cat_revenue.idxmax()
top_ch     = channel_rev.idxmax()
champions  = rfm[rfm['Segment'] == 'Champions']
at_risk    = rfm[rfm['Segment'] == 'At Risk']

print(f"\n💰 Total Revenue:          ₹{total_rev:,.0f}")
print(f"📦 Total Orders:           {len(df):,}")
print(f"👥 Unique Customers:       {df['CustomerID'].nunique()}")
print(f"🛒 Avg Order Value:        ₹{df['Revenue'].mean():.2f}")
print(f"\n🏆 Top Category:           {top_cat} (₹{cat_revenue[top_cat]:,.0f})")
print(f"📣 Best Channel:           {top_ch} (₹{channel_rev[top_ch]:,.0f})")
print(f"\n🥇 Champions ({len(champions)} customers): Avg Spend ₹{champions['Monetary'].mean():,.0f}")
print(f"⚠️  At-Risk ({len(at_risk)} customers):   Avg Spend ₹{at_risk['Monetary'].mean():,.0f}")
print(f"\n📌 RECOMMENDATION: Re-engage {len(at_risk)} at-risk customers")
print(f"   through targeted email campaigns — they represent")
print(f"   ~₹{at_risk['Monetary'].sum():,.0f} in recoverable revenue.")
print("\n" + "=" * 55)
print("\n✅ All outputs saved to /outputs/")
