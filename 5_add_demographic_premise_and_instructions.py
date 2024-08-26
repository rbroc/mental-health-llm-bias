import pandas as pd
import json

persons = ["I", "she", "he", "they", "you"]
verbs = ["am", "is", "is", "are", "are"]

def make_demographic_premise(
        questionnaire='phq-9', 
        n_dem_combinations=100
        ):
    scores = pd.read_csv(f'scores/{questionnaire}.csv')
    specs = json.load(open('specs.json'))[questionnaire]
    dems = json.load(open('dems.json'))

    # TODO: sample per age group
    # TODO: make product
    # TODO: sample n_dem_combinations times

    stories = []
    for _, r in scores.iterrows():

        for person, verb in zip(persons, verbs):
            targets = r.tolist()
            text = f"{specs['premise']}"
            for question_index, option_index in enumerate(targets[:-2]):
                if question_index == 0:
                    txt = f"{person} {verb}"
                else:
                    txt = f"{person.capitalize()} {verb}"
                if option_index == 0:
                    txt += f" {specs['options'][option_index]} {specs['questions'][question_index]}."
                else:
                    txt += f" {specs['questions'][question_index]} {specs['options'][option_index]}."
                text += f' {txt}'
            stories.append([text] + targets + [person]) # for final dataframe
    
    df = pd.DataFrame(stories, columns=['prompt'] + scores.columns.tolist() + ['person'])
    df.to_csv(f'outputs/{questionnaire}.csv', index=False)

if __name__=='__main__':
    make_narratives()