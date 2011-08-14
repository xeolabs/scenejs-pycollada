SceneJS.createScene({
    canvasId: 'scenejsCanvas',
    loggingElementId: 'scenejsLog',
    flags:
        {
            backfaces: false, 
        },
    nodes: [
        {
            nodes: [
                {
                    shine: 12.0,
                    baseColor:
                        {
                            r: 0.5,
                            b: 0.5,
                            g: 0.5,
                        },
                    coreId: 'Plain',
                    specularColor:
                        {
                            r: 0.25,
                            b: 0.25,
                            g: 0.25,
                        },
                    nodes:
                        {
                            layers: [
                                {
                                    url: 'projects/active/development/programs/scenejs-pycollada/test/tex.jpg',
                                    applyTo: 'baseColor',
                                },
                            ],
                            type: 'texture',
                        },
                    type: 'material',
                    emit: 0.0,
                },
                {
                    primitive: 'triangles',
                    resource: 'Cube_007-mesh',
                    positions: [1.0,1.0,-1.0,1.0,-1.0,-1.0,1.0,1.0,1.0,1.0,-1.0,1.0,],
                    uv: [1.0,0.0,0.0,0.0,1.0,1.0,0.0,1.0,],
                    coreId: 'Cube_007-mesh',
                    normals: [1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,],
                    indices: [0,2,3,0,3,1,],
                    type: 'geometry',
                },
            ],
            type: 'library',
        },
        {
            eye:
                {
                    y: -8.65659999847,
                    x: 8.04928302765,
                    z: 4.80725097656,
                },
            nodes: [
                {
                    optics:
                        {
                            far: 100.0,
                            near: 0.1,
                            type: 'perspective',
                            aspect: 1.0,
                            fovy: 27.6380627952,
                        },
                    nodes:
                        {
                            clear:
                                {
                                    color: true, 
                                    depth: true, 
                                    stencil: false, 
                                },
                            nodes: [
                                {
                                    nodes: [
                                        {
                                            color:
                                                {
                                                    r: 1.0,
                                                    b: 1.0,
                                                    g: 1.0,
                                                },
                                            pos:
                                                {
                                                    y: 0.0,
                                                    x: 0.0,
                                                    z: 0.0,
                                                },
                                            quadraticAttenuation: 0.0008,
                                            linearAttenuation: 0.0,
                                            mode: 'point',
                                            type: 'light',
                                            constantAttenuation: 1.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,4.19914579391,-0.827423512936,3.74212694168,1.0,],
                                    type: 'matrix',
                                },
                                {
                                    nodes: [
                                        {
                                            shine: 12.0,
                                            baseColor:
                                                {
                                                    r: 0.5,
                                                    b: 0.5,
                                                    g: 0.5,
                                                },
                                            id: 'Cube_007-mesh-Plain',
                                            coreId: 'Plain',
                                            specularColor:
                                                {
                                                    r: 0.25,
                                                    b: 0.25,
                                                    g: 0.25,
                                                },
                                            nodes: [
                                                {
                                                    coreId: 'Cube_007-mesh',
                                                    type: 'geometry',
                                                },
                                            ],
                                            type: 'material',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,],
                                    type: 'matrix',
                                },
                            ],
                            type: 'renderer',
                            clearColor:
                                {
                                    r: 0.4,
                                    b: 0.4,
                                    g: 0.4,
                                },
                        },
                    type: 'camera',
                },
            ],
            type: 'lookAt',
            look:
                {
                    y: -7.92924976349,
                    x: 7.47775602341,
                    z: 4.42735910416,
                },
            up:
                {
                    y: 0.169707730412,
                    x: -0.386575758457,
                    z: 0.906508982182,
                },
        },
    ],
    type: 'scene',
    id: 'Scene',
});
