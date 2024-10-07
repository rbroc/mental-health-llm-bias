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

def _paraphrase(txt, paraphrase_type, model_name_or_path):
    """Function that takes a string as input and returns a paraphrase"""
    
    if paraphrase_type == 'paraphrase_simple':
        PARAPHRASE_PROMPT = "Paraphrase the following text using \"This person\" as the main subject throughout. Do not switch to other subjects. Avoid using \"they\" as a replacement for \"This person\". Text: " + txt
    elif paraphrase_type == 'paraphrase_story':
        PARAPHRASE_PROMPT = "Create a brief story based on the following text. The story must keep \"This person\" as the main subject throughout. Do not switch to other subjects. Avoid using \"they\" as a replacement for \"This person\". Text: " + txt    
    elif paraphrase_type == 'paraphrase_narrative':
        PARAPHRASE_PROMPT = "Write a brief narrative based on the following text. The narrative must keep \"This person\" as the main subject throughout. Do not switch to other subjects. Avoid using \"they\" as a replacement for \"This person\". Text: " + txt    
    else:
        raise ValueError("Invalid paraphrase_type. Must be 'simple' or 'narrative1' or 'narrative2'.")

    return get_completion(model_name_or_path, PARAPHRASE_PROMPT)

def make_paraphrases(questionnaire="phq-9_no_pronouns", model_name_or_path="gpt-4o"):
    # Load the CSV file
    narratives = pd.read_csv(f"outputs/narratives/{questionnaire}.csv", index_col=None)
    
    paraphrase_type='paraphrase_narrative'
    
    # Apply paraphrasing with 'narrative' type
    narratives["narrative_paraphrased"] = narratives["narrative_raw"].progress_apply(
        lambda txt: _paraphrase(txt, paraphrase_type=paraphrase_type, model_name_or_path=model_name_or_path)
    )
    
    narratives["narrative_paraphrased"] = narratives["narrative_paraphrased"].str.replace('\n', ' ', regex=False)
    
    # Save the results back to CSV
    narratives.to_csv(f"outputs/narratives/{questionnaire}_{paraphrase_type}.csv", index=False)

if __name__ == "__main__":
    make_paraphrases()
