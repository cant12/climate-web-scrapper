import os
import sys
import pdftotext
import pandas as pd
from tqdm import tqdm

pdf_data_dir = sys.argv[1]
output_csv = sys.argv[2]
bad_pdfs_count = 0

def extract_text(pdf_path):
    try:
        text_df = {'Page No.': [], 'Text': []}
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
            page_no = 1
            for page in pdf:
                text_df['Page No.'].append(page_no)
                text_df['Text'].append(page)
                page_no += 1
        text_df = pd.DataFrame(text_df)
        return text_df
    except Exception as e:
        print("There was an issue extracting text from " + pdf_path)
        text_df = {'Page No.': [], 'Text': []}
        text_df = pd.DataFrame(text_df)
        global bad_pdfs_count
        bad_pdfs_count += 1
        return text_df

def generate_text_df(pdf_path, folder_path):
    pdf_text_df = extract_text(pdf_path)
    metadata_df = pd.DataFrame({
        'Report' : [pdf_path[len(folder_path):]]*len(pdf_text_df)
    })
    return pd.concat([metadata_df, pdf_text_df], axis=1)

def extract_text_from_folder(folder_path):
    pdf_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))
    
    df_list = []
    for pdf_path in tqdm(pdf_paths, file=sys.stdout):
        df_list.append(generate_text_df(pdf_path, folder_path))

    return pd.concat(df_list)

df = extract_text_from_folder(pdf_data_dir)
print("Ignoring " + str(bad_pdfs_count) + " pdfs as there was an issue extracting text")
df.to_csv(output_csv)