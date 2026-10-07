# NOVA — Sales & Revenue Analysis Dashboard

An interactive sales intelligence dashboard developed for Thiranex Task 1.

## Overview

NOVA is a business analytics dashboard that helps users explore sales performance, analyze revenue trends, compare product performance, and understand regional sales.

## Features

- Interactive sales overview and KPI cards
- Total revenue, orders, units sold, and average order value
- Monthly revenue trend visualization
- Product and category analysis
- Regional revenue comparison
- Date, region, category, and product filters
- CSV and Excel file upload
- Sales transaction table
- Download filtered sales reports as CSV

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Openpyxl

## Project Structure

```text
Sales-Revenue-Dashboard/
├── app.py
├── sales_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Usage

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd thiranex-sales-revenue-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Dataset

The included sample dataset contains order IDs, dates, products, categories, regions, quantities, and unit prices.

Revenue is calculated as:

`Revenue = Quantity × Unit Price`

Users can upload their own CSV or Excel dataset with the required column names.

## Project Details

- Project: Sales & Revenue Analysis Dashboard
- Platform: Thiranex
- Task: Task 1
- Developer: K. Udaykumar


---

Built with Python and Streamlit.