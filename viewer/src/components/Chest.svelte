<!-- <script lang="ts">
    import * as THREE from "three";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;
    let rotationXChest = 0;
    let rotationYChest = 0;
    let rotationZChest = 0;

    let rotationXUpperArm = 0;
    let rotationYUpperArm = 0;
    let rotationZUpperArm = 0;

    let rotationXForearm = 0;
    let rotationYForearm = 0;
    let rotationZForearm = 0;

    let rotationXUpperArmLeft = 0;
    let rotationYUpperArmLeft = 0;
    let rotationZUpperArmLeft = 0;

    let rotationXForearmLeft = 0;
    let rotationYForearmLeft = 0;
    let rotationZForearmLeft = 0;

    import { raw_data } from "../stores/websocket";



    const quaternion2 = new THREE.Quaternion();
    const quaternion3 = new THREE.Quaternion();
    const chest_Quaternion = new THREE.Quaternion();

    

    raw_data.subscribe((value) => {
        try {

            const camera_data = (value as { camera?: any }).camera;

            for (const id in camera_data) {
                if (id === '17') {
                    cameraPose.chest.position.x = camera_data[id].position.x;
                    cameraPose.chest.position.y = camera_data[id].position.y;
                    cameraPose.chest.position.z = camera_data[id].position.z;
                }
            }
            
            const mcu_data = (value as { mcu?: any }).mcu;
            //iterate thru id 
            for (const id in mcu_data) {
                if (id === '192.168.1.101') {
                    quaternion2.set(
                        mcu_data[id].quaternion.x,
                        mcu_data[id].quaternion.y,
                        mcu_data[id].quaternion.z,
                        mcu_data[id].quaternion.w,
                    );
                }
                else if (id === '192.168.1.103') {
                    quaternion3.set(
                        mcu_data[id].quaternion.x,
                        mcu_data[id].quaternion.y,
                        mcu_data[id].quaternion.z,
                        mcu_data[id].quaternion.w,
                    );
                }
                else if (id === '192.168.1.105') {
                    chest_Quaternion.set(
                        mcu_data[id].quaternion.x,
                        mcu_data[id].quaternion.y,
                        mcu_data[id].quaternion.z,
                        mcu_data[id].quaternion.w,
                    );
                }
            }
        } catch (e) {
            // console.log(e);
        }
    });

    onMount(() => {
        // setup scene
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            canvas.clientWidth / canvas.clientHeight,
            0.1,
            1000,
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

        // Define the colors for each face of the cube
        const colors = [
            0xff0000, // right face
            0x00ff00, // left face
            0x0000ff, // top face
            0xffff00, // bottom face
            0xff00ff, // front face
            0x00ffff, // back face
        ];

        // Create basic components of the human model
        // Chest color is red
        const chestGeometry = new THREE.BoxGeometry(1, 0.5, 0.4);
        const chestMaterial = new THREE.MeshStandardMaterial({
            color: 0xff0000,
        });
        const chest = new THREE.Mesh(chestGeometry, chestMaterial);
        chest.position.y = 0.5;
        scene.add(chest);

        // Upper Arm color is green
        const upperArmGeometry = new THREE.BoxGeometry(0.3, 1, 0.3);
        const upperArmMaterial = new THREE.MeshStandardMaterial({
            color: 0x00ff00,
        });
        const upperArm = new THREE.Mesh(upperArmGeometry, upperArmMaterial);
        upperArm.position.y = -0.1;
        upperArm.position.x = 0.7;
        upperArm.geometry.translate(0, -0.1, 0);
        upperArm.position.y = 0; // Reset the position so it appears attached to the chest
        chest.add(upperArm); // Attach upper arm to chest

        // Forearm color is blue
        const forearmGeometry = new THREE.BoxGeometry(0.25, 0.8, 0.25);
        const forearmMaterial = new THREE.MeshStandardMaterial({
            color: 0x0000ff,
        });
        const forearm = new THREE.Mesh(forearmGeometry, forearmMaterial);
        forearm.position.y = -0.1;
        forearm.geometry.translate(0, -0.1, 0); // Half the height of the forearm to move the pivot to the end
        forearm.position.y = -1; // Position the forearm so it connects to the end of the upper arm
        upperArm.add(forearm); // Attach forearm to upper arm
        // Left Upper Arm
        const upperArmLeft = new THREE.Mesh(
            upperArmGeometry,
            upperArmMaterial.clone(),
        );
        upperArmLeft.position.y = -0.75;
        upperArmLeft.position.x = -0.7; // Mirrored position
        upperArmLeft.geometry.translate(0, -0.5, 0);
        upperArmLeft.position.y = 0; // Adjust position
        chest.add(upperArmLeft);

        // Left Forearm
        const forearmLeft = new THREE.Mesh(
            forearmGeometry,
            forearmMaterial.clone(),
        );
        forearmLeft.position.y = -0.9;
        forearmLeft.geometry.translate(0, -0.4, 0);
        forearmLeft.position.y = -1; // Adjust position
        upperArmLeft.add(forearmLeft);

        //add light
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
        camera.position.z = 5;
        //show axes
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);

        const animate = function () {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
            // Update rotations from sliders, converting degrees to radians
            upperArm.quaternion.copy(quaternion2);
            forearm.quaternion.copy(quaternion3);
            chest.quaternion.copy(chest_Quaternion);
            chest.position.x = cameraPose.chest.position.x;
            chest.position.y = cameraPose.chest.position.y;
            chest.position.z = cameraPose.chest.position.z;
            forearmLeft.rotation.x =
                THREE.MathUtils.degToRad(rotationXForearmLeft);
            forearmLeft.rotation.y =
                THREE.MathUtils.degToRad(rotationYForearmLeft);
            forearmLeft.rotation.z =
                THREE.MathUtils.degToRad(rotationZForearmLeft);
        };

        animate();
    });
</script>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">IK</h5>
        <canvas bind:this={canvas} />
        <div class="mt-3">
            <h6>Forearm Rotation</h6>
            <div class="form-group">
                <label for="forearmRotationX"
                    >X-axis rotation {rotationXForearm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="forearmRotationX"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationXForearm}
                />
            </div>
            <div class="form-group">
                <label for="forearmRotationY"
                    >Y-axis rotation {rotationYForearm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="forearmRotationY"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationYForearm}
                />
            </div>
            <div class="form-group">
                <label for="forearmRotationZ"
                    >Z-axis rotation {rotationZForearm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="forearmRotationZ"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationZForearm}
                />
            </div>
        </div>
        <div class="mt-3">
            <h6>Upper Arm Rotation</h6>
            <div class="form-group">
                <label for="upperArmRotationX"
                    >X-axis rotation {rotationXUpperArm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="upperArmRotationX"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationXUpperArm}
                />
            </div>
            <div class="form-group">
                <label for="upperArmRotationY"
                    >Y-axis rotation {rotationYUpperArm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="upperArmRotationY"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationYUpperArm}
                />
            </div>
            <div class="form-group">
                <label for="upperArmRotationZ"
                    >Z-axis rotation {rotationZUpperArm}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="upperArmRotationZ"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationZUpperArm}
                />
            </div>
        </div>
        <div class="mt-3">
            <h6>Chest Rotation</h6>
            <div class="form-group">
                <label for="chestRotationX"
                    >X-axis rotation {rotationXChest}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="chestRotationX"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationXChest}
                />
            </div>
            <div class="form-group">
                <label for="chestRotationY"
                    >Y-axis rotation {rotationYChest}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="chestRotationY"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationYChest}
                />
            </div>
            <div class="form-group">
                <label for="chestRotationZ"
                    >Z-axis rotation {rotationZChest}</label
                >
                <input
                    type="range"
                    class="form-control-range"
                    id="chestRotationZ"
                    min="0"
                    max="360"
                    step="1"
                    bind:value={rotationZChest}
                />
            </div>
        </div>
    </div>
</div>

<style>
    canvas {
        width: 500px;
        height: 500px;
    }
</style> -->
