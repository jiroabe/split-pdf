import streamlit as st
import pdfplumber
import io
import zipfile

def split_pdf_to_zip(pdf_file):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        with pdfplumber.open(pdf_file) as pdf:
            num_pages = len(pdf.pages)
            
            for page in range(num_pages):
                pdf_writer = io.BytesIO()
                pdf_page = pdf.pages[page]
                pdf_page.to_pdf(pdf_writer)
                
                zip_file.writestr(f"page_{page + 1}.pdf", pdf_writer.getvalue())
    
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
