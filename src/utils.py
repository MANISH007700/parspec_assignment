import os 
import requests 
import sys, pathlib, fitz
import re
from loguru import logger
from nltk.corpus import stopwords


def download_pdf_from_url(file_url: str, file_name: str) -> None:
    """ function to download the pdf using file_url  
        Args: 
            file_url : URL where the file is hosted 
            file_name : name of the file
        Return:
            None
    """
    response = requests.get(file_url)  # get request
    if response.status_code == 200:
        with open(file_name, "wb") as pdf_file:
            pdf_file.write(response.content)

        logger.info(f"PDF-ID {file_name} downloaded successfully") 
        return {"status_code": 200, "downloaded": True, "coming_from_url": True}
    else:
        logger.info(f"Failed to download PDF-ID {file_name}. Status code: {response.status_code}")
        return {"status_code": response.status_code, "downloaded": False, "coming_from_url": True}




def extract_text_from_pdf(pdf_file_name: str, from_url: bool = False) -> None:
    """ function to extract text from the pdf file 
        Args:
            pdf_file_name : name of the pdf file 
        Return:
            None
    """

    # if from_url is False -> This means, the pdf is uploaded directly from streamlit, we first need to save them into proper pdf format and then extract text out of it 
    if not from_url:  # pdf is uploaded 
        save_location = pdf_file_name.name
        with open(save_location, "wb") as f:
            f.write(pdf_file_name.read())

        # now extract text 
        try:
            with fitz.open(pdf_file_name) as doc:  # open document
                text = chr(12).join([page.get_text() for page in doc])
        except Exception as e:
            return {"extracted_text": False}

        logger.info(f"All text extracted, {pdf_file_name},  saving them....")

        # write as a binary file to support non-ASCII characters
        save_text_path = os.path.join(save_location.split(".")[0] + ".txt")
        pathlib.Path(save_text_path).write_bytes(text.encode())
        return {"extracted_text": True, "text_file_path": save_text_path}

    if from_url:  # url was passed first
        try:
            with fitz.open(pdf_file_name) as doc:  # open document
                text = chr(12).join([page.get_text() for page in doc])
        except Exception as e:
            return {"extracted_text": False}

        logger.info(f"All text extracted, {pdf_file_name},  saving them....")

        # write as a binary file to support non-ASCII characters
        save_text_path = os.path.join(pdf_file_name.split(".")[0] + ".txt")
        pathlib.Path(save_text_path).write_bytes(text.encode())
        return {"extracted_text": True, "text_file_path": save_text_path}


def clean_text(text_file: str) -> str:
    """ function to clean the text file before it can be passed into the model for prediction
        Args:
            text_file : path of the text file   
        Return :
            text_str : string of cleaned text
    """

    if text_file.endswith('.txt'):

        # Step 3: Read the content of each text file
        with open(text_file, 'r') as file:
            text_content = file.read()

        sw = stopwords.words('english')

        text_content = text_content.replace("\n", " ").replace("•", "").lower()
        text = re.sub(r"[^a-zA-Z?.!,¿]+", " ", text_content)  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
        text = re.sub(r"http\S+", "", text)  # Removing URLs 
        html = re.compile(r'<.*?>') 
        text = html.sub(r'', text)  # Removing html tags
        
        punctuations = '@#!?+&*[]-%.:/();$=><|{}^' + "'`" + '_'
        for p in punctuations:
            text = text.replace(p, '')  # Removing punctuations
        text = [word.lower() for word in text.split() if word.lower() not in sw]
        text = " ".join(text)  # removing stopwords        
        return {"cleaned_text": text, "status": True}
