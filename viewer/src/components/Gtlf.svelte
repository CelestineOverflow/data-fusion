<script lang="ts">
    //D:\data-fusion\viewer\node_modules\three
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
    import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";
    import { onMount } from "svelte";
    import { rotation_vector_0, position_vector_0, rotation_vector_1, position_vector_1 } from "../stores/vectors";
    let rotation_vector_value: number[] = [0, 0, 0];
    let position_vector_value: number[] = [0, 0, 0];

    let canvas: HTMLCanvasElement;
    
    //load gltf
    

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
        // add cube
        const geometry = new THREE.BoxGeometry();
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const cube = new THREE.Mesh(geometry, material);
        // add rgb lights
        RectAreaLightUniformsLib.init();
        const rectLight1 = new THREE.RectAreaLight( 0xff0000, 5, 4, 10 );
        rectLight1.position.set( - 5, 5, 5 );
        scene.add( rectLight1 );

        const rectLight2 = new THREE.RectAreaLight( 0x00ff00, 5, 4, 10 );
        rectLight2.position.set( 0, 5, 5 );
        scene.add( rectLight2 );

        const rectLight3 = new THREE.RectAreaLight( 0x0000ff, 5, 4, 10 );
        rectLight3.position.set( 5, 5, 5 );
        scene.add( rectLight3 );

        scene.add( new RectAreaLightHelper( rectLight1 ) );
        scene.add( new RectAreaLightHelper( rectLight2 ) );
        scene.add( new RectAreaLightHelper( rectLight3 ) );
        // add plane
        const planeGeometry = new THREE.PlaneGeometry(10, 10, 10);
        // material is a wireframe
        const planeMaterial = new THREE.MeshBasicMaterial({
            color: 0xFFFFFF,
            wireframe: true,
        });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = Math.PI / 2;
        plane.position.y = -2.5;
        scene.add(plane);
        // let cube = new THREE.Mesh();
        // Load a glTF resource
        let fritz_cola = new THREE.Object3D();

        const loader = new GLTFLoader();
        loader.load(
            // resource URL
            "fritz-cola.gltf",
            // called when the resource is loaded
            function (gltf) {
                fritz_cola = gltf.scene;
                //scale fritz-cola
                fritz_cola.scale.set(0.5, 0.5, 0.5);
                fritz_cola.rotation.y = Math.PI / 2;
                scene.add(fritz_cola);
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
        //companion cube
        let companion_cube = new THREE.Object3D();
        loader.load(
            // resource URL
            "companion_cube.gltf",
            // called when the resource is loaded
            function (gltf) {
                companion_cube = gltf.scene;
                //move companion cube 5m to the right
                companion_cube.position.x = 2;
                scene.add(companion_cube);
                console.log("companion-cube loaded");
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

        //move companion cube 1m to the right
        

        //add light
        const light = new THREE.AmbientLight(0xFFFFFF, 1);
        scene.add(light);
        camera.position.z = 5;

        const animate = function () {
            requestAnimationFrame(animate);

            // cube.rotation.x += 0.01;
            // cube.rotation.y += 0.01;

            renderer.render(scene, camera);
            //controls
            controls.update();
        };

        rotation_vector_0.subscribe((value) => {
            fritz_cola.rotation.x = value[0];
            fritz_cola.rotation.y = value[1];
            fritz_cola.rotation.z = value[2];
            rotation_vector_value = [value[0], value[1], value[2]];
        });
        // position_vector_0.subscribe((value) => {
        //     fritz_cola.position.x = value[0];
        //     fritz_cola.position.y = value[1];
        //     fritz_cola.position.z = value[2];
        //     position_vector_value = value;
        // });

        rotation_vector_1.subscribe((value) => {
            companion_cube.rotation.x = value[0];
            companion_cube.rotation.y = value[1];
            companion_cube.rotation.z = value[2];
            rotation_vector_value = [value[0], value[1], value[2]];
        });

        // position_vector_1.subscribe((value) => {
        //     companion_cube.position.x = value[0];
        //     companion_cube.position.y = value[1];
        //     companion_cube.position.z = value[2];
        // });

        animate();
    });
</script>

<h1>cube</h1>
<h2>rotation_vector_value: {rotation_vector_value}</h2>
<h2>position_vector_value: {position_vector_value}</h2>
<canvas bind:this={canvas} ></canvas>


<style>
    canvas {
        width: 500px;
        height: 500px;
    }
</style>
