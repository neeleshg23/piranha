# Neel Gupta
# 09/01/2022
# Check how many of the annotations agree between annotators

import json

numAnnotators = 2
emailAnnotatorsCount = {}
emails = {}
annotators_annotations = {}
annotator1Idx = 0
annotator2Idx = 0

with open("C:\\Users\\neele\\PIRANHA\\ta3_retrieved_using_86_annotations_and_annotated.jsonl", 'r') as f:
    Lines = f.readlines()
    for line in Lines:
        entry = json.loads(line)
        email_hash = entry['_input_hash']
        if email_hash in emailAnnotatorsCount:
            emailAnnotatorsCount[email_hash] += 1
        else:
            emailAnnotatorsCount[email_hash] = 1
        emails[email_hash] = entry['text']
        if 'spans' in entry:
            if entry['_annotator_id'] == 'ta3_retrieved_using_86_annotations-neel':
                annotators_annotations['neel_'+str(email_hash)] = entry['spans']
                annotator1Idx += 1
            elif entry['_annotator_id'] == 'ta3_retrieved_using_86_annotations-mithun':
                annotators_annotations['mithun_'+str(email_hash)] = entry['spans']
                annotator2Idx += 1



print(annotators_annotations)

emails_annotators_list = {}

for key in annotators_annotations:
    notes = annotators_annotations[key]
    keyarr = key.split('_')
    name = keyarr[0]
    email_hash = keyarr[1]
    if email_hash in emails_annotators_list:
        emails_annotators_list[email_hash].append(name)
    else:
        emails_annotators_list[email_hash] = [name]

#print(emails_annotators_list)

intersecting_annotations = {}

for email_hash in emails_annotators_list:
    if len(emails_annotators_list[email_hash]) == 2: #numAnnotators:
        startIdx = 1
        for name in emails_annotators_list[email_hash]:
            notes = annotators_annotations[name+'_'+email_hash]
            intersecting_annotations[email_hash+'_'+str(startIdx)] = notes
            startIdx += 1

#print(intersecting_annotations)

total_annotations = {}

for email_hash in emails_annotators_list:
    startIdx = 1
    for name in emails_annotators_list[email_hash]:
        notes = annotators_annotations[name+'_'+email_hash]
        total_annotations[email_hash+'_'+str(startIdx)] = notes
        startIdx += 1

#print(total_annotations)


with open("C:\\Users\\neele\\PIRANHA\\email_hash_lookup.json", 'w') as out:
    json.dump(emails, out, indent=4)

with open("C:\\Users\\neele\\PIRANHA\\intersecting_annotations_ta3_mitch_neel.json", 'w') as out:
    json.dump(intersecting_annotations, out, indent=4)

with open("C:\\Users\\neele\\PIRANHA\\total_annotations_mitch_neel.json", 'w') as out:
    json.dump(total_annotations, out, indent=4)

combined_annotations = {}

for e_hash_count in intersecting_annotations:
    ehasharr = e_hash_count.split('_')
    email_hash = ehasharr[0]
    annotatorNum = ehasharr[1]
    for note in intersecting_annotations[e_hash_count]:
        del note['start']
        del note['end']
        data = [(note['token_start'], note['token_end'], note['label'])]
        if email_hash in combined_annotations:
            combined_annotations[email_hash].append(data)
        else:
            combined_annotations[email_hash] = data

print(combined_annotations)



# for annotation in annotations:
#     notes, email_hash = annotation
#     email_annotations = []
#     for note in notes:
#         label_data = (note['label'], note['token_start'], note['token_end'])
#         email_annotations.append(label_data)
#     if email_hash in res:
#         res[email_hash].append(email_annotations)
#     else:
#         res[email_hash] = email_annotations

# combined_annotations = {}

        
    

        


  






        