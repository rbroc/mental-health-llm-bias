import pandas as pd
import json

def convert(questionnaire='phq-9'):
    scores = pd.read_csv(f'mappings/scores/{questionnaire}.csv')
    specs = json.load(open('mappings/specs.json'))[questionnaire]
    stories = []
    for i, r in scores.iterrows():
        targets = r.tolist()
        text = f"{specs['premise']}"
        for idx, t in enumerate(targets[:-2]):
            if t == 0:
                txt = f"I have {specs['options'][t]} {specs['questions'][idx]}."
            else:
                txt = f"I have {specs['questions'][idx]} {specs['options'][t]}."
            text += f' {txt}'
        # TODO: add prompt (either asking for qualitative, or numerical assessment, or diagnosis)
        stories.append([text] + targets)
    df = pd.DataFrame(stories, columns=['prompt'] + scores.columns.tolist())
    df.to_csv(f'outputs/{questionnaire}.csv', index=False)

if __name__=='__main__':
    convert()