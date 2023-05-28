<script lang="ts">
    import { onMount } from 'svelte';
    import { rotation_vector, position_vector} from '../stores/vectors.js';

    let socket: WebSocket;
    let state: string = '🟠';
    onMount(() => {
        socket = new WebSocket('ws://localhost:8000/ws');
        socket.onmessage = function (event) {
            try {
                let data = JSON.parse(event.data);
                if (data.type === 'pos-rot-vect'){
                    rotation_vector.set([data.rotation.x, data.rotation.y, data.rotation.z]);
                    position_vector.set([data.position.x, data.position.y, data.position.z]);
                }
                // alert('success');
            } catch (error) {
                alert(error);
                alert(event.data);
            }
            
        };
        socket.onopen = function (event) {
            state = '🟢';
        };
        socket.onclose = function (event) {
            state = '🔴';
            // setTimeout(() => {
            //     socket = new WebSocket('ws://localhost:8000/ws');
            // }, 1000);
        };
        socket.onerror = function (event) {
            state = '🚩';
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
<h1>api server state {state}</h1>
<button on:click={() => send('Hello')}>Send</button>

