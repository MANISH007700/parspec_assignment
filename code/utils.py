import os 
import requests 
import sys, pathlib, fitz
import time 
import pandas as pd 
from loguru import logger

### function to download the pdf using file_url ### 
def download_pdf_from_url(file_id: str, file_url: str, dir_name: str) -> None:
    """
        Args: 
            file_id : id of the file
            file_url : URL where the file is hosted 
            dir_name: Dir where to store the pdf file
        Return:
            None
    """

    save_path = os.path.join(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/download_pdf", dir_name)
    
    response = requests.get(file_url)   # get request
    if response.status_code == 200:
        # The content of the PDF file is in response.content
        # save the file in a pdf 
        with open(os.path.join(save_path, file_id + ".pdf"), "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF-ID {file_id} downloaded successfully.")
    else:
        print(f"Failed to download PDF-ID {file_id}. Status code: {response.status_code}")
    

def extract_text_from_pdf(pdf_dir: str, pdf_file_name: str, save_path_dir: str) -> None:
    """
        Args:
            pdf_dir : dir where the pdf is stored
            pdf_file_name : name of the pdf file 
            save_path_dir : dir where the ocr text of the pdf will be saved
        Return:
            None
    """
    
    full_path = os.path.join(pdf_dir, pdf_file_name)  # get full path

    with fitz.open(full_path) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
    logger.info(f"All text extracted, {pdf_file_name},  saving them....")

    # write as a binary file to support non-ASCII characters
    save_text_path = os.path.join(save_path_dir, pdf_file_name.split(".")[0] + ".txt")
    pathlib.Path(save_text_path).write_bytes(text.encode())


if __name__ == "__main__":

    
    # read the training.csv file to iterate on file_url 
    training_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_train_data - parspec_train_data.csv")
    testing_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_test_data - parspec_test_data.csv")

    # format = {"dataset_category": ["datset_category_df", "dataset_category_dir"]}
    all_dataframe = {"train": [training_df, "train/"], "test": [testing_df, "test/"] }
    
    for set, item in all_dataframe.items():
        start_time = time.time()  # start the time
        logger.info(f"Downloading all the pdf url from {set} set...")
        
        df, dir_path = item[0], item[1]

        for i in range(len(df)):
            # check if ID and URL is not None
            if not pd.isna(df.loc[i, "ID"]) and (not pd.isna(df.loc[i, "URL"])):  
                file_id, file_url = df.loc[i, "ID"], df.loc[i, "URL"]

                try:
                    download_pdf_from_url(file_id, file_url, dir_path)
                except Exception as e:
                    logger.info(f"File id -> {file_id} connection is not secure, cannot download.....")
                
        end_time = time.time()  # end the time

        logger.info(f"Time taken to load and download {set} set --> {end_time - start_time}")

    
    
    # iterate through both train and test pdf directory and extract text out of it and save it
    # format = {"dataset_category": ["datset_category_pdf_path", "dataset_category_save_path"]}
    pdf_paths = {
        "train": ["/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/download_pdf/train", "/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/all_ocr_pdf/train" ],
        "test": ["/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/download_pdf/test", "/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/all_ocr_pdf/test" ]
    }

    start_time = time.time()  # start time 
    for dataset_category, stored_path_info in pdf_paths.items():
        logger.info(f"Extraction started for category {dataset_category}......")
        for f in os.listdir(stored_path_info[0]):

            extract_text_from_pdf(stored_path_info[0], f, stored_path_info[1])
    end_time = time.time()  # end time

    logger.info(f"Time taken to extract text from both train and test set is --> {end_time - start_time} seconds..") 
