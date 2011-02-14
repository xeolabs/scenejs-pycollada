#! /usr/bin/env python

# Main entry point for the scenejs-pycollada translator utility.

import collada
import sys
import getopt
import os.path
from translator import translate
from stream import ScenejsJsonStream, ScenejsJavascriptStream, ScenejsBinaryStream
from sample import generate_html_head, generate_html_body

def main(argv):
    # Get the command-line options given to the program
    try:                                
        opts, args = getopt.getopt(argv, 'hvdo:', ['help', 'verbose', 'output=', 'libraries-only']) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)
    
    debug = False
    verbose = False
    generateSample = False
    embedInHtml = False
    librariesOnly = False
    outputFormat = ScenejsJavascriptStream

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print "Translate a Collada file to a JSON formatted SceneJS file"
            usage()     
            sys.exit()
        elif opt == '-d':
            debug = True
        elif opt in ('-o', '--output'):
            try: 
                outputFormat = { 
                  'json':   ScenejsJsonStream,
                  'js':     ScenejsJavascriptStream,
                  'binary': ScenejsBinaryStream,
                  'html':   ScenejsJavascriptStream,
                  'htmljs': ScenejsJavascriptStream
                }[arg]
                if arg == 'htmljs':
                    generateSample = True
                elif arg == 'html':
                    generateSample = True
                    embedInHtml = True
            except KeyError:
                print "Unknown output format '" + arg + "'"
                usage()
                sys.exit(2)
        elif opt in ('-v', '--verbose'): 
            verbose = True
        elif opt == '--libraries-only':
            librariesOnly = True
        else:
            print "Unknown option supplied '" + opt + "'"
            usage()
            sys.exit(2)

    if not args:
        print "No input files specified"
        usage()
        sys.exit(2)

    #if generateSample and not librariesOnly and len(args) > 1
    #    print "Cannot generate a sample for multiple input files without the --libraries-only option."
    #    usage()
    #    sys.exit(2)

    # Generate an Html file if required
    htmlOutputStream = open('index.html','w') if generateSample else None
    if verbose and htmlOutputStream:
        print "Created the sample file 'index.html'"

    # Write Html header if required
    if htmlOutputStream:
        htmlOutputStream.write(generate_html_head("SceneJS sample"))

    # Load and translate each file specified
    for filename in args:
        # Check whether the file exists and try to load it into a collada object
        if not os.path.isfile(filename):
            print "'" + filename + "' is not a valid file path."
            sys.exit(2)
        colladaObj = collada.Collada(filename, ignore=[collada.DaeUnsupportedError])
        
        # Generate an output stream
        basePath = os.path.splitext(filename)[0]
        outputStream = None
        if embedInHtml and htmlOutputStream:
            # Output should continue in the html file
            outputStream = htmlOutputStream
        else:
            # Create an output file to write the SceneJS scene to
            outputFileName = basePath + '.' + outputFormat.fileExtension
            outputStream = open(outputFileName,'w')
            if verbose and outputStream:
                print "Created the file '" + outputFileName + "'"

        # Translate and output the file
        if htmlOutputStream:
            if embedInHtml:
                htmlOutputStream.write("<script type='text/javascript'>\n")
            else:
                htmlOutputStream.write("<script type='text/javascript' src='" + outputFileName + "'>\n")

        translate(outputFormat(outputStream), colladaObj, debug, verbose)

        if htmlOutputStream:
           htmlOutputStream.write("</script>\n\n")
    
    outputStream.flush()

    if htmlOutputStream:
        htmlOutputStream.write(generate_html_body())
        htmlOutputStream.flush()

def usage():
    print "Usage: "
    print "    python scenejs-collada --help"
    print "    python scenejs-collada [OPTION]... [FILE]..."
    print ""
    print "Miscelaneous options:"
    print "  -h, --help                     Display this help message"
    print "  -v, --verbose                  Display verbose warnings and translation information"
    print "  --libraries-only               Export only libraries, excluding scenes"
    print "  --geometry-only                TODO: export only geometry"
    print "  --geometry-materials           TODO: geometry and materials only"
    print "  -o [FORMAT], --output=[FORMAT] Use the specified output mode, FORMAT may be any one of the following"
    print "                                 json   - Raw JSON data is output"
    print "                                 js     - JavaScript code is output and nodes created"
    print "                                 binary - Output JavaScript code along with accompanying binary"
    print "                                 html   - Output JavaScript code inside an html file"
    print "                                 htmljs - Output JavaScript code separately along with an html file"
    print "  -d                             Turn on debug mode"

if __name__ == "__main__":
    main(sys.argv[1:])
