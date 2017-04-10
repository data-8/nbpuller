import os


def config_for_env(env_name, base_url):
    """
    Takes in an environment and returns a corresponding Config object.
    """
    name_to_env = {
        'production': ProductionConfig(base_url),
        'development': DevelopmentConfig(base_url),
        'testing': TestConfig(base_url),
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

    DELIMITER = ':'

    URL = ''

    def __init__(self, base_url):
        self.URL = base_url

    # Note: we use environ.get becauase all of these statements get run in
    # every environment, so os.environ['FOOBAR'] will throw an error in
    # development.

    # Github API token; used to pull private repos
    GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN', default='')
    GITHUB_DOMAIN = 'github.com'

    # Default domain to pull from is Github
    DEFAULT_DOMAIN = GITHUB_DOMAIN

    # A list of domain that can pull from, delimited by DELIMITER
    ALLOWED_WEB_DOMAINS = os.environ.get(
        'ALLOWED_WEB_DOMAINS', default=GITHUB_DOMAIN).split(DELIMITER)

    # The default and allowed github account(s) that will be pulled from
    # , used only with github.com
    DEFAULT_GITHUB_ACCOUNT = 'data-8'
    ALLOWED_GITHUB_ACCOUNTS = os.environ.get(
        'ALLOWED_GITHUB_ACCOUNTS', default=DEFAULT_GITHUB_ACCOUNT).split(DELIMITER)

    # The branch that will be pulled in
    DEFAULT_BRANCH_NAME = 'gh-pages'

    # Timeout for authentication token retrieval. Used when checking if
    # notebook exists under user's account
    AUTH_TIMEOUT_S = 10

    # This is the url that will be shown to the user if an error occurs
    ERROR_REDIRECT_URL = os.environ.get('ERROR_REDIRECT_URL', default='')

    ALLOWED_URL_DOMAIN = []

    def __getitem__(self, attr):
        """
        Temporary hack in order to maintain Flask config-like config usage.
        TODO(sam): Replace config classes with plain dicts or attrs
        """
        return getattr(self, attr)


class ProductionConfig(Config):
    """Configuration for production"""

    PORT = 8002
    MOCK_AUTH = True
    DEBUG = True

    # where file is copied to, by default use current dir
    COPY_PATH = ""

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/user/{username}/notebooks/{destination}'

    # where users are redirect upon git pull success
    GIT_REDIRECT_PATH = '/user/{username}/tree/{destination}'

    # alowed file extensions
    ALLOWED_FILETYPES = os.environ.get(
        'ALLOWED_FILETYPES', default="ipynb").split(Config.DELIMITER)

    # allowed direct url download from domain
    ALLOWED_URL_DOMAIN = os.environ.get(
        'ALLOWED_URL_DOMAIN', default="").split(Config.DELIMITER)


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
    ALLOWED_URL_DOMAIN = 'http://localhost:8000'

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
    ALLOWED_URL_DOMAIN = 'http://localhost:8000'

    # base_url for the program
    BASE_URL = 'http://localhost:8002'

    # allowed file extensions
    ALLOWED_FILETYPES = ['ipynb']
