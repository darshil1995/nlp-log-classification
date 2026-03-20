import streamlit as st
import pandas as pd
import requests
import io

# Page Config
st.set_page_config(page_title="Log Analytics Dashboard", layout="wide")

st.title("🛡️ NLP Log Classification Dashboard")
st.markdown("---")

# 1. Sidebar - Server Status
st.sidebar.header("Backend Settings")
api_url = st.sidebar.text_input("FastAPI URL", value="http://127.0.0.1:8000/classify/")

# 2. Main Interface - File Upload
uploaded_file = st.file_uploader("Upload your logs (CSV)", type="csv")

if uploaded_file:
    # Display original data
    input_df = pd.read_csv(uploaded_file)
    st.subheader("Raw Log Data")
    st.dataframe(input_df.head(10), use_container_width=True)

    # 3. Process Button
    if st.button("🚀 Process Logs via Backend"):
        with st.spinner("Server is classifying logs..."):
            try:
                # Prepare file for FastAPI
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}

                # Send request to FastAPI
                response = requests.post(api_url, files=files)

                if response.status_code == 200:
                    st.success("Classification Complete!")

                    # Read the returned CSV content
                    output_df = pd.read_csv(io.BytesIO(response.content))

                    # Display Results
                    st.subheader("Classified Results")
                    st.dataframe(output_df, use_container_width=True)

                    # 4. Download Result
                    st.download_button(
                        label="📥 Download Classified CSV",
                        data=response.content,
                        file_name="classified_logs.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Server Error: {response.text}")

            except Exception as e:
                st.error(f"Connection failed: {e}. Is your FastAPI server running?")