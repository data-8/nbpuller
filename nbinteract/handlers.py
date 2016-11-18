"""Views for Interact application, which currently includes

- Landing : with three options for unauthenticated users (1) download zip or
            (2) authenticate and commence copying
- Progress : page containing live updates on server's progress, redirects to
             new content once pull or clone is complete
"""
import json
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
from .auth import HubAuth
from .download_file_and_redirect import download_file_and_redirect
from .git_progress import Progress
from .pull_from_github import pull_from_github

thread_pool = ThreadPoolExecutor(max_workers=4)

url_args = {
    'file': fields.Str(),

    'repo': fields.Str(),
    'path': fields.List(fields.Str()),
}


class LandingHandler(RequestHandler):
    """
    Landing page containing option to download OR (exclusive) authenticate.

    Option 1
    --------

        ?file=public_file_url

    Example: ?file=http://localhost:8000/README.md

    Authenticates, then downloads file into user's system.

    Option 2
    --------

        ?repo=data8_github_repo_name&path=file_or_folder_name&path=other_folder

    Example: ?repo=textbook&path=notebooks&path=chapter1%2Fintroduction.md

    Authenticates, then pulls content into user's file system.
    Note: Only the gh-pages branch is pulled from Github.
    """
    @use_args(url_args)
    def get(self, args):
        is_file_request = ('file' in args)
        is_git_request = ('repo' in args and 'path' in args)
        valid_request = xor(is_file_request, is_git_request)
        if not valid_request:
            self.render('404.html')

        hubauth = HubAuth(options.config)
        # authenticate() returns either a username as a string or a redirect
        redirection = username = hubauth.authenticate(self.request)
        util.logger.info("authenticate returned: {}".format(redirection))
        is_redirect = (redirection.startswith('/') or
                       redirection.startswith('http'))
        if is_redirect:
            values = []
            for k, v in args.items():
                if not isinstance(v, str):
                    v = '&path='.join(v)
                values.append('%s=%s' % (k, v))
            util.logger.info("rendering landing page")
            download_links = (util.generate_git_download_link(args)
                              if is_git_request
                              else [args['file']])
            return self.render(
                'landing.html',
                authenticate_link=redirection,
                download_links=download_links,
                query='&'.join(values))

        util.logger.info("rendering progress page")

        # These config options are passed into the `openStatusSocket`
        # JS function.
        socket_args = json.dumps({
            'is_development': options.config['DEBUG'],
            'base_url': options.config['URL'],
            'username': username,
        })

        self.render("progress.html", socket_args=socket_args)


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
        # it, so this isn't very secure.
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
                message = yield thread_pool.submit(
                    pull_from_github,
                    username=username,
                    repo_name=args['repo'],
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

    host_pattern = '.*'
    route_pattern = url_path_join(web_app.settings['base_url'], '/interact')
    web_app.add_handlers(host_pattern, [(route_pattern, LandingHandler),(route_pattern + '/', LandingHandler)])



