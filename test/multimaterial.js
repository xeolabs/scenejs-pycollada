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
                    coreId: 'Red',
                    baseColor:
                        {
                            r: 0.64,
                            b: 0.0,
                            g: 0.0,
                        },
                    emit: 0.0,
                },
                {
                    type: 'material',
                    coreId: 'Blue',
                    baseColor:
                        {
                            r: 0.0,
                            b: 0.64,
                            g: 0.0,
                        },
                    emit: 0.0,
                },
                {
                    type: 'material',
                    coreId: 'Green',
                    baseColor:
                        {
                            r: 0.0,
                            b: 0.0,
                            g: 0.64,
                        },
                    emit: 0.0,
                },
                {
                    type: 'geometry',
                    coreId: 'Cube-mesh',
                    resource: 'Cube-mesh',
                    positions: [1.0,1.0,-1.0,1.0,-1.0,-1.0,-1.0,-0.999999821186,-1.0,1.0,0.999999523163,1.0,0.999999403954,-1.00000095367,1.0,-1.0,-0.999999701977,1.0,-1.0,1.0,1.0,1.0,1.0,-1.0,1.0,-1.0,-1.0,-1.0,-0.999999821186,-1.0,1.0,0.999999523163,1.0,0.999999403954,-1.00000095367,1.0,-1.0,-0.999999701977,1.0,-1.0,1.0,1.0,1.0,1.0,-1.0,1.0,-1.0,-1.0,-1.0,-0.999999821186,-1.0,1.0,0.999999523163,1.0,0.999999403954,-1.00000095367,1.0,-1.0,-0.999999701977,1.0,-1.0,1.0,1.0,],
                    normals: [1.0,-2.8312200584e-07,0.0,1.0,-2.8312200584e-07,0.0,-2.8312200584e-07,-1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,],
                    nodes: [
                        {
                            type: 'geometry',
                            coreId: 'Cube-mesh0',
                            resource: 'Cube-mesh',
                            primitive: 'triangles',
                            indices: [1,4,5,1,5,2,],
                        },
                        {
                            type: 'geometry',
                            coreId: 'Cube-mesh1',
                            resource: 'Cube-mesh',
                            primitive: 'triangles',
                            indices: [0,3,4,0,4,1,],
                        },
                        {
                            type: 'geometry',
                            coreId: 'Cube-mesh2',
                            resource: 'Cube-mesh',
                            primitive: 'triangles',
                            indices: [3,6,5,3,5,4,],
                        },
                    ],
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
                                    elements: [-0.290864378214,0.955171227455,-0.055189050734,0.0,-0.771100878716,-0.199883162975,0.604524791241,0.0,0.566393375397,0.218391060829,0.794672250748,0.0,1.84446895123,-3.09919691086,4.50007295609,1.0,],
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
                                            quadraticAttenuation: 0.000555556,
                                            linearAttenuation: 0.0,
                                            mode: 'point',
                                            constantAttenuation: 1.0,
                                        },
                                    ],
                                },
                                {
                                    type: 'matrix',
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,],
                                    nodes: [
                                        {
                                            type: 'material',
                                            id: 'Cube-mesh-Red',
                                            coreId: 'Red',
                                            baseColor:
                                                {
                                                    r: 0.64,
                                                    b: 0.0,
                                                    g: 0.0,
                                                },
                                            emit: 0.0,
                                            nodes: [
                                                {
                                                    type: 'geometry',
                                                    coreId: 'Cube-mesh',
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
