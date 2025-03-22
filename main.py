import streamlit as st
import pandas as pd
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="📁 File Converter & Cleaner", layout="wide")

# Title and description
st.title("📁 File Converter & Cleaner")
st.write("Upload your CSV and Excel files to clean data and convert formats effortlessly 🚀")

# File uploader
files = st.file_uploader("Upload your CSV and Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]  # Get file extension
        
        # Read file based on extension
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        
        st.subheader(f"🔎 {file.name} - Preview")
        st.dataframe(df.head())  # Show preview of the data
        
        # Data cleaning - Fill missing values
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled successfully!")
            st.dataframe(df.head())  # Show updated dataframe

        # Column selection
        selected_columns = st.multiselect(f"Select columns to keep - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())  # Show updated dataframe
        
        # Data visualization
        if st.checkbox(f"📊 Show chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])  # Show bar chart for first 2 numerical columns
        
        # Conversion options
        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇ Download {file.name} as {format_choice}"):
            output = BytesIO()
            
            if format_choice == "CSV":
                df.to_csv(output, index=False, encoding="utf-8")
                mime = "text/csv"
                new_name = file.name.replace(f".{ext}", ".csv")
            else:
                df.to_excel(output, index=False, engine='xlsxwriter')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(f".{ext}", ".xlsx")
            
            output.seek(0)
            st.download_button("⬇ Download File", file_name=new_name, data=output, mime=mime)

st.success("✅ Processing completed!")
