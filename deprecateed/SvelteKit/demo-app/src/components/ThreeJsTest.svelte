<script lang="ts">
	import * as THREE from 'three';
    import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
    import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
    import {onMount} from 'svelte';

    let container: HTMLElement;

    onMount(() => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({canvas: container});
        const controls = new OrbitControls(camera, renderer.domElement);
        const loader = new GLTFLoader();

        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.position.z = 5;

        //add a cube with wireframe to the scene
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshBasicMaterial({color: 0x00ff00});
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };

        animate();        
    });
</script>
<canvas bind:this={container}></canvas>