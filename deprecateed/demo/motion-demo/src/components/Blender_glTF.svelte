<script lang="ts">
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { onDestroy } from "svelte";
    import { open } from "@tauri-apps/api/dialog";
    import { readBinaryFile } from "@tauri-apps/api/fs";
    let canvas: HTMLCanvasElement;
    let file_path: string;
    onMount(() => {
        let scene: THREE.Scene;
        let loader = new GLTFLoader();
        let file_obj: THREE.Object3D;
        scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );

        const renderer = new THREE.WebGLRenderer({ canvas });
        // controls
        let controls = new OrbitControls(camera, renderer.domElement);
        controls.listenToKeyEvents(window); // optional
        renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.9);
        document.body.appendChild(renderer.domElement);
        //cube
        const geometry = new THREE.BoxGeometry();
        //wire frame
        const material = new THREE.MeshBasicMaterial({
            color: 0x00ff00,
            wireframe: true,
        });
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        // loader.load(
        //     "susan.glb",
        //     function (gltf) {
        //         file_obj = gltf.scene;
        //         file_obj.scale.set(0.1, 0.1, 0.1);
        //         scene.add(file_obj);
        //     },
        //     undefined,
        //     function (error) {
        //         console.error(error);
        //     }
        // );

        //add a light with loads of brightness
        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(10, 10, 10);
        light.intensity = 2;
        scene.add(light);

        camera.position.z = 5;
        function  checkIfFilesIsAvailable() {
            if (file_path) {
                console.log(file_path);
                readBinaryFile(file_path).then((data) => {
                    let str_data = new TextDecoder("utf-8").decode(data);
                    loader.parse(str_data, "", function (gltf) {
                        file_obj = gltf.scene;
                        file_obj.scale.set(0.1, 0.1, 0.1);
                        scene.add(file_obj);
                    });
                });
            }
            file_path = null;
        }
        const animate = () => {
            checkIfFilesIsAvailable();
            requestAnimationFrame(animate);
            controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
            renderer.render(scene, camera);
        };

        animate();

        window.addEventListener("resize", onWindowResize, false);
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();

            renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.9);
        }
    });
    //open a select file dialog
    async function openFile() {
        const selected = await open({
            multiple: false,
            directory: false,
            filters: [
                {
                    name: "glTF Files",
                    extensions: ["gltf", "glb"],
                },
            ],
        });
        if (Array.isArray(selected)) {
            // user selected multiple files
        } else if (selected === null) {
            // user cancelled the selection
        } else {
            // user selected a single file
            file_path = selected;
        }
    }
    onDestroy(() => {
        console.log("destroyed");
    });
</script>

<canvas bind:this={canvas} />
<button on:click={openFile}>Open</button>
