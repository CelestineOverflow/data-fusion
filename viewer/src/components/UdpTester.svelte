<script lang="ts">
    import { onMount } from 'svelte';
    import { rotation_vector_0, position_vector_0, rotation_vector_1, position_vector_1} from '../stores/vectors.js';
    import { state } from '../stores/server_stats.js';
    let socket: WebSocket;
    onMount(() => {
        socket = new WebSocket('ws://localhost:8000/ws');
        socket.onmessage = function (event) {
            try {
                let data = JSON.parse(event.data);
                if (data.type === 'pos-rot-vect'){
                    if (data.id === 0){
                        rotation_vector_0.set(data.rot);
                        position_vector_0.set(data.pos);
                    }
                    else if (data.id === 1){
                        rotation_vector_1.set(data.rot);
                        position_vector_1.set(data.pos);
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

