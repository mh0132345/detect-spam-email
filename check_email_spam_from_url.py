import clean_data
import check_email_spam
import sys

if __name__ == '__main__':
    # Handle command: python check_spam_email_from_url url
    if len(sys.argv) < 2:
        print("Use command: python check_email_spam_from_url url")
        exit()
    url = sys.argv[1]
    clean_data.extract_email_file(url, folder_name="test_email")
    n_spam_email, email_objs = check_email_spam.check_spam_email_folder("test_email")
    print("Number of spam email: ", n_spam_email)
    print("Assume that all email is spam, the accuracy is: ", n_spam_email*1.0/len(email_objs))