<script lang="ts">
    import * as THREE from "three";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
    import { onMount } from "svelte";
    import { send2Socket } from "../stores/websocket";
    import { limbs_data, resetLocalStorage } from "../stores/body";

    let canvas: HTMLCanvasElement;

    let limbs = [];

    limbs_data.subscribe((value) => {
        limbs = value;
    });

    function sendPositionOrRotation(data, type, tracker) {
        if (type === "position") {
            const message = {
                tracker: tracker,
                position: [data.positionX, data.positionY, data.positionZ],
            };
            send2Socket(JSON.stringify(message));
        }
        else if (type === "rotation") {
            const message = {
                tracker: tracker,
                rotation: [data.rotationX, data.rotationY, data.rotationZ],
            };
            send2Socket(JSON.stringify(message));
        }
    }


    let limbMeshes = new Map(); // Store references to limb meshes
    let limbLines = new Map(); // Store references to limb lines
    let limbOffsets = new Map(); // Store offsets for limbs

    onMount(() => {
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
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.update();

        const planeGeometry = new THREE.PlaneGeometry(10, 10, 10);
        const planeMaterial = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            wireframe: true,
        });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = Math.PI / 2;
        plane.position.y = -2.5;
        scene.add(plane);

        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
        camera.position.z = 5;

        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);

        const lineMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff }); // Lines in blue

        limbs.forEach((limb) => {
            // Handle cubes
            if (!limbMeshes.has(limb.name)) {
                const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
                const material = new THREE.MeshBasicMaterial({
                    color: new THREE.Color().setHex(Math.random() * 0xffffff),
                });
                const cube = new THREE.Mesh(geometry, material);
                scene.add(cube);
                limbMeshes.set(limb.name, cube);
            }

            // Handle lines
            if (limb.connected && limb.connectedTo !== "none") {
                const parentLimb = limbs.find(
                    (l) => l.name === limb.connectedTo,
                );
                if (parentLimb) {
                    const points = [
                        new THREE.Vector3(
                            limb.positionX,
                            limb.positionY,
                            limb.positionZ,
                        ),
                        new THREE.Vector3(
                            parentLimb.positionX,
                            parentLimb.positionY,
                            parentLimb.positionZ,
                        ),
                    ];
                    const geometry = new THREE.BufferGeometry().setFromPoints(
                        points,
                    );
                    const line = new THREE.Line(geometry, lineMaterial);
                    scene.add(line);
                    limbLines.set(`${limb.name}-to-${limb.connectedTo}`, line);
                    // Calculate and store the initial offset
                    const parentPosition = new THREE.Vector3(
                        parentLimb.positionX,
                        parentLimb.positionY,
                        parentLimb.positionZ,
                    );
                    const childPosition = new THREE.Vector3(
                        limb.positionX,
                        limb.positionY,
                        limb.positionZ,
                    );
                    const offset = childPosition.sub(parentPosition);
                    limbOffsets.set(limb.name, offset);
                }
            }
        });

        const animate = function () {
            requestAnimationFrame(animate);

            limbs.forEach((limb) => {



                if (limb.send) {
                sendPositionOrRotation(limb, "rotation", limb.vrchat_name);
                sendPositionOrRotation(limb, "position", limb.vrchat_name);
                }

                const mesh = limbMeshes.get(limb.name);
                if (limb.connected && limb.connectedTo !== "none") {
                    const parentMesh = limbMeshes.get(limb.connectedTo);
                    const parentQuaternion = new THREE.Quaternion().setFromEuler(parentMesh.rotation);

                    // Apply parent's rotation to the offset
                    const offset = limbOffsets.get(limb.name).clone();
                    const newPosition = offset.applyQuaternion(parentQuaternion).add(parentMesh.position);
                    mesh.position.copy(newPosition);

                    // Update this limb's rotation by combining it with its parent's
                    const combinedRotation = new THREE.Euler().setFromQuaternion(
                        parentQuaternion.multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(
                            limb.rotationX * (Math.PI / 180),
                            limb.rotationY * (Math.PI / 180),
                            limb.rotationZ * (Math.PI / 180)
                        )))
                    );
                    mesh.rotation.copy(combinedRotation);

                    // Update the connecting line
                    if (limbLines.has(`${limb.name}-to-${limb.connectedTo}`)) {
                        const line = limbLines.get(`${limb.name}-to-${limb.connectedTo}`);
                        line.geometry.setFromPoints([
                            new THREE.Vector3(mesh.position.x, mesh.position.y, mesh.position.z),
                            new THREE.Vector3(parentMesh.position.x, parentMesh.position.y, parentMesh.position.z),
                        ]);
                        line.geometry.attributes.position.needsUpdate = true;
                    }
                } else {
                    // Update positions and rotations for non-connected limbs
                    mesh.position.set(limb.positionX, limb.positionY, limb.positionZ);
                    mesh.rotation.set(
                        limb.rotationX * (Math.PI / 180),
                        limb.rotationY * (Math.PI / 180),
                        limb.rotationZ * (Math.PI / 180)
                    );
                }
            });

            renderer.render(scene, camera);
        };

        animate();
    });

</script>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">IK</h5>
        <canvas bind:this={canvas} />
    </div>
</div>

<style>
    canvas {
        width: 500px;
        height: 500px;
    }
</style>
