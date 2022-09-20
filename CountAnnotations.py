# Neel Gupta
# 08/18/2022
# Purpose: Count the number of annotations that have been found in the Enron Corpus by parsing the back end JSONL produced by prodigy

import json

result = {}

with open("C:\\Users\\neele\\PIRANHA\\85emailannotations.jsonl", 'r') as in_file:
    Lines = in_file.readlines()
    for line in Lines:
        annotations = json.loads(line)
        if "spans" in annotations:
            for entry in annotations["spans"]:
                label = entry["label"]
                if label in result:
                    result[label] += 1
                else:
                    result[label] = 1

with open("C:\\Users\\neele\\PIRANHA\\85_emails_freqs.json", 'w') as out:
    json.dump(result, out, indent=4)


