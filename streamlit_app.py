import streamlit as st
import io
import zipfile
import re
from PyPDF2 import PdfReader, PdfWriter

def extract_employee_code(pdf_reader):
    for page in pdf_reader.pages:
        text = page.extract_text()
        # 6桁の数字を探す
        match = re.search(r'\b\d{6}\b', text)
        if match:
            return match.group(0)
    return "unknown"  # 従業員コードが見つからない場合

def split_pdf_to_zip(pdf_file):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        employee_code = extract_employee_code(pdf_reader)
        
        for page in range(num_pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page])
            
            page_buffer = io.BytesIO()
            pdf_writer.write(page_buffer)
            page_buffer.seek(0)
            
            zip_file.writestr(f"{employee_code}_page_{page + 1}.pdf", page_buffer.getvalue())
    
    return zip_buffer, num_pages, employee_code

st.title("PDF Splitter with Employee Code")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    zip_buffer, num_pages, employee_code = split_pdf_to_zip(uploaded_file)
    
    st.write(f"Total number of pages: {num_pages}")
    st.write(f"Extracted Employee Code: {employee_code}")
    
    st.download_button(
        label="Download ZIP file with all pages",
        data=zip_buffer.getvalue(),
        file_name=f"{employee_code}_split_pages.zip",
        mime="application/zip"
    )
