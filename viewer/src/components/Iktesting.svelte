<script lang="ts">
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { GUI } from "three/examples/jsm/libs/lil-gui.module.min.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { send2Socket } from "../stores/websocket";
    import { CCDIKSolver } from "three/examples/jsm/animation/CCDIKSolver.js";
    
    let canvas: HTMLCanvasElement;
    let scale = 0.000001;
    
    const mapping = {
        Chest: "1",
        Head: "head",
        upper_armL: "2",
        upper_armR: "3",
        thighL: "4",
        shinL: "5",
        thighR: "6",
        shinR: "7",
    };
    
    // IK chain setup
    const ikChain = [
        {
            target: 'target_handL', // the target object the hand should try to reach
            effector: 'handL',      // the end effector (wrist bone)
            links: [
                {
                    index: 'forearmL',  // index refers to the bone name in your model
                    rotationMin: new THREE.Vector3(-Math.PI / 2, -Math.PI / 4, -Math.PI / 2), // Minimum rotation angles
                    rotationMax: new THREE.Vector3(Math.PI / 2, Math.PI / 4, Math.PI / 2),    // Maximum rotation angles
                },
                {
                    index: 'upper_armL', // upper arm bone
                    rotationMin: new THREE.Vector3(-Math.PI / 2, -Math.PI / 4, -Math.PI / 2),
                    rotationMax: new THREE.Vector3(Math.PI / 2, Math.PI / 4, Math.PI / 2),
                }
            ],
        }
    ];
    
    let camera: THREE.PerspectiveCamera,
        scene: THREE.Scene,
        renderer: THREE.WebGLRenderer,
        clock: THREE.Clock,
        rightArm: THREE.Object3D<THREE.Event> | undefined,
        gui: GUI;
    
    let availableBones: any[] = [];
    let availableBonesControls: any[] = [];
    
    function findBones(obj: any) {
        if (obj.type === "Bone") {
            console.log(obj.name); // Log the name of the bone
            availableBones.push(obj.name); // Add the bone to the list of available bones
        }
        obj.children.forEach(findBones); // Recurse through all children
    }
    
    function init() {
        gui = new GUI();
        camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.01, 10);
        camera.position.set(2, 2, -2);
    
        clock = new THREE.Clock();
    
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);
    
        const light = new THREE.HemisphereLight(0xbbbbff, 0x444422);
        light.position.set(0, 1, 0);
        scene.add(light);
    
        // model loading
        const loader = new GLTFLoader();
        loader.load("test_ik.glb", function (gltf) {
            const model = gltf.scene;
            findBones(model);
            scene.add(model);
    
            let ikTargets = {};
            availableBones.forEach((bone) => {
                let boneControl = model.getObjectByName(bone);
                availableBonesControls.push(boneControl);
                const folder = gui.addFolder(bone);
                folder.add(boneControl.rotation, "x", -Math.PI, Math.PI);
                folder.add(boneControl.rotation, "y", -Math.PI, Math.PI);
                folder.add(boneControl.rotation, "z", -Math.PI, Math.PI);
                folder.add(boneControl.position, "x", -1, 1);
                folder.add(boneControl.position, "y", -1, 1);
                folder.add(boneControl.position, "z", -1, 1);
    
                // Setup target for IK
                if (bone === ikChain[0].effector) {
                    ikTargets[bone] = boneControl;
                }
            });
    
            // Initialize IK Solver
            ikChain.forEach((chain) => {
                chain.links.forEach((link) => {
                    link.index = model.getObjectByName(link.index);
                });
            });
            //lowman_shoes

            const solver = new CCDIKSolver(model.getObjectByName("lowman_shoes"), ikChain);
            animate(); // Start the animation loop
        });
    
        renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
        });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.outputEncoding = THREE.sRGBEncoding;
        document.body.appendChild(renderer.domElement);
    
        window.addEventListener("resize", onWindowResize, false);
    
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 1, 0);
        controls.update();
    }
    
    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    function solveIK(target, bones) {
    for (let i = 0; i < maxIterations; i++) {
        for (let bone of bones) {
            // Calculate the vector from the bone to the target
            let boneToTarget = target.clone().sub(bone.position);
            let boneToEndEffector = endEffector.position.clone().sub(bone.position);

            // Calculate the angle between them
            let angle = boneToTarget.angleTo(boneToEndEffector);

            // Calculate the rotation axis
            let axis = new THREE.Vector3().crossVectors(boneToEndEffector, boneToTarget).normalize();

            // Apply the rotation to the bone
            bone.applyAxisAngle(axis, angle);

            // Optionally apply constraints here
            constrainBoneRotation(bone);

            // Check if the end effector is close enough to the target
            if (endEffector.position.distanceTo(target) < tolerance) {
                break;
            }
        }
    }
    }


    onMount(() => {
        init();
        const animate = function () {
            requestAnimationFrame(animate);
            // sendPoseData();
            renderer.render(scene, camera);
        };
        animate();
    });
    </script>
    
    <svelte:window on:resize={onWindowResize} />
    
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">IK</h5>
            <canvas bind:this={canvas} />
        </div>
    </div>
    
    <style>
    canvas {
        width: 500px;
        height: 500px;
    }
    </style>
    