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

# Helpers
def _scalarAttribute(jsNode, key, val):
  if val:
    jsNode[key] = val

def _rgbAttribute(jsNode, key, val):
  if val:
    jsNode[key] = { 'r': val[0], 'g': val[1], 'b': val[2] }


def translate_material(mat):
    """
      Translates a collada material node into a SceneJS material node.

      :Parameters:
        geom
          An instance of the PyCollada Material class.
    """
    jsMaterial = {
        'type': 'material',
        'id': mat.id,
        'baseColor': { 'r': mat.diffuse[0], 'g': mat.diffuse[1], 'b': mat.diffuse[2] },
        # TODO: not yet supported 'reflect': mat.reflective...
        'emit': (mat.emission[0] + mat.emission[1] + mat.emission[2]) / 3.0
    }
    _scalarAttribute(jsMaterial, 'shine', mat.shininess)
    _scalarAttribute(jsMaterial, 'alpha', mat.transparency)
    _rgbAttribute(jsMaterial, 'specularColor', mat.specular)
    return jsMaterial

"""
def _hashPrimitive(prim)
    hash = ""
    if prim.material
        hash += prim.material.id
"""

def translate_geometry(geom):
    """
      Translates a collada geometry node into one or more SceneJS geometry nodes.

      :Parameters:
        geom
          An instance of the PyCollada Geometry class.
    """
    jsGeom = {
        'type': 'geometry',
        'id': geom.id,
        'resource': geom.id,
    }
    for prim in geom.primitives:
        # Todo: support other primitive types
        # Todo: support nested geometry nodes
        if type(prim) is collada.triangleset.TriangleSet or type(prim) is collada.polylist.PolygonList: 
            #jsGeomBins = {}
            jsGeom['primitive'] = 'triangles'
            
            if not 'positions' in jsGeom:
                jsGeom['positions'] = []
            if not 'normals' in jsGeom:
                jsGeom['normals'] = []
            if not 'indices' in jsGeom:
                jsGeom['indices'] = []

            # old: i = 0

            # todo: increase indices if necessary (but probably create multiple sub-geometries instead)
            
            if type(prim) is collada.triangleset.TriangleSet:
                jsGeom['positions'].extend([float(val) for vert in prim.vertex for val in vert])
                jsGeom['normals'].extend([float(val) for norm in prim.normal for val in norm])
                jsGeom['indices'].extend([int(i) for i in prim.indices])
                # todo: jsGeom['uv']
                # old:
                #for tri in prim.triangles():                
                #    jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
                #    jsGeom['indices'].extend([3 * i + 0, 3 * i + 1, 3 * i + 2])
                #    i += 1
            elif type(prim) is collada.polylist.PolygonList:
                jsGeom['positions'].extend([float(val) for vert in prim.vertex for val in vert])
                jsGeom['normals'].extend([float(val) for norm in prim.normal for val in norm])
                jsGeom['indices'].extend([int(i) for i in prim.indices])
                # todo: jsGeom['uv']
                # old:
                #for poly in prim.polygons():
                #    for tri in poly.triangles():
                #        jsGeom['positions'].extend([val for vert in tri.vertices for val in vert])
                #        jsGeom['indices'].extend([3 * i + 0, 3 * i + 1, 3 * i + 2])
                #        i += 1
            elif _verbose:
                print "Warning: '" + type(prim).__name__ + "' geometry type is not yet supported by the translator"
    return jsGeom

def _translate_scene_nodes(nodes):
    """
      Recursively translates collada scene graph nodes (instantiating the nodes defined in the library).

      :Parameters:
        node
          Any node in the collada visual scene not handled by the other methods.
    """
    jsNodes = []
    for node in nodes:
        #if type(node) is collada.scene.MaterialNode:
        #    print "TODO: Material Node!"
        if type(node) is collada.scene.GeometryNode:
            if _verbose and len(node.materials) > 1:
                print "Warning: Geometry '" + node.geometry.id + "' has more than one material - only the first is used"
            jsGeometryInstance = { 'type': 'instance', 'target': node.geometry.id }
            if len(node.materials) > 0:
                jsMaterial = translate_material(node.materials[0].target)
                jsMaterial['nodes'] = [ jsGeometryInstance ]
                jsNodes.append(jsMaterial)
                #jsNodes.append({ 'type': 'instance', 'target': node.materials[0].target.id, 'nodes': [ jsGeometryInstance ] })
            else:
                jsNodes.append(jsGeometryInstance)
        elif type(node) is collada.scene.TransformNode:
            if node.nodes:
                jsChildNodes = _translate_scene_nodes(node.nodes)
                # Don't append the transform node unless it has children (isolated transform nodes are redundant)
                if jsChildNodes:
                    jsNodes.append({ 
                        'type': 'matrix', 
                        'elements': [element for row in node.matrix for element in row],
                        'nodes': jsChildNodes
                    })
        elif type(node) is collada.scene.ControllerNode:
            print "Controller Node!"
        elif type(node) is collada.scene.CameraNode:
            # TODO: Cameras should be on top of the hierarchy in scenejs
            pass
        elif type(node) is collada.scene.LightNode:
            mode = None 
            if type(node.light) is collada.light.AmbientLight or type(node.light) is collada.light.BoundAmbientLight:
                mode = 'ambient'
            elif type(node.light) is collada.light.PointLight or type(node.light) is collada.light.BoundPointLight:
                mode = 'point'
            elif type(node.light) is collada.light.SunLight or type(node.light) is collada.light.BoundSunLight:
                mode = 'dir'
            elif _verbose:
                print "Warning: Unknown light mode '" + type(node.light).__name__ + "'"
            if mode:
                jsLight = { 
                    'type': 'light',
                    'mode': mode,
                    'color': { 'r': node.light.color[0], 'g': node.light.color[1], 'b': node.light.color[2] }
                    #'diffuse': True # (default value)
                    #'specular': True # (default value)
                }
                if mode == 'point':
                    jsLight['constantAttenuation'] = node.light.constant_att
                    jsLight['linearAttenuation'] = node.light.linear_att
                    jsLight['quadraticAttenuation'] = node.light.quad_att
                
                if mode == 'dir':
                    jsLight['dir'] = {}
                    jsLight['dir']['x'] = node.light.direction[0]
                    jsLight['dir']['y'] = node.light.direction[1]
                    jsLight['dir']['z'] = node.light.direction[2]
                jsNodes.insert(0, jsLight)
        elif type(node) is collada.scene.ExtraNode:
            print "Extra Node!"
        else:
            print "Unknown node"
    return jsNodes

def translate_camera(camera):
    """
      Translates a collada camera into SceneJS lookAt and camera nodes.
    """
    return {
        'type': 'lookAt',
        'eye': { 'x': camera.position[0], 'y': camera.position[1], 'z': camera.position[2] },
        'look': { 'x': camera.position[0] + camera.direction[0], 'y': camera.position[1] + camera.direction[1], 'z': camera.position[2] + camera.direction[2] },
        'up': { 'x': camera.up[0], 'y': camera.up[1], 'z': camera.up[2] },
        'nodes': [{ 
            'type': 'camera',
            'optics': {
                 'type': 'perspective', #TODO: type of camera can't be retrieved a.t.m. assuming "perspective" for now
                 'fovy': camera.fov,
                 'aspect': 1.0, # TODO: aspect ratio is not currently available
                 'near': camera.near,
                 'far': camera.far
            }
        }]
    }

def translate_scene(scene):
    """
      Translates collada scene graph hierarchy into a SceneJS scene graph.
      This makes some changes to the hierarchy, such as placing camera nodes above visual nodes.
    """
    cameras = scene.objects('camera')
    cam = cameras.next()
    if cam:
        jsCamera = translate_camera(cam) 
    else:
        if _verbose:
            print "No camera found in the scene '" + scene.id + "' generating the default one."
        jsCamera = {
            'type': 'lookAt',
            'eye': { 'x': 0.0, 'y': 0.0, 'z': 0.0 },
            'look': { 'x': 0.0, 'y': 0.0, 'z': 1.0 },
            'up': { 'x': 0.0, 'y': 1.0, 'z': 0.0 },
            'nodes': [{ 
                'type': 'camera',
                'optics': {
                     'type': 'perspective',
                     'fovy': 60.0,
                     'aspect': 1.0,
                     'near': 0.1,
                     'far': 10000.0
                },
                'nodes': []
            }]
        }
    jsCamera['nodes'][0]['nodes'] = _translate_scene_nodes(scene.nodes)
    
    return {
        'type': 'scene',
        'id': scene.id,
        'canvasId': 'scenejsCanvas',
        'loggingElementId': 'scenejsLog',
        'nodes': [{
            'type': 'renderer',
            'clear': {
                'depth': True,
                'color': True,
                'stencil': False
            },
            'clearColor': { 'r': 0.4, 'g': 0.4, 'b': 0.4 },
            'nodes': [ jsCamera ]
        }]

    }

