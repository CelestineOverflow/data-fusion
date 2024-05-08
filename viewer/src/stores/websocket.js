import { writable } from 'svelte/store';
import { onMount } from 'svelte';
import * as THREE from "three";

export const state = writable('🟠');

export const rotation_vector_0 = writable([0, 0, 0]);
export const position_vector_0 = writable([0, 0, 0]);
//
export const rotation_vector_1 = writable([0, 0, 0]);
export const position_vector_1 = writable([0, 0, 0]);
export const raw_data = writable({});
//

let quat = new THREE.Quaternion(); // Will hold the quaternion from "98CDAC1D78E6"
let quat2 = new THREE.Quaternion(); // Will hold the quaternion from "AC0BFBDBA9A4"
/**
 * @type {WebSocket}
 */

export let socket2;
export let output_quaternion = writable([0, 0, 0, 0]);
export let output_quaternion2 = writable([0, 0, 0, 0]);

function applyIMURotationWithOffset(imuData, outputquat) {
    if (!imuData) {
        return;
    }
    let lastQuaternion = imuData.clone(); // Save the current quaternion for the next iteration

    // Create the rotation quaternion for the initial rotation
    let rotationQuaternion = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2);

    // Apply the fixed rotation to the IMU data quaternion
    lastQuaternion.premultiply(rotationQuaternion);
    //rotate 180 in x axis
    let rotationQuaternion2 = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI);
    lastQuaternion.premultiply(rotationQuaternion2);

    // Swap Y and X axis in the quaternion; this also inverts the new Y-axis (which is the original X)
    let swappedAndInvertedQuaternion = new THREE.Quaternion(-lastQuaternion.y, -lastQuaternion.x, -lastQuaternion.z, lastQuaternion.w);

    // Set the astronaut's rotation from the adjusted quaternion
    outputquat.set([swappedAndInvertedQuaternion.x, swappedAndInvertedQuaternion.y, swappedAndInvertedQuaternion.z, swappedAndInvertedQuaternion.w]);
}
function extractQuaternionFromIMUData(id, data) {
    if (data.imu && data.imu[id] && data.imu[id].quaternion) {
        return new THREE.Quaternion(
            data.imu[id].quaternion.x,
            data.imu[id].quaternion.y,
            data.imu[id].quaternion.z,
            data.imu[id].quaternion.w
        );
    }
    return null;
}

export function connectToWebSocket() {
    let socket = new WebSocket("wss://192.168.31.58:1456");
    // socket2 = new WebSocket("wss://192.168.31.58:1456");

    socket.onmessage = function (event) {
        try {
            let data = JSON.parse(event.data);
            raw_data.set(data);           
            applyIMURotationWithOffset( extractQuaternionFromIMUData("98CDAC1D78E6", data), output_quaternion);
            applyIMURotationWithOffset( extractQuaternionFromIMUData("AC0BFBDBA9A4", data), output_quaternion2);

        } catch (error) {
            console.log(error);
        }
    };
    socket.onopen = function (event) {
        console.log("Connected to websocket");
        state.set("🟢");
    };
    socket.onclose = function (event) {
        state.set("🔴");
    };
    socket.onerror = function (event) {
        state.set("🚩");
        console.log(event);
    };
    socket2.onmessage = function (event) {
        console.log(event.data);
    };

    socket2.onopen = function (event) {
        console.log("Connected to websocket 2");
    };
    socket2.onclose = function (event) {
        console.log("Disconnected from websocket 2");
    };
    socket2.onerror = function (event) {
        console.log("Error in websocket 2");
    };
}

export function send2Socket(data) {
    //check if the socket is open
    //check if socket is a type of WebSocket
    if (typeof socket2 == "undefined") {
        return;
    }
    if (socket2.readyState == WebSocket.OPEN) {
        socket2.send(data);
        return;
    }

}









