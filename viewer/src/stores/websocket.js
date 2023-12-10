import { writable } from 'svelte/store';
import { onMount } from 'svelte';

export const state = writable('🟠');

export const rotation_vector_0 = writable([0, 0, 0]);
export const position_vector_0 = writable([0, 0, 0]);
//
export const rotation_vector_1 = writable([0, 0, 0]);
export const position_vector_1 = writable([0, 0, 0]);
export const raw_data = writable({});

export function connectToWebSocket() {
    let socket = new WebSocket("ws://localhost:5000/ws");

    socket.onmessage = function (event) {
        try {
            let data = JSON.parse(event.data);

            raw_data.set(JSON.parse(event.data));
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
}

