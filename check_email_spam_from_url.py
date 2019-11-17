import clean_data
import check_email_spam
import sys

if __name__ == '__main__':
	# Handle command: python check_spam_email_from_url url
	if len(sys.argv) < 2:
		print("Use command: python check_email_spam_from_url url")
		exit()
	url = sys.argv[1]
	check_spam_email_folder.check_spam_email_folder("test_email")
