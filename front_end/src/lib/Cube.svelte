<script lang="ts">
	import Ik from './Ik.svelte';
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { send2Socket, output_quaternion, output_quaternion3 } from "../stores/websocket";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

    let data;
    let quat = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"


    let quat_test = new THREE.Quaternion();
    let quat_test2 = new THREE.Quaternion();

    output_quaternion.subscribe((value) => {
        quat_test.set(value[0], value[1], value[2], value[3]);
        //rotate quat x 90 degrees
        //quat_test.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2));
    });

    output_quaternion3.subscribe((value) => {
        quat_test2.set(value[0], value[1], value[2], value[3]);
        quat_test2.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
    });

    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    let astronaut = new THREE.Object3D();
    let astronaut2 = new THREE.Object3D();

    onMount(() => {
        init();
        window.addEventListener("resize", resize);
        return () => {
            window.removeEventListener("resize", resize);
        };
    });

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
        axesHelper.position.set(10, 0, 0);
        scene.add(axesHelper);
        //add global light
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(light);
        // scene.add(cubeRot2);
        // scene.add(cubeRot3);

        const loader = new GLTFLoader();
        loader.load(
            // resource URL
            "test_ik4.glb",
            // called when the resource is loaded
            function (gltf) {
                astronaut = gltf.scene;
                scene.add(astronaut);
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            // called when loading has errors
            function (error) {
                console.error("An error happened", error);
            },
        );

        loader.load(
            // resource URL
            "test_ik4.glb",
            // called when the resource is loaded
            function (gltf) {
                astronaut2 = gltf.scene;
                astronaut2.position.set(5, 0, 0);
                scene.add(astronaut2);
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            // called when loading has errors
            function (error) {
                console.error("An error happened", error);
            },
        );
        render();
    }

    function resize() {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    }

    let lastQuaternion = new THREE.Quaternion();  // Keep track of the last quaternion
    let quatOffset = new THREE.Quaternion();  // Offset quaternion to apply to the incoming quaternion
    let offsetSet = true;  // Flag to check if the offset has been set


    function render() {
        requestAnimationFrame(render);
        controls.update();
        renderer.render(scene, camera);
        //use quaternion to rotate the cube
        // applyIMURotationWithOffset(quat);
        astronaut.setRotationFromQuaternion(quat_test);
        console.log(quat_test);
        astronaut2.setRotationFromQuaternion(quat_test2);
    }
</script>
<button on:click={() => offsetSet = false}>Reset Offset</button>
<canvas bind:this={canvas}></canvas>

<style>
    canvas {
        width: 100%;
        height: 100%;
        display: block;
    }
</style>
