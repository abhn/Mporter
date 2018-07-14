import os


def get_env_var(name):
    """
    simple helper function to safely return environment variables
    :param name:
    :return: environment variable's value if found else raise KeyError
    """
    try:
        return os.environ[name]
    except KeyError:
        return KeyError('{} not found in environment variables'.format(name))

