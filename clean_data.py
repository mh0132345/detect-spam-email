import glob
import os
from pathlib import Path
import email
import collections
import csv
import pandas as pd

c = collections.Counter()

thisdir = Path("D:/spam/honeypot-content")

# r=root, d=directories, f = files
files = []
for r, d, f in os.walk(thisdir):
    for file in f:
        files.append(os.path.join(r, file))

print(len(files))

all_email = []
for email_file in files:
	with open(email_file, encoding="ISO-8859-1") as search:
		data = search.read()
		email_obj = email.message_from_string(data)
		email_final = dict(zip(email_obj.keys(), email_obj.values()))
		print(email_final)
		all_email.append(email_final)

df = pd.DataFrame.from_dict(all_email, orient='columns')
df.to_csv("email.csv")

# with open(files[0], encoding="ISO-8859-1") as search:
# 	data = search.read()
# 	email_obj = email.message_from_string(data)
# 	with open("emails.csv", "w", encoding="utf-8") as output:
# 		w = csv.writer(output)
# 		print(email_obj.keys())
# 		w.writerow(email_obj.keys())

# with open("emails.csv", "a+", encoding="utf-8", new_line="") as output:
# 	for email_file in files:
# 		with open(email_file, encoding="ISO-8859-1") as search:
# 			data = search.read()
# 			email_obj = email.message_from_string(data)
# 			w = csv.writer(output)
# 			w.writerow(email_obj.values())
