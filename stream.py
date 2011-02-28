"""
Wraps a stream object (a file, string or network socket) in order to convert
python dictionary objects into the appropriate format (ascii, binary etc...)
"""

try: import simplejson as json
except ImportError: import json

class ScenejsJsonStream:
    """Wraps a stream object in order to produce ascii json"""

    # File name extension to use for this type of stream
    file_extension = "json"

    def __init__(self, streamobj):
        """Create a JSON output stream

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        self.streamobj = streamobj

    def write(self, node):
        json.dump(node, self.streamobj)
        self.streamobj.write('\n');


class ScenejsJavascriptStream:
    """Wraps a stream object in order to produce JavaScript code (which creates all nodes in the file)"""

    # File name extension to use for this type of stream
    file_extension = "js"

    def __init__(self, streamobj):
        """Create a JSON output stream

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        self.streamobj = streamobj

    def write(self, node):
        """Create a Javascript output stream, where nodes are automatically created via SceneJS.createNode

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        self.streamobj.write("SceneJS.createNode(" + json.dumps(node) + ");\n")

class ScenejsPrettyJavascriptStream:
    """Wraps a stream object in order to produce readable JavaScript code (which creates all nodes in the file)"""

    # File name extension to use for this type of stream
    file_extension = "js"
    
    def __init__(self, streamobj):
        """Create a JSON output stream

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        self.streamobj = streamobj
    
    def _pretty_print(self, node, indent):
        """Prints the dictionary as a readable JavaScript Object instead of raw JSON

        :Parameters:
          node
            A dictionary object containing the scene data
        """
        # TODO: This function should also order the keys in a logical way...

        #for (k,v) in node:
        for n in node:
            yield "    " * indent + str(n)
            #yield k + ": " + str(v)
    
    def write(self, node):
        """Create a Javascript output stream, where nodes are automatically created via SceneJS.createNode

        :Parameters:
          streamobj
            A file, string IO or network socket object
          node
            A dictionary object containing the scene data
        """
        self.streamobj.write("SceneJS.createNode({\n")
        for s in self._pretty_print(node, 1):
            self.streamobj.write(s + ",\n")
        self.streamobj.write("});\n")

class ScenejsBinaryStream:
    """Wraps a stream object in order to produce JavaScript code (which creates all nodes in the file)"""

    # File name extension to use for this type of stream
    file_extension = "js"
    
    """
    TODO: Add output streams for additional binary files
    """

    def __init__(self, streamobj):
        """Create a JSON output stream

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        self.streamobj = streamobj

    def write(self, node):
        """Create several binary output streams, where nodes are automatically created via SceneJS.createNode

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        print "Todo: Binary formatted output is not yet supported..."

