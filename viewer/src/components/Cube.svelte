<!-- <script lang="ts">
    //D:\data-fusion\viewer\node_modules\three
    import * as THREE from "three";
    import { onMount } from "svelte";
    import { rotation_vector, position_vector } from "../stores/vectors.js";
    let rotation_vector_value: number[] = [0, 0, 0];
    let position_vector_value: number[] = [0, 0, 0];

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

        rotation_vector.subscribe((value) => {
            cube.rotation.x = value[0];
            cube.rotation.y = value[1];
            cube.rotation.z = value[2];
            rotation_vector_value = value;
        });
        position_vector.subscribe((value) => {
            cube.position.x = value[0];
            cube.position.y = value[1];
            cube.position.z = value[2];
            position_vector_value = value;
        });

        animate();
    });

</script>

<h1>cube</h1>
<h2>rotation_vector_value: {rotation_vector_value}</h2>
<h2>position_vector_value: {position_vector_value}</h2>
<canvas bind:this={canvas} width="500" height="500" /> -->
