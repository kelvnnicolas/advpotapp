import logging
from urllib.parse import urlsplit


class RequestPathFilter(logging.Filter):
    """Keep access status/path without persisting search terms from the URL."""
    def filter(self, record):
        if record.name == 'django.server' and isinstance(record.args, tuple) and record.args:
            request_line = record.args[0]
            if isinstance(request_line, str):
                parts = request_line.split(' ', 2)
                if len(parts) == 3:
                    parts[1] = urlsplit(parts[1]).path
                    record.args = (' '.join(parts), *record.args[1:])
        return True
