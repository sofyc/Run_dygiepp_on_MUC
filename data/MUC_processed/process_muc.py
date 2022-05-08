import argparse
import os
import json
import re
import spacy
import string

def findIndiceForMention(document, mention):
    for i in range(len(document)- len(mention) + 1):
        for j in range(len(mention)):
            if mention[j] != document[i+j]:
                break

        if (mention[-1] == document[i+len(mention)-1]) and (j+1 == len(mention)):
            return True, i
    return False, -1

def preprocess_string(doc_str):
    doc_str = re.sub("\n", "", doc_str)
    doc_str = doc_str.replace("'", '"')
    return re.sub(r' +', ' ', re.sub(r'(\-\-+|\.\.+)', "", doc_str.lower()))

def main():
    new_train_f = open("new_train.json", "w")
    # new_ptrain_f = open("new_pretty_train.json", "w")
    new_test_f = open("new_test.json", "w")
    # new_ptest_f = open("new_pretty_test.json", "w")
    new_dev_f = open("new_dev.json", "w")
    # new_pdev_f = open("new_pretty_dev.json", "w")

    # files = ["test.json"]
    files = ["train.json", "dev.json", "test.json"]
    for file in files:
        instances = []
        with open(file) as f:
            for row in f:
                # each row (sample) is a json object
                a_dict = json.loads(row)
                instances.append(a_dict)
            print("len(instances): ", len(instances))
            print("type(instances): ", type(instances),"\n")
            for inst in instances:
                doc = {}
                entityWithRole = list()
                entityWithRole.append(list())
                doc["doc_key"] = inst["docid"]
                doc["dataset"] = "MUC"
                document = inst["doctext"]
                prepro_doc = preprocess_string(document)
                nlp = spacy.load("en_core_web_sm")
                spacyed_doc = nlp(prepro_doc)
                tokens = [[preprocess_string(token.text) for token in spacyed_doc if token.text not in string.punctuation]]

                doc["sentences"] = tokens
                templates = inst["templates"]

                for template in templates:
                    roles = ["PerpInd", "PerpOrg", "Target", "Weapon", "Victim"]

                    for role in roles:
                        if len(template[role]) != 0:
                            entities = template[role][0]
                            for entity in entities:
                                enti_tokens = nlp(entity[0])
                                preped_enti_tokens = [[preprocess_string(token.text) for token in enti_tokens if token.text not in string.punctuation]]
                                res = findIndiceForMention(tokens[0], preped_enti_tokens[0])
                                if res[0] == True:
                                    # triple = [res[1], res[1]+len(entity[0])-1, role]
                                    triple = [res[1], res[1]+len(preped_enti_tokens[0])-1, role]
                                    entityWithRole[0].append(triple)

                doc["ner"] = entityWithRole    

                if file == "train.json":
                    new_train_f.write(json.dumps(doc) + "\n")
                    # new_ptrain_f.write(json.dumps(doc, indent=4) + "\n")
                elif file == "dev.json":
                    new_dev_f.write(json.dumps(doc) + "\n")
                    # new_pdev_f.write(json.dumps(doc, indent=4) + "\n")
                elif file == "test.json":
                    new_test_f.write(json.dumps(doc) + "\n")
                    # new_ptest_f.write(json.dumps(doc, indent=4) + "\n")

if __name__ == "__main__":
    main()