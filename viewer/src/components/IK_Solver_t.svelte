<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
    import { animateModel, add_rigged_model } from "./RiggedModel.js";

    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    //righ hand
    let cubeR: THREE.Mesh;
    let transformControlsR: TransformControls;
    //left hand
    let cubeL: THREE.Mesh;
    let transformControlsL: TransformControls;

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
        scene.add(axesHelper);
        //add global light
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(light);
        add_rigged_model(scene);
        transformControlsR = new TransformControls(camera, renderer.domElement);
        transformControlsR.size = 0.75;
        transformControlsR.space = "world";
        //right hand
        cubeR = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
        );
        cubeR.position.set(3, 4, 0);
        scene.add(cubeR);
        transformControlsR.attach(cubeR);
        scene.add(transformControlsR);
        transformControlsR.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsR.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );
        //left hand
        cubeL = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0x0000ff }),
        );
        cubeL.position.set(-3, 4, 0);
        scene.add(cubeL);
        transformControlsL = new TransformControls(camera, renderer.domElement);
        transformControlsL.size = 0.75;
        transformControlsL.space = "world";
        transformControlsL.attach(cubeL);
        scene.add(transformControlsL);
        transformControlsL.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsL.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );

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
        animateModel(cubeR.position, cubeL.position);
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
