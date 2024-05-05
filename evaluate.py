import torch
import sys
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset


MODE = "PYTHON" # PYTHON or KOTLIN


torch.set_default_device("cuda")
#eos_token = tokenizer.convert_tokens_to_ids("\n\n")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1.5", torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1.5")
#tokenizer.pad_token = "\n\n"
dataset = load_dataset("json", data_files="./test.jsonl")

i = 0
outputs = []
for data in tqdm(dataset["train"]):
    if i == 100:
        break
    if MODE == "PYTHON":
        input_text = f'''You are code completion model for python. Please output only code and nothing else, stop after you complete function. Your task is to complete this function
{data["signature"]}
"""
{data["docstring"]}
"""
'''
    elif MODE == "KOTLIN":
        input_text = f'''Write a kotlin method for this signature and docstring, output only kotlin code and nothing else
{data["docstring"]}
{data["signature"]}
'''
    inputs = tokenizer(input_text, return_tensors="pt")#, padding=True, truncation=True, max_length = 512, return_attention_mask=True)

    outputs = model.generate(**inputs, max_length=120)#, do_sample = True, temperature = 0.5, top_k = 30, early_stopping = True, num_beams = 5, num_return_sequences=1)
    text = tokenizer.batch_decode(outputs)[0]
    outputs.append(text[len(input_text):])

    i += 1

with open("predictions.txt", "w") as file:
    for text in outputs:
        file.write(text.replace("\n", "")+"\n")

sys.exit()




print(text[len(input_text):text.find("\n\n")])