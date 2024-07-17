import json
import numpy as np

PHQ_9 = {
        "number": 9,
        "scores": 4,
        "cutoffs": [-1, 4, 9, 14, 19, 1000],
        "labels": ["None or Minimal", "Mild", "Moderate", "Moderately Severe", "Severe"],
        "premise": "Over the past two weeks,",
        "options": ["never", "several days", "more than half the days", "nearly every day"],
        "questions": ["had little interest or pleasure in doing things",
                      "felt down, depressed, or hopeless",
                      "had trouble falling or staying asleep, or sleeping too much",
                      "felt tired or having little energy",
                      "had poor appetite or overeaten",
                      "felt bad about myself — or that I am a failure or have let myself or my family down",
                      "had trouble concentrating on things, such as reading the newspaper or watching television",
                      "moved or spoken so slowly that other people could have noticed", # missing a piece
                      "had thoughts that I would be better off dead or of hurting myself in some way"],
    }

def specs():
    spec_dict = dict()
    spec_dict["phq-9"] = PHQ_9
    with open("specs.json", "w") as fh:
        json.dump(spec_dict, fh)


if __name__ == "__main__":
    specs()
