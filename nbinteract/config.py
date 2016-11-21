import os


def config_for_env(env_name):
    """
    Takes in an environment and returns a corresponding Config object.
    """
    name_to_env = {
        'production': ProductionConfig(),
        'development': DevelopmentConfig(),
        'testing': TestConfig(),
    }

    return name_to_env[env_name]


class Config(object):
    """General configurations"""

    # testing parameters
    DEBUG = False
    MOCK_AUTH = False
    MOCK_SERVER = False
    SUPPRESS_START = False
    TESTING = False

    PORT = 8002

    # Note: we use environ.get becauase all of these statements get run in
    # every environment, so os.environ['FOOBAR'] will throw an error in
    # development.

    # Github API token; used to pull private repos
    GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN', default='')

    # The organization URL on Github. The API token is filled in so that
    # private repos can be pulled
    GITHUB_ORG = 'https://{}@github.com/data-8/'.format(GITHUB_API_TOKEN)

    # The branch that will be pulled in
    REPO_BRANCH = 'gh-pages'

    # Timeout for authentication token retrieval. Used when checking if
    # notebook exists under user's account
    AUTH_TIMEOUT_S = 10

    def __getitem__(self, attr):
        """
        Temporary hack in order to maintain Flask config-like config usage.
        TODO(sam): Replace config classes with plain dicts or attrs
        """
        return getattr(self, attr)


class ProductionConfig(Config):
    """Configuration for production"""

    PORT = 8002

    # URL for users to access. Make sure it has a trailing slash.
    URL = os.environ.get('JPY_BASE_URL', default='') + "/"

    # username of user
    USERNAME = os.environ.get('JPY_USER')

    # where file is copied to
    COPY_PATH = 'home'

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/user/{username}/notebooks/{destination}'

    # where users are redirect upon git pull success
    GIT_REDIRECT_PATH = '/user/{username}/tree/home/{destination}'

    # alowed file extensions
    ALLOWED_FILETYPES = ['ipynb']


class DevelopmentConfig(Config):
    """Configuration for development mode"""

    # testing parameters
    DEBUG = True
    MOCK_AUTH = True
    MOCK_SERVER = True
    SUPPRESS_START = False

    # URL for users to access. Make sure it has a trailing slash.
    URL = '/'

    # JupyterHub API token
    API_TOKEN = 'your_token_here'

    # Cookie name?
    COOKIE = 'interact'

    # where file is copied to
    COPY_PATH = 'home'

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/notebooks/{destination}'

    # where users are redirect upon git pull success
    GIT_REDIRECT_PATH = '/tree/home/{destination}'

    # allowed sources for file parameter in query
    ALLOWED_DOMAIN = 'http://localhost:8000'

    # base_url for the program
    BASE_URL = 'http://localhost:8002'

    SERVER_NAME = 'localhost:8002'

    # allowed file extensions
    ALLOWED_FILETYPES = ['ipynb']

    # Timeout for authentication token retrieval. Used when checking if
    # notebook exists under user's account
    AUTH_TIMEOUT_S = 0.01


class TestConfig(Config):
    """Configuration for testing mode"""

    # testing parameters
    TESTING = True
    MOCK_AUTH = True
    MOCK_SERVER = True
    SUPPRESS_START = False

    # URL for users to access. Make sure it has a trailing slash.
    URL = '/'

    # JupyterHub API token
    API_TOKEN = 'your_token_here'

    # Cookie name?
    COOKIE = 'interact'

    # where file is copied to
    COPY_PATH = 'app/static/users/{username}'

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/static/users/{username}/{destination}'

    # where users are redirected upon git pull success
    GIT_REDIRECT_PATH = None

    # allowed sources for file parameter in query
    ALLOWED_DOMAIN = 'http://localhost:8000'

    # base_url for the program
    BASE_URL = 'http://localhost:8002'

    # allowed file extensions
    ALLOWED_FILETYPES = ['ipynb']
