<script lang="ts">
    import * as THREE from "three";
    import {
        CCDIKSolver,
        CCDIKHelper,
    } from "three/examples/jsm/animation/CCDIKSolver.js";
    import { onMount } from "svelte";
    import { GUI } from "three/examples/jsm/libs/lil-gui.module.min.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

    let canvas: HTMLCanvasElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let controls: OrbitControls;
    let gui: GUI;
    let mesh, bones, skeletonHelper, ikSolver;
    const state = {
        ikSolverAutoUpdate: true,
    };
    function initScene() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        renderer = new THREE.WebGLRenderer({ canvas });
        controls = new OrbitControls(camera, renderer.domElement);
        controls.listenToKeyEvents(window); // optional
        renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.9);
        document.body.appendChild(renderer.domElement);
        camera.position.z = 5;
        gui = new GUI();

        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(10, 10, 10);
        light.intensity = 2;
        scene.add(light);
        // initBones();
        // setupDatGui();
    }

    function createGeometry(sizing) {
        const geometry = new THREE.CylinderGeometry(
            5, // radiusTop
            5, // radiusBottom
            sizing.height, // height
            8, // radiusSegments
            sizing.segmentCount * 1, // heightSegments
            true // openEnded
        );

        const position = geometry.attributes.position;

        const vertex = new THREE.Vector3();

        const skinIndices = [];
        const skinWeights = [];

        for (let i = 0; i < position.count; i++) {
            vertex.fromBufferAttribute(position, i);

            const y = vertex.y + sizing.halfHeight;

            const skinIndex = Math.floor(y / sizing.segmentHeight);
            const skinWeight =
                (y % sizing.segmentHeight) / sizing.segmentHeight;

            skinIndices.push(skinIndex, skinIndex + 1, 0, 0);
            skinWeights.push(1 - skinWeight, skinWeight, 0, 0);
        }

        geometry.setAttribute(
            "skinIndex",
            new THREE.Uint16BufferAttribute(skinIndices, 4)
        );
        geometry.setAttribute(
            "skinWeight",
            new THREE.Float32BufferAttribute(skinWeights, 4)
        );

        return geometry;
    }

    function createBones(sizing) {
        bones = [];

        // "root bone"
        const rootBone = new THREE.Bone();
        rootBone.name = "root";
        rootBone.position.y = -sizing.halfHeight;
        bones.push(rootBone);

        //
        // "bone0", "bone1", "bone2", "bone3"
        //

        // "bone0"
        let prevBone = new THREE.Bone();
        prevBone.position.y = 0;
        rootBone.add(prevBone);
        bones.push(prevBone);

        // "bone1", "bone2", "bone3"
        for (let i = 1; i <= sizing.segmentCount; i++) {
            const bone = new THREE.Bone();
            bone.position.y = sizing.segmentHeight;
            bones.push(bone);
            bone.name = `bone${i}`;
            prevBone.add(bone);
            prevBone = bone;
        }

        // "target"
        const targetBone = new THREE.Bone();
        targetBone.name = "target";
        targetBone.position.y = sizing.height + sizing.segmentHeight; // relative to parent: rootBone
        rootBone.add(targetBone);
        bones.push(targetBone);

        return bones;
    }

    function createMesh(geometry, bones) {
        const material = new THREE.MeshPhongMaterial({
            skinning: true,
            color: 0x00ff00,
        });

        const mesh = new THREE.SkinnedMesh(geometry, material);
        const skeleton = new THREE.Skeleton(bones);

        mesh.add(bones[0]);

        mesh.bind(skeleton);

        skeletonHelper = new THREE.SkeletonHelper(mesh);
        skeletonHelper.material.linewidth = 2;
        scene.add(skeletonHelper);

        return mesh;
    }

    function setupDatGui() {
        gui.add(mesh, "pose").name("mesh.pose()");

        mesh.skeleton.bones
            .filter((bone) => bone.name === "target")
            .forEach(function (bone) {
                const folder = gui.addFolder(bone.name);

                const delta = 20;
                folder.add(
                    bone.position,
                    "x",
                    -delta + bone.position.x,
                    delta + bone.position.x
                );
                folder.add(
                    bone.position,
                    "y",
                    -bone.position.y,
                    bone.position.y
                );
                folder.add(
                    bone.position,
                    "z",
                    -delta + bone.position.z,
                    delta + bone.position.z
                );
            });

        gui.add(ikSolver, "update").name("ikSolver.update()");
        gui.add(state, "ikSolverAutoUpdate");
    }

    function initBones() {
        const segmentHeight = 8;
        const segmentCount = 3;
        const height = segmentHeight * segmentCount;
        const halfHeight = height * 0.5;

        const sizing = {
            segmentHeight,
            segmentCount,
            height,
            halfHeight,
        };

        const geometry = createGeometry(sizing);
        const bones = createBones(sizing);
        mesh = createMesh(geometry, bones);

        scene.add(mesh);

        //
        // ikSolver
        //

        const iks = [
            {
                target: 5,
                effector: 4,
                links: [{ index: 3 }, { index: 2 }, { index: 1 }],
            },
        ];
        ikSolver = new CCDIKSolver(mesh, iks);
        scene.add(new CCDIKHelper(mesh, iks));
    }

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
        // if (state.ikSolverAutoUpdate) {
        //     ikSolver?.update();
        // }
    };

    onMount(() => {
        initScene();
        animate();
    });
</script>

<canvas bind:this={canvas} />
