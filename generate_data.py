import pandas as pd
import json
import numpy as np
from itertools import product


def generate(n=1000, questionnaire="phq-9"):
    with open(f"specs.json") as fh:
        specs = json.load(fh)
    n_q = specs[questionnaire]["number"]
    n_s = list(range(specs[questionnaire]["scores"]))
    cutoffs = specs[questionnaire]["cutoffs"]
    labels = specs[questionnaire]["labels"]
    d = list(product(n_s, repeat=n_q))
    scores = pd.DataFrame(d, columns=[f"q_{i}" for i in range(n_q)])
    scores["total"] = scores.apply(lambda x: x.sum(), axis=1)
    scores["severity"] = pd.cut(scores["total"], bins=cutoffs, labels=labels)
    scores = scores.groupby("severity").sample(n=int(n / len(labels)))
    scores.to_csv(f"scores/{questionnaire}.csv", index=False)


if __name__ == "__main__":
    generate()
