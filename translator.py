"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys
from numpy import array, append, array_equal

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
def _float_attribute(jsnode, key, val):
  if not val or type(val) is not float:
    return False
  jsnode[key] = val
  return True

def _rgb_attribute(jsnode, key, val):
  if not val or type(val) is not tuple:
    return False
  jsnode[key] = { 'r': val[0], 'g': val[1], 'b': val[2] }    
  return True

def translate_material(mat):
    """
      Translates a collada material node into a SceneJS material node.

      :Parameters:
        geom
          An instance of the PyCollada Material class.
    """
    jstexture = {
        'type': 'texture'
    }
    jsmaterial = {
        'type': 'material',
        'id': mat.id
    }
    if not _rgb_attribute(jsmaterial, 'baseColor', mat.diffuse):
        _rgb_attribute(jsmaterial, 'baseColor', (0.5,0.5,0.5))
        if type(mat.diffuse) is collada.material.Map:
            print "TODO: BUSY HERE (create a texture)"
        elif _verbose:
            print "Unknown diffuse colour input: " + str(mat.diffuse)
    _rgb_attribute(jsmaterial, 'specularColor', mat.specular)
    _float_attribute(jsmaterial, 'shine', mat.shininess)
    _float_attribute(jsmaterial, 'alpha', mat.transparency)
    if mat.emission and type(mat.emission) is tuple:
        jsmaterial['emit'] = (mat.emission[0] + mat.emission[1] + mat.emission[2]) / 3.0
    # TODO: not yet supported 'reflect': mat.reflective...
    return jsmaterial

"""
def _hashPrimitive(prim)
    hash = ""
    if prim.material
        hash += prim.material.id
"""

# Helpers for translate_geometry
#def match_index_indices(index_entry, indexes):
#    return True

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
    
    # OLD: 
    #jssubgeom = {}
    #jssubgeom['triangles'] = {
    #    'type': 'geometry',
    #    'primitive': 'triangles',
    #    'id': geom.id,
    #    'resource': geom.id,
    #    'indices': []
    #}
    #
    ## Note: lines and triangles will share the same resource id as they may share vertices
    #jssubgeom['lines'] = {
    #    'type': 'geometry',
    #    'primitive': 'lines',
    #    'id': geom.id + '-lines',
    #    'resource': geom.id,
    #    'indices': []
    #}
    
    # TODO: Point geometry is not currently supported due to the limitations of the Collada format (also see the notes lower down in this function)
    ## Note: a new resource id is created for point clouds since it usually does not make much sense to use indices with points
    ##       it is possible that points may share vertices with polygons or lines but this feature is unlikely to be supported by
    ##       exporters (such as blender). Blender currently exports points without any indexes...
    #jssubgeom['points'] = {
    #    'type': 'geometry',
    #    'primitive': 'points'
    #    'id': geom.id + '-points',
    #    'resource': geom.id + '-points',
    #    'vertices': []
    #}
    jssubgeoms = []

    c_subgeom = 0
    for prim in geom.primitives:
        # TODO: support other primitive types (<polygons>, <trifans>, <tristrips>, <linestrips>)
        jssubgeom = {
            'type': 'geometry',
            'id': geom.id + str(c_subgeom),
            'resource': geom.id,
            'indices': []
        }
        c_subgeom += 1

        if type(prim) is collada.triangleset.TriangleSet \
              or type(prim) is collada.polylist.PolygonList \
              or type(prim) is collada.lineset.LineSet:

            jssubgeom['primitive'] = 'lines' if type(prim) is collada.lineset.LineSet else 'triangles'

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

            # Initialize the index mapping table for vertex attributes

            # OLD:
            #if prim.normal != None or (prim.texcoordset != None and len(prim.texcoordset) > 0):
            #    packed_empty_index = pack_indices(-1 if prim.normal != None else None,\
            #                                      -1 if prim.texcoordset != None and len(prim.texcoordset) > 0 else None)
            #    #                                 (-1,) if prim.texcoordset != None and len(prim.texcoordset) > 0 else None)
            #    index_map = [(packed_empty_index, -1)] * len(prim.vertex)
            num_index_elems = 1 + (1 if prim.normal != None else 0) + (1 if prim.texcoordset != () else 0)
            index_map = array([[-1] * num_index_elems] * len(prim.vertex))
            use_index_map = (prim.normal != None or (prim.texcoordset != None and len(prim.texcoordset) > 0))
            
            # Initialize jsgeom structure
            if not 'positions' in jsgeom:
                jsgeom['positions'] = []
            if not 'normals' in jsgeom and prim.normal != None:
                jsgeom['normals'] = []
            if not 'uv' in jsgeom and prim.texcoordset != None and len(prim.texcoordset) > 0:
                jsgeom['uv'] = []

            # Initialize the positions (since at least these must be present, possibly more if some vertices must be split)
            jsgeom['positions'].extend([float(val) for vert in prim.vertex for val in vert])
            if prim.normal != None:
                jsgeom['normals'].extend([0.0] * len(prim.vertex) * 3)
            if prim.texcoordset != None and len(prim.texcoordset) > 0:
                jsgeom['uv'].extend([0.0] * len(prim.vertex) * 2)

            # Create a polyindex regardless of the underlying geometry
            polyindex = None
            if type(prim) is collada.triangleset.TriangleSet:
                #polyindex = (array([3 * x, 3 * x + 3]) for x in range(0, len(prim.vertex)))
                polyindex = (array([3 * x, 3 * x + 3]) for x in range(0, prim.ntriangles))
            elif type(prim) is collada.lineset.LineSet:
                #polyindex = (array([2 * x, 2 * x + 2]) for x in range(0, len(prim.vertex)))
                polyindex = (array([2 * x, 2 * x + 2]) for x in range(0, prim.nlines))
            elif type(prim) is collada.polylist.PolygonList:
                polyindex = prim.polyindex

            # Ensure that the index is always correctly shaped
            primindex = None
            if type(prim) is collada.lineset.LineSet or type(prim) is collada.triangleset.TriangleSet:
                primindex = prim.index.copy()
                primindex.resize((len(prim.index.flat)/2, 2))
            else:
                primindex = prim.index

            # Loop through each vertex, check if it has to be split and then write the data to the relevant buffers
            if not use_index_map:
                jssubgeom['indices'].extend([int(i) for prim_vert_index in prim.vertex_index for i in prim_vert_index])
            else:
                norm_index = -1
                prim_index_index = 0
                #for prim_poly_index in polyindex:
                #    print range(prim_poly_index[0], prim_poly_index[1])
                #print polyindex
                for prim_poly_index in polyindex:
                    #prim_norm_index = prim.normal_index[prim_index_index] if prim.normal != None else None
                    #prim_texcoord_indexset = prim.texcoord_indexset[0][prim_index_index] if prim.texcoordset != None and len(prim.texcoord_indexset) > 0 else None
                    #print range(prim_poly_index[0], prim_poly_index[1])
                    for poly_index in range(prim_poly_index[0], prim_poly_index[1]):
                        attr_indexes = primindex[poly_index]
                        #print polyindex
                        #print prim_poly_index
                        #print primindex
                        #print poly_index
                        #if type(prim) is collada.lineset.LineSet:
                        #    print attr_indexes
                        vert_index = attr_indexes[0] # We use the first attribute index as the primary index to determine whether vertex attributes should be shared (this is probably, but not neccesarily the "position" index)
                        #vert_index = prim_vert_index[i]
                        #orm_index = prim_norm_index[i] if prim_norm_index != None else None
                        #texcoord_indexset = prim_texcoord_indexset[i] if prim_texcoord_indexset != None else None                            

                        # Find an entry in the index_map that matches all of the indices of the other vertex attributes
                        #while vert_index != -1 and not match_index_indices(index_map[vert_index][0], norm_index, texcoord_indexset):
                        #print attr_indexes[1:]
                        #print index_map[vert_index][:-1]
                        #print str(vert_index) + ": Is " + str(index_map[vert_index][:-1]) + " == " + str(attr_indexes[1:]) + " = " + str(array_equal(index_map[vert_index][:-1], attr_indexes[1:]))
                        #print index_map[vert_index][0]
                        while vert_index != -1 and not (array_equal(index_map[vert_index][:-1], attr_indexes[1:]) or index_map[vert_index][0] == -1):
                            prev_vert_index = vert_index
                            vert_index = index_map[vert_index][-1]
                            #print "vert index " + str(vert_index)

                        # If a new index has to be added to the index_map, then do so
                        # I.e. vert_index will be -1 if we could not match it to an existing entry in the index_map
                        #print str(vert_index) + "  " + str(index_map[vert_index]) + str(index_map)
                        if vert_index == -1:
                            vert_index = len(jsgeom['positions']) / 3
                            index_map[prev_vert_index][-1] = len(index_map)
                            #print index_map
                            #print append(attr_indexes[1:], [-1])
                            index_map = append(index_map, [append(attr_indexes[1:], [-1])], axis=0)

                            # Now add new entries for vertex attributes themselves
                            #jsgeom['positions'].extend(float(p) for p in prim.vertex[prim_vert_index[i]])
                            if prim.sources['VERTEX']:
                                jsgeom['positions'].extend([float(p) for p in prim.vertex[attr_indexes[prim.sources['VERTEX'][0][0]]]])
                            #if norm_index != None: jsgeom['normals'].extend([float(n) for n in prim.normal[prim_norm_index[i]]])
                            if prim.sources['NORMAL']:
                                jsgeom['normals'].extend([float(n) for n in prim.normal[attr_indexes[prim.sources['NORMAL'][0][0]]]])
                            #if texcoord_indexset != None: jsgeom['uv'].extend([float(uv) for uv in prim.texcoordset[0][prim_texcoord_indexset[i]]])
                            if prim.sources['TEXCOORD']:
                                jsgeom['uv'].extend([float(uv) for uv in prim.texcoordset[0][attr_indexes[prim.sources['TEXCOORD'][0][0]]]])
                        elif index_map[vert_index][0] == -1:
                            # Replace the [-1] entry with the correct attribute indexes
                            #index_map[vert_index] = (pack_indices(norm_index, texcoord_indexset), -1)

                            # Here
                            #print index_map.shape
                            #print attr_indexes.shape
                            #print index_map
                            #print attr_indexes

                            index_map[vert_index][:-1] = attr_indexes[1:]
                            #print attr_indexes
                            #print "attr " + str(attr_indexes[1])
                            #if norm_index != None: jsgeom['normals'][vert_index*3:vert_index*3+3] = [float(n) for n in prim.normal[prim_norm_index[i]]]
                            #print "normals !!!" + str( [float(n) for n in prim.normal[attr_indexes[prim.sources['NORMAL'][0][0]]]] )
                            if prim.sources['NORMAL']:
                                jsgeom['normals'][vert_index*3:vert_index*3+3] = [float(n) for n in prim.normal[attr_indexes[prim.sources['NORMAL'][0][0]]]]
                            #if texcoord_indexset != None: jsgeom['uv'][vert_index*2:vert_index*2+2] = [float(uv) for uv in prim.texcoordset[0][prim_texcoord_indexset[i]]]
                            if prim.sources['TEXCOORD']:
                                jsgeom['uv'][vert_index*2:vert_index*2+2] = [float(uv) for uv in prim.texcoordset[0][attr_indexes[prim.sources['TEXCOORD'][0][0]]]]

                        # If the number of vertices added is > 3 then the polygon must be triangulated
                        # The shared vertices of the set of triangles that form the polygon never need to be split
                        # (This is so by definition: The polygon is a single surface, like a triangle)
                        # To triangulate we simply add the first and last vertex to the geometry again along with the new vertex.
                        vertex_number = poly_index - prim_poly_index[0]  # I.e. number 0 for the first vertex in the poly
                        if vertex_number > 2:
                            first_i = len(jssubgeom['indices']) - (vertex_number - 2) * 3
                            last_i = len(jssubgeom['indices']) - 1
                            jssubgeom['indices'].append(jssubgeom['indices'][first_i])
                            jssubgeom['indices'].append(jssubgeom['indices'][last_i])

                        # Add the newly calculated vertex index (which may be the original one or a new one if the vertex has been split)
                        if prim_poly_index[1] - prim_poly_index[0] >= 2:
                            jssubgeom['indices'].append(int(vert_index))
                    prim_index_index += 1
        elif _verbose:
            print "Warning: '" + type(prim).__name__ + "' geometry type is not yet supported by the translator."

        # TODO: Unfortunately Collada does not support a 'points' geometry type. When blender exports points 
        #       it simply exports them as vertices. However, Collada does not recognize these as a type of 'geometry',
        #       hence there is no way to dependably link these points to the attributes (colors, normals etc) that describe them.
        #       It is also a rather intensive operation to check whether any stand-alone points exist. 
        #       For this reason we could add a flag in the future to check for independent vertices, but the functionality
        #       will not be enabled by default (the fraction of models where points are intermingled with other types
        #       does not justify the overhead of doing this check for all models, ideally Collada should add 'points' 
        #       geometry type instead).
        ## Test whether all of the vertices in the model has been used (for polygons or lines)
        ## If not, then these vertices will be added as points geometry
        #all_vertices_used = True
        #for i in range(len(jssubgeom['triangles']['indices'])):
        #    if index_map[i][0][0] == -1:

        # Add the primitives to the list of subgeometries
        if jssubgeom['primitive']:
            jssubgeoms.append(jssubgeom)

    # Integrate all the different primitives into a parent geometry node with zero or more sub-geometries
    if len(jssubgeoms) == 0:
        if _verbose:
            print "Warning: No recognizable primitives found in Geometry '" + geom.id + "'."
    elif len(jssubgeoms) == 1:
        jsgeom['primitive'] = jssubgeoms[0]['primitive']
        jsgeom['indices'] = jssubgeoms[0]['indices']
    else:
        print 'Subgeometries added....'
        jsgeom['nodes'] = jssubgeoms
    
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
                        'elements': [float(element) for row in node.matrix for element in row],
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
                    #jslight['pos'] = { 'x': node.light.position[0], 'y': node.light.position[1], 'z': node.light.position[2] }
                    jslight['pos'] = {}
                    jslight['pos']['x'] = float(node.light.position[0])
                    jslight['pos']['y'] = float(node.light.position[1])
                    jslight['pos']['z'] = float(node.light.position[2])
                
                if mode == 'dir':
                    jslight['dir'] = {}
                    jslight['dir']['x'] = float(node.light.direction[0])
                    jslight['dir']['y'] = float(node.light.direction[1])
                    jslight['dir']['z'] = float(node.light.direction[2])
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
        'eye': { 'x': float(camera.position[0]), 'y': float(camera.position[1]), 'z': float(camera.position[2]) },
        'look': { 'x': float(camera.position[0] + camera.direction[0]), 'y': float(camera.position[1] + camera.direction[1]), 'z': float(camera.position[2] + camera.direction[2]) },
        'up': { 'x': float(camera.up[0]), 'y': float(camera.up[1]), 'z': float(camera.up[2]) },
        'nodes': [{ 
            'type': 'camera',
            'optics': {
                 'type': 'perspective', #TODO: type of camera can't be retrieved a.t.m. assuming "perspective" for now
                 'fovy': float(camera.fov),
                 'aspect': 1.0, # TODO: aspect ratio is not currently available
                 'near': float(camera.near),
                 'far': float(camera.far)
            }
        }]
    }

def translate_scene(scene):
    """
      Translates collada scene graph hierarchy into a SceneJS scene graph.
      This makes some changes to the hierarchy, such as placing camera nodes above visual nodes.
    """
    cameras = scene.objects('camera')
    try: cam = cameras.next()
    except: cam = None
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

