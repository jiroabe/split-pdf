import streamlit as st
import io
import zipfile
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_employee_code(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        first_page = pdf.pages[0]
        crop_box = (68, 0, 460, 27)  # 確認済みの座標
        cropped_page = first_page.crop(crop_box)
        text = cropped_page.extract_text()
        employee_code = ''.join(filter(str.isdigit, text))[:6]
        return employee_code if len(employee_code) == 6 else "unknown"

def process_pdf(pdf_file):
    pdf_content = pdf_file.read()
    pdf_buffer = io.BytesIO(pdf_content)
    
    employee_code = extract_employee_code(pdf_buffer)
    
    pdf_reader = PdfReader(pdf_buffer)
    num_pages = len(pdf_reader.pages)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for page in range(num_pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page])
            
            page_buffer = io.BytesIO()
            pdf_writer.write(page_buffer)
            page_buffer.seek(0)
            
            zip_file.writestr(f"{employee_code}.pdf", page_buffer.getvalue())
    
    return employee_code, zip_buffer.getvalue(), num_pages

st.title("PDF Splitter with Employee Code")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    employee_code, zip_content, num_pages = process_pdf(uploaded_file)
    
    st.write(f"Employee Code: {employee_code}")
    st.write(f"Total number of pages: {num_pages}")
    
    st.download_button(
        label=f"Download ZIP file for {employee_code}",
        data=zip_content,
        file_name=f"{employee_code}_split.zip",
        mime="application/zip"
    )
