<script lang="ts">
    import * as THREE from "three";
    import {
        CCDIKSolver,
        CCDIKHelper,
    } from "three/examples/jsm/animation/CCDIKSolver.js";
    import { onMount } from "svelte";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    let canvas: HTMLCanvasElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let controls: OrbitControls;
    const target = new THREE.Object3D();
    let ikSolver : CCDIKSolver;
    const OOI = {};
    function initScene() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        renderer = new THREE.WebGLRenderer({ canvas });
        controls = new OrbitControls(camera, renderer.domElement);
        controls.listenToKeyEvents(window); // optional
        renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.9);
        document.body.appendChild(renderer.domElement);
        camera.position.z = 5;

        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(10, 10, 10);
        light.intensity = 2;
        scene.add(light);
        addGTLFModel();
    }

    function addGTLFModel() {
        const loader = new GLTFLoader();
        loader.load("arm.gltf", function (gltf) {
            const file_obj = gltf.scene;
            file_obj.scale.set(1, 1, 1);
            scene.add(file_obj);
            let cylinder = file_obj.getObjectByName("Cylinder003");
            cylinder.add(cylinder.skeleton.bones[0]);
            cylinder.material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
            let count = 0;
            file_obj.traverse((child) => {
                //add the index of the bone
                if (child.name === "Bone") {
                    OOI["Bone"] = count;
                }
                if (child.name === "Bone001") {
                    OOI["Bone001"] = count;
                }
                if (child.name === "Target") {
                    OOI["Target"] = count;
                }
                count++;
            });
            console.log(OOI);
            const iks = [
                {
                    target: OOI["Target"],
                    effector: OOI["Bone001"], // "bone3"
                    links: [{ index: OOI["Bone"] }, { index: OOI["Bone001"] }], // "bone2", "bone1", "bone0"
                },
            ];
            ikSolver = new CCDIKSolver(cylinder, iks);
            scene.add(new CCDIKHelper(cylinder, iks));
        });
    }

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
        // target.position.x = Math.sin(Date.now() / 1000) * 5;
    };

    onMount(() => {
        initScene();
        animate();
    });
</script>

<canvas bind:this={canvas} />
