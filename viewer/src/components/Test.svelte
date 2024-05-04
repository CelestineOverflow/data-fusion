<script lang="ts">
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import { send2Socket } from "../stores/websocket";
    import { limbs_data, resetLocalStorage } from "../stores/body";

    let canvas: HTMLCanvasElement;

    // Unified function to send data
    function sendPositionOrRotation(data, type, tracker) {
        if (type === "position") {
            const message = {
                tracker: tracker,
                position: [data.positionX, data.positionY, data.positionZ],
            };
            send2Socket(JSON.stringify(message));
        }
        else if (type === "rotation") {
            const message = {
                tracker: tracker,
                rotation: [data.rotationX, data.rotationY, data.rotationZ],
            };
            send2Socket(JSON.stringify(message));
        }
    }

    let limbs = [];

    limbs_data.subscribe((value) => {
        limbs = value;
    });

    function getLimb(limbname: string) {
        let limb = limbs.find((limb) => limb.name === limbname);
        return limb;
    }

    let selectedLimb = limbs[0]; // Default to the first limb
    // Function to get world-relative Euler rotation in degrees
    function getWorldEulerRotation(object) {
        const worldQuaternion = new THREE.Quaternion();
        object.getWorldQuaternion(worldQuaternion);
        const worldEuler = new THREE.Euler().setFromQuaternion(
            worldQuaternion,
            "XYZ",
        );
        return {
            x: worldEuler.x * (180 / Math.PI),
            y: worldEuler.y * (180 / Math.PI),
            z: worldEuler.z * (180 / Math.PI),
        };
    }

    function getWorldPosition(object) {
        const worldPosition = new THREE.Vector3();
        object.getWorldPosition(worldPosition);
        return {
            x: worldPosition.x,
            y: worldPosition.y,
            z: worldPosition.z,
        };
    }
    let limbMeshes = new Map(); // Store references to limb meshes

    onMount(() => {
        
        // setup scene
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            canvas.clientWidth / canvas.clientHeight,
            0.1,
            1000,
        );

        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
        });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        // add controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.update();
        // add plane
        const planeGeometry = new THREE.PlaneGeometry(10, 10, 10);
        // material is a wireframe
        const planeMaterial = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            wireframe: true,
        });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = Math.PI / 2;
        plane.position.y = -2.5;
        scene.add(plane);

        // Define the colors for each face of the cube
        const colors = [
            0xff0000, // right face
            0x00ff00, // left face
            0x0000ff, // top face
            0xffff00, // bottom face
            0xff00ff, // front face
            0x00ffff, // back face
        ];

        //add light
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
        camera.position.z = 5;
        //show axes
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        //add linbs
        limbs.forEach(limb => {
        if (!limbMeshes.has(limb.name)) {
            // Create a new cube for the limb if it doesn't exist
            const geometry = new THREE.BoxGeometry(0.2, .2, .2);
            const material = new THREE.MeshBasicMaterial({ color: new THREE.Color().setHex(Math.random() * 0xffffff) });
            const cube = new THREE.Mesh(geometry, material);
            scene.add(cube);
            limbMeshes.set(limb.name, cube);
            
        }
        // Update cube position and rotation
        const mesh = limbMeshes.get(limb.name);
        mesh.position.set(limb.positionX, limb.positionY, limb.positionZ);
        mesh.rotation.set(limb.rotationX, limb.rotationY, limb.rotationZ);
        });

        const animate = function () {
            requestAnimationFrame(animate);
            limbs_data.set(limbs);

            limbs.forEach(limb => {
                
    
        const mesh = limbMeshes.get(limb.name);
        mesh.position.set(limb.positionX, limb.positionY, limb.positionZ);
        // mesh.rotation.set(limb.rotationX, limb.rotationY, limb.rotationZ);
        //convert to radians from degrees
        mesh.rotation.set(
            limb.rotationX * (Math.PI / 180),
            limb.rotationY * (Math.PI / 180),
            limb.rotationZ * (Math.PI / 180),
        );
        });
           

            renderer.render(scene, camera);

        };

        animate();
        
    });
    
</script>

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
