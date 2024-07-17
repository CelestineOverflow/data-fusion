import { writable } from 'svelte/store';
import * as THREE from "three";

export const state = writable('🟠');
export const raw_data = writable({});
export const thighquatL = writable(new THREE.Quaternion(0, 0, 0, 1));
export const thighquatR = writable(new THREE.Quaternion(0, 0, 0, 1));
export const baseBoneQuat = writable(new THREE.Quaternion(0, 0, 0, 1));
export const shinquatL = writable(new THREE.Quaternion(0, 0, 0, 1));
export const shinquatR = writable(new THREE.Quaternion(0, 0, 0, 1));

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function extractQuaternionFromIMUData(id : any, data : any) {
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
    console.log("Connecting to websocket");
    const socket = new WebSocket("wss://192.168.31.58:1456");

    socket.onmessage = function (event) {
        try {
            const data = JSON.parse(event.data);
            raw_data.set(data);

            const _thighquatL = extractQuaternionFromIMUData("083A8DCCC2F4", data); //083A8DCCB5BF
            if (_thighquatL) {
                _thighquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
                _thighquatL.set(_thighquatL.x, -_thighquatL.y, -_thighquatL.z, _thighquatL.w);
                // _thighquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(-1, 0, 0), Math.PI / 2));
                // _thighquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI));
                thighquatL.set(_thighquatL);
            }

            const _thighquatR = extractQuaternionFromIMUData("083A8DD1B0A6", data);
            if (_thighquatR) {
                //_thighquatR.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
                //_thighquatR.set(_thighquatR.x, -_thighquatR.y, -_thighquatR.z, _thighquatR.w);
                _thighquatR.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(-1, 0, 0), Math.PI / 2));
                _thighquatR.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI));
                thighquatR.set(_thighquatR);
            }

            const _baseBoneQuat = extractQuaternionFromIMUData("083A8DCCB5BF", data);
            if (_baseBoneQuat) {
                _baseBoneQuat.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(-1, 0, 0), Math.PI / 2));
                _baseBoneQuat.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI));
                baseBoneQuat.set(_baseBoneQuat);
            }

            const _shinquatL = extractQuaternionFromIMUData("083A8DCCC7B5", data);
            if (_shinquatL) {
                _shinquatL.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2));
                _shinquatL.set(-_shinquatL.x, _shinquatL.y, -_shinquatL.z, _shinquatL.w);
                shinquatL.set(_shinquatL);
            }

            const _shinquatR = extractQuaternionFromIMUData("58BF25DB53DA", data);
            if (_shinquatR) {
                _shinquatR.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2));
                _shinquatR.set(_shinquatR.x, -_shinquatR.y, -_shinquatR.z, _shinquatR.w);
                shinquatR.set(_shinquatR);
            }
        } catch (error) {
            console.log(error);
        }
    };

    socket.onopen = function () {
        console.log("Connected to websocket");
        state.set("🟢");
    };

    socket.onclose = function () {
        state.set("🔴");
    };

    socket.onerror = function () {
        state.set("🚩");
        console.log();
    };
}
