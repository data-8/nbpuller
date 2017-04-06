from nbpuller.handlers import setup_handlers

def _jupyter_server_extension_paths():
    return [{
        'module': 'nbpuller',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "notebook",
        "dest": "nbpuller",
        "src": "static",
        "require": "nbpuller/main"
    }]

def load_jupyter_server_extension(nbapp):
    setup_handlers(nbapp.web_app)
