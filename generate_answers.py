import json



with open("test_kotlin.json", "r") as file:
    data = json.load(file)


with open("answers_kotlin.txt", "w") as file:
    for entry in data[:100]:
        entry = entry["body"].replace("\n", "").replace("\t", "") 
       # print(entry.strip())
       # print("="*80)
        file.write(entry.strip()+"\n")

    