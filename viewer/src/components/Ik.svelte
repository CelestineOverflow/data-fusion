<script lang="ts">
    import { CCDIKHelper } from "three/examples/jsm/animation/CCDIKSolver.js";
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
    import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";
    import { CCDIKSolver } from "three/examples/jsm/animation/CCDIKSolver.js";
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;
    let ikSolver: CCDIKSolver;

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

        //add cube
        const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
        const cubeMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
        scene.add(cube);

        //add light
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
        camera.position.z = 5;
        //add ik
        let bones = [];
        let totalBones = 3;
        // "root"
        let rootBone = new THREE.Bone();
        rootBone.position.y = -12;
        bones.push(rootBone);

        // "bone0"
        let prevBone = new THREE.Bone();
        prevBone.position.y = 0;
        rootBone.add(prevBone);
        bones.push(prevBone);

        // "bone1", "bone2", "bone3"
        for (let i = 1; i <= 3; i++) {
            const bone = new THREE.Bone();
            bone.position.y = 8;
            bones.push(bone);

            prevBone.add(bone);
            prevBone = bone;
        }

        // "target"
        const targetBone = new THREE.Bone();
        targetBone.position.y = 24 + 8;
        rootBone.add(targetBone);
        bones.push(targetBone);

        //
        // skinned mesh
        //

        const mesh = new THREE.SkinnedMesh(
            new THREE.CylinderGeometry(5, 5, 24, 8, 1),
            new THREE.MeshBasicMaterial()
        );
        const skeleton = new THREE.Skeleton(bones);

        mesh.add(bones[0]); // "root" bone
        mesh.bind(skeleton);

        //
        // ikSolver
        //

        const iks = [
            {
                target: 5, // "target"
                effector: 4, // "bone3"
                links: [{ index: 3 }, { index: 2 }, { index: 1 }], // "bone2", "bone1", "bone0"
            },
        ];
        ikSolver = new CCDIKSolver(mesh, iks);

        //
        // debug helpers
        //
        scene.add(mesh);

        const helper = new THREE.SkeletonHelper(mesh);
        helper.visible = false;
        scene.add(helper);

        let time = 0;

        const animate = function () {
            requestAnimationFrame(animate);
            time += 0.01;

            // move random position in horizontal plane
            const radius = 10;
            const angle = time * 0.5;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            targetBone.position.set(x, 0, z);

            ikSolver.update(); // Update IK before rendering

            renderer.render(scene, camera);
        };

        animate();
    });
</script>

<canvas bind:this={canvas} />

<style>
    canvas {
        width: 500px;
        height: 500px;
    }
</style>
