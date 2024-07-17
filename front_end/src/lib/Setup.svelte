<script lang="ts">
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
    import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
    import { MeshToonMaterial, TextureLoader } from 'three';
    import { OutlineEffect } from 'three/examples/jsm/effects/OutlineEffect.js';

    let canvas: HTMLCanvasElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let controls: OrbitControls;
    let effect: OutlineEffect;
    let gradientMap: THREE.Texture;

    onMount(() => {
        init();
        window.addEventListener("resize", onResize);
        return () => {
            window.removeEventListener("resize", onResize);
        };
    });

    function init() {
        renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x222322);
        effect = new OutlineEffect(renderer);

        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 30, 100);

        scene = new THREE.Scene();

        controls = new OrbitControls(camera, renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(0, 50, 50);
        scene.add(directionalLight);

        const textureLoader = new TextureLoader();
        gradientMap = textureLoader.load('path_to_gradient_texture.png'); // Replace with your gradient map
        gradientMap.minFilter = THREE.NearestFilter;
        gradientMap.magFilter = THREE.NearestFilter;

        const loader = new GLTFLoader();
        loader.load(
            'imus/imu_6.glb', // Your model path
            (gltf) => {
                gltf.scene.traverse(function (child) {
                    if (child.isMesh) {
                        child.material = new MeshToonMaterial({
                            gradientMap: gradientMap
                        });
                    }
                });
                scene.add(gltf.scene);
            },
            (xhr) => {
                console.log((xhr.loaded / xhr.total * 100) + '% loaded');
            },
            (error) => {
                console.error('An error happened', error);
            }
        );

        render();
    }

    function onResize() {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    }

    function render() {
        requestAnimationFrame(render);
        controls.update();
        effect.render(scene, camera);
    }
</script>

<svelte:head>
    <style>
        canvas {
            width: 100%;
            height: 100%;
            display: block;
        }
    </style>
</svelte:head>

<canvas bind:this={canvas}></canvas>
