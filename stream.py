"""
Wraps a stream object (a file, string or network socket) in order to convert
python dictionary objects into the appropriate format (ascii, binary etc...)
"""

try: import simplejson as json
except ImportError: import json

class ScenejsJsonStream:
    """Wraps a stream object in order to produce ascii json"""

    # File name extension to use for this type of stream
    fileExtension = "json"

    def __init__(self, streamObj):
        """Create a JSON output stream

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        self.streamObj = streamObj

    def write(self, node):
        json.dump(node, self.streamObj)
        self.streamObj.write('\n');


class ScenejsJavascriptStream:
    """Wraps a stream object in order to produce javascript code (which creates all nodes in the file)"""

    # File name extension to use for this type of stream
    fileExtension = "js"

    def __init__(self, streamObj):
        """Create a JSON output stream

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        self.streamObj = streamObj

    def write(self, node):
        """Create a Javascript output stream, where nodes are automatically created via SceneJS.createNode

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        self.streamObj.write("SceneJS.createNode(" + json.dumps(node) + ");\n")


class ScenejsBinaryStream:
    """Wraps a stream object in order to produce javascript code (which creates all nodes in the file)"""

    # File name extension to use for this type of stream
    fileExtension = "js"
    
    """
    TODO: Add output streams for additional binary files
    """

    def __init__(self, streamObj):
        """Create a JSON output stream

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        self.streamObj = streamObj

    def write(self, node):
        """Create several binary output streams, where nodes are automatically created via SceneJS.createNode

        :Parameters:
          streamObj
            A file, string IO or network socket object
        """
        print "Todo: Binary formatted output is not yet supported..."

