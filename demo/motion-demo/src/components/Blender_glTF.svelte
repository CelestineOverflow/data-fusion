<script lang="ts">
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { onDestroy } from "svelte";
    let canvas: HTMLCanvasElement;

    onMount(() => {
        const scene = new THREE.Scene();
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
        let loader = new GLTFLoader();
        let susan: THREE.Object3D;
        loader.load(
            "susan.glb",
            function (gltf) {
                susan = gltf.scene;
                susan.scale.set(0.1, 0.1, 0.1);
                scene.add(susan);
            },
            undefined,
            function (error) {
                console.error(error);
            }
        );

        //add a light with loads of brightness
        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(10, 10, 10);
        light.intensity = 2;
        scene.add(light);

        camera.position.z = 5;

        const animate = () => {
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
    onDestroy(() => {
        console.log("destroyed");
    });
</script>

<canvas bind:this={canvas} />
