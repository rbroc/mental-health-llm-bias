### Evaluating bias in LLM-based diagnostics and severity assessment

##### File content
- - `1_create_questionnaire_specs.py` creates json files (saved under `specs.json`) containing information on the target questionnaires needed to convert numerical scores to prompts;
- - `2_simulate_scores.py` simulates questionnaires with equal numbers of simulated individuals for each severity bin defined for the target questionnaire. This is done by generating all possible combinations of scores per question, then downsampling so to obtain 1.000 total examples, equally distributed across severity bins. Outputs are saved under `scores`;
- - `3_scores_to_narratives.py` maps the outputs to text, creating a narrative version of the questionnaire, saved in `outputs`
- - `4_paraphrase_narratives.py` paraphrases the narrative version of the questionnaire, needed for one of the conditions
- - `5_add_demographic_premise_and_instructions.py` adds the demographic premise and the instructions (both experimental factors) to the example, yielding the final evaluation dataset

##### TODO:
- Set seeds
- Double-check response conditions (multiclass? open differential diagnosis?) and demographic options
- Simplify conditions and number of examples? E.g., doing some post-hoc analysis
- @Flor: do paraphrases
- @Flor: refine the prompts and run

##### Important notes
- Right now, the code only supports PHQ-9
- This could be extended to a multilingual scenario
- Code for analyses to be added