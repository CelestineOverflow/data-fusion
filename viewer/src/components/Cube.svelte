<script lang="ts">
	import Ik from './Ik.svelte';
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { send2Socket, raw_data, output_quaternion } from "../stores/websocket";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

    let data;
    let quat = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"

    // Subscription to the data stream
    raw_data.subscribe((value) => {
        data = JSON.stringify(value, null, 2);
        if (
            value.imu &&
            value.imu["98CDAC1D78E6"] &&
            value.imu["98CDAC1D78E6"].quaternion
        ) {
            try {
                quat.set(
                    value.imu["98CDAC1D78E6"].quaternion.x,
                    value.imu["98CDAC1D78E6"].quaternion.y,
                    value.imu["98CDAC1D78E6"].quaternion.z,
                    value.imu["98CDAC1D78E6"].quaternion.w,
                );
            } catch (error) {
            }
        } 
    });

    let quat_test = new THREE.Quaternion();

    output_quaternion.subscribe((value) => {
        quat_test.set(value[0], value[1], value[2], value[3]);
    });

    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    let astronaut = new THREE.Object3D();

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

let eulerx = 0;
let eulery = 0;
let eulerz = 0;
function applyIMURotationWithOffset(imuData) {
    let lastQuaternion = imuData.clone(); // Save the current quaternion for the next iteration

    // Create the rotation quaternion for the initial rotation
    let rotationQuaternion = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2);

    // Apply the fixed rotation to the IMU data quaternion
    lastQuaternion.premultiply(rotationQuaternion);

    // Swap Y and X axis in the quaternion; this also inverts the new Y-axis (which is the original X)
    let swappedAndInvertedQuaternion = new THREE.Quaternion(-lastQuaternion.y, lastQuaternion.x, lastQuaternion.z, lastQuaternion.w);

    // Set the astronaut's rotation from the adjusted quaternion
    astronaut.setRotationFromQuaternion(swappedAndInvertedQuaternion);

    let euler = new THREE.Euler();
    euler.setFromQuaternion(lastQuaternion, "XYZ");
     eulerx = THREE.MathUtils.radToDeg(euler.x);
     eulery = THREE.MathUtils.radToDeg(euler.y);
     eulerz = THREE.MathUtils.radToDeg(euler.z);
}


    function render() {
        requestAnimationFrame(render);
        controls.update();
        renderer.render(scene, camera);
        //use quaternion to rotate the cube
        // applyIMURotationWithOffset(quat);
        astronaut.setRotationFromQuaternion(quat_test);
    }
</script>
<h1>3D Cube x {eulerx.toFixed(2)} y {eulery.toFixed(2)} z {eulerz.toFixed(2)}</h1>
<button on:click={() => offsetSet = false}>Reset Offset</button>
<canvas bind:this={canvas}></canvas>

<style>
    canvas {
        width: 100%;
        height: 100%;
        display: block;
    }
</style>
