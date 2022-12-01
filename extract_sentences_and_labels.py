# Neel Gupta
# 08/18/2022
# Purpose: label distribution

import json
import csv
labels=["message_contact_person_asking","message_contact_person_org","message_org","sentence_intent_attachment","sentence_intent_click","sentence_intent_intro","sentence_intent_money","sentence_intent_phonecall","sentence_intent_products","sentence_intent_recruiting","sentence_intent_scheduling","sentence_intent_service","sentence_intent_unsubscribe","sentence_org_used_by_employer","sentence_passwd","sentence_tone_polite","sentence_tone_urgent","sentence_url_no_name","sentence_url_third_party","signature","signature_email","signature_fullname","signature_jobtitle","signature_org","signature_phone","signature_signoff","signature_url","signaure_address","signaure_handle","words_reciever_organization","words_sender_location","words_sender_organization"]
result = {}
for label in labels:
    result[label]=0
sentence_labels={}



#given the start and end of a span return the collection of the tokens corresponding to this in string format
def get_text(span_start, span_end, annotations):
    starts_ends_tokens = []
    for token in annotations['tokens']:
        if (token['start']>=span_start and token['end']<=span_end):
            starts_ends_tokens.append(token['text'])
        if (token['start'] >= span_start and token['end'] > span_end):
            return " ".join(starts_ends_tokens)


with open("/Users/mitch/research/piranha/prodigy-tools/datasets/sentence_labels.tsv", 'w') as out:
    out.write("")

with open("/Users/mitch/research/piranha/prodigy-tools/datasets/ta3_complete_extraction_nov30th2022_onlyuma.jsonl", 'r') as in_file:
    Lines = in_file.readlines()
    for line in Lines:
        annotations = json.loads(line)
        if "spans" in annotations:
            for entry in annotations["spans"]:
                label=entry["label"]
                full_text = get_text(entry['start'], entry['end'], annotations)
                sentence_labels[full_text]=label



    with open("/Users/mitch/research/piranha/prodigy-tools/datasets/sentence_labels.tsv", 'a') as out:
        for sentence, label in sentence_labels.items():
            out.write(f"{sentence}\t{label}\n")
            out.write("----------------\n")



