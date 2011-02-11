#! /usr/bin/env python

# Main entry point for the scenejs-pycollada translator utility.

import collada
import sys
import getopt

def main(argv):
    try:                                
        opts, args = getopt.getopt(argv, "hvd", ["help", "verbose"]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "Translate a Collada file to a JSON formatted SceneJS file"
            usage()     
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-v", "--verbose"): 
            global _verbose
            _verbose = 1

    if not args:
      print "No input files specified"
      usage();
      sys.exit(2);
    
    for filename in args:
      colladaObj = collada.Collada(filename, ignore=[collada.DaeUnsupportedError])
      for geom in col.scene.objects('geometry'):
        for prim in geom.primitives():
          for tri in prim.triangles():
            print tri.vertices

def usage():
    print "Usage: "
    print "    python scenejs-collada --help"
    print "    python scenejs-collada [OPTION]... [FILE]..."
    print ""
    print "Miscelaneous options:"
    print "  -h, --help                 Display this help message"
    print "  -v, --verbose              Display verbose warnings and translation information"
    print "  -d                         Turn on debug mode"

if __name__ == "__main__":
    main(sys.argv[1:])
