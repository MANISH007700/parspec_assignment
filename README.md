# Parspec DataScientist Assignment
This repo contains code and info for parspec assignment for DataScientist Role

Checkout the **APP HERE** -> https://parspec-bert-finetuned-lighting.streamlit.app/ 

----
# How to Run ? 
_There are 2 ways to run the code / make predictions_ 

1 - To ease the process, I have already deployed the fine-tuned model [ **RECOMMENDED** ]
You can click this link -> https://parspec-bert-finetuned-lighting.streamlit.app/  and make preds
 
2 - You can checkout the notebook which I have created. Load the finetuned model and make preds.
< to make it more accessible, I have pushed the finetuned model to huggingface hub : Check here -> https://huggingface.co/luci007/LightingData-Bert-Finetuned/tree/main >

- Clone the repo
- Install the requirements.txt file
- Move into code folder -> `cd /parspec_assignment/code` 
- Run the `tutorial.ipynb` file to make preds
PS -> You need to have proper modules installed with versions to do so

---

# Files and Folders ? 
_There are 5 Folders_ inside the repo
1 - `src/` : Folder containing all the main code for **Streamlit APP for deployment + Frontend**

- **_main.py_** : Main Streamlit code 
- **_model.py_** : Loading model and making preds
- **_utils.py_** : Code for **Downloading PDF from URL** and **Extracting text from pdf** and **cleaning text from extracted text**

2 - `code/` : This is the main experiment code folder. 

- **_BERT_BASED_UNCASED_FINETUNED_CLEAN_DATA.ipynb_** : The Main experiment notebook which has code for loading the data, partitioning, DataLoader, Dataset Class and FineTuning the BERT BASED UNCASED MODEL on Cutom Data and Benchmarking it 
- **_tutorial.ipynb_** : A tutorial notebook which you can run manually to check the entire flow and make preds.  
- **_finetuned_model_** : Folder containing all the model weights and tokenizer weights of the finetuned model
- **_rough_code_** : dir : This has my rough code
- **_tuts_file_** : experimenting files which were stored for tutorial purpose. You can use them if you like 
- **_push_to_hf_hub.ipynb_** : NB to push my finetuned model to HF hub

3 - `clean_data/` : This folder has 2 .csv file 
- **_training and test csv_** :  These CSV's are created after extracting texts from pdf and cleaning them

4 - `holdout_score/` : Folder which has the benchmark score [results.csv] on the holdout data provided. **Accuracy - 91.25 %**

5 - `images` : Folder having readme.md images

---

# Progress Timeline 

- [x] : Download the pdf file from the URL and save them in directory [ ~ 1hrs ] - time taken to download, not for code [ start date - 30/11/23 ]
- [x] : Extract text from the pdf files and save them in a .txt file [ ~ 30 mins ] - time taken to extract text, not for code [ start date - 30/11/23 ]
- [x] : Convert the extracted text into a csv file [ for both train and test ]. This csv will be used for finetuning model
- [x] : Finetuned BERT base model and BERT large model, had issues in bert large model. Satisfied with bert base
- [x] : Try out Debertav3 model from MSFT for text classification  [ couldn't do it, since model is large and no compute power]
- [x] : Benchmarking the scores on test data [ Update : scored 91.25 % Accuracy ]
- [x] : Add a tutorial NB for the team to run the code and check preds
- [x] : Uploaded to huggingface hub [link -> https://huggingface.co/luci007/LightingData-Bert-Finetuned]
- [x] : Host on Streamlit Cloud [link -> https://parspec-bert-finetuned-lighting.streamlit.app/]

-----
# Some Snapshots from the WEB-APP

### [ inp - url , output - lighting pdf ]
![inp: url, output: light pdf](images/url_light.png)

### [ inp - url , output - no lighting pdf ]
![inp: url, output: light pdf](images/url_no_light.png)

### [ inp - pdf , output - lighting pdf ]
![inp: url, output: light pdf](images/pdf_light.png)

### [ inp - pdf , output - no lighting pdf ]
![inp: url, output: light pdf](images/pdf_no_light.png)

----

# Improvements
### will talk in depth in interview and also in my documentation
- [ ] : Try out MultiModality Model [ Text + Images ] to be used for context [ time constraint, couldn't do]