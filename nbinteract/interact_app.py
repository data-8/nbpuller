import os
import tornado.web
from tornado.options import define

from .handlers import LandingHandler, RequestHandler


class InteractApp(tornado.web.Application):
    """
    Entry point for the interact app.
    """
    def __init__(self, config=None):
        # Terrible hack to get config object in global namespace. This allows
        # us to use options.config to get the global config object.
        #
        # TODO(sam): Replace with a better solution
        define('config', config)

        # Assumes config['URL'] has a trailing slash
        base_url = config['URL']
        base_url_without_slash = base_url[:-1]
        socket_url = base_url + r'socket/(\S+)'

        handlers = [
            (base_url, LandingHandler),
            (base_url_without_slash, LandingHandler),
            (socket_url, RequestHandler),
        ]

        settings = dict(
            debug=True,
            serve_traceback=True,
            compiled_template_cache=False,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),

            # Ensure static urls are prefixed with the base url too
            static_url_prefix=config['URL'] + 'static',
        )

        super(InteractApp, self).__init__(handlers, **settings)
