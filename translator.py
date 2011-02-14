"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys

def translate(outputStream, colladaObj):
    """
      Translates a colladaObj given by PyCollada into SceneJS JSON and
      outputs the result to a stream.

      :Parameters:
        outputStream
          A writeable stream. This object can be a File, StringIO or a Socket.
        colladaObj
          Collada object given by PyCollada.
    """

    for geom in colladaObj.scene.objects('geometry'):
        jsGeom = translate_geometry(geom)
        outputStream.write(jsGeom)

def translate_geometry(geom):
    """
      Translates a collada geometry node into one or more SceneJS geometry nodes
    """
    jsGeom = {
        'type': 'geometry',
        'id': geom.original.id,
        'resource': geom.original.id,
    }
    for prim in geom.primitives():
        # Todo: support other primitive types
        if type(prim) is collada.triangleset.BoundTriangleSet or type(prim) is collada.polylist.BoundPolygonList: 
            jsGeom['primitive'] = 'triangles'
            
            if not 'positions' in jsGeom:
                jsGeom['positions'] = []
            
            if type(prim) is collada.triangleset.BoundTriangleSet:
                for tri in prim.triangles():                
                    jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
            elif type(prim) is collada.polylist.BoundPolygonList:
                for poly in prim.polygons():
                    for tri in poly.triangles():
                        jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
      
    return jsGeom

