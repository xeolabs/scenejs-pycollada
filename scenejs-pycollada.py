#! /usr/bin/env python

# Main entry point for the scenejs-pycollada translator utility.

import collada
import sys
import getopt
import os.path
from translator import translate
from stream import ScenejsJsonStream, ScenejsJavascriptStream, ScenejsPrettyJavascriptStream, ScenejsBinaryStream
from sample import generate_html_head, generate_html_body

def main(argv):
    # Get the command-line options given to the program
    try:                                
        opts, args = getopt.getopt(argv, 'hvdpo:', ['help', 'verbose', 'pretty-print', 'output=', 'libraries-only', 'detailed', 'tabsize=']) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)
    
    debug = False
    verbose = False
    generate_sample = False
    embed_in_html = False
    libraries_only = False
    pretty_print = False
    detailed = False
    tabsize = None
    output_format = ScenejsJavascriptStream

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print "Translate a Collada file to a JSON formatted SceneJS file"
            usage()     
            sys.exit()
        elif opt == '-d':
            debug = True
        elif opt in ('-o', '--output'):
            try: 
                output_format = { 
                  'json':   ScenejsJsonStream,
                  'js':     ScenejsJavascriptStream,
                  'binary': ScenejsBinaryStream,
                  'html':   ScenejsJavascriptStream,
                  'htmljs': ScenejsJavascriptStream
                }[arg]
                if arg == 'htmljs':
                    generate_sample = True
                elif arg == 'html':
                    generate_sample = True
                    embed_in_html = True
            except KeyError:
                print "Unknown output format '" + arg + "'"
                usage()
                sys.exit(2)
        elif opt in ('-v', '--verbose'): 
            verbose = True
        elif opt in ('-p', '--pretty-print'): 
            pretty_print = True
        elif opt == '--libraries-only':
            libraries_only = True
        elif opt == '--detailed':
            detailed = True
        else:
            print "Unknown option supplied '" + opt + "'"
            usage()
            sys.exit(2)

    if pretty_print and output_format == ScenejsJavascriptStream:
        output_format = ScenejsPrettyJavascriptStream

    # Check arguments for additional caveats
    if not args:
        print "No input files specified"
        usage()
        sys.exit(2)

    if pretty_print and output_format != ScenejsPrettyJavascriptStream:
        print "Warning: Pretty print is only available with JavaScript output at this time"

    if detailed and generate_sample != True:
        print "Warning: The --detailed flag has no effect when no sample is being generated"

    if tabsize != None and not pretty_print:
        print "Warning: The --tabsize flag has no effect without the --pretty_print flag"

    #if generate_sample and not libraries_only and len(args) > 1
    #    print "Cannot generate a sample for multiple input files without the --libraries-only option."
    #    usage()
    #    sys.exit(2)

    # Generate an Html file if required
    html_output_stream = open('index.html','w') if generate_sample else None
    if verbose and html_output_stream:
        print "Created the sample file 'index.html'"

    # Write Html header if required
    if html_output_stream:
        html_output_stream.write(generate_html_head("SceneJS sample", detailed))

    # Load and translate each file specified
    scene_ids = []
    for filename in args:
        # Check whether the file exists and try to load it into a collada object
        if not os.path.isfile(filename):
            print "'" + filename + "' is not a valid file path."
            sys.exit(2)
        collada_obj = collada.Collada(filename, ignore=[collada.DaeUnsupportedError])

        # Add every scene's id to the list of al scene ids (to be used with sample generation)
        scene_ids.append(collada_obj.scene.id)
        
        # Generate an output stream
        base_path = os.path.splitext(filename)[0]
        output_stream = None
        if embed_in_html and html_output_stream:
            # Output should continue in the html file
            output_stream = html_output_stream
        else:
            # Create an output file to write the SceneJS scene to
            output_file_name = base_path + '.' + output_format.file_extension
            output_stream = open(output_file_name,'w')
            if verbose and output_stream:
                print "Created the file '" + output_file_name + "'"

        # Translate and output the file
        if html_output_stream:
            if embed_in_html:
                html_output_stream.write("    <script type='text/javascript'>\n")
            else:
                html_output_stream.write("    <script type='text/javascript' src='" + output_file_name + "'></script>\n")

        print output_format
        serializer = output_format(output_stream)
        #TODO: serializer.tabstring = ' ' * tabsize if tabsize else "    "
        translate(serializer, collada_obj, debug, verbose)

        if html_output_stream and embed_in_html:
           html_output_stream.write("</script>\n\n")
    
    output_stream.flush()

    if html_output_stream and len(scene_ids) > 0:
        # Todo: support multiple scenes in a sample file... (via a html drop-down)
        html_output_stream.write(generate_html_body(scene_ids[0] if not libraries_only else None))
        html_output_stream.flush()

def usage():
    print "Usage: "
    print "    python scenejs-collada --help"
    print "    python scenejs-collada [OPTION]... [FILE]..."
    print ""
    print "Miscelaneous options:"
    print "  -h, --help                     Display this help message"
    print "  -v, --verbose                  Display verbose warnings and translation information"
    print "  -p, --pretty-print             Pretty print the output"
    print "  --libraries-only               Export only libraries, excluding scenes"
    print "  --geometry-only                TODO: export only geometry"
    print "  --geometry-materials           TODO: geometry and materials only"
    print "  -o [FORMAT], --output=[FORMAT] Use the specified output mode, FORMAT may be any one of the following"
    print "                                 json   - Raw JSON data is output"
    print "                                 js     - JavaScript code is output and nodes created"
    print "                                 binary - Output JavaScript code along with accompanying binary"
    print "                                 html   - Output JavaScript code inside an html file"
    print "                                 htmljs - Output JavaScript code separately along with an html file"
    print "  --detailed                     When generating a sample, use the detailed template"
    print "  -d                             Turn on debug mode"

if __name__ == "__main__":
    main(sys.argv[1:])
