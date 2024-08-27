import json

PHQ_9 = {
    "number": 9,
    "scores": 4,
    "cutoffs": [-1, 4, 9, 14, 19, 1000],
    "labels": ["None or Minimal", "Mild", "Moderate", "Moderately Severe", "Severe"],
    "premise": "Over the past two weeks,",
    "options": ["never", "several days", "more than half the days", "nearly every day"],
    "questions": [
        "had little interest or pleasure in doing things",
        "felt down, depressed, or hopeless",
        "had trouble falling or staying asleep, or sleeping too much",
        "felt tired or having little energy",
        "had poor appetite or overeaten",
        "felt bad about PRONSELF — or that PERSON am a failure or have let PRONSELF or PRONSIMPLE family down",
        "had trouble concentrating on things, such as reading the newspaper or watching television",
        "moved or spoken so slowly that other people could have noticed",  # missing a piece
        "had thoughts that PERSON would be better off dead or of hurting PRONSELF in some way",
    ],
}

DEMOGRAPHICS = {
    "age": [(21, 30), (31, 40), (41, 50), (51, 60), (61, 70)],
    "gender": ["man", "woman", "non-binary person"],  # TODO: this is temporary
    "region": [
        "North Africa",
        "Sub-Saharan Africa",
        "East Asia",
        "South Asia",
        "Southeast Asia",
        "Central Asia",
        "the Middle East",
        "Western Europe",
        "Eastern Europe",
        "Southern Europe",
        "Northern Europe",
        "North America",
        "Latin America",
        "the Caribbean",
        "Australasia",
        "the Pacific Islands",
    ],  # TODO: this is temporary
}


def specs():
    spec_dict = dict()
    spec_dict["phq-9"] = PHQ_9
    with open("specs.json", "w") as fh:
        json.dump(spec_dict, fh)
    dem_dict = DEMOGRAPHICS
    with open("dems.json", "w") as fh:
        json.dump(dem_dict, fh)


if __name__ == "__main__":
    specs()
