import pandas as pd

PARAPHRASE_PROMPT = None  # TODO: replace


def _paraphrase(txt):
    """Function that takes string as input and returns a paraphrase"""
    # TODO: prompt an LLM with PARAPHRASE_PROMPT to paraphrase narrative
    # Should return paraphrased text
    pass


def make_paraphrases(questionnaire="phq-9"):
    narratives = pd.read_csv(f"outputs/narratives/{questionnaire}.csv", index_col=None)
    narratives["narrative_paraphrased"] = narratives["narrative_raw"].apply(_paraphrase)
    narratives.to_csv(
        f"outputs/narratives/{questionnaire}.csv", index=False
    )


if __name__ == "__main__":
    make_paraphrases()
