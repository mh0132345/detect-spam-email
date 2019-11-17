import clean_data
import sys

MESSAGE_ID_DOMAIN_FILE = "./data/message_id_domain.txt"
X_MAILER_SENT_BY_DOMAIN_FILE = "./data/x_mailer_send_by_domain.txt"
REPLY_TO_DOMAIN_FILE = "./data/reply_to_domain.txt"
COMMON_SPAM_WORDS = "./data/spam_words.txt"
SPAM_URLS_IN_SUBJECTS = "./data/urls_in_subjects.txt"
EMAIL_CLIENT = ["Microsoft", "Outlook", "Windows", "Google", "Gmail", "Thunderbird", "Yahoo", "Vk"]


def read_domains_from_file(path):
    with open(path, "r") as input_file:
        domains = input_file.read().splitlines()
        return domains

# Authentication-Results fail
def check_email_authentication(email_obj):
    key_word = "fail"
    if email_obj["Authentication-Results"]:
        return key_word in email_obj["Authentication-Results"]
    return False

# X-Spam-Flag
def check_spam_flag(email_obj):
    if email_obj["X-Spam-Flag"]:
        return email_obj["X-Spam-Flag"]=="YES"
    return False

# X-Mailer
def check_x_mailer(email_obj):
    if email_obj["X-Mailer"]:
        if any(client in email_obj["X-Mailer"] for client in EMAIL_CLIENT):
            return False
    return True

# Message-Id with domain filer
def check_message_id(email_obj):
    if email_obj["Message-Id"] or email_obj["Message-ID"]:
        domains = read_domains_from_file(MESSAGE_ID_DOMAIN_FILE)
        if any((domain in email_obj["Message-ID"] or email_obj["Message-Id"]) for domain in domains):
            return True
    return False

# Reply-to and Reply-To with domain filter
def check_reply_to(email_obj):
    if email_obj["Reply-to"] or email_obj["Reply-To"]:
        domains = read_domains_from_file(REPLY_TO_DOMAIN_FILE)
        if any((domain in email_obj["Reply-to"] or domain in email_obj["Reply-To"]) for domain in domains):
            return True
    return False

# X-Mailer-Sent-By domain filter
def check_x_mailer_sent_by(email_obj):
    if email_obj["X-Mailer-Sent-By"]:
        domains = read_domains_from_file(X_MAILER_SENT_BY_DOMAIN_FILE)
        if any(domain in email_obj["X-Mailer-Sent-By"] for domain in domains):
            return True
    return False

# Check subject
def check_subject_contain_dollar_sign(email_obj):
    if email_obj["Subject"]:
        return "$" in email_obj["Subject"]
    return False

def check_subject_contain_spam_word(email_obj):
    if email_obj["Subject"]:
        return "SPAM: " in email_obj["Subject"]
    return False

def check_subject_contain_at_sign(email_obj):
    if email_obj["Subject"]:
        return "@" in email_obj["Subject"]
    return False

def check_subject_contain_re_keyword(email_obj):
    key_word = "Re: "
    if email_obj["Subject"]:
        return key_word in email_obj["Subject"]
    return False

def check_subject_contain_common_spam_word(email_obj):
    count = 0
    if email_obj["Subject"]:
        spam_words = read_domains_from_file(COMMON_SPAM_WORDS)
        for spam_word in spam_words:
            if spam_word in email_obj["Subject"]:
                count += 1
    return count

def check_subject_contain_harmful_domain(email_obj):
    count = 0
    if email_obj["Subject"]:
        spam_words = read_domains_from_file(SPAM_URLS_IN_SUBJECTS)
        for spam_word in spam_words:
            if spam_word in email_obj["Subject"]:
                count += 1
    return count

def calculate_score(email_obj):
    score_auth = check_email_authentication(email_obj)
    score_spam = check_spam_flag(email_obj)
    score_reply = check_reply_to(email_obj)
    score_message_id = check_message_id(email_obj)
    score_x_mailer = check_x_mailer(email_obj)
    score_subject_at_sign = check_subject_contain_at_sign(email_obj)
    score_subject_dollar_sign = check_subject_contain_dollar_sign(email_obj)
    score_subject_re_keyword = check_subject_contain_re_keyword(email_obj)
    score_subject_spam_word = check_subject_contain_spam_word(email_obj)
    score_subject_common_spam_word = check_subject_contain_common_spam_word(email_obj)
    score_subject_contain_harmful_domain = check_subject_contain_harmful_domain(email_obj)
    scores = [
        score_auth, score_spam, score_reply*2, score_message_id*2,
        score_x_mailer, score_subject_at_sign, score_subject_dollar_sign,
        score_subject_re_keyword, score_subject_spam_word*2,
        score_subject_common_spam_word, score_subject_contain_harmful_domain
    ]
    return sum(scores)

def is_spam(email_obj):
    score = calculate_score(email_obj)
    if score >= 5:
        return True
    return False


def check_spam_email_folder(email_dir):
    email_objs = clean_data.get_all_email_object(email_dir)
    n_spam_email = 0
    for email_obj in email_objs:
        n_spam_email += is_spam(email_obj)
    return n_spam_email, email_objs

if __name__ == '__main__':
    # email_obj = clean_data.get_email_object("D:/spam/spam_email/honeypot-content/1562151052.M507495P20281.mail1-fi1.d-fence.eu,S=9655,W=9888")
    # print(calculate_score(email_obj))
    if len(sys.argv) < 2:
        print("Use command: python check_email_spam folder")
        exit()
    email_dir = "./spam_email"
    print("Start to calculate!")
    n_spam_email, email_objs = check_spam_email_folder(email_dir)
    print("Number of spam email: ", n_spam_email)
    print("Accuracy: ", n_spam_email*1.0/len(email_objs))
