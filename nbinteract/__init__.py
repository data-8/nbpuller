from app.config import config_for_env
from tornado.options import define
from nbinteract.handlers import LandingHandler
from notebook.utils import url_path_join

def _jupyter_server_extension_paths():
    return [{
        'module': 'nbinteract',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "notebook",
        "dest": "nbinteract",
        "src": "static",
        "require": "nbinteract/main"
    }]

def load_jupyter_server_extension(nbapp):

    web_app = nbapp.web_app
    env_name = 'production'
    config = config_for_env(env_name)
    define('config', config)

    host_pattern = '.*'
    route_pattern = url_path_join(web_app.settings['base_url'], '/interact')
    web_app.add_handlers(host_pattern, [(route_pattern, LandingHandler),(route_pattern + '/', LandingHandler)])
