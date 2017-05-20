import os

from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from tornado.gen import sleep
from tornado.options import options
from tornado import process

from .pull_from_remote import pull_from_remote
from . import messages
from . import util

INTERVAL_DELAY = 10

def loop_auto_pulling(thread_pool):
    @coroutine
    def auto_pull_wrapper():
        while True:
            yield auto_pull(thread_pool)
            yield sleep(INTERVAL_DELAY)

    ioloop = IOLoop.current().spawn_callback(auto_pull_wrapper)


@coroutine
def auto_pull(thread_pool):
    if os.path.exists(options.config["AUTO_PULL_LIST_FILE_NAME"]):
        util.logger.info('Starting pull loop...')

        auto_pull_file = open(options.config["AUTO_PULL_LIST_FILE_NAME"], 'r')
        with auto_pull_file as auto_file:
            existing_pulls = [line.strip().split(',') for line in auto_file.readlines()]
        for pull in existing_pulls:
            yield thread_pool.submit(
                    pull_from_remote,
                    username='jovian',
                    repo_name=pull[0],
                    domain=pull[1],
                    account=pull[2],
                    branch_name=pull[3],
                    paths=['README.md'],
                    config=options.config,
                    notebook_path='',
                    progress=None
                )
        util.logger.info('Finished pull loop...')
    else:
        util.logger.info('Auto pull file does not exist')

