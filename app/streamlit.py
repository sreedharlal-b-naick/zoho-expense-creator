import streamlit as st
import tempfile
import os
import json
from pathlib import Path
from flow import process_expense

# Configure the page
st.set_page_config(page_title="Expense Extractor", layout="wide")

# Add title and description
st.title("Expense Information Extractor")
st.markdown(
    """
Upload an image or PDF of your expense receipt or invoice, and we'll extract the key information for you.
"""
)

# Initialize session state for storing results
if "extraction_result" not in st.session_state:
    st.session_state.extraction_result = None
if "temp_file_path" not in st.session_state:
    st.session_state.temp_file_path = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "file_type" not in st.session_state:
    st.session_state.file_type = None


def process_file(file_path: str, file_type: str) -> dict:
    """Process the file using the expense flow"""
    try:
        result = process_expense(file_path, file_type)
        return result
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def display_results(result: dict):
    """Display the extraction results"""
    if not result:
        return

    # Create columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Date", result.get("date", "N/A"))
        st.metric("Amount", f"{result.get('amount', 'N/A')}")

    with col2:
        st.metric("Vendor", result.get("vendor", "N/A"))
        st.metric("Expense Type", result.get("expense_type", "N/A"))

    # Show raw data
    with st.expander("View Raw Data"):
        st.json(result)


# Create two columns for the main layout
left_col, right_col = st.columns([2, 1])

with left_col:
    # File uploader with single file restriction
    uploaded_file = st.file_uploader(
        "Choose an image or PDF file",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=False,
        key="file_uploader",
    )

    # Handle file upload
    if uploaded_file is not None:
        # Clear previous results if a new file is uploaded
        if uploaded_file != st.session_state.uploaded_file:
            st.session_state.extraction_result = None
            st.session_state.uploaded_file = uploaded_file
            st.session_state.file_type = uploaded_file.type.split("/")[-1]

            # Create a temporary file
            if st.session_state.temp_file_path:
                try:
                    Path(st.session_state.temp_file_path).unlink()
                except:
                    pass

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                st.session_state.temp_file_path = tmp_file.name

        # Add Extract button
        if st.button("Extract Information", type="primary"):
            with st.spinner("Extracting expense information..."):
                st.session_state.extraction_result = process_file(
                    st.session_state.temp_file_path, st.session_state.file_type
                )

        # Display results if available
        if st.session_state.extraction_result:
            display_results(st.session_state.extraction_result)
    else:
        # Reset session state when no file is uploaded
        st.session_state.extraction_result = None
        st.session_state.uploaded_file = None
        st.session_state.file_type = None
        if st.session_state.temp_file_path:
            try:
                Path(st.session_state.temp_file_path).unlink()
            except:
                pass
            st.session_state.temp_file_path = None

with right_col:
    # Display the uploaded file
    if st.session_state.uploaded_file is not None:
        if st.session_state.file_type in ["jpg", "jpeg", "png"]:
            st.image(
                st.session_state.uploaded_file,
                caption="Uploaded Image",
                use_container_width=True,
                output_format="JPEG",
                width=None,
                clamp=True,
            )
        else:
            st.warning(
                "PDF preview is not supported. Please use the Extract button to process the file."
            )

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Gemini API")
