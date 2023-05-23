<script lang="ts">
    //D:\data-fusion\viewer\node_modules\three
    import * as THREE from "three";
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    onMount(() => {
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

        
        scene.add(cube);

        camera.position.z = 5;

        const animate = function () {
            requestAnimationFrame(animate);

            // cube.rotation.x += 0.01;
            // cube.rotation.y += 0.01;

            renderer.render(scene, camera);
        };

        animate();
    });

    let data: any;
    async function get() {
        const response = await fetch("http://localhost:8000/get");
        const json = await response.json();
        console.log(json);
        data = JSON.stringify(json)
    }
    async function randomCubeRotation() {
        const response = await fetch("http://localhost:8000/get");
        const json = await response.json();
        //structure
    // {"id":0,"accelerometer":{"x":0,"y":-0.08,"z":1.04},"gyroscope":{"x":0,"y":-0.12,"z":0.1}}
        cube.rotation.x += json.gyroscope.x;
        cube.rotation.y += json.gyroscope.y;
        cube.rotation.z += json.gyroscope.z;
        
    }
</script>

<h1>Welcome to SvelteKit</h1>
<p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
</p>
<canvas bind:this={canvas} width="500" height="500" />
<button on:click={get}>get</button>
<p>{data}</p>

<button on:click={randomCubeRotation}>randomCubeRotation</button>


