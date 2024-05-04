import { writable } from 'svelte/store';
import { onMount } from 'svelte';

export const state = writable('🟠');

export const rotation_vector_0 = writable([0, 0, 0]);
export const position_vector_0 = writable([0, 0, 0]);
//
export const rotation_vector_1 = writable([0, 0, 0]);
export const position_vector_1 = writable([0, 0, 0]);
export const raw_data = writable({});
/**
 * @type {WebSocket}
 */
export let socket2;
export function connectToWebSocket() {
    let socket = new WebSocket("wss://192.168.31.58:1456");
    socket2 = new WebSocket("wss://192.168.31.58:1456");

    socket.onmessage = function (event) {
        try {
            let data = JSON.parse(event.data);
            raw_data.set(data);

        } catch (error) {
            console.log("Error parsing JSON");
            console.log(event.data);
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
