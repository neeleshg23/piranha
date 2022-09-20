# Neel Gupta
# 08/30/2022
# Purpose: Add the origin tag to the JSONL files

import json

emailList = []

with open("C:\\Users\\neele\\PIRANHA\\enron_all_emails.jsonl", 'r') as in_file:
    for line in in_file:
        email = json.loads(line)
        email['origin'] = "enron"
        emailList.append(email)

  
with open("C:\\Users\\neele\\PIRANHA\\enron_origin.jsonl", 'w') as out:
    for email in emailList:
        json.dump(email, out)
        out.write('\n')
    
