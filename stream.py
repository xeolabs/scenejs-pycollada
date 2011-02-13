"""
Wraps a stream object (a file, string or network socket) in order to convert
python dictionary objects into the appropriate format (ascii, binary etc...)
"""

try: import simplejson as json
except ImportError: import json

class ScenejsJsonStream:
    """Wraps a stream object in order to produce ascii json"""

    def __init__(self, streamObj):
        """Create a JSON output stream

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        self.streamObj = streamObj

    def write(self, node):
        json.dump(node, self.streamObj)

