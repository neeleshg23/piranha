# Neel Gupta
# 09/01/2022
# Check how many of the annotations agree between annotators

import json
import sys

numAnnotators = 2
emailAnnotatorsCount = {}
emails = {}
annotators_annotations = {}
annotator1Idx = 0
annotator2Idx = 0
annotator1_name="zoe"
annotator2_name="uma"
#what kind of label would you like to know more inter annotator details about [message,sentence, token]
label_stub="word"

flag_print_hashes_text_emails=False
flag_show_kappa_cohen=True
flag_show_per_person_labels_missed=False

#final output print should look like- of all emails
# no of emails both annotated:
count_emails_both_annotated=0
# no of labels annotator1 annotated:
count_labels_annotated_by_annotator1=0
# no of emails annotator2 annotated:
count_labels_annotated_by_annotator2=0
# no of labels both got right
count_labels_intersection=0
labels_per_email=0
cumulative_of_per_email_agreement=0
annotator_id_vs_name={1:annotator1_name, 2:annotator2_name}
hash_vs_text={}



print(f" Analysis of  {label_stub} level labels annotations between {annotator2_name} vs {annotator1_name}")


#separate out emails annotated by annotator1_name and annotator2_name
#laptop


with open("/Users/mithunpaul/research_code/isi/annotated_data/annotated_enron_retreived_using534_annotations_sep20th2022.jsonl", 'r') as f:

#server
#with open("/Users/mitch/research/piranha/annotated_datasets/ta3_reloading_oct18th_message_level_annotated_3annotators_oct26th_extraction.jsonl", 'r') as f:

    Lines = f.readlines()
    for line in Lines:
        entry = json.loads(line)
        email_hash = entry['_input_hash']
        if email_hash == int("1767252249"):
            pass
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
#
# for hash,text in (emails.items()):
#     print(f"hash:{hash}\ntext:{text}\n****************************")
#     print("\n")



emails_annotators_list = {}
#by now annotators_annotations will contain only those of 2 required annotators
#then take each email hash and find the number of people who annotated this and store it in emails_annotators_list.
# Rather, if its just one of the 2 annotators or both. This is useful in finding intersecting annotaions
for key in annotators_annotations:
    notes = annotators_annotations[key]
    keyarr = key.split('_')
    name = keyarr[0]
    email_hash = keyarr[1]
    if email_hash == "1767252249":
        pass
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



#
# combined_annotations = {}
#
# for e_hash_count in intersecting_annotations:
#     ehasharr = e_hash_count.split('_')
#     email_hash = ehasharr[0]
#     annotatorNum = ehasharr[1]
#     for note in intersecting_annotations[e_hash_count]:
#         del note['start']
#         del note['end']
#         data = [(note['token_start'], note['token_end'], note['label'])]
#         if email_hash in combined_annotations:
#             combined_annotations[email_hash].append(data)
#         else:
#             combined_annotations[email_hash] = data

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

#go through each of the email vs annotator set labels and see if there is a label_stub*
for hash,dict_tango in email_hash_vs_bothannotatorlabelset.items():
    for annotator_id, setlabels in dict_tango.items():
        for label in setlabels:
            if label_stub  in label:
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
# print(f"{label_stub} level label count overall (doesnt reflect per email matched or not)")
# for k,v in annotator_message_label_vs_count.items():
#     print(f" {k}:{v}")

if len(dict_bravo_hash_messageLevelLabel_vs_annotatorId.items())==0:
    print(f"No messages for the given label stub {label_stub}")
    sys.exit(1)
print(f"-------------------------\n{label_stub} label per email")
for k,v in dict_bravo_hash_messageLevelLabel_vs_annotatorId.items():
    if len(v)<2:
        split_key=k.split("@")
        email_hash=split_key[0]
        label=split_key[1]
        annotator_id=v[0]
        annotator_name=annotator_id_vs_name[int(annotator_id)]
        #print(f" For email with hash {email_hash} only {annotator_name} annotated the label {label}")

        
def cohen_kappa(ann1, ann2):
    """Computes Cohen kappa for pair-wise annotators.
    :param ann1: annotations provided by first annotator
    :type ann1: list
    :param ann2: annotations provided by second annotator
    :type ann2: list
    :rtype: float
    :return: Cohen kappa statistic
    """
    count = 0
    for an1, an2 in zip(ann1, ann2):
        if an1 == an2:
            count += 1
    A = count / len(ann1)  # observed agreement A (Po)

    uniq = set(ann1 + ann2)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = ((cnt1 / len(ann1)) * (cnt2 / len(ann2)))
        E += count

    return round((A - E) / (1 - E), 4)


labels_per_email=0
count_emails_both=0
email_hash_labels_annotator1={}
cohen_kappa_score_overall=0

#given a list and max number fill it with empty nodes to max lenght
def fill_list_empty_nodes(list_name, max):
    for x in range(max-len(list_name)):
        list_name.append("")
    return list_name


#for annotations by each annotator, check if his label was annotated by the second guy also
for index,e_hash_count in enumerate(intersecting_annotations.keys()):
    ehasharr = e_hash_count.split('_')
    email_hash = ehasharr[0]
    annotatorNum = ehasharr[1]


    #if the email hash already existsin the dictionary
    if email_hash in email_hash_labels_annotator1:
        #get the labels by first guy
        set_labels_annotator1 = email_hash_labels_annotator1[email_hash]
        #then go get the labels by second guy
        labels_annotator1 = []
        # find the list of labels annotated by this guy
        for each_annotation in intersecting_annotations[e_hash_count]:
            labels_annotator1.append(each_annotation["label"])
        count_labels_annotated_by_annotator1 += len(labels_annotator1)
        labels_annotator2_set = set(labels_annotator1)

        #find intersection-print
        count_labels_intersection+= len(labels_annotator2_set.intersection(set_labels_annotator1))
        labels_per_email+= max(len(labels_annotator2_set),len(set_labels_annotator1))
        cumulative_of_per_email_agreement += (count_labels_intersection/labels_per_email)
        count_emails_both += 1
        if(flag_show_kappa_cohen==True):
            #kappa cohen doesnt like different lenghts
            # pass lists
            #sort them
            # if the lenght of lists are differnt, fill the smaller one with empty values

            if(len(labels_annotator1) == len(labels_annotator2)==1):
                cohen_kappa_score_overall += 1
            else:
                if(len(labels_annotator1) != len(labels_annotator2)):
                    if len(labels_annotator1) > len(labels_annotator2):
                        fill_list_empty_nodes(labels_annotator2,len(labels_annotator1))
                    else:
                        fill_list_empty_nodes(labels_annotator1, len(labels_annotator2))
                    #this is a hack, if there is only one overlapping label in atleast one of the sets, just assign them both as same
                    #labels_annotator2_set==set_labels_annotator1
                    #cohen_kappa_score_overall += cohen_kappa(sorted(labels_annotator2_set), sorted(set_labels_annotator1))
                    # cohen_kappa_score_overall +=1
                cohen_kappa_score_overall+=cohen_kappa(sorted(labels_annotator1),sorted(labels_annotator2))

    else:
        labels_annotator2=[]
        #find the list of labels annotated by this guy
        for each_annotation in intersecting_annotations[e_hash_count]:
            labels_annotator2.append(each_annotation["label"])
        count_labels_annotated_by_annotator2 += len(labels_annotator2)
        labels_annotator2_set=set(labels_annotator2)
        email_hash_labels_annotator1[email_hash]=labels_annotator2_set


if len(intersecting_annotations.keys())==0:
    print("no common emails annotated between the given annotators")
else:
    percentage_v1=count_labels_intersection/labels_per_email
    percentage_v2=cumulative_of_per_email_agreement/count_emails_both
    count_emails_both_annotated=len(email_hash_labels_annotator1)


    print(f"total labels_per_email:{labels_per_email}")
    print(f"count_labels_intersection:{count_labels_intersection}")
    print(f"{percentage_v1},")
    print(f"cumulative_of_per_email_agreement:{cumulative_of_per_email_agreement}")
    print(f"count_emails_both:{count_emails_both}")
    print(f"{percentage_v2},")
    print(f"average kappa cohen score={cohen_kappa_score_overall/count_emails_both},")



        