<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
    import { animateModel, add_rigged_model } from "./RiggedModel.js";
    import {connectToWebSocket, thighquatL, thighquatR, baseBoneQuat } from "../stores/websocket.js";
    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    // spine position
    let spine_position_cube: THREE.Mesh;
    let transformControlsPosition: TransformControls;
    // head rotation
    let cubeRot: THREE.Mesh;
    let transformControlsRotation: TransformControls;
    // test RotationTransform
    let thig_l_cube: THREE.Mesh;
    let transformControlsRotation2: TransformControls;
    // test RotationTransform 2
    let thig_r_cube: THREE.Mesh;
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


    let _thighquatL = new THREE.Quaternion();
    let _thighquatR = new THREE.Quaternion(); 
    let _baseBoneQuat = new THREE.Quaternion(); 

    thighquatL.subscribe((value) => {
        
        _thighquatL.set(value[0], value[1], value[2], value[3]);
        _thighquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
        //inverting z axis
        _thighquatL.set(_thighquatL.x, -_thighquatL.y, -_thighquatL.z, _thighquatL.w);
    });
    thighquatR.subscribe((value) => {
        // 
        _thighquatR.set(value[0], value[1], value[2], value[3]);
        _thighquatR.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
        _thighquatR.set(_thighquatR.x, -_thighquatR.y, -_thighquatR.z, _thighquatR.w);
    });
    baseBoneQuat.subscribe((value) => {
        _baseBoneQuat.set(value[0], value[1], value[2], value[3]);
        _baseBoneQuat.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(-1, 0, 0), Math.PI / 2));
        _baseBoneQuat.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI));
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
        //spine position
        spine_position_cube = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0xff0000 }),
        );
        spine_position_cube.position.set(0, 0, 0);
        transformControlsPosition = new TransformControls(
            camera,
            renderer.domElement,
        );
        transformControlsPosition.addEventListener(
            "mouseDown",
            () => (controls.enabled = false),
        );
        transformControlsPosition.addEventListener(
            "mouseUp",
            () => (controls.enabled = true),
        );

        transformControlsPosition.size = 0.75;
        transformControlsPosition.space = "world";
        transformControlsPosition.attach(spine_position_cube);
        scene.add(transformControlsPosition);
        scene.add(spine_position_cube);

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
        cubeRot.rotation.set(0, 1, 0);
        scene.add(cubeRot);
        //test RotationTransform
        thig_l_cube = new THREE.Mesh(
            new THREE.BoxGeometry(0.2, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0xff00ff }),
        );
        thig_l_cube.rotation.set(0, 0, 0);
        thig_l_cube.position.set(0, 3, 0);
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
        transformControlsRotation2.attach(thig_l_cube);
        scene.add(transformControlsRotation2);
        scene.add(thig_l_cube);
        thig_l_cube.rotation.set(1, 0, 0);
        
        //test RotationTransform 2
        thig_r_cube = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, 0.1, 0.1),
            new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
        );
        //Euler {isEuler: true, _x: 0.19723690127134982, _y: 0.03838020303701466, _z: 0.11460420814749764, _order: 'XYZ', …
        thig_r_cube.rotation.set(1, 0, 0);
        thig_r_cube.position.set(2, 2, 0);
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
        transformControlsRotation3.attach(thig_r_cube);
        scene.add(transformControlsRotation3);
        scene.add(thig_r_cube);
    
        
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
        animateModel(cubeR.position, cubeL.position, cubeRot.rotation, thig_l_cube.quaternion, thig_r_cube.quaternion, _baseBoneQuat, spine_position_cube.position);
    }
</script>

<canvas bind:this={canvas}></canvas>

