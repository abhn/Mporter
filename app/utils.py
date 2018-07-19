from .models import Tasks, Mentees, Mentors
from datetime import datetime, timedelta
import requests
from .app_config import MAILGUN_KEY, MAILGUN_URL, MAILGUN_TESTMAIL_ADDR


def send_email_driver(is_test=None):
    """
    Gets all the email recipients and sends them their mentee's past 24 hour tasks
    :return: None
    """

    # get all mentees
    mentees = Mentees.query.all()

    # track the number of emails to send, for testing and debugging purposes
    ctr = 0

    # for each mentee, get the mentors and tasks
    for mentee in mentees:
        mentors = mentee.mentor

        # get only tasks from the past day
        tasks = Tasks\
            .query\
            .filter_by(mentee=mentee) \
            .filter(Tasks.at_created >= datetime.today() - timedelta(days=1))\
            .all()

        current_mentee_mentor_emails = []
        # get email addresses
        for mentor in mentors:
            current_mentee_mentor_emails.append(mentor.mentor_email)

        # now we have tasks and list of emails
        # for each email, send the email

        email_string = ''

        for count, task in enumerate(tasks, start=1):
            email_string += '#%o %s \n' % (count, task.task)

        if email_string == '':
            continue

        for email in current_mentee_mentor_emails:
            # if this is a test, don't send the email
            if is_test is None:
                send_mail(email, email_string)
            ctr += 1

    return ctr


def send_mail(email, email_string):
    """
    handles email sending procedures
    :param email
    :param email_string
    :return:
    """

    key = MAILGUN_KEY
    recipient = email

    request_url = MAILGUN_URL
    data = {
        'from': MAILGUN_TESTMAIL_ADDR,
        'to': recipient,
        'subject': 'Daily Report',
        'text': email_string
    }
    request = requests.post(request_url, auth=('api', key), data=data)

    return request.text
