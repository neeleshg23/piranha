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
annotator1_name="uma"
annotator2_name="zoe"

with open("/Users/mitch/research/piranha/prodigy-tools/datasets/apwg_annotated_data_oct10th2022.jsonl", 'r') as f:
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
            if "_annotator_id" in entry:
                if annotator1_name in entry['_annotator_id'] :
                    annotators_annotations[annotator1_name+"_"+str(email_hash)] = entry['spans']
                    annotator1Idx += 1
                elif  annotator2_name in entry['_annotator_id'] :
                    annotators_annotations[annotator2_name+"_"+str(email_hash)] = entry['spans']
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

print(emails_annotators_list)

intersecting_annotations = {}

for email_hash in emails_annotators_list:
    if len(emails_annotators_list[email_hash]) == 2: #numAnnotators:
        startIdx = 1
        for name in emails_annotators_list[email_hash]:
            notes = annotators_annotations[name+'_'+email_hash]
            intersecting_annotations[email_hash+'_'+str(startIdx)] = notes
            startIdx += 1

print(intersecting_annotations)

total_annotations = {}

for email_hash in emails_annotators_list:
    startIdx = 1
    for name in emails_annotators_list[email_hash]:
        notes = annotators_annotations[name+'_'+email_hash]
        total_annotations[email_hash+'_'+str(startIdx)] = notes
        startIdx += 1

print(total_annotations)


# with open("C:\\Users\\neele\\PIRANHA\\email_hash_lookup.json", 'w') as out:
#     json.dump(emails, out, indent=4)
#
# with open("C:\\Users\\neele\\PIRANHA\\intersecting_annotations_ta3_mitch_neel.json", 'w') as out:
#     json.dump(intersecting_annotations, out, indent=4)
#
# with open("C:\\Users\\neele\\PIRANHA\\total_annotations_mitch_neel.json", 'w') as out:
#     json.dump(total_annotations, out, indent=4)

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

track_labels_per_email={}

#e.g., {19239202; dict(ann1;set(labels1), ann2:set(labels2))}
email_hash_vs_bothannotatorlabelset={}

for k,v in intersecting_annotations.items():
    splits = k.split("_")
    hash = splits[0]
    anotattor = splits[1]
    labels_this_annotator=[]
    for entry in v:
        if "label" in entry:
            labels_this_annotator.append(entry["label"])
    set_labels_this_annotator=set(labels_this_annotator)
    this_annotator_vs_labelset_dict_charlie={}
    this_annotator_vs_labelset_dict_charlie[anotattor]=set_labels_this_annotator

    if hash in email_hash_vs_bothannotatorlabelset:
        dict_charlie=email_hash_vs_bothannotatorlabelset[hash]
        if anotattor in dict_charlie:
            print("error. this annotator shouldnt be here")
        else:
            dict_charlie[anotattor]=set_labels_this_annotator
            email_hash_vs_bothannotatorlabelset[hash]=dict_charlie
    else:
        email_hash_vs_bothannotatorlabelset[hash]=this_annotator_vs_labelset_dict_charlie

print(email_hash_vs_bothannotatorlabelset)


        
    

        


  






        