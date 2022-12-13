<script lang="ts">
    let writer: any;
    let reader: any;
    let textInput: any;
    let textOutput = "output: ";
    const textDecoder = new TextDecoderStream();
    let connected: boolean = false;
    let port: any;
    let device_id: string = "undefined";
    //add svelte store
    async function connect() {
        try {
            port = await (window.navigator as any).serial.requestPort({});
            await port.open({ baudRate: 115200 });
            writer = port.writable.getWriter();
            console.log("type of writer: " + typeof writer);
            connected = true;
            await listenToPort(port);
        } catch (e) {
            if (connected) {
                alert("Serial Connection Failed" + e);
                connected = false;
            }
        }
    }
    const MAX_BUFFER_SIZE_OF_TEXT = 100;
    async function listenToPort(port: any) {
        port.readable.pipeTo(textDecoder.writable);
        reader = textDecoder.readable.getReader();
        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                reader.releaseLock(); // Release the lock if the stream has ended.
                break;
            }
            if (value.length + textOutput.length > MAX_BUFFER_SIZE_OF_TEXT) {
                console.log("textOutput.length: " + textOutput.length);
                textOutput = textOutput.substring(
                    textOutput.length - MAX_BUFFER_SIZE_OF_TEXT
                );
                textOutput += value;
            } else {
                textOutput += value;
            }
            await new Promise((resolve) => setTimeout(resolve, 5)); // delay to allow UI to update
        }
    }

    async function send() {
        if (connected) {
            const text = textInput.value;
            const encoder = new TextEncoder();
            const encoded = encoder.encode(text);
            await writer.write(encoded);
            textInput.value = "";
        }
    }

    async function disconnect() {
        if (connected) {
            connected = false;
            try {
                await writer.close();
                await reader.cancel();
                await reader.releaseLock();
            } catch (e) {
                alert("Serial Disconnection Failed" + e);
            }
        }
    }
</script>

<main>
    <div class="card text-light bg-dark">
        <div class="card-body">
            <h5 class="card-title">
                Serial Device{#if connected}🟢{:else}🔴{/if}
            </h5>
            <button
                on:click={() => connect()}
                class="btn btn-outline-success"
                type="button">Connect</button
            >
            <button
                on:click={() => disconnect()}
                class="btn btn-outline-warning"
                type="button">disconnect</button
            >
            <!-- <h6 class="card-subtitle mb-2 text-muted">test</h6> -->

            <div class="input-group mb-3">
                <div class="card-text">
                    <p>{textOutput}</p>
                </div>
                <!-- <button
                    on:click={() => {
                        textOutput += "test";
                    }}
                    class="btn btn-outline-success"
                    type="button">Send</button> -->
            </div>
            <p class="card-text" />
            <div class="input-group mb-1">
                <textarea
                    bind:this={textInput}
                    class="form-control"
                    aria-label="With textarea"
                />
            </div>
        </div>
    </div>
</main>

<style>
    div {
        white-space: pre-wrap;
    }
</style>
