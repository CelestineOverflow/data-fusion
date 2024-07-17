import { writable } from 'svelte/store';
import * as THREE from "three";

export const state = writable('🟠');
export const rotation_vector_0 = writable([0, 0, 0]);
export const position_vector_0 = writable([0, 0, 0]);
export const rotation_vector_1 = writable([0, 0, 0]);
export const position_vector_1 = writable([0, 0, 0]);
export const raw_data = writable({});
export const thighquatL = writable([0, 0, 0, 0]);
export const thighquatR = writable([0, 0, 0, 0]);
export const baseBoneQuat = writable([0, 0, 0, 0]);


// eslint-disable-next-line @typescript-eslint/no-explicit-any
function extractQuaternionFromIMUData(id : string, data : any): THREE.Quaternion | null {
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
            const _thighquatL = extractQuaternionFromIMUData("083A8DCCC2F4", data);
            if (_thighquatL) {
                thighquatL.set([_thighquatL.x, _thighquatL.y, _thighquatL.z, _thighquatL.w]);
            }
            const _thighquatR = extractQuaternionFromIMUData("083A8DD1B0A6", data);
            if (_thighquatR) {
                thighquatR.set([_thighquatR.x, _thighquatR.y, _thighquatR.z, _thighquatR.w]);
            }
            const _baseBoneQuat = extractQuaternionFromIMUData("083A8DCCB5BF", data);
            if (_baseBoneQuat) {
                baseBoneQuat.set([_baseBoneQuat.x, _baseBoneQuat.y, _baseBoneQuat.z, _baseBoneQuat.w]);
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









