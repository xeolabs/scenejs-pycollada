"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys

def translate(outputStream, colladaObj, debug = 0):
    """
      Translates a colladaObj given by PyCollada into SceneJS JSON and
      outputs the result to a stream.

      :Parameters:
        outputStream
          A writeable stream. This object can be a File, StringIO or a Socket.
        colladaObj
          Collada object given by PyCollada.
    """
    global _debug
    _debug = debug

    for mat in colladaObj.scene.objects('material'):
        if _debug:
          print "Exporting material '" + mat.original.id + "'..."
        jsMat = translate_material(mat)
        outputStream.write(jsMat)
    for geom in colladaObj.scene.objects('geometry'):
        if _debug:
          print "Exporting geometry '" + geom.original.id + "'..."
        jsGeom = translate_geometry(geom)
        outputStream.write(jsGeom)
    for scene in colladaObj.scene.objects('scene'):
        if _debug:
          print "Exporting scene '" + scene.id + "'..."
        jsScene = translate_scene(scene)
        outputStream.write(jsScene)

def translate_material(mat):
  print "Todo: Translate material"

"""
def hashPrimitive(prim)
    hash = ""
    if prim.material
        hash += prim.material.id
"""

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
        # Todo: support nested geometry nodes
        if type(prim) is collada.triangleset.BoundTriangleSet or type(prim) is collada.polylist.BoundPolygonList: 
            #jsGeomBins = {}
            jsGeom['primitive'] = 'triangles'
            
            if not 'positions' in jsGeom:
                jsGeom['positions'] = []
            if not 'indices' in jsGeom:
                jsGeom['indices'] = []

            i = 0
            
            if type(prim) is collada.triangleset.BoundTriangleSet:
                for tri in prim.triangles():                
                    jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
                    jsGeom['indices'].extend([3 * i + 0, 3 * i + 1, 3 * i + 2])
                    i += 1
            elif type(prim) is collada.polylist.BoundPolygonList:
                for poly in prim.polygons():
                    for tri in poly.triangles():
                        jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
                        jsGeom['indices'].extend([3 * i + 0, 3 * i + 1, 3 * i + 2])
                        i += 1

    return jsGeom

def translate_scene(scene):
  print "Todo: Translate scene"

