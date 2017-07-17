import os


def pull_env(from_, type=None):
    value = os.environ.get(from_) or ''
    if type == bool:
        value = value.strip().lower() == 'true'
    globals()[from_] = value


# LIST OF ENV VARS THAT ARE ADDED TO DJANGO SETTINGS
# KEEP ALPHABETICAL ORDER PLEASE !
# DEFAULT VALUE is '' and False for bool

pull_env('ENVIRONMENT')
pull_env('DATABASE_MOCKER_URL')
pull_env('RAVEN_CONFIG_DSN')
