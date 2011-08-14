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
        """Create a Javascript output stream, where nodes are automatically created via SceneJS.createScene

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        try:
            self.streamobj.write("SceneJS.createScene(" + json.dumps(node) + ");\n")
        except TypeError as e:
            print "ERROR: " + str(e)

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
    
    def _pretty_print_value(self, v, indent):
        """Pretty prints a single value

        :Parameters:
          node
            A dictionary object containing the scene data
          indent
            The indentation level
        """
        if isinstance(v, list):
            output = "[\n" if len(v) > 0 and isinstance(v[0], dict) else "["
            for lv in v:
                output += self._pretty_print_value(lv, indent)
                if isinstance(lv, dict): 
                    output += "\n" 
            output += ("    " * indent + "],") if len(v) > 0 and isinstance(v[0], dict) else "],"
            return output
        elif isinstance(v, dict):
            output = "    " * (indent+1) + "{\n" 
            for s in self._pretty_print(v, indent+2):
                output += s
            output += "    " * (indent+1) + "},"
            return output
        elif isinstance(v, str):
            return "'" + v + "',"
        elif isinstance(v, bool):
            return "true, " if v else "false, "
        else:
            return str(v) + ","
    
    def _pretty_print(self, node, indent):
        """Prints the dictionary as a readable JavaScript Object instead of raw JSON

        :Parameters:
          node
            A dictionary object containing the scene data
          indent
            The indentation level
        """
        # TODO: This function should also order the keys in a logical way...
        for k,v in node.items():
            output = "    " * indent + k + (":\n" if isinstance(v,dict) else ": ")
            yield output + self._pretty_print_value(v, indent) + "\n"
    
    def write(self, node):
        """Create a Javascript output stream, where nodes are automatically created via SceneJS.createScene

        :Parameters:
          streamobj
            A file, string IO or network socket object
          node
            A dictionary object containing the scene data
        """
        self.streamobj.write("SceneJS.createScene({\n")
        for s in self._pretty_print(node, 1):
            self.streamobj.write(s)
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
        """Create several binary output streams

        :Parameters:
          streamobj
            A file, string IO or network socket object
        """
        print "Todo: Binary formatted output is not yet supported..."

