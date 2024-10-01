import streamlit as st
import io
import zipfile
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

def split_pdf_to_zip(pdf_file):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        for page in range(num_pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page])
            
            page_buffer = io.BytesIO()
            pdf_writer.write(page_buffer)
            page_buffer.seek(0)
            
            zip_file.writestr(f"page_{page + 1}.pdf", page_buffer.getvalue())
    
    return zip_buffer, num_pages

st.title("PDF Splitter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    zip_buffer, num_pages = split_pdf_to_zip(uploaded_file)
    
    st.write(f"Total number of pages: {num_pages}")
    
    st.download_button(
        label="Download ZIP file with all pages",
        data=zip_buffer.getvalue(),
        file_name="split_pdf_pages.zip",
        mime="application/zip"
    )
