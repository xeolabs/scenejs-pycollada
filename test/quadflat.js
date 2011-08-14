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
                    coreId: 'Material',
                    baseColor:
                        {
                            r: 0.64,
                            b: 0.64,
                            g: 0.64,
                        },
                    type: 'material',
                    emit: 0.0,
                },
                {
                    primitive: 'triangles',
                    resource: 'Cube-mesh',
                    positions: [1.0,1.0,-1.0,1.0,-1.0,-1.0,1.0,0.999999523163,1.0,0.999999403954,-1.00000095367,1.0,],
                    coreId: 'Cube-mesh',
                    normals: [1.0,-2.8312200584e-07,0.0,1.0,-2.8312200584e-07,0.0,1.0,-2.8312200584e-07,0.0,1.0,-2.8312200584e-07,0.0,],
                    indices: [0,2,3,0,3,1,],
                    type: 'geometry',
                },
            ],
            type: 'library',
        },
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
                                            baseColor:
                                                {
                                                    r: 0.64,
                                                    b: 0.64,
                                                    g: 0.64,
                                                },
                                            id: 'Cube-mesh-Material',
                                            coreId: 'Material',
                                            nodes: [
                                                {
                                                    coreId: 'Cube-mesh',
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
    type: 'scene',
    id: 'Scene',
});
