"""Views for Interact application, which currently includes

- Landing : with three options for unauthenticated users (1) download zip or
            (2) authenticate and commence copying
- Progress : page containing live updates on server's progress, redirects to
             new content once pull or clone is complete
"""
import json
import os
from os.path import join, dirname
from operator import xor
from concurrent.futures import ThreadPoolExecutor
from notebook.utils import url_path_join
from nbinteract.config import config_for_env

from tornado import gen
from tornado.options import define, options
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from webargs import fields
from webargs.tornadoparser import use_args

from . import messages
from . import util
from .download_file_and_redirect import download_file_and_redirect
from .git_progress import Progress
from .pull_from_github import pull_from_github
from .config import Config

thread_pool = ThreadPoolExecutor(max_workers=4)

url_args = {
    'file': fields.Str(),

    'repo': fields.Str(),
    'branch': fields.Str(),
    'path': fields.List(fields.Str()),
}

class LandingHandler(RequestHandler):
    """
    Landing page containing option to download.

    Option 1
    --------

        ?file=public_file_url

    Example: ?file=http://localhost:8000/README.md

    Downloads file into user's system.

    Option 2
    --------

        ?repo=data8_github_repo_name&branch=branch_name_OR_DEFAULT_NAME&path=file_or_folder_name&path=other_folder

    Example: ?repo=textbook&path=notebooks&path=chapter1%2Fintroduction.md, when using default branch name

    Pulls content into user's file system.
    Note: Only the gh-pages branch is pulled from Github.
    """
    @use_args(url_args)
    def get(self, args):
        is_file_request = ('file' in args)
        is_git_request = ('repo' in args and 'path' in args) # branch name can be omitted for default value
        valid_request = xor(is_file_request, is_git_request)

        def server_extension_url(url):
            return 'nbextensions/nbinteract/' + url

        if not valid_request:
            self.render('404.html', server_extension_url=server_extension_url,)

        util.logger.info("rendering progress page")

        # These config options are passed into the `openStatusSocket`
        # JS function.
        socket_args = json.dumps({
            'is_development': options.config['DEBUG'],
            'base_url': options.config['URL'],
            'username': options.config['USERNAME'],
        })

        self.render(
            "progress.html",
            socket_args=socket_args,
            server_extension_url=server_extension_url,
        )

class RequestHandler(WebSocketHandler):
    """
    Handles the long-running websocket connection that the client makes after
    hitting the landing page.

    This is where the important parts of the logic actually happen so we don't
    block the main thread.
    """
    @gen.coroutine
    @use_args(url_args)
    def open(self, username, args):
        util.logger.info('({}) Websocket connected'.format(username))

        # We don't do validation since we assume that the LandingHandler did
        # it. TODO: ENHANCE SECURITY
        is_file_request = ('file' in args)

        try:
            if is_file_request:
                message = yield thread_pool.submit(
                    download_file_and_redirect,
                    username=username,
                    file_url=args['file'],
                    config=options.config,
                )
            else:
                if 'branch' not in args:
                    args['branch'] = Config.DEFAULT_BRANCH_NAME
                message = yield thread_pool.submit(
                    pull_from_github,
                    username=username,
                    repo_name=args['repo'],
                    branch_name=args['branch'],
                    paths=args['path'],
                    config=options.config,
                    progress=Progress(username, self.write_message)
                )

            util.logger.info('Sent message: {}'.format(message))
            self.write_message(message)
        except Exception as e:
            # If something bad happens, the client should see it
            message = messages.error(str(e))
            util.logger.error('Sent message: {}'.format(message))
            self.write_message(message)

def setup_handlers(web_app):
    env_name = 'production'
    config = config_for_env(env_name)
    define('config', config)

    settings = dict(
            debug=True,
            serve_traceback=True,
            compiled_template_cache=False,
            template_path=os.path.join(os.path.dirname(__file__), 'static/'),
            static_path=os.path.join(os.path.dirname(__file__), 'static/'),

            # Ensure static urls are prefixed with the base url too
            static_url_prefix=config['URL'] + 'static/',
        )
    web_app.settings.update(settings)

    socket_url = url_path_join(config['URL'], r'socket/(\S+)')
    host_pattern = '.*'
    route_pattern = url_path_join(web_app.settings['base_url'], '/interact')
    web_app.add_handlers(host_pattern, [
        (route_pattern, LandingHandler),
        (route_pattern + '/', LandingHandler),
        (socket_url, RequestHandler)
    ])



