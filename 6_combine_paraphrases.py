import pandas as pd
import numpy as np


def combine_paraphrases(questionnaire="phq-9"):
    raw = pd.read_csv(f"outputs/narratives/{questionnaire}.csv", index_col=None)
    simple = pd.read_csv(f"outputs/narratives/{questionnaire}_paraphrase_simple_pronoun_replacement.csv", index_col=None)
    narrative = pd.read_csv(f"outputs/narratives/{questionnaire}_paraphrase_narrative_pronoun_replacement.csv", index_col=None)
    raw['paraphrase_condition'] = 'raw'
    simple['paraphrase_condition'] = 'simple'
    narrative['paraphrase_condition'] = 'narrative'

    for data in [simple, narrative]:
        conditions = [
            (data["pronoun_replacement"] == 'first'),
            (data["pronoun_replacement"] == 'second'),
            (data["pronoun_replacement"] == 'he'),
            (data["pronoun_replacement"] == 'she'),
        ]
        pron_choices = ["I", "you", "he", "she"]
        person_choices = ["first", "second", "third", "third"]
        data['pronoun'] = np.select(conditions, pron_choices)
        data['person_condition'] = np.select(conditions, person_choices)
        data['narrative_raw'] = data['text_w_pronoun']
        data.drop(['narrative_paraphrased', 'text_w_pronoun', 'pronoun_replacement'], axis=1, inplace=True)
    all_data = pd.concat([raw, simple, narrative], axis=0, ignore_index=True)
    all_data.rename({'narrative_raw': 'narrative'}, axis=1, inplace=True)
    all_data.to_csv(f"outputs/narratives/{questionnaire}_combined.csv", index=False)


if __name__ == "__main__":
    combine_paraphrases()
