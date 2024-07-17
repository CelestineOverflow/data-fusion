<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
    import { animateModel, add_rigged_model } from "./RiggedModel.js";
    import {connectToWebSocket, thighquatL, thighquatR, baseBoneQuat } from "../stores/websocket";
    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    // head rotation
    let cubeRot: THREE.Mesh;
    let transformControlsRotation: TransformControls;
    // test RotationTransform
    let cubeRot2: THREE.Mesh;
    let transformControlsRotation2: TransformControls;
    // test RotationTransform 2
    let cubeRot3: THREE.Mesh;
    let transformControlsRotation3: TransformControls;
    //righ hand
    let cubeR: THREE.Mesh;
    let transformControlsR: TransformControls;
    //left hand
    let cubeL: THREE.Mesh;
    let transformControlsL: TransformControls;
    onMount(() => {
        init();
        connectToWebSocket();
        window.addEventListener("resize", resize);
        return () => {
            window.removeEventListener("resize", resize);
        };
    });


    let _thighquatL = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"
    let _thighquatR = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"
    let _baseBoneQuat = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"

    // Subscription to the data strea
    thighquatL.subscribe((value: number[]) => {
        _thighquatL.set(value[0], value[1], value[2], value[3]);
        _thighquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
    });
    thighquatR.subscribe((value: number[]) => {
        _thighquatR.set(value[0], value[1], value[2], value[3]);
    });
    baseBoneQuat.subscribe((value: number[]) => {
        _baseBoneQuat.set(value[0], value[1], value[2], value[3]);
        _baseBoneQuat.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
        
    });



    function init() {
        renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
        let width = window.innerWidth / 2;
		let height = window.innerHeight;
		renderer.setSize(width, height);
        renderer.setClearColor(0x222322);

        camera = new THREE.PerspectiveCamera(
            60,
            width / height,
            0.1,
            2000,
        );
        camera.position.set(0, 2, 5);

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
        const light = new THREE.AmbientLight(0xffffff, 2);
        scene.add(light);
        add_rigged_model(scene);
        // let targetL, targetR;
        // targetL, targetR = getTargetPosition();
        transformControlsR = new TransformControls(camera, renderer.domElement);
        transformControlsR.size = 0.75;
        transformControlsR.space = "world";
        //right hand
        cubeR = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
        );
        cubeR.position.set(0.3, 0.4, 0);
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
        cubeL.position.set(-0.3, 0.4, 0);
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
        //head rotation
        cubeRot = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0xff0000 }),
        );
        cubeRot.position.set(0, 0, 0);
        transformControlsRotation = new TransformControls(
            camera,
            renderer.domElement,
        );
        transformControlsRotation.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsRotation.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );
        transformControlsRotation.size = 0.75;
        transformControlsRotation.space = "world";
        transformControlsRotation.setMode("rotate"); // Set mode to rotate
        transformControlsRotation.attach(cubeRot);
        scene.add(transformControlsRotation);
        scene.add(cubeRot);
        //test RotationTransform
        cubeRot2 = new THREE.Mesh(
            new THREE.BoxGeometry(0.2, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0xff00ff }),
        );
        cubeRot2.rotation.set(0, 0, 0);
        cubeRot2.position.set(0, 3, 0);
        transformControlsRotation2 = new TransformControls(
            camera,
            renderer.domElement,
        );
        transformControlsRotation2.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsRotation2.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );
        transformControlsRotation2.size = 0.75;
        transformControlsRotation2.space = "world";
        transformControlsRotation2.setMode("rotate"); // Set mode to rotate
        transformControlsRotation2.attach(cubeRot2);
        scene.add(transformControlsRotation2);
        scene.add(cubeRot2);
        //test RotationTransform 2
        cubeRot3 = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
        );
        //Euler {isEuler: true, _x: 0.19723690127134982, _y: 0.03838020303701466, _z: 0.11460420814749764, _order: 'XYZ', …
        cubeRot3.rotation.set(0, 0, 0);
        cubeRot3.position.set(2, 2, 0);
        transformControlsRotation3 = new TransformControls(
            camera,
            renderer.domElement,
        );
        transformControlsRotation3.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsRotation3.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );
        transformControlsRotation3.size = 0.75;
        transformControlsRotation3.space = "world";
        transformControlsRotation3.setMode("rotate"); // Set mode to rotate
        transformControlsRotation3.attach(cubeRot3);
        scene.add(transformControlsRotation3);
        scene.add(cubeRot3);
    
        
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
        animateModel(cubeR.position, cubeL.position, cubeRot.rotation, thighquatL, thighquatR, baseBoneQuat);
    }
</script>

<canvas bind:this={canvas}></canvas>

