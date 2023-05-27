<script lang="ts">
    import { onMount } from 'svelte';
    let socket: WebSocket;
    let state: string = '🟠';
    onMount(() => {
        socket = new WebSocket('ws://localhost:8000/ws');
        socket.onmessage = function (event) {
            try {
                let data = JSON.parse(event.data);
                if (data.type === 'accelerometer') {
                    console.log(data.accelerometer);
                }
                else if (data.type === 'gyroscope') {
                    console.log(data.gyroscope);
                }
                else if (data.type === 'rotation') {
                    console.log(data.rotation);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'euler') {
                    console.log(data.euler);
                }
                else if (data.type === 'matrix') {
                    console.log(data.matrix);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else if (data.type === 'quaternion') {
                    console.log(data.quaternion);
                }
                else {
                    console.log(data);
                }
                alert('success');
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

