import pandas as pd
import openai
import time
from tqdm import tqdm

# Initialize tqdm progress bars for pandas
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
                temperature = 1,
                max_tokens = 1024,
                top_p = 1
            )

            break
        except Exception as e:
            print(e)
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue

    OUTPUT = response.choices[0].message.content

    return OUTPUT

def _replace_pronoun(txt, pronoun, model_name):
    
    if pronoun == 'first':
        PROMPT = "Rewrite the following text by replacing 'This person' with the first person 'I' and conjugating the verbs accordingly: " + txt
    elif pronoun == 'second':
        PROMPT = "Rewrite the following text by replacing 'This person' with the second person 'You' and conjugating the verbs accordingly: " + txt 
    elif pronoun == 'he':
        PROMPT = "Rewrite the following text by replacing 'This person' with the third person 'He' and conjugating the verbs accordingly: " + txt
    elif pronoun == 'she':
        PROMPT = "Rewrite the following text by replacing 'This person' with the third person 'She' and conjugating the verbs accordingly: " + txt

    return get_completion(model_name, PROMPT)

def make_replacement(questionnaire="phq-9_no_pronouns_paraphrase_story", model_name="gpt-4o"):
    input_narratives_df = pd.read_csv(f"outputs/narratives/{questionnaire}.csv", index_col=None)
    
    pronoun_options=['first', 'second', 'he', 'she']
    
    replacement_dfs = []
    
    for pronoun in pronoun_options:
        pronoun_replaced_df = input_narratives_df.copy()
        
        # Apply pronoun replacement to the 'narrative_paraphrased' column
        pronoun_replaced_df["text_w_pronoun"] = pronoun_replaced_df["narrative_paraphrased"].progress_apply(
            lambda narrative: _replace_pronoun(narrative, pronoun=pronoun, model_name=model_name)
        )
        pronoun_replaced_df["pronoun_replacement"] = pronoun  # Add a column to track the pronoun used
        
        replacement_dfs.append(pronoun_replaced_df)
    
    final_narratives_df = pd.concat(replacement_dfs, ignore_index=True)
    final_narratives_df.to_csv(f"outputs/narratives/{questionnaire}_pronoun_replacement.csv", index=False)

if __name__ == "__main__":
    make_replacement()
