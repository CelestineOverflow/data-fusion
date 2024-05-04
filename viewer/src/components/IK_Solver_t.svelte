<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { CCDIKSolver } from "three/examples/jsm/animation/CCDIKSolver.js";
    import { SkinnedMesh } from "three";

    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    let defaultBoneDirection: THREE.Vector3;
    let defaultBoneLength: number;
    let target: THREE.Vector3;
    let upperArmBone : any;
    let forearmBone : any;
    let handBone : any;
    let target_handL : any;
    let transformControls : TransformControls;
    let orbitControls : OrbitControls;
    let solver : CCDIKSolver;
    let cube : THREE.Mesh;

    onMount(() => {
        init();
        window.addEventListener("resize", resize);
        return () => {
            window.removeEventListener("resize", resize);
        };
    });
    let availableBones: string[] = [];
    let model: any;


    function findBone(root, name) {
        let target = null;
        root.traverse((node) => {
            if (node.name === name) {
                target = node;
            }
        });
        return target;
    }
    let skeleton : any;
    

function add_rigged_model() {
    const loader = new GLTFLoader();
    loader.load("test_ik3.glb", function (gltf) {
        model = gltf.scene;
        let skinnedMesh;
        model.traverse((node) => {
            if (node.name === "lowman_shoes") {
                node.traverse((child) => {
                    if (child.type === "SkinnedMesh") {
                        skinnedMesh = child;
                    }
                });
            }
        });

        if (skinnedMesh) {
            console.log("SkinnedMesh found", skinnedMesh);
            model.scale.set(20, 20, 20);
            console.log(skinnedMesh.skeleton.bones);
            for (let i = 0; i < skinnedMesh.skeleton.bones.length; i++) {
                if (skinnedMesh.skeleton.bones[i].name === "upper_armL") {
                    upperArmBone = skinnedMesh.skeleton.bones[i];
                } else if (skinnedMesh.skeleton.bones[i].name === "forearmL") {
                    forearmBone = skinnedMesh.skeleton.bones[i];
                } else if (skinnedMesh.skeleton.bones[i].name === "handL") {
                    handBone = skinnedMesh.skeleton.bones[i];
                } else if (skinnedMesh.skeleton.bones[i].name === "index_target_handL") {
                    target_handL = skinnedMesh.skeleton.bones[i];
                }
            }
            if (upperArmBone && forearmBone && handBone) {
                console.log("Bones found:", upperArmBone, forearmBone, handBone);
                let index_upperArm = skinnedMesh.skeleton.bones.indexOf(upperArmBone);
                let index_forearm = skinnedMesh.skeleton.bones.indexOf(forearmBone);
                let index_hand = skinnedMesh.skeleton.bones.indexOf(handBone);
                let index_target_handL = skinnedMesh.skeleton.bones.indexOf(target_handL);
                console.log("Indices:", index_upperArm, index_forearm, index_hand, index_target_handL);
                
                // Define IK Chains

                const iks = [
                {
                target: index_target_handL, // "target"
                effector: index_hand, // "bone3"
                links: [ { index: index_forearm }, { index: index_upperArm } ] // "bone2", "bone1", "bone0"
                }
                ];

                // Initialize CCDIKSolver with the SkinnedMesh
                solver = new CCDIKSolver(skinnedMesh, iks);
            } else {
                console.error("Error: One or more bones not found.");
            }

            // Visualize skeleton
            skeleton = new THREE.SkeletonHelper(model);
            skeleton.visible = true;
            scene.add(skeleton);
            scene.add(model);
        } else {
            console.error("SkinnedMesh not found.");
        }
    });
}
    
    // function add_rigged_model() {
    //     const loader = new GLTFLoader();
    //     loader.load("test_ik3.glb", function (gltf) {
    //         model = gltf.scene;
    //         let skinedMesh ;
    //         model.traverse((node) => {
    //             // console.log(node.name);
    //             if (node.name === "lowman_shoes") {
    //                 //print the type of the node
    //                 console.log(node.type);
    //                 node.traverse((child) => {
    //                     //print the name of the child node
    //                     console.log(child.type);
    //                     if (child.type === "SkinnedMesh") {
    //                         skinedMesh = child;
    //                     }
    //                 });
    //             }
    //         });
    //         if (skinedMesh) {
    //             console.log("skinedMesh found");
    //         }
    //         model.scale.set(20, 20, 20);
    //         upperArmBone = findBone(model, "upper_armL");
    //         forearmBone = findBone(model, "forearmL");
    //         handBone = findBone(model, "handL");
    //         skeleton = new THREE.SkeletonHelper( model );
    //         skeleton.visible = true;
    //         scene.add( skeleton );
    //         scene.add(model);
    //     });
        
    // }

    function init() {
        renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x222322);

        camera = new THREE.PerspectiveCamera(
            60,
            window.innerWidth / window.innerHeight,
            0.1,
            2000,
        );
        camera.position.set(0, 30, 100);

        scene = new THREE.Scene();
        const gridHelper = new THREE.GridHelper(100, 10);
        scene.add(gridHelper);

        const ambientLight = new THREE.AmbientLight(0x101010);
        scene.add(ambientLight);

        controls = new OrbitControls(camera, renderer.domElement);

        //add axes helper
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        //add global light
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(light);
        add_rigged_model();
        //orbitControls = new OrbitControls( camera, renderer.domElement );
        transformControls = new TransformControls( camera, renderer.domElement );
        transformControls.size = 0.75;
        transformControls.space = 'world';
        cube = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ color: 0x00ff00 }));
        cube.position.set(3, 4, 0);
        scene.add(cube);
        transformControls.attach( cube );
        scene.add( transformControls );
        transformControls.addEventListener( 'mouseDown', () => controls.enabled = false );
        transformControls.addEventListener( 'mouseUp', () => controls.enabled = true );
        render();
    }


    

    function resize() {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    }

    function render() {
        requestAnimationFrame(render);
        controls.update();
        renderer.render(scene, camera);
        solver.update();

        target_handL.position.copy(cube.position);
    }
</script>

<canvas bind:this={canvas}></canvas>

<style>
    canvas {
        width: 100%;
        height: 100%;
        display: block;
    }
</style>
