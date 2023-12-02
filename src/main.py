import streamlit as st
import requests
from io import BytesIO
import sys

from transformers import BertTokenizer, BertForSequenceClassification
from utils import download_pdf_from_url, extract_text_from_pdf, clean_text
from model import make_pred

import nltk 
nltk.download('stopwords')


# load pytorch model and tokenizer from HF spaces
# @st.cache
def get_model():
    tokenizer = BertTokenizer.from_pretrained('luci007/LightingData-Bert-Finetuned')
    model = BertForSequenceClassification.from_pretrained("luci007/LightingData-Bert-Finetuned")

    return model, tokenizer


# Main Streamlit app
def main(model, tokenizer):
    st.title("Welcome to PDF Text Classification Web-App")
    input_clean_text = ""
    # Select input option (URL or File Upload)
    input_option = st.radio("Choose Input Option:", ["PDF URL", "Upload PDF File"])
    pdf_name = "temp.pdf"  # default name

    if input_option == "PDF URL":
        url = ""
        url = st.text_input("Enter URL:")
        if url != "":
            st.success("URL properly loaded, downloading PDF, extracting and cleaning text... [estimate time ~ 10 seconds]")

            response = download_pdf_from_url(url, pdf_name)  # download pdf from url
            if response['downloaded']:
                st.text("Downloaded ✅")
            else:
                st.text("Download Issue ❌. Please re-run the code..")
                sys.exit()
            
            response_text = extract_text_from_pdf(pdf_name, response['coming_from_url'])  # extracting text from pdf
            if response_text['extracted_text']:
                st.text("Extraction ✅")
            else:
                st.text("Extraction Issue ❌. Please re-run the code..")
                sys.exit()
            
            input_clean_text_response = clean_text(response_text['text_file_path'])   # cleaning the text
            if input_clean_text_response['status']:
                st.text("Cleaning ✅")
                input_clean_text = input_clean_text_response['cleaned_text']
            else:
                st.text("Cleaning Issue ❌. Please re-run the code..")
                sys.exit()



    elif input_option == "Upload PDF File":
        pdf_name_upload = st.file_uploader("Choose a PDF file", type=["pdf"])
        if pdf_name_upload:
            st.success("PDF uploaded successfully, extracting and cleaning text... [estimate time ~ 10 seconds]")
           
            response_text = extract_text_from_pdf(pdf_name_upload)  # extracting text from pdf
            if response_text['extracted_text']:
                st.text("Extraction ✅")
            else:
                st.text("Extraction Issue ❌. Please re-run the code..")
                sys.exit()

            input_clean_text_response = clean_text(response_text['text_file_path'])  # cleaning the text
            if input_clean_text_response['status']:
                st.text("Cleaning ✅")
                input_clean_text = input_clean_text_response['cleaned_text']
            else:
                st.text("Cleaning Issue ❌. Please re-run the code..")
                sys.exit()

    
    ## finally pass this cleaned text into model and get the predictions ##

    if input_clean_text != "":
        response = make_pred(model, tokenizer, input_clean_text)
        st.success(f"Category --> {response}")
    else:
        sys.exit()

    st.markdown("---")
    st.text("Built with ❤️ by Manish Sharma")

if __name__ == "__main__":
    model, tokenizer = get_model()
    main(model, tokenizer)
