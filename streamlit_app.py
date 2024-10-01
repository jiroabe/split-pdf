import streamlit as st
import io
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

def process_pdfs(pdf_files):
    processed_files = []
    for pdf_file in pdf_files:
        pdf_content = pdf_file.read()
        pdf_buffer = io.BytesIO(pdf_content)
        
        employee_code = extract_employee_code(pdf_buffer)
        
        # PDFWriter を使用してPDFコンテンツをコピー
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(pdf_buffer)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        output_buffer = io.BytesIO()
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        
        processed_files.append({
            "filename": f"{employee_code}.pdf",
            "content": output_buffer.getvalue()
        })
    
    return processed_files

st.title("PDF Employee Code Extractor")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    processed_files = process_pdfs(uploaded_files)
    
    st.write(f"Processed {len(processed_files)} file(s)")
    
    for file in processed_files:
        st.download_button(
            label=f"Download {file['filename']}",
            data=file['content'],
            file_name=file['filename'],
            mime="application/pdf"
        )
