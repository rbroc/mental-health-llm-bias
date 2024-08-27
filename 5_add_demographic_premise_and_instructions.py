import pandas as pd
import json
import numpy as np
import itertools
import random

subjects = {
    "first": "I am",
    "second": "You are",
    "third": "The person who wrote this text is",
}


def make_final_data(questionnaire="phq-9", n_dem_combinations=100):
    dems = json.load(open("dems.json"))
    narratives = pd.read_csv(f"outputs/{questionnaire}.csv", index_col=None)

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
        dem_premise = (
            f'{subjects[n["person_condition"]]} a {d[0]}-year-old {d[1]} from {d[2]}.'
        )
        # Duplicate examples by whether we feed the narrative or a paraphase
        for par_condition in ["narrative_raw"]:  # "narrative_paraphrased" TODO: edit
            narrative = n[par_condition]
            # Duplicate examples by response conditions
            for resp_condition in ["binary", "severity", "score"]:  # TODO: edit
                response = "Please provide an answer."  # TODO: edit with actual conditions
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
    df = df.drop(['narrative_raw'], axis=1) # TODO: add narrative_paraphrase
    df.to_csv(f"outputs/{questionnaire}_final.csv", index=False)


if __name__ == "__main__":
    make_final_data()
