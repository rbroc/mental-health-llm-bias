import re
import pandas as pd
import openai
from tqdm import tqdm
import time
import logging
import fire
import os

tqdm.pandas()

def get_completion(model_name_or_path, text):

    time.sleep(1)
    
    prompt = text

    INPUT = [{"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": prompt}]

    while True:
        try:
            response = openai.chat.completions.create(
                model = model_name_or_path,
                messages = INPUT,
                temperature = 0,
                max_tokens = 256,
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0
            )

            break
        except Exception as e:
            print(e)
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue

    OUTPUT = response.choices[0].message.content

    return OUTPUT

def main():
    
    test_data_input_path = '/home/Plaza/mental-health-llm-bias/outputs/final/phq-9_final.csv'
    n_test_samples = 1000
    model_name_or_path = 'gpt-4'
    test_set = 'phq-9_final.csv'

    test_df = pd.read_csv(test_data_input_path)
    print(test_df)
    #test_df = pd.read_csv(test_data_input_path) #for the explanations
    logging.info(f"Loaded TEST data: {test_df.shape[0]} rows")
    
    if n_test_samples > 0:
        test_df = test_df.sample(n_test_samples, random_state=123)
        logging.info(f"Sampled {n_test_samples} rows from TEST data")

    test_df["model_completion"] = test_df.progress_apply(lambda x: get_completion(model_name_or_path, x.text), axis=1)
    test_df["model_completion"] = test_df["model_completion"].replace(r'\n',' ', regex=True)  

    test_data_output_path = f'./evaluation/data/model_completions/{model_name_or_path}/{test_set}'
    print(test_data_output_path)
    os.makedirs(test_data_output_path.rsplit("/", 1)[0])
    logging.info(f"Creating new path {test_data_output_path.rsplit('/', 1)[0]}")
        
    test_data_output_path = f'{test_data_output_path}'
    print(test_data_output_path)
    logging.info(f"Saving completions to {test_data_output_path}")
    test_df.to_csv(test_data_output_path, index=False)

if __name__ == "__main__":
    main()
    st = time.time()
    logging.info(f'Total execution time: {time.time() - st:.2f} seconds')