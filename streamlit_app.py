import streamlit as st
import io
import zipfile
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_employee_code(pdf_page):
    crop_box = (68, 0, 460, 27)  # 確認済みの座標
    cropped_page = pdf_page.crop(crop_box)
    text = cropped_page.extract_text()
    employee_code = ''.join(filter(str.isdigit, text))[:6]
    return employee_code if len(employee_code) == 6 else "unknown"

def process_pdfs(pdf_files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        total_pages = 0
        for pdf_file in pdf_files:
            pdf_content = pdf_file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            
            for page_num, page in enumerate(pdf_reader.pages):
                # PDFページをPDFプランバーで開く
                with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                    plumber_page = pdf.pages[page_num]
                    employee_code = extract_employee_code(plumber_page)
                
                # 新しいPDFライターを作成し、現在のページを追加
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                
                # メモリ上にPDFを書き込む
                page_buffer = io.BytesIO()
                pdf_writer.write(page_buffer)
                page_buffer.seek(0)
                
                # ZIPファイルにPDFを追加
                zip_file.writestr(f"{employee_code}.pdf", page_buffer.getvalue())
                
                total_pages += 1
    
    return zip_buffer.getvalue(), total_pages

st.title("Multiple PDF Splitter with Employee Code")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    zip_content, total_pages = process_pdfs(uploaded_files)
    
    st.write(f"Total number of processed pages: {total_pages}")
    
    st.download_button(
        label="Download ZIP file with all processed PDFs",
        data=zip_content,
        file_name="processed_pdfs.zip",
        mime="application/zip"
    )
