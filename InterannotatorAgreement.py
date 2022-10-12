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

annotator_id_vs_name={1:annotator1_name, 2:annotator2_name}


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



intersecting_annotations = {}

for email_hash in emails_annotators_list:
    if len(emails_annotators_list[email_hash]) == 2: #numAnnotators:
        startIdx = 1
        for name in emails_annotators_list[email_hash]:
            notes = annotators_annotations[name+'_'+email_hash]
            intersecting_annotations[email_hash+'_'+str(startIdx)] = notes
            startIdx += 1


total_annotations = {}

for email_hash in emails_annotators_list:
    startIdx = 1
    for name in emails_annotators_list[email_hash]:
        notes = annotators_annotations[name+'_'+email_hash]
        total_annotations[email_hash+'_'+str(startIdx)] = notes
        startIdx += 1




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


annotator_message_label_vs_count={}
dict_bravo_hash_messageLevelLabel_vs_annotatorId={}

#go through each of the email vs annotator set labels and see if there is a message_*
for hash,dict_tango in email_hash_vs_bothannotatorlabelset.items():
    for annotator_id, setlabels in dict_tango.items():
        for label in setlabels:
            if "message" in label:

                key_hash_label = hash + "@" + label
                if label in dict_bravo_hash_messageLevelLabel_vs_annotatorId:

                    current=dict_bravo_hash_messageLevelLabel_vs_annotatorId[label]
                    current.append(annotator_id)
                    dict_bravo_hash_messageLevelLabel_vs_annotatorId[key_hash_label]=current
                else:
                    dict_bravo_hash_messageLevelLabel_vs_annotatorId[key_hash_label] = [annotator_id]


                name_annotator=annotator_id_vs_name[int(annotator_id)]
                key_annotator_label= name_annotator +"_" + label
                if key_annotator_label in annotator_message_label_vs_count:
                    current_value=annotator_message_label_vs_count[key_annotator_label]
                    annotator_message_label_vs_count[key_annotator_label]  =current_value+1
                else:
                    annotator_message_label_vs_count[key_annotator_label]=1
#
# print(f"message level label count overall (doesnt reflect per email matched or not)")
# for k,v in annotator_message_label_vs_count.items():
#     print(f" {k}:{v}")


print(f"message level label per email")
for k,v in dict_bravo_hash_messageLevelLabel_vs_annotatorId.items():
    if len(v)<2:
        split_key=k.split("@")
        email_hash=split_key[0]
        label=split_key[1]
        annotator_id=v[0]
        annotator_name=annotator_id_vs_name[int(annotator_id)]
        print(f" For email with hash {email_hash} only {annotator_name} annotated the label {label}")

        



  






        