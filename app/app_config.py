from utils import get_env_var

SEND_MAIL_HOUR = 8
CELERY_BROKER_URL = get_env_var('RABBITMQ_BIGWIG_URL')
DB_URL = get_env_var('DATABASE_URL')
DB_URL_TEST = get_env_var('HEROKU_POSTGRESQL_GRAY_URL')

SECRET_KEY = get_env_var('MPORTER_SECRET')

MAILGUN_KEY = get_env_var('MAILGUN_API_KEY')
MAILGUN_SANDBOX = get_env_var('MAILGUN_DOMAIN')
MAILGUN_URL = 'https://api.mailgun.net/v2/{0}/messages'.format(MAILGUN_SANDBOX)
MAILGUN_TESTMAIL_ADDR = 'postmaster@{}'.format(MAILGUN_SANDBOX)