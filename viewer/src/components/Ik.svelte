<!-- <script lang="ts">
	import Camera from './Camera.svelte';
    import { CCDIKHelper } from "three/examples/jsm/animation/CCDIKSolver.js";
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
    import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;
    import {camera_data, mcu} from './../stores/websocket.js';

    let mcu_quat = new THREE.Quaternion();
    let camera_quat = new THREE.Quaternion();
    mcu.subscribe((value) => {
        for (const id in value) {
                if (id === '192.168.1.105') {
                    mcu.subscribe((value: { [key: string]: any }) => {
                        for (const id in value) {
                            if (id === '192.168.1.105') {
                                mcu_quat = new THREE.Quaternion(value[id].quaternion.x, value[id].quaternion.y, value[id].quaternion.z, value[id].quaternion.w);
                            }
                        }
                    });
                } 
            }
    });

    camera_data.subscribe((value) => {
        for (const id in value) {
                if (id === '192.168.1.105') {
                    mcu.subscribe((value: { [key: string]: any }) => {
                        for (const id in value) {
                            if (id === '192.168.1.105') {
                                mcu_quat = new THREE.Quaternion(value[id].quaternion.x, value[id].quaternion.y, value[id].quaternion.z, value[id].quaternion.w);
                            }
                        }
                    });
                } 
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
            if (context) {
                context.fillStyle = `#${color.toString(16)}`;
            }

        });

        // Create the cube geometry and material
        const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
        const cubeMaterial = new THREE.MeshStandardMaterial({
            map: new THREE.CanvasTexture(canvas),
        });


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
            astronaut.quaternion.copy(mcu_quat);
            astronaut2.quaternion.copy(quaternion2);
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
</style> -->
