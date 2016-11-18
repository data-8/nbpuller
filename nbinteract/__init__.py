from nbinteract.handlers import setup_handlers

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
    setup_handlers(nbapp.web_app)
