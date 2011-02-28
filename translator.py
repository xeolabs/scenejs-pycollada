"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys

def translate(output_stream, collada_obj, debug = False, verbose = False):
    """
      Translates a collada_obj given by PyCollada into SceneJS JSON and
      outputs the result to a stream.

      :Parameters:
        output_stream
          A writeable stream. This object can be a File, StringIO or a Socket.
        collada_obj
          Collada object given by PyCollada.
    """
    global _debug, _verbose
    _debug, _verbose = debug, verbose

    # Export libraries
    lib = { 'type': 'library', 'nodes': [] }

    if _debug:
        print "Exporting libraries..."
    for mat in collada_obj.materials:
        if _debug:
           print "Exporting material '" + mat.id + "'..."
        jsmat = translate_material(mat)
        if jsmat:
            lib['nodes'].append(jsmat)
    for geom in collada_obj.geometries:
        if _debug:
            print "Exporting geometry '" + geom.id + "'..."
        jsgeom = translate_geometry(geom)
        if jsgeom:
            lib['nodes'].append(jsgeom)

    output_stream.write(lib)

    # Export scenes
    for scene in [collada_obj.scene]:
        if _debug:
            print "Exporting scene '" + scene.id + "'..."
        jsscene = translate_scene(scene)
        if jsscene:
            output_stream.write(jsscene)

# Helpers
def _scalar_attribute(jsnode, key, val):
  if val:
    jsnode[key] = val

def _rgb_attribute(jsnode, key, val):
  if val:
    jsnode[key] = { 'r': val[0], 'g': val[1], 'b': val[2] }


def translate_material(mat):
    """
      Translates a collada material node into a SceneJS material node.

      :Parameters:
        geom
          An instance of the PyCollada Material class.
    """
    jsmaterial = {
        'type': 'material',
        'id': mat.id,
        'baseColor': { 'r': mat.diffuse[0], 'g': mat.diffuse[1], 'b': mat.diffuse[2] },
        # TODO: not yet supported 'reflect': mat.reflective...
        'emit': (mat.emission[0] + mat.emission[1] + mat.emission[2]) / 3.0
    }
    _scalar_attribute(jsmaterial, 'shine', mat.shininess)
    _scalar_attribute(jsmaterial, 'alpha', mat.transparency)
    _rgb_attribute(jsmaterial, 'specularColor', mat.specular)
    return jsmaterial

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
    jsgeom = {
        'type': 'geometry',
        'id': geom.id,
        'resource': geom.id,
    }

    warn_nontriangles_found = False # TEMPORARY

    for prim in geom.primitives:
        # TODO: support other primitive types
        # TODO: support nested geometry nodes
        # TODO: support flat shaded geometry (only smooth shading is currently supported)

        # TODO: Use an index buffer offset when multiple triangle sets or polygon lists are used
        #       Or possibly create multiple sub-geometries instead...
        if 'positions' in jsgeom:
            if _verbose:
                print "Warning: Multiple primitive types in one geometry is not yet supported."
            break;

        if type(prim) is collada.triangleset.TriangleSet or type(prim) is collada.polylist.PolygonList: 

            jsgeom['primitive'] = 'triangles'

            # Note: WebGL does not support multiple sources of indices when drawing primitives, 
            #       hence it is not possible to have a different position and normal streams.
            #       When a vertex is shared by two faces has multiple attributes (e.g. normals)
            #       it has to be split into multiple vertices. The following strategy is used to
            #       make this happen:
            #       When we read each vertex for every primitive, test whether the normal for 
            #       this vertex has already been used before. We do this by storing a table with 
            #       table[vertex_index] = (normal_index, next_index)
            #       If the normal index for this vertex has already been used and is different
            #       from the current normal index, continue and perform the check on table[next_index].
            #       Eventually either the same normal index will be found or next_index will be 
            #       its initial value -1. If it is -1 then we add a new entry to the table and update
            #       the last next_index to point there. We also append a new vertex position and
            #       normal.
            # TODO: support other attributes (sources) in a similar manner

            # Initialize the index mapping table for the normals
            if prim.normal != None:
                index_map = [((-1,), -1)] * len(prim.vertex)
            use_index_map = (prim.normal != None)

            #jsgeomBins = {}
            
            if not 'positions' in jsgeom:
                jsgeom['positions'] = []
            if not 'normals' in jsgeom and prim.normal != None:
                jsgeom['normals'] = []
            if not 'indices' in jsgeom:
                jsgeom['indices'] = []

            # Initialize the positions (since at least these must be present, possibly more if some vertices must be split)
            jsgeom['positions'].extend([float(val) for vert in prim.vertex for val in vert])
            if prim.normal != None:
                jsgeom['normals'].extend([0.0] * len(prim.vertex) * 3)

            # Loop through each vertex, check if it has to be split and then write the data to the relevant buffers
            if not use_index_map:
                jsgeom['indices'].extend([int(i) for prim_vert_index in prim.vertex_index for i in prim_vert_index])
            else:
                norm_index = -1
                prim_index_index = 0
                for prim_vert_index in prim.vertex_index:
                  
                     # TEMPORARY
                    if _verbose and len(prim_vert_index) != 3:
                        warn_nontriangles_found = True
                        if len(prim_vert_index) < 3: 
                            pass

                    if prim.normal != None:
                        prim_norm_index = prim.normal_index[prim_index_index]

                    # TODO for i in range(len(prim_vert_index)):
                    for i in range(min(len(prim_vert_index), 3)):
                        vert_index = prim_vert_index[i]
                        norm_index = prim_norm_index[i]

                        # Find an entry in the index_map that matches all of the indices of the other vertex attributes
                        while vert_index != -1 and index_map[vert_index][0][0] != -1 and index_map[vert_index][0] != (norm_index,):
                            prev_vert_index = vert_index
                            vert_index = index_map[vert_index][1]
                        
                        # If a new index has to be added to the index_map, then do so
                        if vert_index == -1:
                            vert_index = len(jsgeom['positions']) / 3
                            index_map[prev_vert_index] = (index_map[prev_vert_index][0], len(index_map))
                            index_map.append(((norm_index,), -1))
                            # Now add new entries for vertex attributes themselves
                            jsgeom['positions'].extend(float(p) for p in prim.vertex[prim_vert_index[i]])
                            jsgeom['normals'].extend([float(n) for n in prim.normal[prim_norm_index[i]]])
                        elif index_map[vert_index][0][0] == -1:
                            # Replace the (-1, -1, ...) entry with the correct attribute indexes tupple
                            index_map[vert_index] = ((norm_index,), -1)
                            jsgeom['normals'][vert_index*3:vert_index*3+3] = [float(n) for n in prim.normal[prim_norm_index[i]]]
                        
                        # Add the newly calculated vertex index (which may be the original one or a new one if the vertex has been split)
                        jsgeom['indices'].append(int(vert_index))
                    
                    prim_index_index += 1
        elif _verbose:
            print "Warning: '" + type(prim).__name__ + "' geometry type is not yet supported by the translator"

    if _verbose and warn_nontriangles_found:
        print "Warning: Geometry '" + geom.id + "' contains polygons that are not triangles. This is not yet supported."
    
    return jsgeom

def _translate_scene_nodes(nodes):
    """
      Recursively translates collada scene graph nodes (instantiating the nodes defined in the library).

      :Parameters:
        node
          Any node in the collada visual scene not handled by the other methods.
    """
    jsnodes = []
    for node in nodes:
        if type(node) is collada.scene.GeometryNode:
            if _verbose and len(node.materials) > 1:
                print "Warning: Geometry '" + node.geometry.id + "' has more than one material - only the first is currently used"
            jsgeometry_instance = { 'type': 'instance', 'target': node.geometry.id }
            if len(node.materials) > 0:
                jsmaterial = translate_material(node.materials[0].target)
                jsmaterial['id'] = node.geometry.id + '-' + jsmaterial['id']
                jsmaterial['nodes'] = [ jsgeometry_instance ]
                jsnodes.append(jsmaterial)
                #jsnodes.append({ 'type': 'instance', 'target': node.materials[0].target.id, 'nodes': [ jsgeometry_instance ] })
            else:
                jsnodes.append(jsgeometry_instance)
        elif type(node) is collada.scene.TransformNode:
            if node.nodes:
                jschild_nodes = _translate_scene_nodes(node.nodes)
                # Don't append the transform node unless it has children (isolated transform nodes are redundant)
                if jschild_nodes:
                    jsnodes.append({ 
                        'type': 'matrix', 
                        'elements': [element for row in node.matrix for element in row],
                        'nodes': jschild_nodes
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
                jslight = { 
                    'type': 'light',
                    'mode': mode,
                    'color': { 'r': node.light.color[0], 'g': node.light.color[1], 'b': node.light.color[2] }
                    #'diffuse': True # (default value)
                    #'specular': True # (default value)
                }
                if mode == 'point':
                    jslight['constantAttenuation'] = node.light.constant_att
                    jslight['linearAttenuation'] = node.light.linear_att
                    jslight['quadraticAttenuation'] = node.light.quad_att
                
                if mode == 'dir':
                    jslight['dir'] = {}
                    jslight['dir']['x'] = node.light.direction[0]
                    jslight['dir']['y'] = node.light.direction[1]
                    jslight['dir']['z'] = node.light.direction[2]
                jsnodes.insert(0, jslight)
        elif type(node) is collada.scene.ExtraNode:
            print "Extra Node!"
        else:
            print "Unknown node"
    return jsnodes

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
        jscamera = translate_camera(cam) 
    else:
        if _verbose:
            print "No camera found in the scene '" + scene.id + "' generating the default one."
        jscamera = {
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
    jscamera['nodes'][0]['nodes'] = _translate_scene_nodes(scene.nodes)
    
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
            'nodes': [ jscamera ]
        }]

    }

