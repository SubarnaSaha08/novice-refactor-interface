import streamlit as st
from state.session import reset_session
import os
import zipfile
from io import BytesIO


def zip_folder(folder_path):
    """Create a zip file in memory from a folder."""
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the relative path to maintain folder structure
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                zf.write(file_path, arcname=arcname)
    memory_file.seek(0)
    return memory_file

def show_admin_options():
    st.header("Hello Admin!")
    st.markdown("---")

    # Define the folder path
    folder_path = "responses"

    # Check if the folder exists
    if not os.path.exists(folder_path):
        st.error("The 'responses' folder does not exist in the app's root directory.")
        return

    # Create a button to trigger the download
    if st.button("Download Responses Folder"):
        try:
            # Generate the zip file in memory
            zip_file = zip_folder(folder_path)
            
            # Provide the zip file for download via st.download_button
            st.download_button(
                label="Download responses.zip",
                data=zip_file,
                file_name="responses.zip",
                mime="application/zip",
                key="download_zip"
            )
            st.success("Zip file created! Click the download button above to save it.")
        except Exception as e:
            st.error(f"An error occurred while creating the zip file: {str(e)}")
 
    if st.button("🔁 Logout"):
        reset_session()
        st.rerun()

def reset_session() -> None:
    # Copy keys to a list so we can delete safely while iterating
    for key in list(st.session_state.keys()):
        # Delete only the keys you actually want to clear
        del st.session_state[key]
