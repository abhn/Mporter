from .models import Tasks, Mentees, Mentors
from datetime import datetime, timedelta
from requests import post
from .app_config import MAILGUN_KEY, MAILGUN_SANDBOX


def send_email_driver():
    """
    Gets all the email recipients and sends them their mentee's past 24 hour tasks
    :return: None
    """

    # get all mentees
    mentees = Mentees.query.all()

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
            send_mail(email, email_string)


def send_mail(email, email_string):
    """
    handles email sending procedures
    :param email
    :param email_string
    :return:
    """

    key = MAILGUN_KEY
    sandbox = MAILGUN_SANDBOX
    recipient = email

    request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
    data = {
        'from': "postmaster@" + MAILGUN_SANDBOX,
        'to': recipient,
        'subject': 'Daily Report',
        'text': email_string
    }
    request = post(request_url, auth=('api', key), data=data)

    return request.text
