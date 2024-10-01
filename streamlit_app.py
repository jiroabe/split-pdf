import streamlit as st
import PyPDF2
import io

def split_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    
    for page in range(num_pages):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page])
        
        output = io.BytesIO()
        pdf_writer.write(output)
        st.download_button(
            label=f"Download page {page + 1}",
            data=output.getvalue(),
            file_name=f"page_{page + 1}.pdf",
            mime="application/pdf"
        )
    
    return num_pages

st.title("PDF Splitter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    num_pages = split_pdf(uploaded_file)
    st.write(f"Total number of pages: {num_pages}")
