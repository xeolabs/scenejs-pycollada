SceneJS.createNode({
    nodes: [
        {
            baseColor:
                {
                    r: 0.64,
                    b: 0.64,
                    g: 0.64,
                },
            type: 'material',
            id: 'Material-effect',
            emit: 0.0,
        },
        {
            primitive: 'lines',
            resource: 'Cube-mesh',
            positions: [1.0,1.0,-1.0,1.0,-1.0,-1.0,-1.0,-0.999999821186,-1.0,-0.999999701977,1.0,-1.0,1.0,0.999999523163,1.0,0.999999403954,-1.00000095367,1.0,-1.0,-0.999999701977,1.0,-1.0,1.0,1.0,0.977304816246,2.10886001587,1.0,0.977304279804,2.10886001587,-0.999999523163,-0.028740759939,1.6484940052,2.47447395325,-0.815371215343,-0.5016310215,2.17498397827,-0.794783592224,-2.70871400833,0.346526801586,-1.16639399529,-1.50765895844,2.00356197357,-0.267441302538,-1.71102797985,0.187304794788,1.53667402267,-0.0513397417963,-1.78009104729,0.148037597537,-2.01348900795,-0.821267485619,2.06411910057,0.8370642066,-1.34161901474,1.97824299335,0.730930805206,-0.867338001728,1.82024002075,0.421330094337,-1.12671601772,],
            indices: [0,1,1,2,2,3,3,4,4,5,],
            type: 'geometry',
            id: 'Cube-mesh',
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
                            y: -6.50764,
                            x: 7.48113,
                            z: 5.34367,
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
                                            baseColor:
                                                {
                                                    r: 0.64,
                                                    b: 0.64,
                                                    g: 0.64,
                                                },
                                            nodes: [
                                                {
                                                    type: 'instance',
                                                    target: 'Cube-mesh',
                                                },
                                            ],
                                            type: 'material',
                                            id: 'Cube-mesh-Material-effect',
                                            emit: 0.0,
                                        },
                                    ],
                                    elements: [1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,],
                                    type: 'matrix',
                                },
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
                                            quadraticAttenuation: 0.000555556,
                                            linearAttenuation: 0.0,
                                            mode: 'point',
                                            type: 'light',
                                            constantAttenuation: 1.0,
                                        },
                                    ],
                                    elements: [-0.290864,-0.771101,0.566393,4.07624,0.955171,-0.199883,0.218391,1.00545,-0.0551891,0.604525,0.794672,5.90386,0.0,0.0,0.0,1.0,],
                                    type: 'matrix',
                                },
                            ],
                            type: 'camera',
                        },
                    ],
                    type: 'lookAt',
                    look:
                        {
                            y: -5.89697,
                            x: 6.82627,
                            z: 4.89842,
                        },
                    up:
                        {
                            y: 0.312469,
                            x: -0.31737,
                            z: 0.895343,
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
