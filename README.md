Marketing Analytics Dashboard
### RFM Customer Segmentation & Sales Intelligence | MBA Marketing Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![MBA](https://img.shields.io/badge/MBA-Marketing%20%2B%20Finance-purple)

---

## Project Overview

This project applies **data-driven marketing analytics** to an e-commerce dataset, combining business strategy with Python-based analysis. It demonstrates how marketers can use customer behavior data to drive revenue decisions â€” a core skill for Marketing Analyst, FinTech, and Consulting roles.

**Business Problem:** A retail company wants to understand which customers are most valuable, which are at risk of churning, and where to focus marketing spend for maximum ROI.

---

## Key Insights Generated

| Metric | Value |
|---|---|
| Total Revenue Analyzed | 8,81,497 |
| Unique Customers | 495 |
| Average Order Value | 440.75 |
| At-Risk Revenue (Recoverable) | 54,957 |
| Top Revenue Channel | Organic Search (28.8%) |
| Best Performing Category | Electronics (59%) |

---

## Analysis Breakdown

### 1. RFM Customer Segmentation
RFM (Recency, Frequency, Monetary) is the gold standard for customer segmentation in marketing. Each customer is scored across three dimensions:

- **Recency**  How recently did they purchase?
- **Frequency** How often do they buy?
- **Monetary** How much do they spend?

| Segment | Count | Strategy |
|---|---|---|
| Champions | 133 | Reward & retain your VIPs |
| Loyal Customers | 123 | Upsell & cross-sell |
| Potential | 111 | Nurture with targeted campaigns |
| At Risk | 87 | Re-engage via email/offers |
| Lost Customers | 41 | Win-back campaigns |

### 2. Sales Trend Analysis
- Monthly revenue tracked across 18 months (Jan 2023 â€“ Jun 2024)
- Identified **Q4 seasonal uplift** (Novâ€“Dec) of ~30%
- Detected **summer peak** (Junâ€“Aug) of ~10%

### 3. Channel Performance
Evaluated 5 marketing channels by revenue contribution:
- Organic Search, Paid Ads, Email Campaigns, Social Media, Direct

### 4. Product Category Analysis
Revenue breakdown across Electronics, Clothing, Home & Garden, Sports, Beauty â€” to inform inventory and campaign budget allocation.

---

## Dashboard Preview

![Marketing Dashboard](outputs/marketing_dashboard.png)

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core analysis language |
| Pandas | Data wrangling & aggregation |
| NumPy | Numerical computations |
| Matplotlib & Seaborn | Data visualization |
| Excel / CSV | Data input/output |

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/yourusername/marketing-analytics-dashboard.git
cd marketing-analytics-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python marketing_analysis.py
```

Output files will be saved in the `/outputs/` folder.

---

## Project Structure

```
marketing-analytics-dashboard/
 marketing_analysis.py     # Main analysis script
 data/
 ecommerce_data.csv    # Generated e-commerce dataset
 outputs/
 marketing_dashboard.png  # Final dashboard
 requirements.txt
 README.md
```

---

## Business Recommendations

Based on the analysis:

1. **Re-engage At-Risk customers** (87 customers, 54,957 recoverable revenue) via personalized email campaigns with discount codes
2. **Double down on Organic Search**  highest ROI channel; invest in SEO content strategy
3. **Electronics upsell opportunity** Champions spend 5x more than average; create premium product bundles
4. **Seasonal planning** Pre-load inventory & ad spend ahead of Novâ€“Dec peak

---

## Concepts Applied

- RFM Analysis (Recency, Frequency, Monetary)
- Customer Lifetime Value (CLV) thinking
- Marketing Channel Attribution
- Cohort-based Segmentation
- Data Storytelling for Business Stakeholders

---

## Author

**[Aniket]**
MBA Marketing & Finance (Dual Specialization)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/yourusername)

---

> *"Data beats opinions. Good marketers use both."*
