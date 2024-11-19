import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Stock Analysis App", layout="wide")

# Load CSV file
def load_data(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Sidebar for file upload
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    # Load and display data
    data = load_data(uploaded_file)

    if data is not None:
        st.sidebar.header("Data Filtering")

        # Select columns to display
        columns = st.sidebar.multiselect(
            "Select columns to display:", options=data.columns, default=data.columns
        )

        # Search functionality
        search_column = st.sidebar.selectbox("Column to search in:", options=data.columns)
        search_query = st.sidebar.text_input("Search query")

        # Filter data based on search
        if search_query:
            data = data[data[search_column].astype(str).str.contains(search_query, case=False)]

        # Apply column selection
        data = data[columns]

        # Display data table
        st.write("## Filtered Data Table")
        st.dataframe(data, use_container_width=True)

        # Plotting options
        st.sidebar.header("Chart Options")
        x_axis = st.sidebar.selectbox("X-Axis:", options=data.columns)
        y_axis = st.sidebar.selectbox("Y-Axis:", options=data.columns)

        chart_type = st.sidebar.radio("Select chart type:", ["Line", "Bar"])

        if x_axis and y_axis:
            st.write("## Chart")
            if chart_type == "Line":
                fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            else:
                fig = px.bar(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")

            st.plotly_chart(fig, use_container_width=True)
else:
    st.write("## Welcome to the Stock Analysis App")
    st.write("Upload a CSV file using the sidebar to get started!")
