import streamlit as st
import pandas as pd

st.set_page_config(page_title="Export Dashboard", layout="wide")
st.title("📦 Unified Export Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload Combined CSV Export Data", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Cleaning ---
    df.columns = df.columns.str.strip()
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df['PRODUCT'] = df['PRODUCT'].astype(str).str.strip()
    df['QUANTITY'] = pd.to_numeric(df['QUANTITY'], errors='coerce')
    df['UNIT RATE'] = pd.to_numeric(df['UNIT RATE'], errors='coerce')
    df['TOTAL USD'] = pd.to_numeric(df['TOTAL USD'], errors='coerce')

    df = df.dropna(subset=['PRODUCT'])

    # --- Product Search ---
    st.sidebar.header("🔍 Filters")
    product_search = st.sidebar.text_input("Search Product Name (partial match)", "")

    filtered_df = df[df["PRODUCT"].str.contains(product_search, case=False, na=False)]

    # --- Sidebar Filters ---
    countries = filtered_df["DESTINATION"].dropna().unique()
    selected_countries = st.sidebar.multiselect("Destination Country", countries, default=countries)

    exporters = filtered_df["EXPORTER"].dropna().unique()
    selected_exporters = st.sidebar.multiselect("Exporter", exporters, default=exporters)

    importers = filtered_df["IMPORTER"].dropna().unique()
    selected_importers = st.sidebar.multiselect("Importer", importers, default=importers)

    # Date Range
    min_date = filtered_df["DATE"].min()
    max_date = filtered_df["DATE"].max()
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

    # --- Apply Filters ---
    filtered_df = filtered_df[
        filtered_df["DESTINATION"].isin(selected_countries) &
        filtered_df["EXPORTER"].isin(selected_exporters) &
        filtered_df["IMPORTER"].isin(selected_importers)
    ]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            filtered_df["DATE"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
        ]

    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Quantity", f"{filtered_df['QUANTITY'].sum():,.2f}")
    with col2:
        st.metric("Total Revenue (USD)", f"${filtered_df['TOTAL USD'].sum():,.2f}")
    with col3:
        st.metric("Avg. Unit Rate", f"${filtered_df['UNIT RATE'].mean():,.2f}")

    # --- View and Download ---
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data", csv, "filtered_export_data.csv", "text/csv")

else:
    st.info("Please upload the combined export CSV file to begin.")
