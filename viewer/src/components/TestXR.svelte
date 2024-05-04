<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { XRButton } from "three/examples/jsm/webxr/XRButton.js";
    import { XRControllerModelFactory } from "three/examples/jsm/webxr/XRControllerModelFactory.js";
    import { XRHandModelFactory } from "three/addons/webxr/XRHandModelFactory.js";
    import { onMount } from "svelte";
    import { send2Socket } from "../stores/websocket";

    import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

    let container;
    let camera: any, scene: any, renderer: any;
    let controller1, controller2;
    let hand1, hand2;
    let plane2;
    let controllerGrip1, controllerGrip2;

    const controllers = [] as any;
    let controls, group;

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

        // const light = new THREE.DirectionalLight(0xffffff, 1);
        // light.position.set(0, 6, 0);
        // light.castShadow = true;
        // light.shadow.camera.top = 2;
        // light.shadow.camera.bottom = -2;
        // light.shadow.camera.right = 2;
        // light.shadow.camera.left = -2;
        // light.shadow.mapSize.set(4096, 4096);
        // scene.add(light);

        //

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

        // test gtlf
        let astronaut = new THREE.Object3D();

        const loader = new GLTFLoader();
        loader.load(
            // resource URL
            "text2.glb",
            // called when the resource is loaded
            function (gltf) {
                astronaut = gltf.scene;
                //scale fritz-cola

                scene.add(astronaut);
                console.log("fritz-cola loaded");
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            // called when loading has errors
            function (error) {
                console.error("An error happened", error);
            },
        );

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

                counter = 0;
            }
            counter++;
        };

        animate();
    });
</script>
