<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { XRButton } from "three/examples/jsm/webxr/XRButton.js";
    import { XRControllerModelFactory } from "three/examples/jsm/webxr/XRControllerModelFactory.js";
    import { XRHandModelFactory } from "three/addons/webxr/XRHandModelFactory.js";
    import { onMount } from "svelte";
    import { send2Socket } from "../stores/websocket";
    import { FIK } from "./libs/FIK_dev";
    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

    let container;
    let camera: any, scene: any, renderer: any;
    let controller1, controller2;
    let hand1, hand2;
    let plane2;
    let controllerGrip1, controllerGrip2;
    let availableBones: string[] = [];
    let model: any;
    const controllers = [] as any;
    let controls, group;
    let solver: FIK.Structure3D;
    let target: THREE.Vector3;
    let armChain : FIK.Chain3D;
    let upperArmBone : any;
    let forearmBone : any;
    let handBone : any;

    function setupChainsRigged() {
        // Assuming upper_armL, forearmL, and handL are the bones for the left arm
        armChain = new FIK.Chain3D(0x999999);
        upperArmBone = findBone(model, "upper_armL");
         forearmBone = findBone(model, "forearmL");
         handBone = findBone(model, "handL");

        if (upperArmBone && forearmBone && handBone) {
            let _upper = getBoneStartEndPositions(upperArmBone);
            let _forearm = getBoneStartEndPositions(forearmBone);
            let _hand = getBoneStartEndPositions(handBone);
            let baseBone = new FIK.Bone3D(_upper.start, _upper.end);
            armChain.addBone(baseBone);
            let forearm = new FIK.Bone3D(_forearm.start, _forearm.end);
            armChain.addBone(forearm);
            let hand = new FIK.Bone3D(_hand.start, _hand.end);
            armChain.addBone(hand);

            target = new THREE.Vector3(3, 4, 0); // Example target
        //add axis helper on target
        const axesHelper = new THREE.AxesHelper(5);
        axesHelper.position.copy(target);
        scene.add(axesHelper);
        solver.add(armChain, target, true);
        console.log(solver);
        //set the rotation of each bone to the ik model
        // applyRotationsToModel([upperArmBone, forearmBone, handBone], solver);
        }

        
    }

    function getBoneStartEndPositions(bone) {
        // Get the start position of the bone
        let worldStartPos = new THREE.Vector3();
        bone.getWorldPosition(worldStartPos);

        // Initialize the end position vector
        let worldEndPos = new THREE.Vector3();

        // Determine the end position of the bone
        if (bone.children.length > 0) {
            // Use the first child's start position as the end position of the bone
            let childBone = bone.children[0];
            childBone.getWorldPosition(worldEndPos);
        } else {
            // Define a default end position if there are no children
            let defaultLength = 1; // Default length, adjust as necessary
            let localEndPoint = new THREE.Vector3(0, defaultLength, 0); // Assumes length along Y-axis
            worldEndPos = localEndPoint.applyMatrix4(bone.matrixWorld);
        }

        // Return both start and end positions as an object
        return {
            start: worldStartPos,
            end: worldEndPos,
        };
    }

    function findBone(root, name) {
        let target = null;
        root.traverse((node) => {
            if (node.name === name) {
                target = node;
            }
        });
        return target;
    }

    function add_rigged_model() {
        const loader = new GLTFLoader();
        loader.load("test_ik2.glb", function (gltf) {
            model = gltf.scene;
            //scale the model
            model.scale.set(2, 2, 2);
            setupChainsRigged();
            scene.add(model);
        });
    }

    function createTextTexture(
        text: string,
        width: number = 800,
        height: number = 800,
    ): THREE.Texture {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const context = canvas.getContext("2d");

        if (!context) {
            throw new Error("Cannot create canvas context");
        }

        // Fill background if necessary
        context.fillStyle = "#FFFFFF"; // White background
        context.fillRect(0, 0, width, height);

        // Text style
        context.fillStyle = "#000000"; // Black text
        context.font = "Bold 40px Arial";
        context.textAlign = "center";
        context.textBaseline = "middle";

        // Handle multiple lines
        const lines = text.split("\n");
        const lineHeight = 48; // Adjust line height as needed
        const initialY = height / 2 - (lineHeight * (lines.length - 1)) / 2;

        lines.forEach((line, index) => {
            context.fillText(line, width / 2, initialY + index * lineHeight);
        });

        // Create texture
        const texture = new THREE.Texture(canvas);
        texture.needsUpdate = true; // Important to update the texture with new canvas

        return texture;
    }
    function get_rotation_from_bone(bone) {
        let start_pos = bone.start;
        let end_pos = bone.end;
        //create an arrow in the direction of the bone
        let dir = new THREE.Vector3();
        dir.subVectors(new THREE.Vector3(end_pos.x, end_pos.y, end_pos.z), new THREE.Vector3(start_pos.x, start_pos.y, start_pos.z));
        //set the arrow in the direction of the bone
        let arrow = new THREE.ArrowHelper(dir.normalize(), new THREE.Vector3(start_pos.x, start_pos.y, start_pos.z), 10, 0xff0000);
        return arrow.rotation;
    }
    function inv_get_rotation_from_bone(bone) {
        let start_pos = bone.end;
        let end_pos = bone.start;
        //create an arrow in the direction of the bone
        let dir = new THREE.Vector3();
        dir.subVectors(new THREE.Vector3(end_pos.x, end_pos.y, end_pos.z), new THREE.Vector3(start_pos.x, start_pos.y, start_pos.z));
        //set the arrow in the direction of the bone
        let arrow = new THREE.ArrowHelper(dir.normalize(), new THREE.Vector3(start_pos.x, start_pos.y, start_pos.z), 10, 0xff0000);
        return arrow.rotation;
    }


    function update_vector_chain() {

        let bone = armChain.bones[0];
        let rotation = get_rotation_from_bone(bone);
        upperArmBone.rotation.set(rotation.x, rotation.y, rotation.z);
        bone = armChain.bones[1];
        rotation = inv_get_rotation_from_bone(bone);
        forearmBone.rotation.set(rotation.x, rotation.y, rotation.z);
        bone = armChain.bones[2];
        rotation = inv_get_rotation_from_bone(bone);
        handBone.rotation.set(rotation.x, rotation.y, rotation.z);

    }

    function init() {
        container = document.createElement("div");
        document.body.appendChild(container);

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x808080);

        camera = new THREE.PerspectiveCamera(
            50,
            window.innerWidth / window.innerHeight,
            0.1,
            10,
        );
        camera.position.set(0, 1.6, 3);

        controls = new OrbitControls(camera, container);
        controls.target.set(0, 1.6, 0);
        controls.update();
        solver = new FIK.Structure3D(scene, THREE);
        solver.isVisible = false;
        add_rigged_model();

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.xr.enabled = true;
        container.appendChild(renderer.domElement);

        document.body.appendChild(XRButton.createButton(renderer));

        document.getElementById("XRButton");

        // controllers

        controller1 = renderer.xr.getController(0);
        scene.add(controller1);

        controller2 = renderer.xr.getController(1);
        scene.add(controller2);

        const controllerModelFactory = new XRControllerModelFactory();
        const handModelFactory = new XRHandModelFactory();

        controllerGrip1 = renderer.xr.getControllerGrip(0);
        controllerGrip1.addEventListener("connected", controllerConnected);
        controllerGrip1.addEventListener(
            "disconnected",
            controllerDisconnected,
        );
        controllerGrip1.add(
            controllerModelFactory.createControllerModel(controllerGrip1),
        );
        scene.add(controllerGrip1);

        controllerGrip2 = renderer.xr.getControllerGrip(1);
        controllerGrip2.addEventListener("connected", controllerConnected);
        controllerGrip2.addEventListener(
            "disconnected",
            controllerDisconnected,
        );
        controllerGrip2.add(
            controllerModelFactory.createControllerModel(controllerGrip2),
        );
        scene.add(controllerGrip2);
        //

        // Hand 1
        controllerGrip1 = renderer.xr.getControllerGrip(0);
        controllerGrip1.add(
            controllerModelFactory.createControllerModel(controllerGrip1),
        );
        scene.add(controllerGrip1);

        hand1 = renderer.xr.getHand(0);
        hand1.add(handModelFactory.createHandModel(hand1));

        scene.add(hand1);
        //cube

        // Hand 2
        controllerGrip2 = renderer.xr.getControllerGrip(1);
        controllerGrip2.add(
            controllerModelFactory.createControllerModel(controllerGrip2),
        );
        scene.add(controllerGrip2);

        hand2 = renderer.xr.getHand(1);
        hand2.add(handModelFactory.createHandModel(hand2));
        scene.add(hand2);
        // add plane
        const planeGeometry = new THREE.PlaneGeometry(10, 10, 10);
        const planeMaterial = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            wireframe: true,
        });
        //global light
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(light);

        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = Math.PI / 2;
        scene.add(plane);
        //text on plane
        // Create the plane geometry
        const geometry = new THREE.PlaneGeometry(1, 1);
        const texture = createTextTexture("Hello, Three.js!");
        const material = new THREE.MeshBasicMaterial({ map: texture });
        plane2 = new THREE.Mesh(geometry, material);

        scene.add(plane2);

        //add axis helper
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);


    

        window.addEventListener("resize", onWindowResize);
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function controllerConnected(evt: { data: { gamepad: any }; target: any }) {
        controllers.push({
            gamepad: evt.data.gamepad,
            grip: evt.target,
            colliding: false,
            playing: false,
        });
    }

    function controllerDisconnected(evt: { target: any }) {
        const index = controllers.findIndex(
            (o: { controller: any }) => o.controller === evt.target,
        );
        if (index !== -1) {
            controllers.splice(index, 1);
        }
    }

    let counter = 0;

    onMount(() => {
        init();

        const animate = function () {
            renderer.setAnimationLoop(render);
        };

        const render = function () {
            renderer.render(scene, camera);

            // Only update text and reposition the plane occasionally to reduce overhead
            if (counter % 1 === 0) {
                let hmdCamera = renderer.xr.getCamera(camera);
                let position = hmdCamera.position;

                // Set plane position directly in front of the camera
                let distanceInFrontOfCamera = 2; // Adjust this value to set how far the plane should be
                let cameraDirection = new THREE.Vector3();
                camera.getWorldDirection(cameraDirection);
                cameraDirection.multiplyScalar(distanceInFrontOfCamera);
                let planePosition = new THREE.Vector3().addVectors(
                    position,
                    cameraDirection,
                );

                plane2.position.set(
                    planePosition.x,
                    planePosition.y,
                    planePosition.z,
                );

                // Make the plane face the camera
                plane2.lookAt(camera.position);

                // Update the text texture
                let textLine1 =
                    "Position: " +
                    position.x.toFixed(2) +
                    ", " +
                    position.y.toFixed(2) +
                    ", " +
                    position.z.toFixed(2) +
                    "\n";
                //get the position of the hand controller
                
                textLine1 +=
                    "Hand Position: " +
                    controller1.position.x.toFixed(2) +
                    ", " +
                    controller1.position.y.toFixed(2) +
                    ", " +
                    controller1.position.z.toFixed(2) +
                    "\n";

                // Repeat for the second hand controller
                textLine1 +=
                    "Hand Position2: " +
                    controller2.position.x.toFixed(2) +
                    ", " +
                    controller2.position.y.toFixed(2) +
                    ", " +
                    controller2.position.z.toFixed(2) +
                    "\n";

                let newTexture = createTextTexture(textLine1);
                plane2.material.map = newTexture;
                plane2.material.needsUpdate = true; // Ensure the material updates with the new texture
                if (controller1){
                target.copy(controller1.position);
                }
                solver.update();
                update_vector_chain();
                counter = 0;
            }
            counter++;
        };

        animate();
    });
</script>
