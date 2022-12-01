# Neel Gupta
# 08/18/2022
# Purpose: label distribution

import json
import csv
labels=["message_contact_person_asking","message_contact_person_org","message_org","sentence_intent_attachment","sentence_intent_click","sentence_intent_intro","sentence_intent_money","sentence_intent_phonecall","sentence_intent_products","sentence_intent_recruiting","sentence_intent_scheduling","sentence_intent_service","sentence_intent_unsubscribe","sentence_org_used_by_employer","sentence_passwd","sentence_tone_polite","sentence_tone_urgent","sentence_url_no_name","sentence_url_third_party","signature","signature_email","signature_fullname","signature_jobtitle","signature_org","signature_phone","signature_signoff","signature_url","signaure_address","signaure_handle","words_reciever_organization","words_sender_location","words_sender_organization"]
result = {}
for label in labels:
    result[label]=0

with open("/Users/mitch/research/piranha/prodigy-tools/datasets/ta3_complete_extraction_nov30th2022_onlyuma.jsonl", 'r') as in_file:
    Lines = in_file.readlines()
    for line in Lines:
        annotations = json.loads(line)
        if "spans" in annotations:
            for entry in annotations["spans"]:
                key=entry["label"]
                label = entry["label"]
                if key in result:
                    result[key] += 1
                else:
                    result[key] = 1

with open("/Users/mitch/research/piranha/prodigy-tools/datasets/per_label_distribution_ta3.tsv", 'w') as out:

    for k,v in result.items():
        out.write(f"{k}\t{v}\n")



