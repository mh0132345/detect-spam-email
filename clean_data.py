import email
import os
import pandas as pd
import tarfile

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlretrieve

def extract_email_file(url, filename="./honeypot-content.tar.gz"):
    urlretrieve(url, filename=filename)
    print("Download complete!")
    print("Unzipping dataset (this may take a while)")
    os.makedirs("spam_email", exist_ok=True)
    tfile = tarfile.open("honeypot-content.tar.gz", "r:gz")
    tfile.extractall("./spam_email")

def get_all_file(email_dir):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(email_dir):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def get_email_object(email_file, encoding="ISO-8859-1"):
    with open(email_file, encoding=encoding) as search:
        data = search.read()
        email_obj = email.message_from_string(data)
        return email_obj

def get_all_email_object(email_dir):
    files = get_all_file(email_dir)
    email_objs = []
    for email_file in files:
        email_objs.append(get_email_object(email_file))
    return email_objs

def clean_html(html):
    soup = BeautifulSoup(html, features="html.parser") # create a new bs4 object from the html data loaded
    for script in soup(["script"]):
        script.extract()
    text = soup.get_text()
    return text

def get_all_email_header(email_objs):
    all_email = []
    for email_obj in email_objs:
        email_final = dict(zip(email_obj.keys(), email_obj.values()))
        all_email.append(email_final)
    return all_email

def export_email_headers(all_email, output_file="email_header.csv"):
    df = pd.DataFrame.from_dict(all_email, orient='columns')
    df.to_csv(output_file)

def get_all_email_content(email_objs):
    messages = []
    for email_obj in email_objs:
        if email_obj.is_multipart():
            for part in email_obj.walk():
                if part.get_content_type() == 'text/html':
                    removed_html =  clean_html(str(part.get_payload(decode=True)))
                    cleantext = removed_html.replace('\\n', '').replace('\\r', '').replace('\\t', '').strip()
                    if cleantext:
                        messages.append((email_obj["Subject"], part.get_content_type(), cleantext))
                elif part.get_content_type() == 'text/plain':
                    msg = clean_html(str(part.get_payload(decode=True))).strip()
                    if msg:
                        messages.append((email_obj["Subject"], part.get_content_type(), msg))
        else:
            msg = str(clean_html(email_obj.get_payload(decode=True))).strip()
            if msg:
                messages.append((email_obj["Subject"], email_obj.get_content_type(), msg))
    return messages

def export_email_content(messages, output_file="email_message.csv"):
    df_email_message = pd.DataFrame(messages, columns =['Subject', 'Content Type', 'Content'])
    df_email_message.to_csv(output_file)

if __name__ == '__main__':
    url = "https://hackjunction.d-fence.eu/ItrryOmHB1HNzyB/honeypot-content.tar.gz"
    extract_email_file(url)
    email_dir = Path("D:/spam/spam_email")
    files = get_all_file(email_dir)