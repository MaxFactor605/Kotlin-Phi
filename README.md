# JetBrain Intership test task
## Files
* *extract_func.py* - specify variable REP_DIR with path that lead to Kotlin repo, will extract and prepare dataset (Expected clean formating how it is done in Kotlin repo, tried grammar parsing, too slow. More in *grammar_parser*). Dataset have same format as CodeXGlue-MethodGeneration - {"signature":"", "docstring":"", "body":""}
* *evaluate.py*; *evaluate.ipynb* - use phi1.5 model to generate prediction file in format needed for CodeXGlue-MethodGeneration evaluator
* *evaluator.py*; *bleu.py* - evaluator files taken from CodeXGlue-MethodGeneration
Usage:
```
python3 evaluator.py --answer answer_file.txt --predictions predictions_file.txt
```
* *generate_answers.py* - will help to generate answers file from dataset
* *FineTune.ipynb* - code for finetunning, I didn't have time to run the fine-tunning itself because of one annoying error (and of course lack of time because of studying)