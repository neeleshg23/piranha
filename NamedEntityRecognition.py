# Neel Gupta
# 8/17/2022
# Serialize and select emails from the Enron corpus that have entities (as defined by spacy)

import json
import spacy
nlp = spacy.load('en_core_web_sm')

def show_ents(doc):
    if doc.ents:
        entities = []
        counts = {}
        total = 0
        for ent in doc.ents:
            entities.append((ent.text.replace("\n", "").replace("\t", "").strip(), ent.label_))
            if counts.get(ent.label_) is None:
                counts[ent.label_] = 1
                total += 1
            else: 
                counts[ent.label_] += 1
                total += 1
        return entities, counts, total
    else:
        return None, None, None

result = {}

with open("C:\\Users\\neele\\PIRANHA\\enron.json", 'r') as file:
    Lines = file.readlines()
    i = 1000000
    for line in Lines:
        JSON_string = json.loads(line.strip())
        text = JSON_string['text']
        if len(text) < 1000000: document = nlp(text)
        else: continue
        ents, cnts, total = show_ents(document)
        if ents is not None:
            data = {
                "text": text,
                "entities": ents, 
                "counts": cnts,
                "total": total
            }
            result[i] = data
            i += 1
            #print("email with serial", i, "has been run and saved on runtime")

with open("C:\\Users\\neele\\PIRANHA\\final_enron_NER.json", 'w') as out:
    json.dump(result, out, indent=4)

    
            
        


