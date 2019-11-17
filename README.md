Detect Spam Email for D-fence at Junction
==============================

What Is This?
-------------

This is a simple Python application to detect spam email. The project is written in Python and open source modules. It extracts spam mail's important variables, features and contents and adds them to our black list database. By using this database, we create a program to identify exactly which mail is spam mail.

We also do machine learning as novelty detection with OneClassSVM and TensorFlow Hub to predict spam email with their subjects, however, it seems took a lot of time to predict and not suitable for quick email filtering.

You can check out our data analysis and machine learning results in our notebooks on our Github repository.


How To Use This
---------------

1. Run `pip install -r requirements.txt` to install dependencies
2. Run `python check_email_spam.py`


