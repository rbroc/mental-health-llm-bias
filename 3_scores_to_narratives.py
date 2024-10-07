import pandas as pd
import json

persons = ["I", "she", "he", "you"] # "they"
verbs = ["have", "has", "has", "have"] # "have"
pronouns = ["my", "her", "his", "your"] # "them"
pronrefs = ["myself", "herself", "himself", "yourself"] #  "themselves"
pnames = ["first", "third", "third", "second"] # "third"
beverbs = ["am", "is", "is", "are"]


def make_narratives(questionnaire="phq-9"):
    scores = pd.read_csv(f"outputs/scores/{questionnaire}.csv")
    specs = json.load(open("outputs/specs/questionnaires.json"))[questionnaire]
    stories = []
    for _, r in scores.iterrows():
        for person, verb, pronoun, pronref, name, beverb in zip(
            persons, verbs, pronouns, pronrefs, pnames, beverbs
        ):
            # This creates the narratives with first, second, and third person pronouns
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
                txt = txt.replace("PERSON", person)
                txt = txt.replace("PRONSIMPLE", pronoun)
                txt = txt.replace("PRONSELF", pronref)
                txt = txt.replace("HAVEVERB", verb)
                txt = txt.replace("BEVERB", beverb)
                text += f" {txt}"
            stories.append([text] + targets + [person] + [name])

    df = pd.DataFrame(
        stories,
        columns=["narrative_raw"]
        + scores.columns.tolist()
        + ["pronoun", "person_condition"],
    )
    df.to_csv(f"outputs/narratives/{questionnaire}.csv", index=False)


if __name__ == "__main__":
    make_narratives()
