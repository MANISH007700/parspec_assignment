import os 
import requests 
import sys, pathlib, fitz
import time 
import pandas as pd 
from tqdm import tqdm
from pandas import DataFrame
from loguru import logger


def download_pdf_from_url(file_id: str, file_url: str, dir_name: str) -> None:
    """ function to download the pdf using file_url  
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
    """ function to extract text from the pdf file 
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


def convert_text_file_into_dataframe(file_dir: str, training_df: DataFrame) -> DataFrame: 
    """ convert the input text file into a dataframe column 
        Args:
            file_dir : the dir of the text file which contains all the raw OCR text of the pdf
            training_df : the training df which has the info of the pdf and it's respective category
        Return:
            DataFrame : A pandas dataframe which has inp text and target as lighting / no lighting
    """

    # Step 0 : Create a target map 
    target_map = {"Yes": 1, "No": 0}
    # Step 1: Create an empty list which will later be converted into df
    training_data = {
        "input_id": [],
        "input_text": [], 
        "target": []
    }

    # Step 2 : Iterate through the input text directory
    for filename in tqdm(os.listdir(file_dir)):
        if filename.endswith('.txt'):
            file_path = os.path.join(file_dir, filename)

            # Step 3: Read the content of each text file
            with open(file_path, 'r') as file:
                text_content = file.read()

            clean_text_content = text_content.replace("\n", " ").replace("•", "")

            # breakpoint()
            # Step 4 : Find the target category from the training df 
            file_id = filename.split(".")[0]
            target_row = training_df[training_df['ID'] == file_id]
            # print(target_row)
            if len(target_row) != 0:
                # target_value = target_map[target_row['Is lighting product?'].values[0]]   # mapping the category into 0 and 1  [ do this only for training data ]
                target_value = target_row['Is lighting product?'].values[0]  # testing data is already in 0 and 1
            
                # Step 5 : Add the clean content and target value in the dict
                
                training_data['input_id'].append(file_id)
                training_data['input_text'].append(clean_text_content)
                training_data['target'].append(target_value)

    # Step 6 : Create the dataframe and save it
    clean_train_df = pd.DataFrame.from_dict(training_data) 
    clean_train_df.to_csv("testing_df_info.csv", index=False)

if __name__ == "__main__":

    
    # read the training.csv file to iterate on file_url 
    training_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_train_data - parspec_train_data.csv")
    testing_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_test_data - parspec_test_data.csv")

    '''
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

    '''
    # convert every text file into df and add the target col too
    convert_text_file_into_dataframe( "/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/all_ocr_pdf/train", training_df)    # training
    convert_text_file_into_dataframe("/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/all_ocr_pdf/test", testing_df)  # training
    
