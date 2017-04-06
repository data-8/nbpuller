from collections import deque

import git

from . import util
from . import messages


class Progress(git.RemoteProgress):
    """
    Subclass of git.RemoteProgress that is initialized with a callback that
    gets called each time it gets an update.

    The callback is called with a log message object with the current lines as
    the payload.

    We define a callback in the RequestHandler to emit updates to the socket.
    """
    def __init__(self, username, callback, max_lines=10):
        git.RemoteProgress.__init__(self)
        self.lines = deque(maxlen=max_lines)
        self.username = username
        self.callback = callback

    def _create_message(self):
        lines = list(self.lines)
        return messages.log('\n'.join(lines))

    def line_dropped(self, line):
        util.logger.info('({}) {}'.format(self.username, line))
        self.lines.append(line)
        self.callback(self._create_message())

    def update(self, *args):
        # The docs say:
        #
        #     You may read the contents of the current line in self._cur_line
        #
        # So that's what we're going to do...
        util.logger.info('({}) {}'.format(self.username, self._cur_line))
        self.lines.append(self._cur_line)
        self.callback(self._create_message())
