import pandas as pd
import glob
import os
from tqdm import tqdm

def combineCSVFiles(input_path, output_file):
    all_files = glob.glob(os.path.join(input_path, "*.csv")) #get all csv files in input path directory
    
    if not input_path or not output_file:
        raise ValueError("Input and output paths must be provided.")
    
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in the directory: {input_path}")

    df_list = [] #empty pandas list for individual dfs
    
    for file in tqdm(all_files, desc="Processing CSV files"): #tdqm for progress bar, loop through all csv's in input path directory
        df = pd.read_csv(file)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True) #concatenate all dfs in list
    
    combined_df.to_csv(output_file, index=False) #save to output file
    print(f"Combined CSV saved to: {output_file}") 
    print(f"Total rows in combined file: {len(combined_df)}")

