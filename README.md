### Evaluating bias in LLM-based diagnostics and severity assessment

##### File content
- - `create_specs.py` creates json files (saved under `specs.json`) containing information on the target questionnaires needed to convert numerical scores to prompts;
- - `generate_data.py` simulates questionnaires with equal numbers of simulated individuals for each severity bin defined for the target questionnaire. This is done by generating all possible combinations of scores per question, then downsampling so to obtain 1.000 total examples, equally distributed across severity bins. Outputs are saved under `scores`;
- - `convert_scores.py` maps the outputs to text, creating a narrative version of the questionnaire, saved in `outputs`.

##### Important notes
- Right now, the code only supports PHQ-9
- This could be extended to a multilingual scenario
- There is no demographic information right now, this needs to be added
- Also, there is no explicit prompt, but I'm thinking we could both ask the model open diagnosis questions ("Which psychiatric condition might I have?"), as well severity assessment either in numerical form ("How severe is my depression, on a scale from 0 to 27?") or in qualitative form ("How severe is my depression? Choose between None or Minimal, Mild, Moderate, Moderately Severe, Severe")