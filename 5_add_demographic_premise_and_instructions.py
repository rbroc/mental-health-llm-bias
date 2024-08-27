import pandas as pd
import json
import numpy as np
import itertools
import random

verbs = {"I": "am", "you": "are", "he": "is", "she": "is", "they": "are"}

phrases = {
    "I": "Do I have",
    "you": "Do you have",
    "he": "Does he have",
    "she": "Does she have",
    "they": "Do they have",
}

condict = {"phq-9": "depression"}  # TODO: edit if we add more questionnaires
conditions = [
    "depression",
    "generalized anxiety disorder",
    "schizophrenia",
]  # TODO: remove if we add more questionnaires


def make_final_data(questionnaire="phq-9", n_dem_combinations=100):
    dems = json.load(open("outputs/specs/demographics.json"))
    q_specs = json.load(open("outputs/specs/questionnaires.json"))[questionnaire]
    response_opts = json.load(open("outputs/specs/responses.json"))
    narratives = pd.read_csv(f"outputs/narratives/{questionnaire}.csv", index_col=None)

    ages = []
    for d in dems["age"]:
        ages += list(np.random.randint(low=d[0], high=d[1] + 1, size=10))
    dem_combos = list(itertools.product(ages, dems["gender"], dems["region"]))
    k = min(n_dem_combinations, len(dem_combos))
    print(f"*** Sampling {k} demographic profiles ***")
    dem_combos = random.sample(dem_combos, k=k)

    print("*** Combining demographic and severity profiles ***")
    combos = list(itertools.product(dem_combos, [r for _, r in narratives.iterrows()]))
    combos = [
        (d, n)
        for d, n in combos
        if not (
            ((n["pronoun"] == "she") and (d[1] != "woman"))
            or ((n["pronoun"] == "he") and (d[1] != "man"))
            or ((n["pronoun"] == "they") and (d[1] != "non-binary person"))
        )
    ]

    print(f"*** Creating final dataset ***")
    data = []
    for d, n in combos:
        narrative_data = n.tolist()
        dem_premise = f'{n["pronoun"].capitalize()} {verbs[n["pronoun"]]} a {d[0]}-year-old {d[1]} from {d[2]}.'
        for par_condition in ["narrative_raw"]:  # "narrative_paraphrased" TODO: edit
            narrative = n[par_condition]
            for resp_condition in [
                "binary_simple",
                "binary_explain",
                "severity_qual",
                "severity_score",
                "multiclass",
            ]:  # TODO: potentially edit
                response = response_opts[resp_condition]
                response = response.replace(
                    "PRONPHRASE", f"{phrases[n['pronoun']].capitalize()}"
                )
                response = response.replace("CONDNAME", f"{condict[questionnaire]}")
                response = response.replace("AUXVERB", f"{verbs[n['pronoun']]}")
                response = response.replace("PERSON", f"{n['pronoun']}")
                response = response.replace("CONDOPTIONS", ", ".join(conditions))
                response = response.replace(
                    "SEVRANGE",
                    f'{str(q_specs["cutoffs"][0]+1)} to {str(q_specs["cutoffs"][-1])}',
                )
                response = response.replace("SEVOPTIONS", ", ".join(q_specs["labels"]))
                txt = f"{dem_premise} {narrative} {response}"
                data.append(
                    [txt] + narrative_data + [resp_condition, par_condition] + list(d)
                )
    df = pd.DataFrame(
        data,
        columns=["text"]
        + narratives.columns.tolist()
        + [
            "response_condition",
            "paraphrase_condition",
            "age_condition",
            "gender_condition",
            "region_condition",
        ],
    )
    # TODO: add further sampling?
    df = df.drop(["narrative_raw"], axis=1)  # TODO: add narrative_paraphrase
    print(f"*** Saving: {df.shape[0]} examples ***")
    df.to_csv(f"outputs/final/{questionnaire}_final.csv.gz", index=False, compression='gzip')


if __name__ == "__main__":
    make_final_data()
