# datainsightx

**Automated KPI Summary & Trend Analysis Toolkit**  
Published by **Prakruthi Rao**

---

`datainsightx` is a lightweight Python package that generates business insights from transactional datasets without the need for BI tools or dashboards. It produces KPI summaries, trend analysis, and visual reports with a single function call.

---

## Features

- Automatically detects date, value, and category columns
- Computes total value, monthly average, MoM change, YoY change, and peak month
- Highlights top N performing categories
- Generates trendline and category comparison plots
- Exports:
  - Summary report (`insight_summary.txt`)
  - JSON output (`insight_kpis.json`)
  - Self-contained HTML report (`insight_report.html`)

---

## Installation

```bash
pip install datainsightx
```
