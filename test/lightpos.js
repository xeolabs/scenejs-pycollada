SceneJS.createNode({
    nodes: [
        {
            baseColor:
                {
                    r: 0.5,
                    b: 0.5,
                    g: 0.5,
                },
            type: 'material',
            id: 'Material_001_001',
            emit: 0.0,
        },
        {
            primitive: 'triangles',
            resource: 'Cube_003-mesh-mes_000-mesh',
            positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
            normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
            indices: [0,3,2,0,2,1,],
            type: 'geometry',
            id: 'Cube_003-mesh-mes_000-mesh',
        },
        {
            primitive: 'triangles',
            resource: 'Cube_002-mesh-mes_000-mesh',
            positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
            normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
            indices: [0,3,2,0,2,1,],
            type: 'geometry',
            id: 'Cube_002-mesh-mes_000-mesh',
        },
        {
            primitive: 'triangles',
            resource: 'Cube_001-mesh-mes_000-mesh',
            positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
            normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
            indices: [0,3,2,0,2,1,],
            type: 'geometry',
            id: 'Cube_001-mesh-mes_000-mesh',
        },
        {
            primitive: 'triangles',
            resource: 'Cube-mesh-mesh_001-mesh',
            positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
            normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
            indices: [0,3,2,0,2,1,],
            type: 'geometry',
            id: 'Cube-mesh-mesh_001-mesh',
        },
    ],
    type: 'library',
});
SceneJS.createNode({
    nodes: [
        {
            clear:
                {
                    color: true, 
                    depth: true, 
                    stencil: false, 
                },
            nodes: [
                {
                    eye:
                        {
                            y: -6.50763988495,
                            x: 7.48113203049,
                            z: 5.34366512299,
                        },
                    nodes: [
                        {
                            optics:
                                {
                                    far: 100.0,
                                    near: 0.1,
                                    type: 'perspective',
                                    aspect: 1.0,
                                    fovy: 87.3499486965,
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
                                            quadraticAttenuation: 0.00555556,
                                            linearAttenuation: 0.0,
                                            mode: 'point',
                                            type: 'light',
                                            constantAttenuation: 1.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,-1.5,1.5,1.0,],
                                    type: 'matrix',
                                },
                                {
                                    nodes: [
                                        {
                                            baseColor:
                                                {
                                                    r: 0.5,
                                                    b: 0.5,
                                                    g: 0.5,
                                                },
                                            nodes: [
                                                {
                                                    type: 'instance',
                                                    target: 'Cube_003-mesh-mes_000-mesh',
                                                },
                                            ],
                                            type: 'material',
                                            id: 'Cube_003-mesh-mes_000-mesh-Material_001_001',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,1.5,-1.5,0.0,1.0,],
                                    type: 'matrix',
                                },
                                {
                                    nodes: [
                                        {
                                            baseColor:
                                                {
                                                    r: 0.5,
                                                    b: 0.5,
                                                    g: 0.5,
                                                },
                                            nodes: [
                                                {
                                                    type: 'instance',
                                                    target: 'Cube_002-mesh-mes_000-mesh',
                                                },
                                            ],
                                            type: 'material',
                                            id: 'Cube_002-mesh-mes_000-mesh-Material_001_001',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,1.5,1.5,0.0,1.0,],
                                    type: 'matrix',
                                },
                                {
                                    nodes: [
                                        {
                                            baseColor:
                                                {
                                                    r: 0.5,
                                                    b: 0.5,
                                                    g: 0.5,
                                                },
                                            nodes: [
                                                {
                                                    type: 'instance',
                                                    target: 'Cube_001-mesh-mes_000-mesh',
                                                },
                                            ],
                                            type: 'material',
                                            id: 'Cube_001-mesh-mes_000-mesh-Material_001_001',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,1.5,0.0,1.0,],
                                    type: 'matrix',
                                },
                                {
                                    nodes: [
                                        {
                                            baseColor:
                                                {
                                                    r: 0.5,
                                                    b: 0.5,
                                                    g: 0.5,
                                                },
                                            nodes: [
                                                {
                                                    type: 'instance',
                                                    target: 'Cube-mesh-mesh_001-mesh',
                                                },
                                            ],
                                            type: 'material',
                                            id: 'Cube-mesh-mesh_001-mesh-Material_001_001',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,-1.5,0.0,1.0,],
                                    type: 'matrix',
                                },
                            ],
                            type: 'camera',
                        },
                    ],
                    type: 'lookAt',
                    look:
                        {
                            y: -5.89697408676,
                            x: 6.82627010345,
                            z: 4.89841985703,
                        },
                    up:
                        {
                            y: 0.312468677759,
                            x: -0.317370116711,
                            z: 0.895343244076,
                        },
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
    ],
    loggingElementId: 'scenejsLog',
    canvasId: 'scenejsCanvas',
    type: 'scene',
    id: 'Scene',
});
