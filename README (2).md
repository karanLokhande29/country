
# Unified Export Dashboard

This is a Streamlit app to visualize and filter pharmaceutical product export data.

## Features

- Upload a combined CSV file with all product export records.
- Filter by:
  - Product name (partial match)
  - Country
  - Exporter
  - Importer
  - Date range
- View key metrics (Quantity, Revenue, Avg Unit Rate)
- See country-wise revenue, monthly trend, and top importers
- Export filtered data as CSV

## To Run

1. Place your cleaned dataset as `data.csv`.
2. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
3. Launch the app:
    ```bash
    streamlit run app.py
    ```

Ensure your CSV has the following columns:
- `DATE`
- `PRODUCT`
- `QUANTITY`
- `UNIT RATE`
- `TOTAL USD`
- `DESTINATION`
- `EXPORTER`
- `IMPORTER`
