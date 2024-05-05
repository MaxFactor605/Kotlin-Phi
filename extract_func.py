import os
import io
import json
from tqdm import tqdm
import random

REP_DIR = "./JetBrains_test/kotlin"




def get_filepaths():
    
    filepaths = []
    for root, subdirs, files in os.walk(REP_DIR):
        for file in files:
            if file.endswith(".kt"): #or file.endswith(".kts"):
                filepaths.append(os.path.join(root, file))


    return filepaths


def combine_files(filepaths, new_file_path = "GigaFile.kt"):

    lines = []
    for path in filepaths:
        with open(path, "r") as file:
            lines.append("".join(file.readlines()))

    with open(new_file_path, "w") as file:
        file.write("\n\n".join(lines))

    
    
def get_functions(lines):
    functions = []; docstring_functions = []
    mode = 0  # 0 - function search 1 - function signature scanning 2 - function body scaning
    signature = ""
    body = ""
    docstring = ""

    for i, line in enumerate(lines):
        
        if  mode == 0:
            stripped_line = line.strip()
            if "fun" in stripped_line.split(" "):
                intend = len(line) - len(stripped_line) - 1
                mode = 1
                #signature += line[intend:]
                if i - 1 >= 0 and lines[i-1].strip() == "*/" :
                    j = 1
                    while i - j >= 0 and lines[i-j].strip().startswith("*"):
                        docstring = lines[i-j].strip() + "\n" + docstring
                        j+=1
                    docstring = lines[i-j].strip() + "\n" + docstring[:-1]
                elif i - 2>= 0 and lines[i-2].strip == "*/":
                    j = 2
                    while i-j >= 0 and lines[i-j].strip().startswith("*"):
                        docstring = lines[i-j].strip() + "\n" + docstring
                        j +=1
                    docstring = lines[i-j].strip() + "\n" + docstring[:-1]
        if mode == 1:
            signature += line[intend:]
            if signature.endswith("{\n"):
                mode = 2
                continue
            if signature.endswith("=\n"):
                mode = 2
                continue

            
        elif mode == 2:
            body += line[intend:] 
            if line.startswith("\t"*intend + "}") or line == "\n":
                if line == "\n":
                    body = body[:-1]
                if docstring == "":
                    functions.append({"docstring":docstring, "signature":signature, "body":body})
                else:
                    docstring_functions.append({"docstring":docstring, "signature":signature, "body":body})
                docstring = ""
                signature = ""
                body = ""
                mode = 0
                intend = 0

    return (functions, docstring_functions)

def main(filepaths):


    count_all = 0
    count_docstring = 0
    p_bar = tqdm(filepaths)
    all_functions = []
    all_docstring_functions = []
    for filepath in p_bar:
        with open(filepath, "r") as file:
            functions, docstring_functions = get_functions(file.readlines())
        count_all += len(functions) + len(docstring_functions)
        count_docstring += len(docstring_functions)
        p_bar.set_description(f"{count_all} functions; {count_docstring} with docstring")
        all_functions += functions
        all_docstring_functions += docstring_functions
    print(f"Founded {count_all} functions including {count_docstring} functions with docstrings")
    #for docstring, sign, body in all_functions:
     #   print(f"{sign}*************\n{docstring}************\n{body}")
      #  print("="*50)
    
    test_functions = all_functions[:int(len(all_functions) * 0.1)]
    test_doctstring_functions = all_docstring_functions[:int(len(all_docstring_functions)*0.1)]
    test_dataset = test_functions + test_doctstring_functions
    train_functions = all_functions[len(test_functions):]
    train_doctstring_functions = all_docstring_functions[len(test_doctstring_functions):]
    train_dataset = train_functions + train_doctstring_functions
    random.shuffle(test_dataset)
    random.shuffle(train_dataset)
    with open("test_kotlin.json", "w") as file:
        json.dump(test_dataset, file)
    with open("train_kotlin.json", "w") as file:
        json.dump(train_dataset, file)

if __name__ == "__main__":
    paths = get_filepaths()
    print(f"Founded {len(paths)} .kt files")
    #combine_files()
    main(paths)
