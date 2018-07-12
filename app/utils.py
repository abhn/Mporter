from .models import Task, Mentee, Mentor
import datetime


def send_email_driver():
    """
    first get all mentees,
        then for each mentee, get his mentors and his tasks in the last 24 hours
            then for each mentor, send an email
    :return: None
    """

    # get all mentees
    mentees = Mentee.query.all()

    # for each mentee, get the mentors and tasks
    for mentee in mentees:
        mentors = mentee.mentor

        # get only tasks from the past day
        tasks = Task\
            .query\
            .filter_by(mentee=mentee) \
            .filter(Task.at_created >= datetime.datetime.today() - datetime.timedelta(days=1))\
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

        for email in current_mentee_mentor_emails:
            send_mail(email, email_string)


def send_mail(email, email_string):
    """
    handles email sending procedures
    :param email:
    :param email_string:
    :return:
    """
    print('send mail called')
