import pandas as pd
import json
import numpy as np
import itertools
import random

random.seed(42)

verbs = {"I": "am", "you": "are", "he": "is", "she": "is",}
possessives = {"I": "my", "you": "your", "he": "his", "she": "her"}
phrases = {
    "I": "Do I have",
    "you": "Do you have",
    "he": "Does he have",
    "she": "Does she have",
}
condict = {"phq-9": "depression"}
conditions = [
    "Depression",
    "Generalized Anxiety Disorder",
    "Schizophrenia",
    "Other",
    "None",
]


def make_final_data(questionnaire="phq-9", n_dem_combinations=100):
    dems = json.load(open("outputs/specs/demographics.json"))
    q_specs = json.load(open("outputs/specs/questionnaires.json"))[questionnaire]
    response_opts = json.load(open("outputs/specs/responses.json"))

    narratives = pd.read_csv(f"outputs/narratives/{questionnaire}_combined.csv", index_col=None)

    dem_combos = list(itertools.product(dems["gender"]))
    k = min(n_dem_combinations, len(dem_combos))
    print(f"*** Sampling {k} demographic profiles ***")
    dem_combos = random.sample(dem_combos, k=k)

    print("*** Combining demographic and severity profiles ***")
    combos = list(itertools.product(dem_combos, [r for _, r in narratives.iterrows()]))
    combos = [
        (d, n)
        for d, n in combos
        if not (
            ((n["pronoun"] == "she") and (d[0] != "woman"))
            or ((n["pronoun"] == "he") and (d[0] != "man"))
        )
    ]
    print(len(combos))

    print(f"*** Creating final dataset ***")
    data = []
    for d, n in combos:
        narrative_data = n.tolist()
        dem_premise = f'{n["pronoun"].capitalize()} {verbs[n["pronoun"]]} a {d[0]}.'
        narrative = n["narrative"]
        for resp_condition in [
            "binary_simple",
            "binary_explain",
            "severity_qual",
            "severity_score",
            "multiclass",
        ]:
            response = response_opts[resp_condition]
            response = response.replace(
                "PRONPHRASE", f"{phrases[n['pronoun']].capitalize()}"
            )
            response = response.replace("CONDNAME", f"{condict[questionnaire]}")
            response = response.replace("AUXVERB", f"{verbs[n['pronoun']]}")
            response = response.replace("PERSON", f"{n['pronoun']}")
            cond_labels = [f"'{s}'" for s in conditions]
            response = response.replace("CONDOPTIONS", ", ".join(cond_labels))
            response = response.replace("PRONSIMPLE", f"{possessives[n['pronoun']]}")
            response = response.replace(
                "SEVRANGE",
                f'{str(q_specs["cutoffs"][0]+1)} to {str(q_specs["cutoffs"][-1])}',
            )
            sev_labels = [f"'{s}'" for s in q_specs["labels"]]
            response = response.replace("SEVOPTIONS", ", ".join(sev_labels))
            txt = f"{dem_premise} {narrative} {response}"
            data.append(
                [txt] + narrative_data + [resp_condition] + list(d)
            )
    df = pd.DataFrame(
        data,
        columns=["text"]
        + narratives.columns.tolist()
        + [
            "response_condition",
            "gender_condition",
        ],
    )
    print(f"*** Saving: {df.shape[0]} examples ***")
    df.drop('narrative', axis=1, inplace=True)
    df['text'] = df['text'].str.replace('\n', '')
    df.to_csv(
        f"outputs/final/{questionnaire}.csv", index=False,
    )
    df.to_excel(f"outputs/final/{questionnaire}.xlsx")


if __name__ == "__main__":
    make_final_data()
