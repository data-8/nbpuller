"""
Helper methods to create JSON messages to send to client over
socket. All messages have this schema:

{
    'type',
    'payload',
}
"""
from toolz.functoolz import curry

TYPES = {
  'log': 'LOG',
  'status': 'STATUS',
  'redirect': 'REDIRECT',
  'error': 'ERROR',
}


@curry
def _message(message_type, payload, error=False):
    """
    Helper function that's curried to generate the actual message functions
    """
    message = {
        'type': message_type,
        'payload': payload,
    }

    return message

log = _message(TYPES['log'])
status = _message(TYPES['status'])
redirect = _message(TYPES['redirect'])
error = _message(TYPES['error'])
