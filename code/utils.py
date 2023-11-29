import os 
import requests 
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


    


if __name__ == "__main__":

    # read the training.csv file to iterate on file_url 
    training_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_train_data - parspec_train_data.csv")
    testing_df = pd.read_csv(r"/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/data/parspec_test_data - parspec_test_data.csv")

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