import streamlit as st
import io
import zipfile
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_employee_code(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        # ここで座標を調整します。実際のPDFに合わせて調整が必要です。
        # 例: bbox=(左, 上, 右, 下)
        crop_box = (100, 100, 200, 150)  # この値は実際のPDFに合わせて調整してください
        cropped_page = first_page.crop(crop_box)
        text = cropped_page.extract_text()
        # 6桁の数字を抽出
        employee_code = ''.join(filter(str.isdigit, text))[:6]
        return employee_code if len(employee_code) == 6 else "unknown"

def split_pdf_to_zip(pdf_file):
    pdf_path = io.BytesIO(pdf_file.getvalue())
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        employee_code = extract_employee_code(pdf_path)
        
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
