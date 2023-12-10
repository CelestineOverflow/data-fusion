<script lang="ts">
	import Camera from './Camera.svelte';
    import { CCDIKHelper } from "three/examples/jsm/animation/CCDIKSolver.js";
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
    import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;

    import {raw_data } from "../stores/websocket";
    
    let pose = {
        "head": {
            "rotation": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        },
        "chest": {
            "rotation": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        },
    }

    raw_data.subscribe((value) => {
        try {

            //Raw data: {"camera":{"id":19,"position":{"x":0.13985661012449555,"y":0.2898161857917122,"z":3.113400428397921},"rotation":{"x":0.03922555945961362,"y":0.05990199461313228,"z":0.08151047280510973}},"mcu":{"id":0,"orientation":{"pitch":-0.06,"roll":0,"yaw":-1.56,"unit":"rad/s"}}}


            pose.head.rotation.x = parseFloat(value.camera?.rotation?.x);
            pose.head.rotation.y = parseFloat(value.camera?.rotation?.y);
            pose.head.rotation.z = parseFloat(value.camera?.rotation?.z);
            pose.head.position.x = parseFloat(value.camera?.position?.x);
            pose.head.position.y = parseFloat(value.camera?.position?.y);
            pose.head.position.z = parseFloat(value.camera?.position?.z);

            pose.chest.rotation.x = parseFloat(value.mcu?.orientation?.pitch);
            pose.chest.rotation.y = parseFloat(value.mcu?.orientation?.roll);
            pose.chest.rotation.z = parseFloat(value.mcu?.orientation?.yaw);
            //convert to radians
            pose.chest.rotation.x = pose.chest.rotation.x * (Math.PI / 180);
            pose.chest.rotation.y = pose.chest.rotation.y * (Math.PI / 180);
            pose.chest.rotation.z = pose.chest.rotation.z * (Math.PI / 180);
            

        } catch (e) {
            console.log(e);
        }
    });
    onMount(() => {
        // setup scene
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            canvas.clientWidth / canvas.clientHeight,
            0.1,
            1000
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

        // Create a canvas element to use as a texture
        const canvas2 = document.createElement('canvas');
        canvas2.width = 256;
        canvas2.height = 256;
        const context = canvas2.getContext('2d');

        // Create a texture with a different color for each face of the cube
        colors.forEach((color, index) => {
            context.fillStyle = `#${color.toString(16)}`;

        });

        // Create the cube geometry and material
        const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
        const cubeMaterial = new THREE.MeshStandardMaterial({
            map: new THREE.CanvasTexture(canvas),
        });

        // Create the head cube and add it to the scene
        // const head_cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
        // scene.add(head_cube);

        // Create the chest cube and add it to the scene
        // const chest_cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
        // chest_cube.position.y = -1;
        // scene.add(chest_cube);

        //add light
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
        camera.position.z = 5;
        //show axes
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        //import model gtlf
        let astronaut = new THREE.Object3D();

        const loader = new GLTFLoader();
        loader.load(
            // resource URL
            "NeilArmstrong.glb",
            // called when the resource is loaded
            function (gltf) {
                astronaut = gltf.scene;
                //scale fritz-cola
                astronaut.scale.set(0.5, 0.5, 0.5);
                astronaut.rotation.y = Math.PI / 2;
                scene.add(astronaut);
                console.log("fritz-cola loaded");
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            // called when loading has errors
            function (error) {
                console.error("An error happened", error);
            }
        );

        let astronaut2 = new THREE.Object3D();
        loader.load(
            // resource URL
            "NeilArmstrong.glb",
            // called when the resource is loaded
            function (gltf) {
                astronaut2 = gltf.scene;
                //scale fritz-cola
                astronaut2.scale.set(0.5, 0.5, 0.5);
                astronaut2.rotation.y = Math.PI / 2;
                scene.add(astronaut2);
                console.log("fritz-cola loaded");
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            // called when loading has errors
            function (error) {
                console.error("An error happened", error);
            }
        );


        let time = 0;

        const animate = function () {
            requestAnimationFrame(animate);
            astronaut.rotation.x = pose.head.rotation.x;
            astronaut.rotation.y = pose.head.rotation.y;
            astronaut.rotation.z = pose.head.rotation.z;
            astronaut.position.x = -pose.head.position.x;
            astronaut.position.y = -pose.head.position.y;
            astronaut.position.z = -pose.head.position.z;
            astronaut2.rotation.x = pose.chest.rotation.x;
            astronaut2.rotation.y = pose.chest.rotation.y;
            astronaut2.rotation.z = pose.chest.rotation.z;
            time += 0.01;
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
