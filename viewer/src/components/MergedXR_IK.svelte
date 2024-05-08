<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { XRButton } from "three/examples/jsm/webxr/XRButton.js";
    import { XRControllerModelFactory } from "three/examples/jsm/webxr/XRControllerModelFactory.js";
    import { XRHandModelFactory } from "three/addons/webxr/XRHandModelFactory.js";
    import { onMount } from "svelte";
    import { send2Socket, output_quaternion } from "../stores/websocket";
    import { animateModel, add_rigged_model } from "./RiggedModel.js";
    import { createTextTexture } from "./GenerateTextureFromText";
    import { Reflector } from "three/examples/jsm/objects/Reflector.js";
    let container;
    let camera: any, scene: any, renderer: any;
    let controller1, controller2;
    let hand1, hand2;
    let plane2;
    let controllerGrip1, controllerGrip2;
    let ball;
    const controllers = [] as any;
    let reflector: Reflector;

    let quat = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"

    // Subscription to the data stream
    output_quaternion.subscribe((value) => {
        quat.set(value[0], value[1], value[2], value[3]);
    });


    function init() {
        console.log("init");

        container = document.createElement("div");
        document.body.appendChild(container);

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x808080);

        camera = new THREE.PerspectiveCamera(
            50,
            window.innerWidth / window.innerHeight,
            0.1,
            20,
        );
        camera.position.set(0, 1.6, 3);

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
        //orbit controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 1.6, 0);
        controls.update();

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
        const planeGeometry = new THREE.PlaneGeometry(2, 2, 2);
        const planeMaterial = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            wireframe: true,
        });
        //global light
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(light);
        //wireframe ball
        const ballGeometry = new THREE.SphereGeometry(0.1, 32, 32);
        const ballMaterial = new THREE.MeshBasicMaterial({
            color: 0x00ff00,
            wireframe: true,
        });
        // ball = new THREE.Mesh(ballGeometry, ballMaterial);
        // scene.add(ball);

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
        //add reflector
        reflector = new Reflector(planeGeometry, {
            clipBias: 0.003,
            textureWidth: window.innerWidth * window.devicePixelRatio,
            textureHeight: window.innerHeight * window.devicePixelRatio,
            color: 0x889999,
        });
        reflector.position.set(0,0, 2);
        scene.add(reflector);

        //add axis helper
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);

        window.addEventListener("resize", onWindowResize);
        //
        add_rigged_model(scene);
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
            let hmdCamera = renderer.xr.getCamera(camera);
            let position = hmdCamera.position;

            // Set plane position directly in front of the camera
            let distanceInFrontOfCamera = 3; // Adjust this value to set how far the plane should be
            let cameraDirection = new THREE.Vector3();
            camera.getWorldDirection(cameraDirection);
            cameraDirection.multiplyScalar(distanceInFrontOfCamera);
            let planePosition = new THREE.Vector3().addVectors(
                position,
                cameraDirection,
            );

            reflector.position.set(
                planePosition.x,
                planePosition.y,
                planePosition.z,
            );

            // Make the plane face the camera
            reflector.lookAt(camera.position);

            //refle

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
            //check if controller 1 is connected
            if (controller1.position !== undefined) {
                //console.log(controller1.position);
                // ball.position.set(
                //     controller1.position.x,
                //     controller1.position.y,
                //     controller1.position.z,
                // );
            }
            
            
            
            
            if (counter > 100) {
                let rot = new THREE.Vector3();
                rot.x = hmdCamera.rotation.x;
                rot.y = hmdCamera.rotation.y + Math.PI;
                rot.z = hmdCamera.rotation.z;
                
                animateModel( controller1.position, controller2.position, rot, quat);
            }
            counter += 1;
        };

        animate();
    });
</script>
