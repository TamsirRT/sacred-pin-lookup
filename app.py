import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import StringIO

# ---- Supabase connection ----
url = "https://kvivmdijijlvtnskcrry.supabase.co"
key = "sb_secret_ORLlBtQggl4_yqB_32H45A_ZVnGnDQG"
supabase: Client = create_client(url, key)

# ---- Load data ----
@st.cache_data
def load_data():
    columns = """
    pin,
    first_name,
    last_name,
    grade_level,
    home_room
    """
    response = supabase.table("students").select(columns).execute()
    return pd.DataFrame(response.data)

st.title("🔍 MealMode Luncher PIN Lookup")

df = load_data()

# ---- Sidebar filters ----
st.sidebar.header("Filters")
search = st.sidebar.text_input("Search text")

# Filter by text search (checks all columns)
if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# Optionally add column filters (multi-select example)
for col in df.select_dtypes(include="object").columns:
    options = st.sidebar.multiselect(f"Filter by {col}", sorted(df[col].dropna().unique()))
    if options:
        df = df[df[col].isin(options)]

# ---- Display table ----
st.dataframe(df, use_container_width=True)

# ---- CSV export ----
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button(
    label="⬇️ Download CSV",
    data=csv_buffer.getvalue(),
    file_name="export.csv",
    mime="text/csv"
)
