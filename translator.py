"""
Translate a collada object defined by PyCollada into SceneJS JSON and 
outputs the result to a stream (a file, string or network socket)
"""

import collada
import sys
from numpy import array, append, array_equal

def translate(output_stream, collada_obj, options = {}, debug = False, verbose = False):
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
    jslib = { 'type': 'library', 'nodes': [] }

    if _debug:
        print "Exporting libraries..."
    for mat in collada_obj.materials:
        if _debug:
           print "Exporting material '" + mat.id + "'..."
        jsmat = translate_material(mat)
        if jsmat:
            jslib['nodes'].append(jsmat)
    for geom in collada_obj.geometries:
        if _debug:
            print "Exporting geometry '" + geom.id + "'..."
        jsgeom = translate_geometry(geom)
        if jsgeom:
            jslib['nodes'].append(jsgeom)

    if options['libraries_only']:
      # Export the library only
      output_stream.write(jslib, options)
    else:
      # Export scenes
      for scene in [collada_obj.scene]:
          if _debug:
              print "Exporting scene '" + scene.id + "'..."

          jsscene = translate_scene(scene)
          if jsscene:
              # Link the library node to the current scene (as a core library)
              jsscene['nodes'].insert(0, jslib)

              # Output the scene
              output_stream.write(jsscene, options)

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

def translate_material_map(material_map):
    jslayer = {}

    # Pre-conditions
    if not material_map.sampler: return None
    if not material_map.sampler.surface: return None
    if not material_map.sampler.surface.image: return None
    if not material_map.sampler.surface.image.path: return None

    # TODO: Rewrite the texture urls using a regular path
    jslayer['url'] = str(material_map.sampler.surface.image.path)

    # TODO: Support other texture formats?
    #if material_map.sampler.surface.format:
    #    formats = {
    #        'A8R8G8B8':
    #    }
    if material_map.sampler.minfilter:
        filters = {
            'NONE': 'nearest',
            'NEAREST': 'nearest',
            'LINEAR': 'linear',
            'NEAREST_MIPMAP_NEAREST': 'nearestMipMapNearest',
            'LINEAR_MIPMAP_NEAREST': 'linearMipMapNearest',
            'NEAREST_MIPMAP_LINEAR': 'nearestMipMapLinear',
            'LINEAR_MIPMAP_LINEAR': 'linearMipMapLinear'
        }
        try:
            jslayer['minFilter'] = filters[material_map.sampler.minfilter.upper()]
        except:
            if _verbose: print "Could not assign value to min filter: " + str(material_map.sampler.minfilter)
    if material_map.sampler.magfilter:
        filters = {
            'NONE': 'nearest',
            'NEAREST': 'nearest',
            'LINEAR': 'linear',
            'NEAREST_MIPMAP_NEAREST': 'linear',
            'LINEAR_MIPMAP_NEAREST': 'linear',
            'NEAREST_MIPMAP_LINEAR': 'linear',
            'LINEAR_MIPMAP_LINEAR': 'linear'
        }
        try:
            jslayer['magFilter'] = filters[material_map.sampler.magfilter.upper()]
        except:
            if _verbose: print "Could not assign value to mag filter: " + str(material_map.sampler.magfilter)
    # TODO: material_map.sampler.wrapS is not yet supported by PyCollada
    # TODO: material_map.sampler.wrapT is not yet supported by PyCollada
    return jslayer

def translate_material(mat):
    """
      Translates a collada material node into a SceneJS material node.

      :Parameters:
        geom
          An instance of the PyCollada Material class.
    """
    jstexture = {
        'type': 'texture',
        'layers': []
    }
    jsmaterial = {
        'type': 'material',
        'coreId': mat.id
    }
    if not _rgb_attribute(jsmaterial, 'baseColor', mat.effect.diffuse):
        _rgb_attribute(jsmaterial, 'baseColor', (0.5,0.5,0.5))
        if type(mat.effect.diffuse) is collada.material.Map:
            # Create a texture layer for the diffuse map
            jslayer = translate_material_map(mat.effect.diffuse)
            if jslayer:
                jslayer['applyTo'] = 'baseColor'
                jstexture['layers'].append(jslayer)
        elif _verbose and mat.effect.diffuse:
            print "Unknown diffuse input: " + str(mat.effect.diffuse)
    if not _rgb_attribute(jsmaterial, 'specularColor', mat.effect.specular):
        if type(mat.effect.specular) is collada.material.Map:
            # Create a texture layer for the specular map
            jslayer = translate_material_map(mat.effect.specular)
            if jslayer:
                jslayer['applyTo'] = 'specular'
                jstexture['layers'].append(jslayer)
        elif _verbose and mat.effect.specular:
            print "Unknown specular input: " + str(mat.effect.specular)
    if not _float_attribute(jsmaterial, 'shine', mat.effect.shininess):
        if _verbose and mat.effect.shininess:
            print "Unknown shininess input: " + str(mat.effect.shininess)
    if not _float_attribute(jsmaterial, 'alpha', mat.effect.transparency):
        if type(mat.effect.transparency) is collada.material.Map:
            # Create a texture layer for the alpha map
            jslayer = translate_material_map(mat.effect.transparency)
            if jslayer:
                jslayer['applyTo'] = 'alpha'
                jstexture['layers'].append(jslayer)
        elif _verbose and mat.effect.transparency:
            print "Unknown alpha input: " + str(mat.effect.transparency)
    if mat.effect.emission and type(mat.effect.emission) is tuple:
        jsmaterial['emit'] = (mat.effect.emission[0] + mat.effect.emission[1] + mat.effect.emission[2]) / 3.0
    else:
        if type(mat.effect.emission) is collada.material.Map:
            # Create a texture layer for the emission map
            jslayer = translate_material_map(mat.effect.emission)
            if jslayer:
                jslayer['applyTo'] = 'emit'
                jstexture['layers'].append(jslayer)
        elif _verbose and mat.effect.emission:
            print "Unknown emit input: " + str(mat.effect.emission)
    # TODO: not yet supported 'reflect': mat.effect.reflective...
    # TODO: normal maps not yet supported

    # Add the texture to the material if suitable
    if jstexture['layers']:
        jsmaterial['nodes'] = jstexture
    
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
        'coreId': geom.id,
    }
    
    # TODO: Point geometry is not currently supported due to the limitations of the Collada format (also see the notes lower down in this function)
    # Note: Blender currently exports points without any indexes... It is debatable whether these could be implemented as point sprites (collada does not properly support
    #       support point clouds, so it seems unlikely.
    jssubgeoms = []

    c_subgeom = 0
    for prim in geom.primitives:
        # TODO: support other primitive types (<polygons>, <trifans>, <tristrips>, <linestrips>)
        jssubgeom = {
            'type': 'geometry',
            'coreId': geom.id + str(c_subgeom),
            'indices': []
        }
        c_subgeom += 1

        if type(prim) is collada.triangleset.TriangleSet \
              or type(prim) is collada.polylist.Polylist \
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
            # Possibly use len(prim.texcoordset) to determine number for texture coordinate sets
            #num_index_elems = 1 + (1 if prim.normal != None else 0) + (1 if prim.texcoordset != () else 0)

            # Note that the number of indices stored per vertex is the last dimension of the prim.index.shape
            # E.g. For a polylist the prim.index looks like [[0,1],[3,4]] but for triangles the prim.index
            #      looks like [[[0,1],[2,3],[4,5]], [[6,7],[8,9],[10,11]]] 
            #      (So the shape of the index may vary)
            num_index_elems = prim.index.shape[len(prim.index.shape)-1]
            if prim.vertex is None:
                continue
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
                polyindex = (array([3 * x, 3 * x + 3]) for x in range(0, prim.ntriangles))
            elif type(prim) is collada.lineset.LineSet:
                polyindex = (array([2 * x, 2 * x + 2]) for x in range(0, prim.nlines))
            elif type(prim) is collada.polylist.Polylist:
                polyindex = prim.polyindex

            # Ensure that the index is always correctly shaped
            primindex = None
            if type(prim) is collada.lineset.LineSet or type(prim) is collada.triangleset.TriangleSet:
                primindex = prim.index.copy()
                primindex.resize((len(prim.index.flat)/num_index_elems, num_index_elems))
            else:
                primindex = prim.index

            # Loop through each vertex, check if it has to be split and then write the data to the relevant buffers
            if not use_index_map:
                jssubgeom['indices'].extend([int(i) for prim_vert_index in prim.vertex_index for i in prim_vert_index])
            else:
                norm_index = -1
                prim_index_index = 0
                for prim_poly_index in polyindex:
                    for poly_index in range(prim_poly_index[0], prim_poly_index[1]):
                        attr_indexes = primindex[poly_index]
                        vert_index = attr_indexes[0] # We use the first attribute index as the primary index to determine whether vertex attributes should be shared (this is probably, but not neccesarily the "position" index)

                        # Find an entry in the index_map that matches all of the indices of the other vertex attributes
                        while vert_index != -1 and not (array_equal(index_map[vert_index][:-1], attr_indexes[1:]) or index_map[vert_index][0] == -1):
                            prev_vert_index = vert_index
                            vert_index = index_map[vert_index][-1]

                        # If a new index has to be added to the index_map, then do so
                        # I.e. vert_index will be -1 if we could not match it to an existing entry in the index_map
                        #print str(vert_index) + "  " + str(index_map[vert_index]) + str(index_map)
                        if vert_index == -1:
                            vert_index = len(jsgeom['positions']) / 3
                            index_map[prev_vert_index][-1] = len(index_map)
                            index_map = append(index_map, [append(attr_indexes[1:], [-1])], axis=0)

                            # Now add new entries for vertex attributes themselves
                            if prim.sources['VERTEX']:
                                jsgeom['positions'].extend([float(p) for p in prim.vertex[attr_indexes[prim.sources['VERTEX'][0][0]]]])
                            if prim.sources['NORMAL']:
                                jsgeom['normals'].extend([float(n) for n in prim.normal[attr_indexes[prim.sources['NORMAL'][0][0]]]])
                            if prim.sources['TEXCOORD']:
                                jsgeom['uv'].extend([float(uv) for uv in prim.texcoordset[0][attr_indexes[prim.sources['TEXCOORD'][0][0]]]])
                        elif index_map[vert_index][0] == -1:
                            # Replace the [-1] entry with the correct attribute indexes
                            #index_map[vert_index] = (pack_indices(norm_index, texcoord_indexset), -1)
                            
                            index_map[vert_index][:-1] = attr_indexes[1:]
                            if prim.sources['NORMAL']:
                                jsgeom['normals'][vert_index*3:vert_index*3+3] = [float(n) for n in prim.normal[attr_indexes[prim.sources['NORMAL'][0][0]]]]
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

def contains_light_nodes(jsnodes):
    # TODO: For now this function just checks if there's a child light node, it does not check all the way down the hierarchy
    #       If lights are nested deeply, then it's likely there would be an ordering problem anyway that couldn't be resolved
    #       with a simple reordering algorithm
    # Because lights are inserted first, it is only necessary to test whether the first node is a light
    return jsnodes and jsnodes[0]['type'] == 'light'

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
            if len(node.materials) > 1:
                jsgeometry_instance = { 'type': 'geometry', 'coreId': node.geometry.id, 'nodes': [] }
                for i in range(0, len(node.materials)):
                    jssubgeometry_instance = { 'type': 'geometry', 'coreId': node.geometry.id + str(i) }
                    jsgeometry_instance['nodes'].append({ 'type': 'material', 'coreId': node.materials[i].target.id, 'nodes': [ jssubgeometry_instance ] })
                jsnodes.append(jsgeometry_instance)
            elif len(node.materials) == 1:
                jsgeometry_instance = { 'type': 'geometry', 'coreId': node.geometry.id }
                jsnodes.append({ 'type': 'material', 'coreId': node.materials[0].target.id, 'nodes': [ jsgeometry_instance ] })
            else:
                jsgeometry_instance = { 'type': 'geometry', 'coreId': node.geometry.id }
                jsnodes.append(jsgeometry_instance)
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
            elif type(node.light) is collada.light.DirectionalLight or type(node.light) is collada.light.BoundDirectionalLight:
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
                
                # Light nodes should always be placed first in the list (because they are activated in order)
                jsnodes.insert(0, jslight)
        elif type(node) is collada.scene.ExtraNode:
            print "Extra Node!"
        elif type(node) in (collada.scene.Node, collada.scene.NodeNode):
            if isinstance(node, collada.scene.NodeNode):
                node = node.node
            # An unspecialized node is assumed to just contain a transformation matrix
            if node.children:
                jschild_nodes = _translate_scene_nodes(node.children)
                # Don't append the transform node unless it has children (isolated transform nodes are redundant)
                if jschild_nodes:
                    # Matrices from COLLADA are transposed
                    elems = [float(element) for row in node.matrix.transpose() for element in row]
                    # Light nodes should always be placed first in the list (because they are activated in order)
                    tnode = {
                        'type': 'matrix',
                        'elements': elems,
                        'nodes': jschild_nodes
                        }
                    if contains_light_nodes(jschild_nodes):
                        jsnodes.insert(0, tnode)
                    else:
                        jsnodes.append(tnode)
        else:
            print "Unknown node \'" + str(type(node)) + "\'"
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
                 'fovy': float(camera.yfov),
                 'aspect': 1.0, # TODO: aspect ratio is not currently available
                 'near': float(camera.znear),
                 'far': float(camera.zfar)
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

    jsrenderer = {
        'type': 'renderer',
        'clear': {
            'depth': True,
            'color': True,
            'stencil': False
        },
        'clearColor': { 'r': 0.4, 'g': 0.4, 'b': 0.4 },
        'nodes': []
    }

    #jscamera['nodes'][0]['nodes'] = _translate_scene_nodes(scene.nodes)
    jsrenderer['nodes'] = _translate_scene_nodes(scene.nodes)
    jscamera['nodes'][0]['nodes'] = [jsrenderer]
    
    return {
        'type': 'scene',
        'id': scene.id,
        'canvasId': 'scenejsCanvas',
        'loggingElementId': 'scenejsLog',
        'flags': {
                'backfaces': False
            },
        'nodes': [jscamera]
    }

