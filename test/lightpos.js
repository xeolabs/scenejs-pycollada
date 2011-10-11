SceneJS.createScene({
    type: 'scene',
    id: 'Scene',
    canvasId: 'scenejsCanvas',
    loggingElementId: 'scenejsLog',
    flags:
        {
            backfaces: false, 
        },
    nodes: [
        {
            type: 'library',
            nodes: [
                {
                    type: 'material',
                    coreId: 'Material_001_001',
                    baseColor:
                        {
                            r: 0.5,
                            b: 0.5,
                            g: 0.5,
                        },
                    emit: 0.0,
                },
                {
                    type: 'geometry',
                    coreId: 'Cube_003-mesh-mes_000-mesh',
                    primitive: 'triangles',
                    positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
                    normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
                    indices: [0,3,2,0,2,1,],
                },
                {
                    type: 'geometry',
                    coreId: 'Cube_002-mesh-mes_000-mesh',
                    primitive: 'triangles',
                    positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
                    normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
                    indices: [0,3,2,0,2,1,],
                },
                {
                    type: 'geometry',
                    coreId: 'Cube_001-mesh-mes_000-mesh',
                    primitive: 'triangles',
                    positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
                    normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
                    indices: [0,3,2,0,2,1,],
                },
                {
                    type: 'geometry',
                    coreId: 'Cube-mesh-mesh_001-mesh',
                    primitive: 'triangles',
                    positions: [1.0,1.0,0.0,1.0,-1.0,0.0,-1.0,-1.0,0.0,-1.0,1.0,0.0,],
                    normals: [0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,],
                    indices: [0,3,2,0,2,1,],
                },
            ],
        },
        {
            type: 'lookAt',
            eye:
                {
                    y: -6.50763988495,
                    x: 7.48113203049,
                    z: 5.34366512299,
                },
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
            nodes: [
                {
                    type: 'camera',
                    optics:
                        {
                            type: 'perspective',
                            far: 100.0,
                            near: 0.1,
                            aspect: 1.0,
                            fovy: 27.6380627952,
                        },
                    nodes: [
                        {
                            type: 'renderer',
                            clear:
                                {
                                    color: true, 
                                    depth: true, 
                                    stencil: false, 
                                },
                            clearColor:
                                {
                                    r: 0.4,
                                    b: 0.4,
                                    g: 0.4,
                                },
                            nodes: [
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,-1.5,1.5,1.0,],
                                    nodes: [
                                        {
                                            type: 'light',
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
                                            constantAttenuation: 1.0,
                                        },
                                    ],
                                },
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,1.5,-1.5,0.0,1.0,],
                                    nodes: [
                                        {
                                            type: 'material',
                                            coreId: 'Material_001_001',
                                            nodes: [
                                                {
                                                    type: 'geometry',
                                                    coreId: 'Cube_003-mesh-mes_000-mesh',
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,1.5,1.5,0.0,1.0,],
                                    nodes: [
                                        {
                                            type: 'material',
                                            coreId: 'Material_001_001',
                                            nodes: [
                                                {
                                                    type: 'geometry',
                                                    coreId: 'Cube_002-mesh-mes_000-mesh',
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,1.5,0.0,1.0,],
                                    nodes: [
                                        {
                                            type: 'material',
                                            coreId: 'Material_001_001',
                                            nodes: [
                                                {
                                                    type: 'geometry',
                                                    coreId: 'Cube_001-mesh-mes_000-mesh',
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,-1.5,-1.5,0.0,1.0,],
                                    nodes: [
                                        {
                                            type: 'material',
                                            coreId: 'Material_001_001',
                                            nodes: [
                                                {
                                                    type: 'geometry',
                                                    coreId: 'Cube-mesh-mesh_001-mesh',
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
});
