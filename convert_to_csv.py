import json
with open("/Users/mitch/research/piranha/annotated_datasets/enron_reloading_nov3rd2022_extraction_nov22nd.jsonl", 'r') as f:
    for line in f:
        entry = json.loads(line)
        email_hash = entry['_input_hash']
        #go through spans
        # for each given start end token, find the corresponding words in them.
        #finally your file should look like:
        # "reply to me immediately and let me know if 5pm works for a call"-> [message_contact_person_asking,sentences_intent_scheduling]
