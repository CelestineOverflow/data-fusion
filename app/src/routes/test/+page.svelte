<script lang="ts">
    import * as THREE from 'three';
    import { onMount, onDestroy } from 'svelte';
	import { add_rigged_model } from '$lib/RiggedModel.js';
    let canvas: HTMLCanvasElement;

    onMount(() => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

        camera.position.z = 5;

        const renderer = new THREE.WebGLRenderer({ canvas });
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);

        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);



        add_rigged_model(scene);

        const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };

        animate();

        const onWindowResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('resize', onWindowResize);

        // Cleanup event listener on component destruction
        onDestroy(() => {
            window.removeEventListener('resize', onWindowResize);
        });
    });
</script>

<canvas bind:this={canvas}></canvas>

<style>
    canvas {
        width: 100%;
        height: 100%;
    }
</style>
