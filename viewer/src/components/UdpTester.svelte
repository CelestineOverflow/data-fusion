<script lang="ts">
    import { onMount } from 'svelte';
    import { rotation_vector_0, position_vector_0, rotation_vector_1, position_vector_1} from '../stores/vectors.js';
    import { state, raw_data } from '../stores/server_stats.js';
    let socket: WebSocket;
    onMount(() => {
        socket = new WebSocket('ws://localhost:8000/ws');
        socket.onmessage = function (event) {
            try {
                let data = JSON.parse(event.data);
                // console.log(data);
                raw_data.set(data);
                //let data: {"id":0,"position":{"x":0.09,"y":-0.03,"z":0.97},"rotation":{"x":-0.00504833459854126,"y":-0.009087002277374268,"z":-0.024232006072998045},"type":"pos-rot-vect"}
                if (data.type === 'pos-rot-vect') {
                    if (data.id === 0) {
                        // position_vector_0.set([data.position.x, data.position.y, data.position.z])
                        rotation_vector_0.set([data.rotation.x, data.rotation.y, data.rotation.z])
                    }
                    if (data.id === 42) {
                        // position_vector_1.set([data.position.x, data.position.y, data.position.z])
                        rotation_vector_1.set([data.rotation.x, data.rotation.y, data.rotation.z])
                    }
                }
            } catch (error) {
                alert(error);
                alert(event.data);
            }
            
        };
        socket.onopen = function (event) {
            state.set('🟢');
        };
        socket.onclose = function (event) {
            state.set('🔴');
        };
        socket.onerror = function (event) {
            state.set('🚩');
            console.log(event);
        };
    });

    export function send(message: string) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(message);
        }
        else {
            alert("Not connected to server");
        }
    }
</script>
<button on:click={() => send('Hello')}>Send</button>

