from os import environ


def get_env_var(name):
    """
    simple helper function to safely return environment variables
    :param name:
    :return: environment variable's value if found else raise KeyError
    """
    try:
        return environ[name]
    except KeyError:
        return KeyError('{} not found in environment variables'.format(name))

