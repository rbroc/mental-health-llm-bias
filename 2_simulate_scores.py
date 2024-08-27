import pandas as pd
import json
import numpy as np
from itertools import product


def generate(n=100, questionnaire="phq-9"):
    with open(f"specs.json") as fh:
        specs = json.load(fh)
    n_q = specs[questionnaire]["number"]
    n_s = list(range(specs[questionnaire]["scores"]))
    cutoffs = specs[questionnaire]["cutoffs"]
    labels = specs[questionnaire]["labels"]
    d = list(product(n_s, repeat=n_q))
    scores = pd.DataFrame(d, columns=[f"q_{i}" for i in range(n_q)])
    scores["severity_score"] = scores.apply(lambda x: x.sum(), axis=1)
    scores["severity_qual"] = pd.cut(
        scores["severity_score"], bins=cutoffs, labels=labels
    )
    scores = scores.groupby("severity_qual").sample(
        n=int(n / len(labels))
    )  # TODO: set seed
    scores.to_csv(f"scores/{questionnaire}.csv", index=False)


if __name__ == "__main__":
    generate()
