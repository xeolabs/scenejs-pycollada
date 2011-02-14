"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys

def translate(outputStream, colladaObj, debug = False, verbose = False):
    """
      Translates a colladaObj given by PyCollada into SceneJS JSON and
      outputs the result to a stream.

      :Parameters:
        outputStream
          A writeable stream. This object can be a File, StringIO or a Socket.
        colladaObj
          Collada object given by PyCollada.
    """
    global _debug, _verbose
    _debug, _verbose = debug, verbose

    # Export libraries
    lib = { 'type': 'library', 'nodes': [] }

    if _debug:
        print "Exporting libraries..."
    for mat in colladaObj.materials:
        if _debug:
           print "Exporting material '" + mat.id + "'..."
        jsMat = translate_material(mat)
        if jsMat:
            lib['nodes'].append(jsMat)
    for geom in colladaObj.geometries:
        if _debug:
            print "Exporting geometry '" + geom.id + "'..."
        jsGeom = translate_geometry(geom)
        if jsGeom:
            lib['nodes'].append(jsGeom)

    outputStream.write(lib)

    # Export scenes
    for scene in [colladaObj.scene]:
        if _debug:
            print "Exporting scene '" + scene.id + "'..."
        jsScene = translate_scene(scene)
        if jsScene:
            outputStream.write(jsScene)

def translate_material(mat):
  print "Todo: Translate material"

"""
def _hashPrimitive(prim)
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
        'id': geom.id,
        'resource': geom.id,
    }
    for prim in geom.primitives:
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
            elif _verbose:
                print "Warning: '" + type(prim) + "' geometry type is not yet supported by the translator"
    return jsGeom

def _translate_scene_nodes(nodes):
    jsNodes = []
    for node in nodes:
        if type(node) is collada.scene.MaterialNode:
            print "Material Node!"
        elif type(node) is collada.scene.GeometryNode:
            jsNodes.append({ 'type': 'instance', 'target': node.geometry.id })
        elif type(node) is collada.scene.TransformNode:
            if node.nodes:
                jsNodes.append({ 
                    'type': 'matrix', 
                    'elements': [element for row in node.matrix for element in row],
                    'nodes': _translate_scene_nodes(node.nodes) 
                })
        elif type(node) is collada.scene.ControllerNode:
            print "Controller Node!"
        elif type(node) is collada.scene.CameraNode:
            # TODO: Cameras should be on top of the hierarchy in scenejs
            jsNodes.append({ 
                'type': 'camera',
                'optics': {
                     'type': 'perspective',
                     'fovy': node.camera.fov,
                     'aspect': 1.0, # TODO: aspect ratio is not currently available
                     'near': node.camera.near,
                     'far': node.camera.far
                }
            })
        elif type(node) is collada.scene.LightNode:
            print "Light Node!"
        elif type(node) is collada.scene.ExtraNode:
            print "Extra Node!"
        else:
            print "Unknown node"
    return jsNodes

def translate_scene(scene):
    return {
        'type': 'scene',
        'id': scene.id,
        'canvasId': 'scenejsCanvas',
        'loggingElementId': 'scenejsLog',
        'nodes': _translate_scene_nodes(scene.nodes)
    }
