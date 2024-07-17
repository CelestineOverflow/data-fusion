<!-- <script lang="ts">
    import { onMount } from "svelte";
    import {
        rotation_vector_0,
        position_vector_0,
        rotation_vector_1,
        position_vector_1,
    } from "../stores/vectors.js";
    import { state, raw_data } from "../stores/server_stats.js";
    let socket: WebSocket;
    
    export function send(message: string) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(message);
        } else {
            alert("Not connected to server");
        }
    }

</script> -->
